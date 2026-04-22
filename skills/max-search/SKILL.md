---
name: max-search
description: Direct-first MiniMax web search skill for coding-plan-search. Default usage is direct run; optional plan/run is available for reusable JSON workflows.
---

# max-search

Default: direct run (single-step).

```bash
python3 scripts/max_search.py --q "MiniMax latest updates"
```

Optional: plan/run.

```bash
python3 scripts/max_search.py plan --interactive
python3 scripts/max_search.py run --plan-file <plan.json>
```
