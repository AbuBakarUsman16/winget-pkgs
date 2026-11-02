import math, subprocess, wave, numpy as np
from PIL import Image, ImageDraw, ImageFont
from tts import say, SR
W,H,FPS=1280,720,24
FT=lambda s:ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",s)
BG=(253,248,236); BLUE=(35,95,175); HOOD=(40,90,200); SKIN=(240,190,150); HAIR=(25,20,25)
def P(**k):return k
POSES=[
('Cat Stretch','cat',"Pose one! Cat stretch! Get on your hands and knees, and arch your back like a happy cat. Meow!",
 P(neck=(-110,-5),head=(-160,-30),le=(-112,45),lh=(-112,92),re=(-100,45),rh=(-100,92),lk=(0,92),lf=(70,92),rk=(12,92),rf=(82,92))),
('Doggy Stretch','dog',"Pose two! Doggy stretch! Hands and feet on the mat, lift your hips up high. Woof woof!",
 P(neck=(-80,90),head=(-108,118),le=(-118,130),lh=(-155,172),re=(-106,130),rh=(-143,172),lk=(38,86),lf=(72,172),rk=(48,86),rf=(84,172))),
('Cobra Pose','snake',"Pose three! Cobra pose! Lie on your tummy, push your hands down, and lift your chest. Hiss hiss!",
 P(neck=(-95,-60),head=(-118,-100),le=(-85,-20),lh=(-95,22),re=(-75,-20),rh=(-82,22),lk=(75,15),lf=(150,15),rk=(80,22),rf=(155,22))),
('Butterfly Pose','butterfly',"Pose four! Butterfly pose! Sit down, put your feet together, and flap your knees like wings!",
 P(neck=(0,-115),head=(0,-160),le=(-38,-55),lh=(-14,8),re=(38,-55),rh=(14,8),lk=(-85,-12),lf=(-10,15),rk=(85,-12),rf=(10,15))),
('Frog Jump','frog',"Pose five! Frog pose! Squat down low, hands on the floor, and get ready to jump! Ribbit!",
 P(neck=(-5,-105),head=(-5,-150),le=(-30,-30),lh=(-18,58),re=(30,-30),rh=(18,58),lk=(-75,-25),lf=(-50,58),rk=(75,-25),rf=(50,58))),
('Flamingo Balance','flamingo',"Pose six! Flamingo balance! Stand on one leg, open your arms wide, and stay very still.",
 P(neck=(0,-115),head=(0,-160),le=(-60,-100),lh=(-120,-120),re=(60,-100),rh=(120,-120),lk=(-6,72),lf=(-6,145),rk=(45,50),rf=(5,82))),
]
def cap(d,a,b,w,c):
    d.line([a,b],fill=c,width=int(w))
    for q in (a,b):d.ellipse((q[0]-w/2,q[1]-w/2,q[0]+w/2,q[1]+w/2),fill=c)
def girl(p,flap=0):
    S=2;im=Image.new('RGBA',(900*S,720*S));d=ImageDraw.Draw(im)
    p=dict(p);p['hip']=(0,0)
    if flap:p['lk']=(p['lk'][0],p['lk'][1]-flap);p['rk']=(p['rk'][0],p['rk'][1]-flap)
    xs=[v[0] for v in p.values()];ys=[v[1] for v in p.values()]
    sc=1.75;mx=(max(xs)+min(xs))/2
    T=lambda q:((450+(q[0]-mx)*sc)*S,(640+(q[1]-max(ys))*sc)*S)
    c=lambda k:T(p[k])
    # back limbs darker
    dk=(30,70,165)
    cap(d,c('neck'),c('re'),30*S*sc/1.75,dk);cap(d,c('re'),c('rh'),26*S,dk)
    cap(d,c('hip'),c('rk'),40*S,dk);cap(d,c('rk'),c('rf'),34*S,dk)
    for k in('rh',):x,y=c(k);r=17*S;d.ellipse((x-r,y-r,x+r,y+r),fill=SKIN)
    x,y=c('rf');d.ellipse((x-22*S,y-14*S,x+22*S,y+14*S),fill=SKIN)
    cap(d,c('hip'),c('neck'),62*S,HOOD)
    cap(d,c('hip'),c('lk'),40*S,HOOD);cap(d,c('lk'),c('lf'),34*S,HOOD)
    x,y=c('lf');d.ellipse((x-22*S,y-14*S,x+22*S,y+14*S),fill=SKIN)
    cap(d,c('neck'),c('le'),30*S,HOOD);cap(d,c('le'),c('lh'),26*S,HOOD)
    x,y=c('lh');r=17*S;d.ellipse((x-r,y-r,x+r,y+r),fill=SKIN)
    hx,hy=c('head');R=62*S
    for sgn in(-1,1):  # braids
        bx=hx+sgn*R*0.85
        for i in range(5):
            yy=hy+R*0.3+i*20*S;d.ellipse((bx-14*S,yy-12*S,bx+14*S,yy+12*S),fill=HAIR)
        d.polygon([(bx-12*S,yy+12*S),(bx+12*S,yy+12*S),(bx,yy+40*S)],fill=HAIR)
        d.ellipse((bx-14*S,hy+R*0.5-8*S,bx-2*S,hy+R*0.5+8*S),fill=(130,190,240));d.ellipse((bx+2*S,hy+R*0.5-8*S,bx+14*S,hy+R*0.5+8*S),fill=(130,190,240))
    d.ellipse((hx-R*1.05,hy-R*1.1,hx+R*1.05,hy+R*0.6),fill=HAIR)
    d.ellipse((hx-R*0.85,hy-R*0.7,hx+R*0.85,hy+R*0.95),fill=SKIN)
    d.chord((hx-R*0.95,hy-R*1.1,hx+R*0.95,hy-R*0.05),180,360,fill=HAIR)
    for sgn in(-1,1):
        ex=hx+sgn*R*0.35;ey=hy+R*0.15
        d.ellipse((ex-11*S,ey-15*S,ex+11*S,ey+15*S),fill=(40,25,20));d.ellipse((ex-6*S,ey-10*S,ex,ey-3*S),fill='white')
        d.ellipse((ex+sgn*4*S-12*S,ey+18*S,ex+sgn*4*S+12*S,ey+28*S),fill=(245,150,140))
    d.arc((hx-18*S,hy+R*0.35,hx+18*S,hy+R*0.65),20,160,fill=(160,60,50),width=4*S)
    return im.resize((900,720),Image.LANCZOS)
def animal(kind,cx,cy):
    im=Image.new('RGBA',(440,440));d=ImageDraw.Draw(im);x,y=220,230
    def face(col,ear,extra=None):
        for s in(-1,1):d.ellipse((x+s*95-35,y-120-35,x+s*95+35,y-120+35),fill=ear)
        d.ellipse((x-130,y-140,x+130,y+110),fill=col)
        if extra:extra()
        for s in(-1,1):d.ellipse((x+s*50-18,y-40-22,x+s*50+18,y-40+22),fill=(30,20,20));d.ellipse((x+s*50-8,y-52,x+s*50+2,y-42),fill='white');d.ellipse((x+s*85-22,y+5,x+s*85+22,y+30),fill=(255,150,150))
        d.arc((x-40,y-10,x+40,y+50),20,160,fill=(80,30,30),width=8)
    if kind=='cat':face((170,170,180),(150,150,160),lambda:[d.polygon([(x-130,y-80),(x-110,y-200),(x-40,y-125)],fill=(150,150,160)),d.polygon([(x+130,y-80),(x+110,y-200),(x+40,y-125)],fill=(150,150,160)),[d.line([(x+s*60,y+15),(x+s*150,y+s*0+5)],fill=(60,60,60),width=5) for s in(-1,1)]])
    elif kind=='dog':face((205,150,90),(120,75,40),lambda:d.ellipse((x-30,y-5,x+30,y+25),fill=(40,25,20)))
    elif kind=='frog':
        for s in(-1,1):d.ellipse((x+s*70-55,y-170,x+s*70+55,y-60),fill=(90,190,80))
        face((100,200,90),(100,200,90))
    elif kind=='snake':
        d.arc((60,150,380,400),200,520,fill=(100,180,70),width=60);d.ellipse((260,110,400,220),fill=(100,180,70))
        d.ellipse((300,135,325,165),fill='black');d.ellipse((345,135,370,165),fill='black');d.line([(330,210),(330,250),(315,265)],fill='red',width=6);d.line([(330,250),(345,265)],fill='red',width=6)
    elif kind=='butterfly':
        for s in(-1,1):d.ellipse((x+s*95-90,y-170,x+s*95+90,y+10),fill=(240,120,180));d.ellipse((x+s*80-65,y-10,x+s*80+65,y+130),fill=(255,190,80));d.ellipse((x+s*95-30,y-110,x+s*95+30,y-50),fill='white')
        d.ellipse((x-22,y-140,x+22,y+140),fill=(80,50,90));d.line([(x-8,y-135),(x-50,y-200)],fill=(80,50,90),width=6);d.line([(x+8,y-135),(x+50,y-200)],fill=(80,50,90),width=6)
    elif kind=='flamingo':
        d.ellipse((x-120,y-40,x+90,y+80),fill=(250,130,160));d.line([(x+60,y),(x+80,y-150)],fill=(250,130,160),width=30);d.ellipse((x+40,y-210,x+130,y-130),fill=(250,130,160))
        d.polygon([(x+125,y-175),(x+180,y-160),(x+125,y-150)],fill=(40,40,40));d.ellipse((x+85,y-190,x+102,y-172),fill='black');d.line([(x-10,y+75),(x-10,y+200)],fill=(230,110,140),width=10)
    return im.resize((200,200),Image.LANCZOS)
# timeline
INTRO,SEG,OUT=6,18.5,3
DUR=int(INTRO+SEG*len(POSES)+OUT)
aud=np.zeros(int(DUR*SR),np.float32)
import os
VO={"Hello friends! Welcome to kids yoga! Let's stretch like our animal friends!":'intro',"Great job!":'greatjob',"Yay! You did it! See you next time. Namaste!":'outro'}
def place(text,t,clip=None):
    clip=clip or VO.get(text);mp3=f'voices/{clip}.mp3' if clip else None
    if mp3 and os.path.exists(mp3):
        subprocess.run(['ffmpeg','-y','-v','error','-i',mp3,'-ar',str(SR),'-ac','1','k/v.wav'])
    else:
        say(text,'k/v.wav')
    w=wave.open('k/v.wav');a=np.frombuffer(w.readframes(w.getnframes()),np.int16)/32768;i=int(t*SR);a=a[:len(aud)-i];aud[i:i+len(a)]+=a*0.9;return len(a)/SR
place("Hello friends! Welcome to kids yoga! Let's stretch like our animal friends!",0.5)
nums="ten nine eight seven six five four three two one".split()
for k,(name,an,txt,_) in enumerate(POSES):
    t0=INTRO+k*SEG;dl=place(txt,t0+0.3,f'pose{k+1}');assert dl<8.4,(name,dl)
    if os.path.exists('voices/count.mp3'):place('',t0+8,'count')
    else:
        for j in range(10):place(nums[j],t0+8+j)
    place("Great job!",t0+17.9)
place("Yay! You did it! See you next time. Namaste!",DUR-OUT+0.1)
t=np.arange(len(aud))/SR;mus=np.zeros_like(aud)
notes=[261.6,329.6,392,523.3,392,329.6,293.7,349.2,440,587.3,440,349.2]
for i in range(int(DUR/0.5)):
    f=notes[i%len(notes)];s=int(i*0.5*SR);n=min(int(0.5*SR),len(aud)-s);tt=np.arange(n)/SR
    mus[s:s+n]+=(np.sin(2*np.pi*f*tt)+0.3*np.sin(4*np.pi*f*tt))*np.exp(-tt*5)*0.07
aud=aud+mus;aud/=max(1,np.abs(aud).max())
with wave.open('k/a.wav','wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR);f.writeframes((aud*32000).astype(np.int16).tobytes())
# frames
base=Image.new('RGB',(W,H),BG);bd=ImageDraw.Draw(base);bd.rounded_rectangle((250,640,1150,720),30,fill=(170,205,240))
gcache=[girl(p[3]) for p in POSES];acache=[animal(p[1],0,0) for p in POSES]
fly=[girl(POSES[3][3],flap=f) for f in(0,15,30)]
intro_g=girl(POSES[3][3])
pr=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i','k/a.wav','-c:v','libx264','-pix_fmt','yuv420p','-crf','22','-c:a','aac','-b:a','128k','-shortest','kids_yoga.mp4'],stdin=subprocess.PIPE)
def badge(d,num,frac):
    cx,cy,r=1180-40,105,85
    d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=BLUE)
    for a in range(0,360,6):
        A=math.radians(a);d.ellipse((cx+(r-6)*math.cos(A)-2,cy+(r-6)*math.sin(A)-2,cx+(r-6)*math.cos(A)+2,cy+(r-6)*math.sin(A)+2),fill='white')
    if frac is not None:d.arc((cx-r-10,cy-r-10,cx+r+10,cy+r+10),-90,-90+360*frac,fill=(255,190,60),width=10)
    d.text((cx,cy),str(num),font=FT(100),fill='white',anchor='mm')
for fi in range(int(DUR*FPS)):
    T=fi/FPS;im=base.copy();d=ImageDraw.Draw(im)
    if T<INTRO:
        d.text((640,110),"Kids Yoga Time!",font=FT(84),fill=BLUE,anchor='mm');d.text((640,190),"Stretch like animals",font=FT(44),fill=(240,120,60),anchor='mm')
        for k,a in enumerate(acache):im.paste(a.resize((120,120)),(40+(k%2)*1080,240+(k//2)*130),a.resize((120,120)))
        g=intro_g;bob=int(6*math.sin(T*3));im.paste(g,(190,bob),g)
    elif T<DUR-OUT:
        k=int((T-INTRO)//SEG);lt=(T-INTRO)-k*SEG;name=POSES[k][0]
        g=fly[int(T*6)%3] if POSES[k][1]=='butterfly' and lt>7.5 else gcache[k]
        bob=int(4*math.sin(T*2.5));im.paste(g,(220,bob+10),g);a=acache[k];im.paste(a,(55,170+int(8*math.sin(T*4))),a)
        d.text((60,80),name+':',font=FT(60),fill=(20,20,20),anchor='lm')
        if lt<8:badge(d,k+1,None)
        elif lt<18:badge(d,10-int(lt-8),(lt-8)/10)
        else:badge(d,'★' if False else 'OK',None)
        if lt>17.9:d.text((640,330),"Great job!",font=FT(90),fill=(240,120,60),anchor='mm',stroke_width=6,stroke_fill='white')
        # progress bar segments
        for s in range(len(POSES)):
            x0=10+s*(W-20)/len(POSES);x1=x0+(W-20)/len(POSES)-8;d.rectangle((x0,H-8,x1,H-2),fill=(200,200,200))
            fr=1 if s<k else (lt/SEG if s==k else 0);d.rectangle((x0,H-8,x0+(x1-x0)*fr,H-2),fill=(230,30,50))
    else:
        d.text((640,250),"Namaste!",font=FT(120),fill=BLUE,anchor='mm');d.text((640,360),"Great job, yoga stars!",font=FT(54),fill=(240,120,60),anchor='mm')
    pr.stdin.write(im.tobytes())
pr.stdin.close();pr.wait()
