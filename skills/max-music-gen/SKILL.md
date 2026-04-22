---
name: max-music-gen
description: Use when user wants MiniMax music generation with full mmx music parameters, through one-skill plan then run workflow.
---

# max-music-gen

Two-stage workflow in one skill:

1. `plan` - configure music mode and all parameters, save JSON.
2. `run` - execute from plan.

## Commands

```bash
python3 scripts/max_music_gen.py plan --interactive
python3 scripts/max_music_gen.py run --plan-file <plan.json>
```

Supports major `mmx music generate` parameters including lyrics / lyrics-file / lyrics-optimizer / instrumental modes and detailed controls: vocals, genre, mood, instruments, tempo, bpm, key, avoid, use-case, structure, references, extra, output-format, watermark, sample-rate, bitrate, stream, output path.
