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
    mapping = {
        "api_key": "--api-key",
        "region": "--region",
        "base_url": "--base-url",
        "output": "--output",
        "timeout": "--timeout",
    }
    for k, flag in mapping.items():
        if cfg.get(k):
            cmd += [flag, str(cfg[k])]
    if cfg.get("verbose"):
        cmd.append("--verbose")
    if cfg.get("dry_run"):
        cmd.append("--dry-run")
    if cfg.get("no_color"):
        cmd.append("--no-color")


def build_cmd(cfg):
    action = cfg.get("action", "generate")
    if action == "generate":
        cmd = ["mmx", "video", "generate", "--prompt", cfg["prompt"]]
        if cfg.get("model"):
            cmd += ["--model", cfg["model"]]
        if cfg.get("first_frame"):
            cmd += ["--first-frame", cfg["first_frame"]]
        if cfg.get("last_frame"):
            cmd += ["--last-frame", cfg["last_frame"]]
        if cfg.get("subject_image"):
            cmd += ["--subject-image", cfg["subject_image"]]
        if cfg.get("callback_url"):
            cmd += ["--callback-url", cfg["callback_url"]]
        if cfg.get("download"):
            cmd += ["--download", os.path.expanduser(cfg["download"])]
        if cfg.get("poll_interval"):
            cmd += ["--poll-interval", str(cfg["poll_interval"])]
        if cfg.get("async_mode"):
            cmd += ["--async"]
    elif action == "status":
        cmd = ["mmx", "video", "task", "get", "--task-id", cfg["task_id"], "--output", "json"]
    else:
        cmd = ["mmx", "video", "download", "--file-id", cfg["file_id"], "--out", os.path.expanduser(cfg["out"])]

    add_global_flags(cmd, cfg)
    if cfg.get("quiet", True):
        cmd.append("--quiet")
    if cfg.get("non_interactive", True):
        cmd.append("--non-interactive")
    return cmd


def plan(args):
    cfg = {
        "mode": "video",
        "action": args.action,
        "prompt": args.prompt,
        "model": args.model,
        "first_frame": args.first_frame,
        "last_frame": args.last_frame,
        "subject_image": args.subject_image,
        "callback_url": args.callback_url,
        "download": args.download,
        "poll_interval": args.poll_interval,
        "async_mode": args.async_mode,
        "task_id": args.task_id,
        "file_id": args.file_id,
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
        cfg["action"] = ask("Action(generate/status/download)", cfg["action"])
        if cfg["action"] == "generate":
            if not cfg["prompt"]:
                cfg["prompt"] = ask("Video prompt", "A cinematic ocean scene")
            cfg["model"] = ask("Model", cfg["model"])
            cfg["download"] = ask("Download path (optional)", cfg.get("download", ""))
            cfg["async_mode"] = ask("Async mode? (y/N)", "N").lower() == "y"
        elif cfg["action"] == "status":
            cfg["task_id"] = ask("Task ID", cfg.get("task_id", ""))
        else:
            cfg["file_id"] = ask("File ID", cfg.get("file_id", ""))
            cfg["out"] = ask("Output path", cfg.get("out", "~/Downloads/max-gen/videos/out.mp4"))

    if cfg["action"] == "generate" and not cfg.get("prompt"):
        raise SystemExit("generate action requires --prompt or --interactive")
    if cfg["action"] == "status" and not cfg.get("task_id"):
        raise SystemExit("status action requires --task-id")
    if cfg["action"] == "download" and (not cfg.get("file_id") or not cfg.get("out")):
        raise SystemExit("download action requires --file-id and --out")

    os.makedirs(os.path.expanduser(os.path.dirname(args.plan_file)), exist_ok=True)
    with open(os.path.expanduser(args.plan_file), "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

    cmd = build_cmd(cfg)
    print("Plan saved:", os.path.expanduser(args.plan_file))
    print("Preview command:")
    print(" ".join(shlex.quote(x) for x in cmd))


def run(args):
    cfg = {}
    if args.plan_file:
        with open(os.path.expanduser(args.plan_file), "r", encoding="utf-8") as f:
            cfg = json.load(f)

    overrides = {
        "action": args.action,
        "prompt": args.prompt,
        "model": args.model,
        "first_frame": args.first_frame,
        "last_frame": args.last_frame,
        "subject_image": args.subject_image,
        "callback_url": args.callback_url,
        "download": args.download,
        "poll_interval": args.poll_interval,
        "async_mode": args.async_mode,
        "task_id": args.task_id,
        "file_id": args.file_id,
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
    }
    for k, v in overrides.items():
        if v not in (None, ""):
            cfg[k] = v

    cfg.setdefault("action", "generate")
    cfg.setdefault("non_interactive", True)

    cmd = build_cmd(cfg)
    raise SystemExit(subprocess.call(cmd))


def add_common(p):
    p.add_argument("--action", choices=["generate", "status", "download"], default="generate")
    p.add_argument("--prompt")
    p.add_argument("--model", default="MiniMax-Hailuo-2.3")
    p.add_argument("--first-frame")
    p.add_argument("--last-frame")
    p.add_argument("--subject-image")
    p.add_argument("--callback-url")
    p.add_argument("--download")
    p.add_argument("--poll-interval", type=int)
    p.add_argument("--async", dest="async_mode", action="store_true")
    p.add_argument("--task-id")
    p.add_argument("--file-id")
    p.add_argument("--out", default="~/Downloads/max-gen/videos/out.mp4")

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
    parser = argparse.ArgumentParser(description="max-video-gen with plan/run")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_plan = sub.add_parser("plan")
    add_common(p_plan)
    default_plan = f"~/Downloads/max-gen/plans/video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    p_plan.add_argument("--plan-file", default=default_plan)
    p_plan.add_argument("--interactive", action="store_true")

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
