# ASCII Time Blocker

A zero-dependency Python script for Cal Newport's time-block planning in plain
text. It renders proportional 15-minute ASCII blocks and branches into a new
column to the right whenever you cross off blocks and replan.

## Input Format

Create a text file (e.g., `2026-10-15.txt`):

```text
start 08:00
60 Deep: revise methods
15 Break
x 30 Admin: ethics
x 45 Deep: eval review
45 Admin: ethics
30 Shallow: email triage
```

- `start HH:MM`: Sets the start time of the schedule. If multiple `start` lines
  exist, only the last one is parsed.
- `<mins> <label>`: A scheduled block (snaps to 15-minute slots).
- `x <mins> <label>`: Marks a block as crossed out. Consecutive `x` blocks stay
  in the current column; the next active block starts a new column at the time
  the first `x` block began.
- Any other lines (headers, notes, or previous ASCII outputs) are ignored.

## Usage

Render to terminal:

```bash
python blocks.py < 2026-10-15.txt
```

Append the rendered schedule directly into your active file in Vim:

```vim
:r !python blocks.py < %
```

## Example Output

```text
08:00 +------------------------+
      |                        |
      |                        |
      |                        |
      |  Deep: revise methods  |
      |                        |
      |                        |
      |                        |
09:00 +------------------------+
      |         Break          |
09:15 +------------------------+ +------------------------+
      |////////////////////////| |                        |
      |//// Admin: ethics /////| |                        |
      |////////////////////////| |     Admin: ethics      |
09:45 +------------------------+ |                        |
      |////////////////////////| |                        |
      |////////////////////////| +------------------------+
      |// Deep: eval review ///| |                        |
      |////////////////////////| | Shallow: email triage  |
      |////////////////////////| |                        |
10:30 +------------------------+ +------------------------+
```

## Tips

- **Prefix categories** (`Deep:`, `Shallow:`, `Admin:`, `Meeting:`) to easily
  `grep` your plain-text files for weekly reviews.
- **Daily template:** Keep a `template.txt` with fixed blocks (lunch, shutdown
  ritual) and copy it each morning: `cp template.txt $(date +%F).txt`.