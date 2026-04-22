#!/usr/bin/env python3
import argparse
import json
import os
import shlex
import subprocess
import sys
from datetime import datetime


def ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    v = input(f"{prompt}{suffix}: ").strip()
    return v if v else default


def load_key(explicit_key=None):
    if explicit_key:
        return explicit_key
    if os.environ.get("MINIMAX_API_KEY"):
        return os.environ["MINIMAX_API_KEY"]
    cfg = os.path.expanduser("~/.mmx/config.json")
    if os.path.exists(cfg):
        with open(cfg, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k in ("apiKey", "api_key", "key"):
            if data.get(k):
                return data[k]
    raise SystemExit("MINIMAX_API_KEY not found in env or ~/.mmx/config.json")


def run_json(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        print(p.stderr or p.stdout, file=sys.stderr)
        raise SystemExit(p.returncode)
    print(p.stdout.strip())


def build_cmd(cfg, key):
    api_host = cfg.get("api_host") or os.environ.get("MINIMAX_API_HOST", "https://api.minimaxi.com")
    action = cfg.get("action", "upload")
    if action == "upload":
        return [
            "curl", "-sS", "-X", "POST", f"{api_host}/v1/files/upload",
            "-H", f"Authorization: Bearer {key}",
            "-F", "purpose=voice_clone",
            "-F", f"file=@{cfg['file']}",
        ]

    payload = {
        "file_id": int(cfg["file_id"]),
        "voice_id": cfg["voice_id"],
        "text": cfg["text"],
        "model": cfg["model"],
    }
    if cfg.get("prompt_audio") and cfg.get("prompt_text"):
        payload["clone_prompt"] = {
            "prompt_audio": int(cfg["prompt_audio"]),
            "prompt_text": cfg["prompt_text"],
        }
    return [
        "curl", "-sS", "-X", "POST", f"{api_host}/v1/voice_clone",
        "-H", f"Authorization: Bearer {key}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload, ensure_ascii=False),
    ]


def plan(args):
    cfg = {
        "mode": "voice_clone",
        "action": args.action,
        "file": args.file,
        "file_id": args.file_id,
        "voice_id": args.voice_id,
        "text": args.text,
        "model": args.model,
        "prompt_audio": args.prompt_audio,
        "prompt_text": args.prompt_text,
        "api_host": args.api_host,
        "api_key": args.api_key,
    }

    if args.interactive:
        cfg["action"] = ask("Action(upload/clone)", cfg["action"])
        if cfg["action"] == "upload":
            cfg["file"] = ask("Audio file path", cfg.get("file", ""))
        else:
            cfg["file_id"] = ask("Uploaded file_id", cfg.get("file_id", ""))
            cfg["voice_id"] = ask("Voice ID", cfg.get("voice_id", "MyVoice001"))
            cfg["text"] = ask("Preview text", cfg.get("text", "你好，这是试听"))

    if cfg["action"] == "upload" and not cfg.get("file"):
        raise SystemExit("upload requires --file")
    if cfg["action"] == "clone" and (not cfg.get("file_id") or not cfg.get("voice_id")):
        raise SystemExit("clone requires --file-id and --voice-id")

    os.makedirs(os.path.expanduser(os.path.dirname(args.plan_file)), exist_ok=True)
    with open(os.path.expanduser(args.plan_file), "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

    key = load_key(cfg.get("api_key"))
    cmd = build_cmd(cfg, key)
    print("Plan saved:", os.path.expanduser(args.plan_file))
    print("Preview command:")
    print(" ".join(shlex.quote(x) for x in cmd))


def run(args):
    cfg = {}
    if args.plan_file:
        with open(os.path.expanduser(args.plan_file), "r", encoding="utf-8") as f:
            cfg = json.load(f)

    for k in ["action", "file", "file_id", "voice_id", "text", "model", "prompt_audio", "prompt_text", "api_host", "api_key"]:
        v = getattr(args, k)
        if v not in (None, ""):
            cfg[k] = v

    key = load_key(cfg.get("api_key"))
    cmd = build_cmd(cfg, key)
    run_json(cmd)


def add_common(p):
    p.add_argument("--action", choices=["upload", "clone"], default="upload")
    p.add_argument("--file")
    p.add_argument("--file-id")
    p.add_argument("--voice-id")
    p.add_argument("--text", default="你好，这是音色复刻试听。")
    p.add_argument("--model", default="speech-2.8-hd")
    p.add_argument("--prompt-audio")
    p.add_argument("--prompt-text")
    p.add_argument("--api-host")
    p.add_argument("--api-key")


def main():
    parser = argparse.ArgumentParser(description="max-voice-clone with plan/run")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_plan = sub.add_parser("plan")
    add_common(p_plan)
    p_plan.add_argument("--interactive", action="store_true")
    p_plan.add_argument("--plan-file", default=f"~/Downloads/max-gen/plans/voiceclone_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

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
