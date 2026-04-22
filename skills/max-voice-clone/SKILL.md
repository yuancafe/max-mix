---
name: max-voice-clone
description: Use when user wants MiniMax voice cloning (upload + clone) with two-stage plan then run workflow in one skill.
---

# max-voice-clone

Two-stage workflow in one skill:

1. `plan` - prepare upload/clone parameters, save JSON.
2. `run` - call MiniMax voice clone APIs from the plan.

## Commands

```bash
python3 scripts/max_voice_clone.py plan --interactive
python3 scripts/max_voice_clone.py run --plan-file <plan.json>
```

Actions:
- `upload`: upload source audio to obtain `file_id`
- `clone`: create/preview cloned voice with `voice_id` and text
