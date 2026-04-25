# Hash Cracker

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Type](https://img.shields.io/badge/Type-Security%20Tool-red)
![Topic](https://img.shields.io/badge/Topic-Cryptography%20%7C%20Password%20Security-darkgreen)

A command-line dictionary and brute-force hash cracking tool supporting multiple hashing algorithms. Built for educational use and authorized security testing.

## Features

- **Multi-algorithm support** — MD5, SHA-1, SHA-256, SHA-512 and more
- **Dictionary attack** — wordlist-based cracking with configurable input
- **Brute-force mode** — exhaustive character-space search
- **Performance metrics** — real-time speed display (H/s), elapsed time, attempt count
- **Batch mode** — crack multiple hashes from a file in one run
- **Clear output** — per-hash result with algorithm identification and timing

## Usage

```bash
# Single hash, dictionary attack
python hash_cracker.py --hash 5f4dcc3b5aa765d61d8327deb882cf99 --wordlist rockyou.txt

# Multiple hashes from file
python hash_cracker.py --file hashes.txt --wordlist wordlist.txt

# Specify algorithm explicitly
python hash_cracker.py --hash <hash> --wordlist wordlist.txt --algo sha256
```

## Sample Output

```
=======================================================
  Hash Cracker
=======================================================
  [+] CRACKED  5f4dcc3b5aa7...  =>  password
      Algorithm: MD5 | 1,024 attempts | 0.03s | 34,133 H/s
  [-] FAILED   2cf24dba5fb0...
      Algorithm: SHA256 | 14,344,391 attempts | 8.21s
=======================================================
  Results: 1/2 cracked in 8.24s
```

## Supported Algorithms

| Algorithm | Hash Length |
|---|---|
| MD5 | 32 hex chars |
| SHA-1 | 40 hex chars |
| SHA-256 | 64 hex chars |
| SHA-512 | 128 hex chars |

## Requirements

```
Python 3.10+  — standard library only (hashlib, no external dependencies)
```

## Ethical Use

This tool is intended for:
- Recovering your own forgotten passwords
- CTF (Capture The Flag) competitions
- Authorized penetration testing
- Understanding why weak/unsalted hashes are insecure

**Do not use against systems or hashes you do not own or have explicit permission to test.**
