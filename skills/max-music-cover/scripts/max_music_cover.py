#!/usr/bin/env python3
import argparse, json, os, shlex, subprocess
from datetime import datetime

def ask(p,d=""):
    s=f" [{d}]" if d else ""
    v=input(f"{p}{s}: ").strip()
    return v if v else d

def add_global(cmd,cfg):
    for k,flag in {"api_key":"--api-key","region":"--region","base_url":"--base-url","output":"--output","timeout":"--timeout"}.items():
        if cfg.get(k): cmd += [flag,str(cfg[k])]
    if cfg.get("verbose"): cmd += ["--verbose"]
    if cfg.get("dry_run"): cmd += ["--dry-run"]
    if cfg.get("no_color"): cmd += ["--no-color"]

def build(cfg):
    cmd=["mmx","music","cover","--prompt",cfg["prompt"],"--model",cfg["model"]]
    if cfg.get("audio"): cmd += ["--audio",cfg["audio"]]
    elif cfg.get("audio_file"): cmd += ["--audio-file",cfg["audio_file"]]
    else: raise SystemExit("need --audio or --audio-file")
    if cfg.get("lyrics"): cmd += ["--lyrics",cfg["lyrics"]]
    if cfg.get("lyrics_file"): cmd += ["--lyrics-file",cfg["lyrics_file"]]
    if cfg.get("seed") is not None: cmd += ["--seed",str(cfg["seed"])]
    if cfg.get("format"): cmd += ["--format",cfg["format"]]
    if cfg.get("sample_rate") is not None: cmd += ["--sample-rate",str(cfg["sample_rate"])]
    if cfg.get("bitrate") is not None: cmd += ["--bitrate",str(cfg["bitrate"])]
    if cfg.get("channel") is not None: cmd += ["--channel",str(cfg["channel"])]
    if cfg.get("stream"): cmd += ["--stream"]
    if cfg.get("out"): cmd += ["--out",os.path.expanduser(cfg["out"])]
    add_global(cmd,cfg)
    if cfg.get("quiet",True): cmd += ["--quiet"]
    if cfg.get("non_interactive",True): cmd += ["--non-interactive"]
    return cmd

def plan(a):
    cfg={"mode":"music.cover","prompt":a.prompt,"model":a.model,"audio":a.audio,"audio_file":a.audio_file,"lyrics":a.lyrics,"lyrics_file":a.lyrics_file,"seed":a.seed,"format":a.format,"sample_rate":a.sample_rate,"bitrate":a.bitrate,"channel":a.channel,"stream":a.stream,"out":a.out,"api_key":a.api_key,"region":a.region,"base_url":a.base_url,"output":a.output,"timeout":a.timeout,"verbose":a.verbose,"dry_run":a.dry_run,"no_color":a.no_color,"quiet":a.quiet,"non_interactive":True}
    if a.interactive:
        if not cfg["prompt"]: cfg["prompt"]=ask("Cover style prompt","Indie folk, warm male vocal")
        if not cfg["audio"] and not cfg["audio_file"]: cfg["audio_file"]=ask("Reference audio file path")
    if not cfg.get("prompt"): raise SystemExit("plan requires --prompt")
    if not cfg.get("audio") and not cfg.get("audio_file"): raise SystemExit("plan requires --audio or --audio-file")
    os.makedirs(os.path.expanduser(os.path.dirname(a.plan_file)), exist_ok=True)
    with open(os.path.expanduser(a.plan_file),"w",encoding="utf-8") as f: json.dump(cfg,f,ensure_ascii=False,indent=2)
    print("Plan saved:",os.path.expanduser(a.plan_file)); print("Preview command:"); print(" ".join(shlex.quote(x) for x in build(cfg)))

def run(a):
    cfg={}
    if a.plan_file:
        with open(os.path.expanduser(a.plan_file),"r",encoding="utf-8") as f: cfg=json.load(f)
    for k in ["prompt","model","audio","audio_file","lyrics","lyrics_file","seed","format","sample_rate","bitrate","channel","stream","out","api_key","region","base_url","output","timeout","verbose","dry_run","no_color","quiet"]:
        v=getattr(a,k)
        if v not in (None,""): cfg[k]=v
    cfg.setdefault("non_interactive",True)
    if cfg.get("out"): os.makedirs(os.path.dirname(os.path.expanduser(cfg["out"])) or ".", exist_ok=True)
    raise SystemExit(subprocess.call(build(cfg)))

def add(p):
    p.add_argument("--prompt")
    p.add_argument("--model",default="music-cover")
    p.add_argument("--audio")
    p.add_argument("--audio-file")
    p.add_argument("--lyrics")
    p.add_argument("--lyrics-file")
    p.add_argument("--seed",type=int)
    p.add_argument("--format",default="mp3")
    p.add_argument("--sample-rate",dest="sample_rate",type=int)
    p.add_argument("--bitrate",type=int)
    p.add_argument("--channel",type=int)
    p.add_argument("--stream",action="store_true")
    p.add_argument("--out",default="~/Downloads/max-gen/music/cover_output.mp3")
    p.add_argument("--api-key")
    p.add_argument("--region")
    p.add_argument("--base-url")
    p.add_argument("--output")
    p.add_argument("--timeout",type=int)
    p.add_argument("--verbose",action="store_true")
    p.add_argument("--dry-run",action="store_true")
    p.add_argument("--no-color",action="store_true")
    p.add_argument("--quiet",action="store_true")

def main():
    p=argparse.ArgumentParser(description="max-music-cover with plan/run")
    sp=p.add_subparsers(dest="cmd",required=True)
    pp=sp.add_parser("plan"); add(pp); pp.add_argument("--interactive",action="store_true"); pp.add_argument("--plan-file",default=f"~/Downloads/max-gen/plans/music_cover_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    pr=sp.add_parser("run"); add(pr); pr.add_argument("--plan-file")
    a=p.parse_args(); plan(a) if a.cmd=="plan" else run(a)

if __name__=="__main__": main()
