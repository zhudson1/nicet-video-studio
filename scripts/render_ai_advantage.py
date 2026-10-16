import json, os, pathlib, subprocess, sys, textwrap, wave
from PIL import Image, ImageDraw, ImageFont
ROOT=pathlib.Path(__file__).resolve().parents[1]
episodes=json.loads((ROOT/"ai-advantage/episodes.json").read_text())
idx=int(os.environ.get("EPISODE","1"))-1
if not 0<=idx<len(episodes): raise ValueError("EPISODE must be 1..10")
episode=episodes[idx]
out=ROOT/"output"/"ai-advantage";out.mkdir(parents=True,exist_ok=True)
W,H=720,1280
font="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
regular="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def run(cmd):subprocess.run(cmd,check=True)
sentences=[s.strip() for s in episode["narration"].replace("! ", ". ").split(". ") if s.strip()]
scenes=[episode["title"]]+sentences+[episode["cta"]]
paths=[]
for i,caption in enumerate(scenes):
 im=Image.new("RGB",(W,H),"#101820");d=ImageDraw.Draw(im)
 d.rectangle((0,0,W,12),fill="#6ee7b7")
 d.text((42,65),"THE AI ADVANTAGE",font=ImageFont.truetype(font,29),fill="#6ee7b7")
 d.text((42,110),f"EPISODE {idx+1:02d}  /  DRAFT",font=ImageFont.truetype(regular,23),fill="#a0aec0")
 for j,line in enumerate(textwrap.wrap(caption,29)[:9]):
  d.text((46,380+j*66),line,font=ImageFont.truetype(font,35),fill="white")
 d.text((42,1150),"ORIGINAL COMMENTARY • REVIEW BEFORE POSTING",font=ImageFont.truetype(regular,17),fill="#6ee7b7")
 png=out/f"frame{i}.png";im.save(png)
 wav=out/f"voice{i}.wav"
 run(["espeak-ng","-v","en-us","-s","155","-w",str(wav),caption])
 with wave.open(str(wav),"rb") as f: duration=f.getnframes()/f.getframerate()+0.5
 mp4=out/f"clip{i}.mp4"
 run(["ffmpeg","-loglevel","error","-y","-loop","1","-framerate","24","-i",str(png),"-i",str(wav),"-af","apad","-t",str(duration),"-c:v","libx264","-preset","ultrafast","-pix_fmt","yuv420p","-c:a","aac",str(mp4)])
 paths.append(mp4)
concat=out/"concat.txt";concat.write_text("".join("file '"+str(p.resolve())+"'\n" for p in paths))
target=out/f"episode-{idx+1:02d}-REVIEW-ONLY.mp4"
run(["ffmpeg","-loglevel","error","-y","-f","concat","-safe","0","-i",str(concat),"-c","copy",str(target)])
print(target)
