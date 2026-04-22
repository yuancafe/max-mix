---
name: max-vision
description: Direct-first MiniMax image understanding skill for coding-plan-vlm. Default usage is direct run; optional plan/run is available for reusable JSON workflows.
---

# max-vision

Default: direct run (single-step).

```bash
python3 scripts/max_vision.py --image ./screenshot.png --prompt "Extract all text"
```

Optional: plan/run.

```bash
python3 scripts/max_vision.py plan --interactive
python3 scripts/max_vision.py run --plan-file <plan.json>
```
