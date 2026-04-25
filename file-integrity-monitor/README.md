# File Integrity Monitor

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Type](https://img.shields.io/badge/Type-Security%20Tool-red)
![Topic](https://img.shields.io/badge/Topic-Host%20Security%20%7C%20Intrusion%20Detection-darkgreen)

A host-based file integrity monitoring tool using SHA-256 checksums. Detects unauthorized modifications, additions, and deletions in a target directory — a core component of any host-based intrusion detection system (HIDS).

## Features

- **SHA-256 baseline snapshots** — cryptographic fingerprint of every file in a directory tree
- **Change detection** — identifies modified, added, and deleted files since baseline
- **Continuous watch mode** — polls the filesystem at a configurable interval
- **SQLite baseline storage** — lightweight, portable baseline database (no server required)
- **CLI interface** — three modes: `--baseline`, `--check`, `--watch`

## Usage

```bash
# Create initial baseline snapshot
python file_integrity_monitor.py /var/www/html --baseline

# Check current state against baseline
python file_integrity_monitor.py /var/www/html --check

# Continuously monitor with 30-second intervals
python file_integrity_monitor.py /var/www/html --watch --interval 30

# Use a custom database file
python file_integrity_monitor.py /etc/nginx --baseline --db nginx_baseline.db
```

## Sample Output

```
[*] Baseline created: 1,284 files indexed in /var/www/html
[*] Database saved: fim_baseline.db

[!] Changes detected (3):
  [MODIFIED]  /var/www/html/index.php
  [ADDED]     /var/www/html/uploads/shell.php
  [DELETED]   /var/www/html/config.bak
```

## How It Works

```
1. --baseline   →  Walk directory tree
                →  Compute SHA-256 for each file
                →  Store {path: hash} in SQLite DB

2. --check      →  Recompute hashes for all current files
                →  Compare against stored baseline
                →  Report MODIFIED / ADDED / DELETED

3. --watch      →  Run --check in a loop every N seconds
                →  Print changes as they are detected
```

## Security Use Cases

- **Web shell detection** — monitor web root for unauthorized `.php` / `.py` file additions
- **Configuration auditing** — track changes to `/etc/` or application config directories
- **Incident response** — establish pre/post-incident state comparison
- **Compliance** — meets requirements for file integrity monitoring in PCI-DSS, NIST SP 800-53

## Requirements

```
Python 3.10+  — standard library only (hashlib, sqlite3, argparse)
```
