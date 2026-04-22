---
name: max-tts
description: Use when user wants MiniMax text-to-speech with full mmx speech parameters, using plan then run in one skill.
---

# max-tts

Two-stage workflow in one skill:

1. `plan` - gather voice/model/audio parameters and save JSON.
2. `run` - synthesize audio from the plan.

## Commands

```bash
python3 scripts/max_tts.py plan --interactive
python3 scripts/max_tts.py run --plan-file <plan.json>
```

Supports major `mmx speech synthesize` parameters: text/text-file, voice, model, speed, volume, pitch, format, sample-rate, bitrate, channels, language, subtitles, pronunciations, stream, and output path.
