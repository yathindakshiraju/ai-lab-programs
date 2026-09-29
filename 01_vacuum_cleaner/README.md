# Vacuum Cleaner Agent

## Algorithm
Simple **reflex agent** in the classic two-room vacuum world (rooms A and B).

Condition–action rules:
1. If current room is Dirty → **Suck**
2. Else if in room A → **Move Right**
3. Else if in room B → **Move Left**

Performance: `+10` per dirt cleaned, `-1` per action.

## How to run
```powershell
python 01_vacuum_cleaner/vacuum_cleaner_agent.py
```

Optional interactive dirt setup:
```powershell
python 01_vacuum_cleaner/vacuum_cleaner_agent.py --interactive
```

## What to screenshot
- Header `=== Vacuum Cleaner Agent Demo ===`
- Environment ASCII grid each step (rooms A/B, AGENT marker, Clean/Dirty)
- Percept + Action lines
- Final performance score and action history
