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
    cmd=["mmx","text","chat","--model",cfg.get("model","MiniMax-M2.7-highspeed")]
    if cfg.get("system"): cmd += ["--system",cfg["system"]]
    if cfg.get("messages_file"): cmd += ["--messages-file",cfg["messages_file"]]
    else:
        msgs=cfg.get("message",[])
        if isinstance(msgs,str): msgs=[msgs]
        for m in msgs: cmd += ["--message",m]
    if cfg.get("max_tokens") is not None: cmd += ["--max-tokens",str(cfg["max_tokens"])]
    if cfg.get("temperature") is not None: cmd += ["--temperature",str(cfg["temperature"])]
    if cfg.get("top_p") is not None: cmd += ["--top-p",str(cfg["top_p"])]
    if cfg.get("stream"): cmd += ["--stream"]
    tools=cfg.get("tool",[])
    if isinstance(tools,str): tools=[tools]
    for t in tools: cmd += ["--tool",t]
    add_global(cmd,cfg)
    if cfg.get("quiet",True): cmd += ["--quiet"]
    if cfg.get("non_interactive",True): cmd += ["--non-interactive"]
    return cmd

def plan(a):
    cfg={"mode":"text.chat","model":a.model,"message":a.message or [],"messages_file":a.messages_file,"system":a.system,"max_tokens":a.max_tokens,"temperature":a.temperature,"top_p":a.top_p,"stream":a.stream,"tool":a.tool or [],"api_key":a.api_key,"region":a.region,"base_url":a.base_url,"output":a.output,"timeout":a.timeout,"verbose":a.verbose,"dry_run":a.dry_run,"no_color":a.no_color,"quiet":a.quiet,"non_interactive":True}
    if a.interactive and not cfg["messages_file"] and not cfg["message"]:
        cfg["message"]=[ask("User message","user:请简要介绍MiniMax模型能力")]
    if not cfg["messages_file"] and not cfg["message"]:
        raise SystemExit("plan requires --message or --messages-file")
    os.makedirs(os.path.expanduser(os.path.dirname(a.plan_file)), exist_ok=True)
    with open(os.path.expanduser(a.plan_file),"w",encoding="utf-8") as f: json.dump(cfg,f,ensure_ascii=False,indent=2)
    print("Plan saved:",os.path.expanduser(a.plan_file)); print("Preview command:"); print(" ".join(shlex.quote(x) for x in build(cfg)))

def run(a):
    cfg={}
    if a.plan_file:
        with open(os.path.expanduser(a.plan_file),"r",encoding="utf-8") as f: cfg=json.load(f)
    for k in ["model","messages_file","system","max_tokens","temperature","top_p","api_key","region","base_url","output","timeout","verbose","dry_run","no_color","quiet"]:
        v=getattr(a,k)
        if v not in (None,""): cfg[k]=v
    if a.message: cfg["message"]=a.message
    if a.tool: cfg["tool"]=a.tool
    if a.stream: cfg["stream"]=True
    cfg.setdefault("non_interactive",True)
    raise SystemExit(subprocess.call(build(cfg)))

def add(p):
    p.add_argument("--model",default="MiniMax-M2.7-highspeed")
    p.add_argument("--message",action="append")
    p.add_argument("--messages-file")
    p.add_argument("--system")
    p.add_argument("--max-tokens",type=int)
    p.add_argument("--temperature",type=float)
    p.add_argument("--top-p",type=float)
    p.add_argument("--stream",action="store_true")
    p.add_argument("--tool",action="append")
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
    p=argparse.ArgumentParser(description="max-text-chat with plan/run")
    sp=p.add_subparsers(dest="cmd",required=True)
    pp=sp.add_parser("plan"); add(pp); pp.add_argument("--interactive",action="store_true"); pp.add_argument("--plan-file",default=f"~/Downloads/max-gen/plans/text_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    pr=sp.add_parser("run"); add(pr); pr.add_argument("--plan-file")
    a=p.parse_args(); plan(a) if a.cmd=="plan" else run(a)

if __name__=="__main__": main()
