#!/usr/bin/env python3
import json, os, pathlib, socket, subprocess, urllib.request

def proc(pattern):
    r=subprocess.run(['pgrep','-f',pattern],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True)
    return r.returncode==0

def container(name):
    r=subprocess.run(['docker','inspect','-f','{{.State.Status}}|{{if .State.Health}}{{.State.Health.Status}}{{end}}',name],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True)
    return r.stdout.strip() if r.returncode==0 else 'missing'

def http(url):
    try:
        with urllib.request.urlopen(url,timeout=3) as r: return {'ok':200 <= r.status < 300,'status':r.status}
    except Exception as e: return {'ok':False,'error':type(e).__name__}

recordings=pathlib.Path.home()/'Videos'/'NABEEL'/'Recordings'
recent=[]
if recordings.exists():
    recent=sorted([str(p) for p in recordings.glob('*') if p.is_file()], key=lambda x: pathlib.Path(x).stat().st_mtime, reverse=True)[:5]

gates={
 'chiaki_binary': pathlib.Path('/usr/bin/chiaki').exists(),
 'chiaki_running': proc(r'(^|/)chiaki([ -]|$)'),
 'obs_binary': pathlib.Path('/usr/bin/obs').exists(),
 'obs_running': proc(r'(^|/)obs([ -]|$)'),
 'obs_profile': (pathlib.Path.home()/'.config/obs-studio/basic/profiles/NABEEL-1080p60/basic.ini').exists(),
 'obs_scene': (pathlib.Path.home()/'.config/obs-studio/basic/scenes/NABEEL-Station.json').exists(),
 'mediamtx_container': container('nabeel-mediamtx'),
 'owncast_container': container('nabeel-owncast'),
 'owncast_http': http('http://127.0.0.1:8081/api/status'),
 'recording_files': recent,
}
required_bool=['chiaki_binary','chiaki_running','obs_binary','obs_running','obs_profile','obs_scene']
ok=all(bool(gates[k]) for k in required_bool) and gates['mediamtx_container'].startswith('running') and gates['owncast_container'].startswith('running') and gates['owncast_http'].get('ok',False) and bool(recent)
result={'schema':'nabeel.staging-certificate.v1','pass':ok,'production_live_enabled':False,'gates':gates}
print(json.dumps(result,indent=2))
raise SystemExit(0 if ok else 1)
