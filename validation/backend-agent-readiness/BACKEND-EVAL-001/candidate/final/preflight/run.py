#!/usr/bin/env python3
import os,sys,subprocess,base64
from pathlib import Path
root=Path(__file__).resolve().parents[1]
php='/opt/homebrew/opt/php@8.3/bin/php'
if (root/'.env').exists() or (root/'.env.testing').exists() or (root/'bootstrap/cache/config.php').exists():
    raise SystemExit('Refusing unreviewed env or cached configuration')
env={'PATH':'/usr/bin:/bin','HOME':str(root.parent),'TMPDIR':str(root.parent),'APP_ENV':'testing','APP_DEBUG':'false','APP_URL':'http://localhost','APP_KEY':'base64:'+base64.b64encode(os.urandom(32)).decode(),'DB_CONNECTION':'sqlite','DB_DATABASE':':memory:','DB_URL':'','CACHE_STORE':'array','SESSION_DRIVER':'array','MAIL_MAILER':'array','QUEUE_CONNECTION':'sync','QUEUE_FAILED_DRIVER':'null','BROADCAST_CONNECTION':'null','FILESYSTEM_DISK':'local','LOG_CHANNEL':'single','LOG_LEVEL':'warning','BCRYPT_ROUNDS':'4','PULSE_ENABLED':'false','TELESCOPE_ENABLED':'false','NIGHTWATCH_ENABLED':'false'}
mode=sys.argv[1] if len(sys.argv)>1 else ''
commands={'concurrency':['preflight/concurrency.php'],'inspect':['preflight/inspect.php'],'test-list':['vendor/bin/phpunit','--list-tests'],'test':['vendor/bin/phpunit'],'format-check':['vendor/bin/pint','--test'],'routes':['artisan','route:list','--json']}
if mode not in commands or len(sys.argv)!=2:raise SystemExit('Allowed modes: '+', '.join(commands))
cmd=[php,'-n','-d','sys_temp_dir='+str(root.parent)]+commands[mode]
raise SystemExit(subprocess.call(cmd,cwd=root,env=env))
