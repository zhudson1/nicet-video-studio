#!/usr/bin/env python3
"""Assemble six approved 9:16 scene clips and narration into a review MP4.
Usage: python scripts/assemble_template.py assets/episode-01
Requires ffmpeg and ffprobe. Does not create or invent branded footage.
"""
import pathlib, subprocess, sys, json
def run(args):
    subprocess.run(args, check=True)
def probe(path):
    p=subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=width,height","-of","json",str(path)],capture_output=True,text=True,check=True)
    return json.loads(p.stdout)["streams"][0]
def main():
    if len(sys.argv)!=2: raise SystemExit("Usage: python scripts/assemble_template.py assets/episode-01")
    root=pathlib.Path(sys.argv[1]); shots=[root/f"shot-{i:02}.mp4" for i in range(1,7)]
    missing=[str(p) for p in shots if not p.is_file()]
    if missing: raise SystemExit("Missing approved scene clips: "+", ".join(missing))
    for p in shots:
        d=probe(p)
        if d["width"]*9!=d["height"]*16: raise SystemExit(f"{p} is not 9:16")
    voice=root/"voiceover.wav"
    if not voice.is_file(): raise SystemExit("Missing natural voiceover.wav")
    out=pathlib.Path("output");out.mkdir(exist_ok=True)
    norm=[]
    for i,p in enumerate(shots):
        dest=out/f"normalized-{i:02}.mp4"
        run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(p),"-vf","scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p","-an","-c:v","libx264","-preset","medium","-crf","19",str(dest)])
        norm.append(dest.resolve())
    playlist=out/"shots.txt"
    playlist.write_text("".join("file '"+str(p).replace("'","'\\''")+"'\n" for p in norm))
    video=out/"joined.mp4"
    run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(playlist),"-c","copy",str(video)])
    final=out/"episode-review.mp4"
    cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(video),"-i",str(voice),"-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","aac","-b:a","192k","-shortest"]
    captions=root/"captions.srt"
    if captions.is_file():
        # Captions kept as a selectable subtitle track; platform-specific burned-in
        # subtitles require a separate QC step.
        cmd+=["-i",str(captions)]
        # Reorder inputs/maps to add subtitle track.
        cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(video),"-i",str(voice),"-i",str(captions),"-map","0:v:0","-map","1:a:0","-map","2:s:0","-c:v","copy","-c:a","aac","-b:a","192k","-c:s","mov_text","-shortest"]
    run(cmd+[str(final)])
    print("Review render:",final.resolve())
if __name__=="__main__": main()
