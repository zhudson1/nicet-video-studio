import math, os, pathlib, subprocess, textwrap, wave
from PIL import Image, ImageDraw, ImageFont
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/"output"; OUT.mkdir(exist_ok=True)
W,H=720,1280
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SCENES=[
("WHAT DOES A CONTROL MODULE DO?","This small device can control another system, but how?",0),
("PANEL COMMAND","A compatible fire alarm panel sends a command to its addressable control module.",1),
("MODULE OUTPUT","Depending on the listed model, the module operates an output circuit or relay.",2),
("CONNECTED EQUIPMENT","That output may interface with equipment according to the approved system design.",3),
("CHECK THE DOCUMENTATION","Always verify the manufacturer's wiring instructions and approved design.",4)]
def run(args): subprocess.run(args,check=True)
def label(draw,xy,s,size=29,color="#f3f8fc",bold=False):
    draw.text(xy,s,font=ImageFont.truetype(BOLD if bold else FONT,size),fill=color)
def draw_scene(title,caption,step):
    im=Image.new("RGB",(W,H),"#091725"); d=ImageDraw.Draw(im)
    for y in range(0,H,45):d.line((0,y,W,y),fill="#102536",width=1)
    d.rectangle((0,0,W,9),fill="#22dbc0")
    label(d,(42,55),"FIRE ALARM  /  TECH EXPLAINED",23,"#22dbc0",True)
    label(d,(42,140),title,34,"#ffffff",True)
    # Simplified conceptual illustration, not a wiring diagram.
    boxes=[(40,380,224,625,"FIRE ALARM","PANEL"),(266,380,455,625,"CONTROL","MODULE"),(497,380,683,625,"EXTERNAL","EQUIPMENT")]
    for i,(x1,y1,x2,y2,t1,t2) in enumerate(boxes):
        active=i<=min(step,2)
        d.rounded_rectangle((x1,y1,x2,y2),radius=17,fill="#143449" if active else "#112434",outline="#22dbc0" if active else "#456174",width=4)
        label(d,(x1+13,y1+72),t1,17,"#e4f8f5",True);label(d,(x1+13,y1+103),t2,17,"#e4f8f5",True)
        for k in range(3):d.ellipse((x1+25+k*30,y1+158,x1+36+k*30,y1+169),fill="#22dbc0" if active else "#466377")
    for j,(xa,xb) in enumerate([(224,266),(455,497)]):
        on=step>=j+1
        d.line((xa,500,xb,500),fill="#22dbc0" if on else "#496a7b",width=7)
        if on:d.polygon([(xb-4,490),(xb+5,500),(xb-4,510)],fill="#22dbc0")
    d.rounded_rectangle((40,720,680,968),radius=22,fill="#102d40")
    words=textwrap.wrap(caption,width=35)
    for i,line in enumerate(words):label(d,(70,755+i*50),line,27,"#ffffff")
    label(d,(40,1090),"CONCEPTUAL ANIMATION — NOT A WIRING DIAGRAM",17,"#91aaba")
    label(d,(40,1140),f"NICET STUDY  •  {step+1:02}/{len(SCENES):02}",22,"#22dbc0",True)
    return im
clips=[]
for i,(title,narration,step) in enumerate(SCENES):
    png=OUT/f"scene_{i}.png"; draw_scene(title,narration,step).save(png)
    wav=OUT/f"scene_{i}.wav"
    run(["espeak-ng","-v","en-us","-s","150","-w",str(wav),narration])
    with wave.open(str(wav),"rb") as w: duration=w.getnframes()/w.getframerate()+0.6
    mp4=OUT/f"scene_{i}.mp4"
    run(["ffmpeg","-hide_banner","-loglevel","error","-y","-loop","1","-framerate","24","-i",str(png),"-i",str(wav),"-filter_complex","[1:a]apad=pad_dur=0.6[a]","-map","0:v","-map","[a]","-t",f"{duration:.2f}","-c:v","libx264","-preset","ultrafast","-pix_fmt","yuv420p","-r","24","-c:a","aac","-b:a","128k",str(mp4)])
    clips.append(mp4)
concat=OUT/"concat.txt"
concat.write_text("".join("file '"+str(p.resolve())+"'\n" for p in clips))
final=OUT/"preview.mp4"
run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(concat),"-c","copy",str(final)])
if final.stat().st_size<20000:raise RuntimeError("Output too small")
print("Created",final,final.stat().st_size)
