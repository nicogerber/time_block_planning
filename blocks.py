import re
import sys
from datetime import datetime, timedelta

if len(sys.argv) < 2:
    print("Usage: uv run blocks.py <2026-10-19.txt>")
    sys.exit(1)

default_width = 24

with open(sys.argv[1]) as f:
    raw = [l.strip() for l in f if l.strip()]
starts = [i for i, l in enumerate(raw) if l.startswith("start ")]
if not starts:
    sys.exit("no 'start HH:MM' line found")
lines = raw[starts[-1] :]
t0 = datetime.strptime(lines[0].split()[1], "%H:%M")

tasks = []
for l in lines[1:]:
    m = re.match(r"^(x\s+)?(\d+)\s+(.+)$", l)
    if m:
        slots = max(1, int(m.group(2)) // 15)
        tasks.append((bool(m.group(1)), slots, m.group(3)))

grid, ticks = {}, set()
col, slot, x_slot = 0, 0, None

for crossed, slots, label in tasks:
    if crossed:
        if x_slot is None:
            x_slot = slot
        s, x_slot = x_slot, x_slot + slots
    else:
        if x_slot is not None:
            col, x_slot = col + 1, None
        s, slot = slot, slot + slots

    y0, y1 = s * 2, (s + slots) * 2
    ticks.update([y0, y1])
    fill = "/" if crossed else " "
    grid[(y0, col)] = grid[(y1, col)] = f"+{'-' * default_width}+"
    for y in range(y0 + 1, y1):
        text = f" {label} " if y == (y0 + y1) // 2 else ""
        grid[(y, col)] = f"|{text:{fill}^{default_width}.{default_width}}|"

if grid:
    max_y = max(y for y, _ in grid)
    max_col = max(c for _, c in grid)
    blank = " " * (default_width + 2)
    print()
    for y in range(max_y + 1):
        t = t0 + timedelta(minutes=(y // 2) * 15)
        prefix = f"{t:%H:%M} " if y in ticks else "      "
        row = " ".join(grid.get((y, c), blank) for c in range(max_col + 1))
        print((prefix + row).rstrip())
    print()
