#!/usr/bin/env python3
import argparse, json, os, shlex, subprocess, sys
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
    cmd=["mmx","vision","describe"]
    if cfg.get("image"): cmd += ["--image",cfg["image"]]
    elif cfg.get("file_id"): cmd += ["--file-id",cfg["file_id"]]
    else: raise SystemExit("need --image or --file-id")
    if cfg.get("prompt"): cmd += ["--prompt",cfg["prompt"]]
    add_global(cmd,cfg)
    if cfg.get("quiet",True): cmd += ["--quiet"]
    if cfg.get("non_interactive",True): cmd += ["--non-interactive"]
    return cmd

def plan(a):
    cfg={"mode":"vision.describe","image":a.image,"file_id":a.file_id,"prompt":a.prompt,"api_key":a.api_key,"region":a.region,"base_url":a.base_url,"output":a.output,"timeout":a.timeout,"verbose":a.verbose,"dry_run":a.dry_run,"no_color":a.no_color,"quiet":a.quiet,"non_interactive":True}
    if a.interactive:
        if not cfg["image"] and not cfg["file_id"]: cfg["image"]=ask("Image path or URL")
        if not cfg["prompt"]: cfg["prompt"]=ask("Question prompt","Describe the image.")
    if not cfg.get("image") and not cfg.get("file_id"): raise SystemExit("plan requires --image or --file-id")
    os.makedirs(os.path.expanduser(os.path.dirname(a.plan_file)), exist_ok=True)
    with open(os.path.expanduser(a.plan_file),"w",encoding="utf-8") as f: json.dump(cfg,f,ensure_ascii=False,indent=2)
    print("Plan saved:",os.path.expanduser(a.plan_file)); print("Preview command:"); print(" ".join(shlex.quote(x) for x in build(cfg)))

def run(a):
    cfg={}
    if getattr(a, "plan_file", None):
        with open(os.path.expanduser(a.plan_file),"r",encoding="utf-8") as f: cfg=json.load(f)
    for k in ["image","file_id","prompt","api_key","region","base_url","output","timeout","verbose","dry_run","no_color","quiet"]:
        v=getattr(a,k,None)
        if v not in (None,""): cfg[k]=v
    cfg.setdefault("non_interactive",True)
    raise SystemExit(subprocess.call(build(cfg)))

def add(p):
    p.add_argument("--image")
    p.add_argument("--file-id")
    p.add_argument("--prompt")
    p.add_argument("--api-key")
    p.add_argument("--region")
    p.add_argument("--base-url")
    p.add_argument("--output")
    p.add_argument("--timeout",type=int)
    p.add_argument("--verbose",action="store_true")
    p.add_argument("--dry-run",action="store_true")
    p.add_argument("--no-color",action="store_true")
    p.add_argument("--quiet",action="store_true")

def parse_args():
    # Direct-first: if first token is not plan/run, treat as run mode.
    argv = sys.argv[1:]
    if not argv or argv[0] not in {"plan", "run"}:
        argv = ["run", *argv]

    p=argparse.ArgumentParser(description="max-vision (direct-first, optional plan/run)")
    sp=p.add_subparsers(dest="cmd",required=True)
    pp=sp.add_parser("plan"); add(pp); pp.add_argument("--interactive",action="store_true"); pp.add_argument("--plan-file",default=f"~/Downloads/max-gen/plans/vision_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    pr=sp.add_parser("run"); add(pr); pr.add_argument("--plan-file")
    return p.parse_args(argv)

def main():
    a=parse_args()
    plan(a) if a.cmd=="plan" else run(a)

if __name__=="__main__": main()
