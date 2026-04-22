#!/usr/bin/env python3
import argparse
import json
import os
import shlex
import subprocess
from datetime import datetime


def ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    v = input(f"{prompt}{suffix}: ").strip()
    return v if v else default


def add_global_flags(cmd, cfg):
    for k, flag in {
        "api_key": "--api-key",
        "region": "--region",
        "base_url": "--base-url",
        "output": "--output",
        "timeout": "--timeout",
    }.items():
        if cfg.get(k):
            cmd += [flag, str(cfg[k])]
    if cfg.get("verbose"):
        cmd.append("--verbose")
    if cfg.get("dry_run"):
        cmd.append("--dry-run")
    if cfg.get("no_color"):
        cmd.append("--no-color")


def build_cmd(cfg):
    cmd = ["mmx", "speech", "synthesize", "--model", cfg["model"], "--voice", cfg["voice"]]
    if cfg.get("text"):
        cmd += ["--text", cfg["text"]]
    elif cfg.get("text_file"):
        cmd += ["--text-file", cfg["text_file"]]
    else:
        raise SystemExit("Need text or text_file")

    for k, flag in {
        "speed": "--speed",
        "volume": "--volume",
        "pitch": "--pitch",
        "format": "--format",
        "sample_rate": "--sample-rate",
        "bitrate": "--bitrate",
        "channels": "--channels",
        "language": "--language",
        "out": "--out",
    }.items():
        if cfg.get(k) not in (None, ""):
            val = os.path.expanduser(cfg[k]) if k == "out" else cfg[k]
            cmd += [flag, str(val)]

    if cfg.get("subtitles"):
        cmd.append("--subtitles")
    if cfg.get("stream"):
        cmd.append("--stream")
    for p in cfg.get("pronunciation", []):
        cmd += ["--pronunciation", p]

    add_global_flags(cmd, cfg)
    if cfg.get("quiet", True):
        cmd.append("--quiet")
    if cfg.get("non_interactive", True):
        cmd.append("--non-interactive")
    return cmd


def plan(args):
    cfg = {
        "mode": "speech.synthesize",
        "text": args.text,
        "text_file": args.text_file,
        "model": args.model,
        "voice": args.voice,
        "speed": args.speed,
        "volume": args.volume,
        "pitch": args.pitch,
        "format": args.format,
        "sample_rate": args.sample_rate,
        "bitrate": args.bitrate,
        "channels": args.channels,
        "language": args.language,
        "subtitles": args.subtitles,
        "stream": args.stream,
        "pronunciation": args.pronunciation or [],
        "out": args.out,
        "api_key": args.api_key,
        "region": args.region,
        "base_url": args.base_url,
        "output": args.output,
        "timeout": args.timeout,
        "verbose": args.verbose,
        "dry_run": args.dry_run,
        "no_color": args.no_color,
        "quiet": args.quiet,
        "non_interactive": True,
    }

    if args.interactive:
        if not cfg["text"] and not cfg["text_file"]:
            cfg["text"] = ask("TTS text", "你好，这是MiniMax语音测试")
        cfg["voice"] = ask("Voice", cfg["voice"])
        cfg["model"] = ask("Model", cfg["model"])
        cfg["out"] = ask("Output path", cfg["out"])

    if not cfg["text"] and not cfg["text_file"]:
        raise SystemExit("plan requires --text/--text-file or --interactive")

    os.makedirs(os.path.expanduser(os.path.dirname(args.plan_file)), exist_ok=True)
    with open(os.path.expanduser(args.plan_file), "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

    print("Plan saved:", os.path.expanduser(args.plan_file))
    print("Preview command:")
    print(" ".join(shlex.quote(x) for x in build_cmd(cfg)))


def run(args):
    cfg = {}
    if args.plan_file:
        with open(os.path.expanduser(args.plan_file), "r", encoding="utf-8") as f:
            cfg = json.load(f)

    for k in [
        "text", "text_file", "model", "voice", "speed", "volume", "pitch", "format",
        "sample_rate", "bitrate", "channels", "language", "out", "api_key", "region",
        "base_url", "output", "timeout", "subtitles", "stream", "verbose", "dry_run", "no_color", "quiet"
    ]:
        v = getattr(args, k)
        if v not in (None, ""):
            cfg[k] = v

    if args.pronunciation:
        cfg["pronunciation"] = args.pronunciation

    cfg.setdefault("non_interactive", True)
    if cfg.get("out"):
        os.makedirs(os.path.dirname(os.path.expanduser(cfg["out"])) or ".", exist_ok=True)

    raise SystemExit(subprocess.call(build_cmd(cfg)))


def add_common(p):
    p.add_argument("--text")
    p.add_argument("--text-file")
    p.add_argument("--model", default="speech-2.8-hd")
    p.add_argument("--voice", default="English_expressive_narrator")
    p.add_argument("--speed", type=float)
    p.add_argument("--volume", type=float)
    p.add_argument("--pitch", type=float)
    p.add_argument("--format", default="mp3")
    p.add_argument("--sample-rate", dest="sample_rate", type=int)
    p.add_argument("--bitrate", type=int)
    p.add_argument("--channels", type=int)
    p.add_argument("--language")
    p.add_argument("--subtitles", action="store_true")
    p.add_argument("--stream", action="store_true")
    p.add_argument("--pronunciation", action="append")
    p.add_argument("--out", default="~/Downloads/max-gen/tts/output.mp3")

    p.add_argument("--api-key")
    p.add_argument("--region")
    p.add_argument("--base-url")
    p.add_argument("--output")
    p.add_argument("--timeout", type=int)
    p.add_argument("--verbose", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--no-color", action="store_true")
    p.add_argument("--quiet", action="store_true")


def main():
    parser = argparse.ArgumentParser(description="max-tts with plan/run")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_plan = sub.add_parser("plan")
    add_common(p_plan)
    p_plan.add_argument("--interactive", action="store_true")
    p_plan.add_argument("--plan-file", default=f"~/Downloads/max-gen/plans/tts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

    p_run = sub.add_parser("run")
    add_common(p_run)
    p_run.add_argument("--plan-file")

    args = parser.parse_args()
    if args.cmd == "plan":
        plan(args)
    else:
        run(args)


if __name__ == "__main__":
    main()
