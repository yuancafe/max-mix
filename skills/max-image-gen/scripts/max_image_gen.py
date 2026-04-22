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


def parse_subject_ref(v: str):
    return v if v else ""


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


def build_generate_cmd(cfg):
    cmd = ["mmx", "image", "generate", "--prompt", cfg["prompt"]]
    if cfg.get("aspect_ratio"):
        cmd += ["--aspect-ratio", cfg["aspect_ratio"]]
    if cfg.get("n"):
        cmd += ["--n", str(cfg["n"])]
    if cfg.get("seed") is not None:
        cmd += ["--seed", str(cfg["seed"])]
    if cfg.get("width") is not None:
        cmd += ["--width", str(cfg["width"])]
    if cfg.get("height") is not None:
        cmd += ["--height", str(cfg["height"])]
    if cfg.get("prompt_optimizer"):
        cmd.append("--prompt-optimizer")
    if cfg.get("aigc_watermark"):
        cmd.append("--aigc-watermark")
    if cfg.get("subject_ref"):
        cmd += ["--subject-ref", cfg["subject_ref"]]
    if cfg.get("out_dir"):
        cmd += ["--out-dir", os.path.expanduser(cfg["out_dir"])]
    if cfg.get("out_prefix"):
        cmd += ["--out-prefix", cfg["out_prefix"]]

    add_global_flags(cmd, cfg)

    if cfg.get("quiet", True):
        cmd.append("--quiet")
    if cfg.get("non_interactive", True):
        cmd.append("--non-interactive")
    return cmd


def plan(args):
    cfg = {
        "mode": "image.generate",
        "prompt": args.prompt,
        "aspect_ratio": args.aspect_ratio,
        "n": args.n,
        "seed": args.seed,
        "width": args.width,
        "height": args.height,
        "prompt_optimizer": args.prompt_optimizer,
        "aigc_watermark": args.aigc_watermark,
        "subject_ref": parse_subject_ref(args.subject_ref),
        "out_dir": args.out_dir,
        "out_prefix": args.out_prefix,
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
        if not cfg["prompt"]:
            cfg["prompt"] = ask("Image prompt", "A cinematic scene")
        cfg["aspect_ratio"] = ask("Aspect ratio", cfg["aspect_ratio"])
        cfg["n"] = int(ask("Number of images", str(cfg["n"])))
        cfg["out_dir"] = ask("Output directory", cfg["out_dir"])
        cfg["out_prefix"] = ask("Filename prefix", cfg["out_prefix"])

    if not cfg["prompt"]:
        raise SystemExit("plan requires --prompt or --interactive")

    os.makedirs(os.path.expanduser(os.path.dirname(args.plan_file)), exist_ok=True)
    with open(os.path.expanduser(args.plan_file), "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

    cmd = build_generate_cmd(cfg)
    print("Plan saved:", os.path.expanduser(args.plan_file))
    print("Preview command:")
    print(" ".join(shlex.quote(x) for x in cmd))


def run(args):
    cfg = {}
    if args.plan_file:
        with open(os.path.expanduser(args.plan_file), "r", encoding="utf-8") as f:
            cfg = json.load(f)

    overrides = {
        "prompt": args.prompt,
        "aspect_ratio": args.aspect_ratio,
        "n": args.n,
        "seed": args.seed,
        "width": args.width,
        "height": args.height,
        "prompt_optimizer": args.prompt_optimizer,
        "aigc_watermark": args.aigc_watermark,
        "subject_ref": args.subject_ref,
        "out_dir": args.out_dir,
        "out_prefix": args.out_prefix,
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

    cfg.setdefault("non_interactive", True)
    if not cfg.get("prompt"):
        raise SystemExit("run requires --prompt or --plan-file containing prompt")

    out_dir = os.path.expanduser(cfg.get("out_dir", "~/Downloads/max-gen/images"))
    os.makedirs(out_dir, exist_ok=True)

    cmd = build_generate_cmd(cfg)
    raise SystemExit(subprocess.call(cmd))


def add_common(p):
    p.add_argument("--prompt")
    p.add_argument("--aspect-ratio", default="1:1")
    p.add_argument("--n", type=int, default=1)
    p.add_argument("--seed", type=int)
    p.add_argument("--width", type=int)
    p.add_argument("--height", type=int)
    p.add_argument("--prompt-optimizer", action="store_true")
    p.add_argument("--aigc-watermark", action="store_true")
    p.add_argument("--subject-ref")
    p.add_argument("--out-dir", default="~/Downloads/max-gen/images")
    p.add_argument("--out-prefix", default="max_image")

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
    parser = argparse.ArgumentParser(description="max-image-gen with plan/run")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_plan = sub.add_parser("plan", help="Collect params and save plan JSON")
    add_common(p_plan)
    default_plan = f"~/Downloads/max-gen/plans/image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    p_plan.add_argument("--plan-file", default=default_plan)
    p_plan.add_argument("--interactive", action="store_true")

    p_run = sub.add_parser("run", help="Run generation from plan JSON and/or overrides")
    add_common(p_run)
    p_run.add_argument("--plan-file")

    args = parser.parse_args()
    if args.cmd == "plan":
        plan(args)
    else:
        run(args)


if __name__ == "__main__":
    main()
