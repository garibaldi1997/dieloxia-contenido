import json,sys,subprocess
d,voz,sp,qs,wa=sys.argv[1],sys.argv[2],float(sys.argv[3]),sys.argv[4].split(','),sys.argv[5]
W=json.load(open(voz+'.json'))
def at(w,n=0):
    m=[x['t'] for x in W if x['w'].lower().strip('¿?.,')==w or (len(w)>3 and x['w'].lower().strip('¿?.,').startswith(w))]
    return m[min(n,len(m)-1)]
dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',voz+'.mp3']))/sp
dings=','.join(f'{at(q)/sp:.2f}' for q in qs)
a=at(wa)/sp
subprocess.run(['/usr/bin/python3','/home/user/dieloxia-contenido/plantillas/reel_historia/bed.py',d+'/bed.wav',f'{dur+.5:.2f}',dings,f'{a-.4:.2f},{a+.4:.2f}'],check=True)
print(d,dings,a)
