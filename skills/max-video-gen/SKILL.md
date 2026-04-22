---
name: max-video-gen
description: Use when user wants MiniMax video generation and task operations with full mmx video parameters, via built-in plan then run workflow.
---

# max-video-gen

Two-stage workflow in one skill:

1. `plan` - step-by-step parameter planning (`generate` / `status` / `download`), save JSON.
2. `run` - execute from planned JSON.

## Commands

```bash
python3 scripts/max_video_gen.py plan --interactive
python3 scripts/max_video_gen.py run --plan-file <plan.json>
```

Supports major `mmx video generate` parameters: model, prompt, first/last frame, subject image, callback URL, async, poll interval, download path, plus status/download actions.
