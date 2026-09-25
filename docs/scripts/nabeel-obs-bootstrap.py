#!/usr/bin/env python3
import configparser, json, os, shutil, time
from pathlib import Path

home=Path.home()
root=Path(os.environ.get('NABEEL_MEDIA_ROOT',home/'Videos'/'NABEEL'))
for name in ('Recordings','Clips','Exports','Archive'): (root/name).mkdir(parents=True,exist_ok=True)
cfg=Path(os.environ.get('OBS_CONFIG_ROOT',home/'.config'/'obs-studio'))
profile=cfg/'basic'/'profiles'/'NABEEL-1080p60'
scenes=cfg/'basic'/'scenes'
profile.mkdir(parents=True,exist_ok=True); scenes.mkdir(parents=True,exist_ok=True)

for f in (profile/'basic.ini', profile/'service.json', scenes/'NABEEL-Station.json'):
    if f.exists(): shutil.copy2(f, f.with_suffix(f.suffix+'.bak-'+time.strftime('%Y%m%dT%H%M%S')))

basic=configparser.ConfigParser(interpolation=None)
basic.optionxform=str
basic['General']={'Name':'NABEEL-1080p60'}
basic['Video']={'BaseCX':'1920','BaseCY':'1080','OutputCX':'1920','OutputCY':'1080','FPSCommon':'60','ScaleType':'bicubic'}
basic['Output']={'Mode':'Advanced','FilenameFormatting':'NABEEL-%CCYY-%MM-%DD-%hh%mm%ss'}
basic['AdvOut']={'RecType':'Standard','RecFilePath':str(root/'Recordings'),'RecFormat2':'mkv','RecEncoder':'obs_x264','RecTracks':'1','RecMuxerCustom':'','TrackIndex':'1'}
basic['Audio']={'SampleRate':'48000','ChannelSetup':'Stereo'}
with (profile/'basic.ini').open('w',encoding='utf-8') as fh: basic.write(fh)
(profile/'service.json').write_text(json.dumps({'type':'rtmp_custom','settings':{'server':'','key':'','use_auth':False}},indent=2)+'\n')

scene={
 'name':'NABEEL Station',
 'current_scene':'Gameplay',
 'current_program_scene':'Gameplay',
 'scene_order':[{'name':'Gameplay'}],
 'sources':[{'prev_ver':536936448,'name':'Gameplay','uuid':'nabeel-gameplay-scene','id':'scene','versioned_id':'scene','settings':{'id_counter':0,'custom_size':False,'items':[]},'mixers':0,'sync':0,'flags':0,'volume':1.0,'balance':0.5,'enabled':True,'muted':False,'push-to-mute':False,'push-to-mute-delay':0,'push-to-talk':False,'push-to-talk-delay':0,'hotkeys':{},'deinterlace_mode':0,'deinterlace_field_order':0,'monitoring_type':0,'private_settings':{}}],
 'groups':[], 'transitions':[], 'saved_projectors':[],
}
(scenes/'NABEEL-Station.json').write_text(json.dumps(scene,indent=2)+'\n')
print(json.dumps({'profile':str(profile),'scene_collection':str(scenes/'NABEEL-Station.json'),'recording_path':str(root/'Recordings'),'format':'mkv','resolution':'1920x1080','fps':60},indent=2))
