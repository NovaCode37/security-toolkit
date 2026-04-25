#!/usr/bin/env python3

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime

DEFAULT_DB = "fim_baseline.json"

def hash_file(filepath: str, algorithm: str = "sha256") -> str | None:
    h = hashlib.new(algorithm)
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except (PermissionError, OSError):
        return None

def scan_directory(directory: str, extensions: list[str] | None = None) -> dict:
    file_hashes = {}
    for root, _dirs, files in os.walk(directory):
        for filename in files:
            if extensions:
                if not any(filename.endswith(ext) for ext in extensions):
                    continue
            filepath = os.path.join(root, filename)
            file_hash = hash_file(filepath)
            if file_hash is not None:
                try:
                    stat = os.stat(filepath)
                except (PermissionError, OSError):
                    continue
                file_hashes[filepath] = {
                    "hash": file_hash,
                    "size": stat.st_size,
                    "modified": stat.st_mtime,
                }
    return file_hashes

def save_baseline(data: dict, db_path: str):
    payload = {
        "timestamp": datetime.now().isoformat(),
        "file_count": len(data),
        "files": data,
    }
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

def load_baseline(db_path: str) -> dict:
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Baseline not found: {db_path}")
    with open(db_path, "r", encoding="utf-8") as f:
        return json.load(f)

def compare(baseline: dict, current: dict) -> dict:
    baseline_files = set(baseline.keys())
    current_files = set(current.keys())

    created = current_files - baseline_files
    deleted = baseline_files - current_files
    common = baseline_files & current_files

    modified = set()
    for filepath in common:
        if baseline[filepath]["hash"] != current[filepath]["hash"]:
            modified.add(filepath)

    return {
        "created": sorted(created),
        "deleted": sorted(deleted),
        "modified": sorted(modified),
        "unchanged": len(common) - len(modified),
    }

def print_changes(changes: dict) -> None:
    total = len(changes["created"]) + len(changes["deleted"]) + len(changes["modified"])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if total == 0:
        print(f"  [{timestamp}] No changes detected. ({changes['unchanged']} files OK)")
        return

    print(f"\n{'=' * 60}")
    print(f"  INTEGRITY CHECK — {timestamp}")
    print(f"  {total} change(s) detected!")
    print(f"{'=' * 60}")

    if changes["created"]:
        print(f"\n  [+] NEW FILES ({len(changes['created'])})")
        for f in changes["created"]:
            print(f"      + {f}")

    if changes["modified"]:
        print(f"\n  [~] MODIFIED FILES ({len(changes['modified'])})")
        for f in changes["modified"]:
            print(f"      ~ {f}")

    if changes["deleted"]:
        print(f"\n  [-] DELETED FILES ({len(changes['deleted'])})")
        for f in changes["deleted"]:
            print(f"      - {f}")

    print(f"\n  Unchanged: {changes['unchanged']}")
    print(f"{'=' * 60}\n")

def cmd_baseline(args) -> None:
    print(f"[*] Scanning directory: {args.directory}")
    files = scan_directory(args.directory)
    save_baseline(files, args.db)
    print(f"[+] Baseline created: {len(files)} files hashed")
    print(f"    Saved to: {args.db}")

def cmd_check(args) -> None:
    try:
        baseline = load_baseline(args.db)
    except FileNotFoundError as e:
        print(f"[!] {e}")
        print("    Run with --baseline first to create one.")
        sys.exit(1)
    print(f"[*] Baseline from: {baseline['timestamp']} ({baseline['file_count']} files)")
    print(f"[*] Scanning directory: {args.directory}")
    current = scan_directory(args.directory)
    print(f"[*] Current scan: {len(current)} files")
    changes = compare(baseline["files"], current)
    print_changes(changes)

def cmd_watch(args) -> None:
    print(f"[*] Creating initial baseline for: {args.directory}")
    baseline_files = scan_directory(args.directory)
    print(f"[+] Monitoring {len(baseline_files)} files (interval: {args.interval}s)")
    print(f"    Press Ctrl+C to stop.\n")

    try:
        while True:
            time.sleep(args.interval)
            current = scan_directory(args.directory)
            changes = compare(baseline_files, current)
            print_changes(changes)
            baseline_files = current
    except KeyboardInterrupt:
        print("\n[*] Monitoring stopped.")

def main() -> None:
    parser = argparse.ArgumentParser(
        description="File Integrity Monitor — detect file system changes with SHA-256"
    )
    parser.add_argument("directory", help="Directory to monitor")
    parser.add_argument("--db", default=DEFAULT_DB,
                        help=f"Baseline database file (default: {DEFAULT_DB})")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--baseline", action="store_true",
                       help="Create a new baseline snapshot")
    group.add_argument("--check", action="store_true",
                       help="Check current state against baseline")
    group.add_argument("--watch", action="store_true",
                       help="Continuously monitor for changes")

    parser.add_argument("-i", "--interval", type=int, default=10,
                        help="Watch interval in seconds (default: 10)")
    args = parser.parse_args()

    args.directory = os.path.abspath(args.directory)
    if not os.path.isdir(args.directory):
        print(f"[!] Not a directory: {args.directory}")
        sys.exit(1)

    if args.baseline:
        cmd_baseline(args)
    elif args.check:
        cmd_check(args)
    elif args.watch:
        cmd_watch(args)

if __name__ == "__main__":
    main()
