#!/usr/bin/env python3
"""Local-only evidence runner. No dependency installation or network server.
Usage: python3 campaign/run-evidence.py /private/tmp/.../app [--filter BE001]
Uses an already provisioned disposable copy and fails closed on unreviewed config.
"""
import os,sys,base64,subprocess,json,hashlib
from pathlib import Path

def run(root,args):
    root=Path(root).resolve()
    if not str(root).startswith('/private/tmp/backend-eval-001-'): raise SystemExit('Not campaign disposable path')
    if any((root/p).exists() for p in ['.env','.env.testing','bootstrap/cache/config.php']): raise SystemExit('Unreviewed environment/cache')
    env={'PATH':'/usr/bin:/bin','HOME':str(root.parent),'TMPDIR':str(root.parent),'APP_ENV':'testing','APP_DEBUG':'false','APP_URL':'http://localhost','APP_KEY':'base64:'+base64.b64encode(os.urandom(32)).decode(),'DB_CONNECTION':'sqlite','DB_DATABASE':':memory:','DB_URL':'','CACHE_STORE':'array','SESSION_DRIVER':'array','MAIL_MAILER':'array','QUEUE_CONNECTION':'sync','QUEUE_FAILED_DRIVER':'null','BROADCAST_CONNECTION':'null','FILESYSTEM_DISK':'local','LOG_CHANNEL':'single','LOG_LEVEL':'warning','BCRYPT_ROUNDS':'4','PULSE_ENABLED':'false','TELESCOPE_ENABLED':'false','NIGHTWATCH_ENABLED':'false'}
    cmd=['/opt/homebrew/opt/php@8.3/bin/php','-n','-d','sys_temp_dir='+str(root.parent),'vendor/bin/phpunit','--colors=never']+args
    p=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True)
    return {'cwd':str(root),'command':cmd,'exit_code':p.returncode,'output':p.stdout+p.stderr}
if __name__=='__main__':
    result=run(sys.argv[1],sys.argv[2:]); print(result['output'],end=''); sys.exit(result['exit_code'])
