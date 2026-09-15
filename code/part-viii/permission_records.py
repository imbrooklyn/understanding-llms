# SPDX-License-Identifier: Apache-2.0
"""Observable permission matrix using fresh local state for each action."""
from dataclasses import replace
from pathlib import Path
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'code/knowledge-assistant'))
from reliable_runtime import Principal, Store, action
from security_controls import dispatch


def run():
    rows=[]
    with tempfile.TemporaryDirectory(prefix='book-viii-permissions-') as directory:
        user=Principal('north','mira',scopes=('orders:read:own','orders:cancel:own'))
        reviewer=Principal('north','reviewer','approver',scopes=('orders:approve',))
        cases=['own_read','south_own_read','wrong_owner','wrong_tenant','wrong_audience','expired_credential','missing_scope','reader_cancel','approved_cancel','missing_approval','denied_approval','expired_approval','changed_object','changed_version','reviewer_read','reviewer_cancel','tenant_argument','network_tool','unprivileged_approve','cross_tenant_approve']
        for name in cases:
            store=Store(Path(directory)/(name+'.sqlite'),clock=lambda:1000.0)
            principal=user
            variants={'wrong_owner':replace(user,user='leo'),'wrong_tenant':replace(user,tenant='south'),'wrong_audience':replace(user,audience='other'),'expired_credential':replace(user,expires_at=999),'missing_scope':replace(user,scopes=()),'south_own_read':Principal('south','leo')}
            try:
                if name in ['tenant_argument','network_tool']:
                    proposal=dict(name='get_order',arguments=dict(order_id='A-104',tenant='south')) if name=='tenant_argument' else dict(name='send_http',arguments={})
                    result=dispatch(proposal,store,user);allowed=result['allowed']
                elif name in ['unprivileged_approve','cross_tenant_approve']:
                    result=store.approve(user if name=='unprivileged_approve' else replace(reviewer,tenant='south'),user,action());allowed=True
                elif 'cancel' in name or 'approval' in name or name in ['changed_object','changed_version']:
                    approval=None
                    if name!='missing_approval':approval=store.approve(reviewer,user,action(),decision='denied' if name=='denied_approval' else 'approved',expires=999 if name=='expired_approval' else 1100)
                    principal=Principal('north','mira') if name=='reader_cancel' else reviewer if name=='reviewer_cancel' else user
                    proposal=action('A-105') if name=='changed_object' else action()
                    if name=='changed_version':
                        with store.db:store.db.execute('UPDATE orders SET version=2 WHERE tenant=? AND id=?',('north','A-104'))
                    result=store.cancel(principal,proposal,approval,'intent-1');allowed=True
                else:
                    principal=reviewer if name=='reviewer_read' else variants.get(name,user)
                    result=store.read(principal,'A-104');allowed=True
            except (PermissionError,ValueError) as error:allowed=False;result=dict(reason=str(error))
            rows.append(dict(case=name,allowed=allowed,result=result,north_effects=store.read(user,'A-104')['effects']))
            store.close()
    return dict(provenance='Actual local matrix; fresh SQLite database per row; host principals and approvals are synthetic, not production credentials.',rows=rows)

if __name__=='__main__':
    import json
    (ROOT/'data/part-viii/permission-run.json').write_text(json.dumps(run(),indent=2)+'\n')
