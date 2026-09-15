# SPDX-License-Identifier: Apache-2.0
"""Dated MCP 2026-07-28 stdio teaching subset, sharing KA-3 execution."""
import json
from pathlib import Path
import subprocess
import sys
from contracts import encode, no_duplicates, reject_constant
from read_tools import execute, INPUT_SCHEMA

VERSION = '2026-07-28'
PREFIX = 'io.modelcontextprotocol/'
SERVER_INFO = {'name': 'book-orders', 'version': '1.0.0'}
TOOL = {'name': 'get_order', 'description': 'Read an owned fictional order snapshot; no mutation.',
        'inputSchema': INPUT_SCHEMA, 'annotations': {'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False}}


def request(number, method, **params):
    params['_meta'] = {PREFIX + 'protocolVersion': VERSION, PREFIX + 'clientCapabilities': {},
                       PREFIX + 'clientInfo': {'name': 'book-host', 'version': '1.0.0'}}
    return dict(jsonrpc='2.0', id=number, method=method, params=params)


def dispatch(message):
    number = message.get('id') if isinstance(message, dict) else None
    def error(code, reason, data=None):
        value = dict(code=code, message=reason)
        if data is not None:
            value['data'] = data
        return dict(jsonrpc='2.0', id=number, error=value)
    if not isinstance(message, dict) or message.get('jsonrpc') != '2.0' or not isinstance(message.get('method'), str):
        return error(-32600, 'Invalid Request')
    if 'id' not in message:
        return None
    if type(number) not in {int, str}:
        return error(-32600, 'Invalid Request')
    params = message.get('params', {})
    if not isinstance(params, dict) or not isinstance(params.get('_meta'), dict):
        return error(-32602, 'Missing request metadata')
    meta = params['_meta']
    if not isinstance(meta.get(PREFIX + 'protocolVersion'), str) or not isinstance(meta.get(PREFIX + 'clientCapabilities'), dict):
        return error(-32602, 'Missing required protocol fields')
    if meta[PREFIX + 'protocolVersion'] != VERSION:
        return error(-32022, 'Unsupported protocol version', {'supported': [VERSION], 'requested': meta[PREFIX + 'protocolVersion']})
    method = message['method']
    result = {'resultType': 'complete', '_meta': {PREFIX + 'serverInfo': SERVER_INFO}}
    if method == 'server/discover':
        result.update(supportedVersions=[VERSION], capabilities={'tools': {}})
    elif method == 'tools/list':
        if params.get('cursor'):
            return error(-32602, 'Invalid cursor')
        result['tools'] = [TOOL]
    elif method == 'tools/call':
        if params.get('name') != 'get_order':
            return error(-32602, 'Unknown tool')
        outcome = execute({'name': params['name'], 'arguments': params.get('arguments')}, principal='mira')
        if outcome.get('reason') == 'invalid_arguments':
            return error(-32602, 'Invalid arguments')
        body = outcome.get('result', {'error': outcome.get('reason')})
        result.update(content=[{'type': 'text', 'text': encode(body)}], structuredContent=body,
                      isError=outcome['status'] != 'completed')
    else:
        return error(-32601, 'Method not found')
    return dict(jsonrpc='2.0', id=number, result=result)


def serve():
    while True:
        line = sys.stdin.buffer.readline(65537)
        if not line:
            return
        if len(line) > 65536:
            print(encode({'jsonrpc': '2.0', 'id': None, 'error': {'code': -32600, 'message': 'Request too large'}}), flush=True)
            return
        try:
            value = json.loads(line, object_pairs_hook=no_duplicates, parse_constant=reject_constant)
            response = dispatch(value)
        except (ValueError, UnicodeDecodeError):
            response = {'jsonrpc': '2.0', 'id': None, 'error': {'code': -32700, 'message': 'Parse error'}}
        if response is not None:
            print(encode(response), flush=True)


def demo():
    messages = [request(1, 'server/discover'), request(2, 'tools/list'),
                request(3, 'tools/call', name='get_order', arguments={'order_id': 'A-104'}),
                request(4, 'tools/call', name='get_order', arguments={'order_id': 'B-205'}),
                request(5, 'tools/call', name='cancel_order', arguments={'order_id': 'A-104'})]
    payload = '\n'.join(map(encode, messages)) + '\n'
    completed = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--serve'],
                               input=payload, text=True, capture_output=True, timeout=5, check=True)
    replies = [json.loads(line) for line in completed.stdout.splitlines()]
    if [r['id'] for r in replies] != [m['id'] for m in messages]:
        raise ValueError('response_correlation_failed')
    return dict(protocol_version=VERSION, transport='actual subprocess stdio; no initialize handshake',
                exchanges=[dict(request=m, response=r) for m, r in zip(messages, replies)], stderr=completed.stderr)


if __name__ == '__main__':
    if '--serve' in sys.argv:
        serve()
    else:
        print(json.dumps(demo(), indent=2))
