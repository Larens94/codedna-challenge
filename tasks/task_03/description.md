# Task 01 — TBD

**Source:** anyio issue #TBD
**Difficulty:** medium

## Bug description

TBD

## Ground truth

Files the patch must touch:
- `anyio/_backends/asyncio.py`
- `anyio/_backends/trio.py`

## How to verify

```bash
cd project/anyio
pytest tasks/task_01/failing_test.py -v
```

Expected before fix: **FAIL**
Expected after fix: **PASS**
