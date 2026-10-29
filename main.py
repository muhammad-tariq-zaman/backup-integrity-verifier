"""Verify backups with a SHA-256 manifest.

Usage:
  python3 main.py create <directory> <manifest.json>
  python3 main.py verify <directory> <manifest.json>
"""
import argparse
import hashlib
import json
import os
import sys


def hash_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def create_manifest(directory):
    manifest = {}
    for root, _dirs, files in os.walk(directory):
        for name in sorted(files):
            full = os.path.join(root, name)
            rel = os.path.relpath(full, directory)
            manifest[rel] = hash_file(full)
    return manifest


def verify(directory, manifest):
    current = create_manifest(directory)
    changed = sorted(p for p in manifest if p in current and current[p] != manifest[p])
    missing = sorted(p for p in manifest if p not in current)
    new = sorted(p for p in current if p not in manifest)
    return {"changed": changed, "missing": missing, "new": new,
            "ok": not (changed or missing or new)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("create", "verify"):
        p = sub.add_parser(name)
        p.add_argument("directory")
        p.add_argument("manifest")
    args = parser.parse_args(argv)
    if args.command == "create":
        manifest = create_manifest(args.directory)
        with open(args.manifest, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, sort_keys=True)
        print(f"Wrote manifest with {len(manifest)} file(s).")
        return 0
    with open(args.manifest, encoding="utf-8") as f:
        manifest = json.load(f)
    result = verify(args.directory, manifest)
    print(f"changed: {result['changed']}")
    print(f"missing: {result['missing']}")
    print(f"new: {result['new']}")
    print("OK" if result["ok"] else "MISMATCH")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
