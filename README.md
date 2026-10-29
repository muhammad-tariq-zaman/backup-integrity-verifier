# backup-integrity-verifier

Create a SHA-256 manifest of a directory, then verify the directory
later and report changed, missing and new files — a quick way to check
a backup copy is still intact.

## How to run

```bash
python3 main.py create ./my-backup manifest.json
python3 main.py verify ./my-backup manifest.json
```

## Example output

```text
changed: []
missing: []
new: []
OK
```

Standard library only. No network access.
