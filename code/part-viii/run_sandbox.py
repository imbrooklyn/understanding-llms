# SPDX-License-Identifier: Apache-2.0
"""Optional macOS process-confinement probe using only temporary fake data."""
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import shutil
import socket
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[2]
PROBE='''import json,sys,socket\nfrom pathlib import Path\nr={}\nfor label,path in [('allowed',sys.argv[1]),('outside',sys.argv[2])]:\n try:r[label]=Path(path).read_text()\n except OSError as e:r[label]=dict(error=type(e).__name__,errno=e.errno)\ntry:\n s=socket.create_connection(('127.0.0.1',int(sys.argv[3])),timeout=1);s.close();r['network']='connected'\nexcept OSError as e:r['network']=dict(error=type(e).__name__,errno=e.errno)\nprint(json.dumps(r))\n'''


def run():
    if sys.platform!='darwin' or not shutil.which('sandbox-exec'):
        raise RuntimeError('macos_sandbox_unavailable: this optional probe is not a portable sandbox implementation')
    with tempfile.TemporaryDirectory(prefix='book-viii-sandbox-') as directory:
        root=Path(directory).resolve();work=root/'work';work.mkdir();outside=root/'outside';outside.mkdir()
        script=work/'probe.py';script.write_text(PROBE)
        good=work/'allowed.txt';good.write_text('public-fixture')
        secret=outside/'secret.txt';secret.write_text('DEMO-SECRET-ORCHID')
        server=socket.socket();server.bind(('127.0.0.1',0));server.listen(4)
        profile='\n'.join(['(version 1)','(allow default)','(deny network*)',
            '(deny file-read* (subpath "'+str(outside)+'"))','(deny file-write*)',
            '(allow file-write* (subpath "'+str(work)+'") (literal "/dev/null"))'])
        argv=[sys.executable,'-I',str(script),str(good),str(secret),str(server.getsockname()[1])]
        results={}
        for label,command in [('unconfined',argv),('confined',['sandbox-exec','-p',profile,*argv])]:
            result=subprocess.run(command,text=True,capture_output=True,timeout=5)
            results[label]=dict(returncode=result.returncode,stdout=result.stdout,stderr=result.stderr)
            if result.returncode==0:results[label]['observation']=json.loads(result.stdout)
        server.close()
        clean_profile=profile.replace(str(work),'<temporary-work>').replace(str(outside),'<protected-fixture-directory>')
    report=dict(recorded_at=datetime.now(timezone.utc).isoformat(),platform=platform.platform(),python=sys.version,
                profile=clean_profile,results=results,conditions='Actual subprocesses, temporary fake secret, loopback listener. No third-party network endpoint.',
                limits='macOS-specific diagnostic profile; general runtime reads remain allowed; only the designated fake-secret directory is denied, all network is denied and file writes are restricted; not a production sandbox, authorization system or escape-resistance proof.')
    (ROOT/'data/part-viii/sandbox-run.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    return report

if __name__=='__main__':run()
