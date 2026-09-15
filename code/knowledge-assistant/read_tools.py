# SPDX-License-Identifier: Apache-2.0
"""KA-3 read-only execution boundary. Model proposals never supply the principal."""
import re
import time
from contracts import load

INPUT_SCHEMA = {'type': 'object', 'properties': {'order_id': {'type': 'string', 'pattern': '^A-[0-9]{3}$|^B-[0-9]{3}$'}}, 'required': ['order_id'], 'additionalProperties': False}


def lookup(order_id, principal):
    snapshot = load('ka3-orders-v1.json')
    order = next((row for row in snapshot['orders'] if row['order_id'] == order_id), None)
    if order is None:
        return {'error': 'not_found'}
    if order['owner'] != principal:
        return {'error': 'forbidden'}
    return dict(order_id=order_id, status=order['status'], as_of=snapshot['as_of'], source_version=snapshot['version'])


def execute(proposal, principal='mira', backend=lookup):
    trace = [dict(stage='proposed', proposal=proposal)]
    if not isinstance(proposal, dict) or set(proposal) != {'name', 'arguments'} or proposal.get('name') != 'get_order':
        return dict(status='rejected', reason='tool_not_allowed', trace=trace)
    args = proposal['arguments']
    if not isinstance(args, dict) or set(args) != {'order_id'} or not isinstance(args['order_id'], str) or not re.fullmatch('[AB]-[0-9]{3}', args['order_id']):
        return dict(status='rejected', reason='invalid_arguments', trace=trace)
    trace.append(dict(stage='validated', arguments=args))
    permission = lookup(args['order_id'], principal)
    if 'error' in permission:
        trace.append(dict(stage='authorization_denied', reason=permission['error']))
        return dict(status='rejected', reason=permission['error'], trace=trace)
    trace.append(dict(stage='authorized', principal=principal, permission='orders:read:own'))
    try:
        result = backend(args['order_id'], principal)
    except TimeoutError:
        trace.append(dict(stage='execution_failed', reason='timeout', completion='unknown'))
        return dict(status='error', reason='timeout', trace=trace)
    trace.append(dict(stage='executed', result=result))
    expected = {'order_id', 'status', 'as_of', 'source_version'}
    if (not isinstance(result, dict) or set(result) != expected or result['order_id'] != args['order_id']
            or result['status'] not in {'processing', 'shipped'} or not all(isinstance(v, str) for v in result.values())):
        return dict(status='error', reason='invalid_tool_result', trace=trace)
    trace.append(dict(stage='result_validated', order_id=result['order_id']))
    trace.append(dict(stage='returned_as_data', result=result))
    return dict(status='completed', result=result, trace=trace)


def retry_read(fetch, attempts=2, timeout_s=0.2, deadline_s=1.0, clock=time.monotonic, sleep=time.sleep):
    """fetch(timeout_s) must enforce its own I/O timeout. No writes are accepted here."""
    started = clock()
    history = []
    for attempt in range(attempts):
        remaining = deadline_s - (clock() - started)
        if remaining <= 0:
            break
        try:
            status, body, retry_after = fetch(min(timeout_s, remaining))
        except (TimeoutError, OSError):
            status, body, retry_after = None, {'error': 'transport_timeout_or_failure'}, 0
        history.append(dict(attempt=attempt + 1, status=status, body=body))
        if status is not None and status not in {429, 503}:
            return dict(status=status, body=body, attempts=history)
        if attempt + 1 < attempts:
            delay = max(0.05 * (2 ** attempt), float(retry_after or 0))
            if delay >= deadline_s - (clock() - started):
                break
            sleep(delay)
    return dict(status='unavailable', body=None, attempts=history)
