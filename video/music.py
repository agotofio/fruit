import numpy as np, wave, json
sr=44100; T=json.load(open('timeline.json'))['total']+0.5; n=int(sr*T); t=np.arange(n)/sr
out=np.zeros(n)
def note(f): return 440*2**((f-69)/12)
prog=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]  # Am F C G
beat=2.0
for k in range(int(T/beat)+1):
    ch=prog[k%4]; st=int(k*beat*sr); L=min(int(beat*1.6*sr),n-st)
    if L<=0: break
    tt=np.arange(L)/sr; env=np.minimum(tt/0.4,1)*np.exp(-tt*0.9)
    for m in ch:
        f=note(m); out[st:st+L]+=env*(np.sin(2*np.pi*f*tt)+0.3*np.sin(4*np.pi*f*tt))*0.12
    f=note(ch[0]-12); out[st:st+L]+=env*np.sin(2*np.pi*f*tt)*0.18
    for j,m in enumerate([ch[2]+12,ch[1]+12,ch[0]+12,ch[1]+12]):  # soft arpeggio
        s2=st+int(j*0.5*sr); L2=min(int(0.9*sr),n-s2)
        if L2<=0: continue
        t2=np.arange(L2)/sr; out[s2:s2+L2]+=np.exp(-t2*4)*np.sin(2*np.pi*note(m)*t2)*0.08
rng=np.random.default_rng(1); noise=rng.standard_normal(n)
from numpy.fft import rfft,irfft
F=rfft(noise); fr=np.fft.rfftfreq(n,1/sr); F[fr>3000]*=0.15; F[fr<200]*=0.2
out+=irfft(F,n)*0.025
out/=np.abs(out).max()*1.1
w=wave.open('music.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
