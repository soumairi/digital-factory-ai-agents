#!/usr/bin/env python3
"""Optional BE006 probe on a NEW local PostgreSQL cluster, Unix socket only.
No existing DSN, credential, service or production target is accepted.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import shlex
import subprocess
import sys

sys.dont_write_bytecode=True
ASSETS=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('runner',ASSETS/'runner.py')
runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace',required=True)
    parser.add_argument('--pg-bin',required=True,type=Path)
    args=parser.parse_args()
    root,state=runner.workspace(args.workspace,'BE-006');runner.check_assets()
    binaries={name:args.pg_bin.resolve()/name for name in ['postgres','initdb','pg_ctl','createdb']}
    if not all(p.is_file() for p in binaries.values()):
        print(json.dumps({'status':'NOT EXECUTED','reason':'Complete local PostgreSQL server toolchain missing','checked_directory':str(args.pg_bin)}));return 2
    data=root/'pgdata';socket=root/'pgsocket'
    if data.exists() or socket.exists():raise ValueError('Refusing to reuse an existing cluster/socket')
    socket.mkdir(mode=0o700)
    env=runner.environment(root);env['PATH']=str(args.pg_bin.resolve())+':/usr/bin:/bin'
    commands=[];started=False
    def run(command):
        p=subprocess.run([str(x) for x in command],env=env,cwd=root/'app',capture_output=True,text=True,timeout=60)
        commands.append({'command':[str(x) for x in command],'exit_code':p.returncode,'output':p.stdout+p.stderr})
        if p.returncode:raise RuntimeError('PostgreSQL adapter command failed; inspect postgres.json')
        return p
    try:
        run([binaries['initdb'],'-D',data,'--auth=trust','--username=adapter_fixture','--no-locale','--encoding=UTF8'])
        options="-h '' -k "+shlex.quote(str(socket))+" -p 55432 -c unix_socket_permissions=0700"
        run([binaries['pg_ctl'],'-D',data,'-l',root/'postgres.log','-o',options,'-w','start']);started=True
        run([binaries['createdb'],'-h',socket,'-p','55432','-U','adapter_fixture','adapter_fixture'])
        result=run([state['php'],'-n','reviewer/common/postgres-probe.php'])
        print(result.stdout,end='')
    finally:
        try:
            if started or (data/'postmaster.pid').exists():run([binaries['pg_ctl'],'-D',data,'-m','immediate','-w','stop'])
        finally:
            (root/'evidence/postgres.json').write_text(json.dumps(commands,indent=2)+'\n')
    return 0

if __name__=='__main__':
    try:sys.exit(main())
    except (ValueError,RuntimeError,OSError,subprocess.TimeoutExpired) as exc:
        print(json.dumps({'status':'INCOMPLETE','error':str(exc)}),file=sys.stderr);sys.exit(2)
