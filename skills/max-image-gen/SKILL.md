---
name: max-image-gen
description: Use when user wants MiniMax image generation with full mmx image parameters, using two-stage workflow: plan first, then run.
---

# max-image-gen

Two-stage workflow in one skill:

1. `plan` - collect/confirm parameters, save JSON plan.
2. `run` - execute generation from the plan (with optional overrides).

## Commands

```bash
python3 scripts/max_image_gen.py plan --interactive
python3 scripts/max_image_gen.py run --plan-file <plan.json>
```

Supports major `mmx image generate` parameters: prompt, aspect ratio, n, seed, width, height, prompt optimizer, watermark, subject ref, output dir/prefix, and global flags.
