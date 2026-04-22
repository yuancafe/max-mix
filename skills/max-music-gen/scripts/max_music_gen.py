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
    cmd = ["mmx", "music", "generate", "--prompt", cfg["prompt"], "--model", cfg["model"]]

    mode_count = int(bool(cfg.get("lyrics") or cfg.get("lyrics_file"))) + int(bool(cfg.get("lyrics_optimizer"))) + int(bool(cfg.get("instrumental")))
    if mode_count != 1:
        raise SystemExit("Need exactly one mode: lyrics OR lyrics-optimizer OR instrumental")

    if cfg.get("lyrics"):
        cmd += ["--lyrics", cfg["lyrics"]]
    if cfg.get("lyrics_file"):
        cmd += ["--lyrics-file", cfg["lyrics_file"]]
    if cfg.get("lyrics_optimizer"):
        cmd += ["--lyrics-optimizer"]
    if cfg.get("instrumental"):
        cmd += ["--instrumental"]

    for k, flag in {
        "vocals": "--vocals",
        "genre": "--genre",
        "mood": "--mood",
        "instruments": "--instruments",
        "tempo": "--tempo",
        "bpm": "--bpm",
        "key": "--key",
        "avoid": "--avoid",
        "use_case": "--use-case",
        "structure": "--structure",
        "references": "--references",
        "extra": "--extra",
        "output_format": "--output-format",
        "format": "--format",
        "sample_rate": "--sample-rate",
        "bitrate": "--bitrate",
        "out": "--out",
    }.items():
        if cfg.get(k) not in (None, ""):
            v = os.path.expanduser(cfg[k]) if k == "out" else cfg[k]
            cmd += [flag, str(v)]

    if cfg.get("aigc_watermark"):
        cmd.append("--aigc-watermark")
    if cfg.get("stream"):
        cmd.append("--stream")

    add_global_flags(cmd, cfg)
    if cfg.get("quiet", True):
        cmd.append("--quiet")
    if cfg.get("non_interactive", True):
        cmd.append("--non-interactive")
    return cmd


def plan(args):
    cfg = {
        "mode": "music.generate",
        "prompt": args.prompt,
        "model": args.model,
        "lyrics": args.lyrics,
        "lyrics_file": args.lyrics_file,
        "lyrics_optimizer": args.lyrics_optimizer,
        "instrumental": args.instrumental,
        "vocals": args.vocals,
        "genre": args.genre,
        "mood": args.mood,
        "instruments": args.instruments,
        "tempo": args.tempo,
        "bpm": args.bpm,
        "key": args.key,
        "avoid": args.avoid,
        "use_case": args.use_case,
        "structure": args.structure,
        "references": args.references,
        "extra": args.extra,
        "output_format": args.output_format,
        "aigc_watermark": args.aigc_watermark,
        "format": args.format,
        "sample_rate": args.sample_rate,
        "bitrate": args.bitrate,
        "stream": args.stream,
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
        if not cfg["prompt"]:
            cfg["prompt"] = ask("Music prompt", "Lo-fi chill beat")
        mode = ask("Mode (lyrics/lyrics-optimizer/instrumental)", "instrumental")
        cfg["lyrics_optimizer"] = mode == "lyrics-optimizer"
        cfg["instrumental"] = mode == "instrumental"
        if mode == "lyrics":
            cfg["lyrics"] = ask("Lyrics text", "[Verse]\n...")
        cfg["out"] = ask("Output path", cfg["out"])

    if not cfg.get("prompt"):
        raise SystemExit("plan requires --prompt or --interactive")

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
        "prompt", "model", "lyrics", "lyrics_file", "lyrics_optimizer", "instrumental", "vocals", "genre", "mood",
        "instruments", "tempo", "bpm", "key", "avoid", "use_case", "structure", "references", "extra",
        "output_format", "aigc_watermark", "format", "sample_rate", "bitrate", "stream", "out",
        "api_key", "region", "base_url", "output", "timeout", "verbose", "dry_run", "no_color", "quiet"
    ]:
        v = getattr(args, k)
        if v not in (None, ""):
            cfg[k] = v

    cfg.setdefault("non_interactive", True)
    if cfg.get("out"):
        os.makedirs(os.path.dirname(os.path.expanduser(cfg["out"])) or ".", exist_ok=True)

    raise SystemExit(subprocess.call(build_cmd(cfg)))


def add_common(p):
    p.add_argument("--prompt")
    p.add_argument("--model", default="music-2.6-free")
    p.add_argument("--lyrics")
    p.add_argument("--lyrics-file")
    p.add_argument("--lyrics-optimizer", action="store_true")
    p.add_argument("--instrumental", action="store_true")
    p.add_argument("--vocals")
    p.add_argument("--genre")
    p.add_argument("--mood")
    p.add_argument("--instruments")
    p.add_argument("--tempo")
    p.add_argument("--bpm", type=int)
    p.add_argument("--key")
    p.add_argument("--avoid")
    p.add_argument("--use-case", dest="use_case")
    p.add_argument("--structure")
    p.add_argument("--references")
    p.add_argument("--extra")
    p.add_argument("--output-format", dest="output_format")
    p.add_argument("--aigc-watermark", action="store_true")
    p.add_argument("--format", default="mp3")
    p.add_argument("--sample-rate", dest="sample_rate", type=int)
    p.add_argument("--bitrate", type=int)
    p.add_argument("--stream", action="store_true")
    p.add_argument("--out", default="~/Downloads/max-gen/music/output.mp3")

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
    parser = argparse.ArgumentParser(description="max-music-gen with plan/run")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_plan = sub.add_parser("plan")
    add_common(p_plan)
    p_plan.add_argument("--interactive", action="store_true")
    p_plan.add_argument("--plan-file", default=f"~/Downloads/max-gen/plans/music_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

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
