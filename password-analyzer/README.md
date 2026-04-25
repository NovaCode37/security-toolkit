# Password Analyzer

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Type](https://img.shields.io/badge/Type-Security%20Tool-red)
![Topic](https://img.shields.io/badge/Topic-Cryptography%20%7C%20Password%20Security-darkgreen)

A command-line password strength analyzer with entropy-based scoring, crack time estimation, and charset analysis. Supports single password analysis and batch file processing.

## Features

- **Shannon entropy calculation** — measures true randomness in bits
- **Crack time estimation** — estimates brute-force time at 10 billion hashes/sec
- **Strength classification** — VERY WEAK / WEAK / MODERATE / GOOD / STRONG
- **Charset analysis** — detects uppercase, lowercase, digits, special characters
- **Issue detection** — flags common weaknesses (sequential chars, repeated patterns, dictionary words)
- **Score 0–100** — composite strength score
- **Batch mode** — analyze a full wordlist or leaked password dump from a file
- **Interactive mode** — real-time analysis without arguments

## Usage

```bash
# Analyze a single password
python password_analyzer.py -p "MyP@ssw0rd!"

# Batch analyze from file
python password_analyzer.py -f passwords.txt

# Interactive mode
python password_analyzer.py
```

## Sample Output

```
==================================================
  Password Analysis: My********
==================================================
  Length          : 11 characters
  Entropy         : 62 bits
  Score           : 78/100
  Strength        : 🟢 GOOD
  Crack Time (BF) : 4.7e+08 years
  Character Types : 4/4 (A-Z, a-z, 0-9, !@#)

  No known weaknesses detected.
==================================================

==================================================
  Password Analysis: pa********
==================================================
  Length          : 8 characters
  Entropy         : 18 bits
  Score           : 12/100
  Strength        : 🔴 VERY WEAK
  Crack Time (BF) : < 1 second

  Issues Found:
    [!] Password found in common wordlists
    [!] All lowercase — add uppercase letters
    [!] No special characters
==================================================
```

## Scoring Breakdown

| Component | Weight |
|---|---|
| Length | High |
| Character type diversity (4/4) | High |
| Shannon entropy | High |
| Common pattern penalties | Negative |

## Crack Time Reference

| Entropy | Crack Time (10B H/s) |
|---|---|
| < 28 bits | < 1 second |
| 36 bits | ~1 minute |
| 50 bits | ~13 days |
| 60 bits | ~36 years |
| 70+ bits | Centuries |

## Requirements

```
Python 3.10+  — standard library only (math, argparse, re)
```

## Use Cases

- Password policy enforcement tooling
- Security awareness training demos
- CTF password challenge analysis
- Auditing credential databases for weak entries
