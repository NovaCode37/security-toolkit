# Security Toolkit

A collection of Python-based security utilities: hash cracking, network scanning, password analysis and file integrity monitoring.

Each tool is self-contained in its own directory and can be run independently.

## Tools

| Tool | Description | Key Features |
|------|-------------|--------------|
| [`hash-cracker/`](hash-cracker/) | Crack MD5, SHA-1, SHA-256 hashes | Dictionary & brute-force attacks |
| [`tcp-port-scanner/`](tcp-port-scanner/) | Multi-threaded TCP port scanner | Service detection, configurable timeout |
| [`password-analyzer/`](password-analyzer/) | Password strength analyzer | Entropy calculation, pattern detection |
| [`file-integrity-monitor/`](file-integrity-monitor/) | File change monitoring | SHA-256 checksums, tampering alerts |

## Quick Start

```bash
# Clone the repository
git clone https://github.com/NovaCode37/security-toolkit.git
cd security-toolkit

# Run any tool
cd hash-cracker
python hash_cracker.py --help

cd ../tcp-port-scanner
python port_scanner.py --help

cd ../password-analyzer
python password_analyzer.py --help

cd ../file-integrity-monitor
python file_integrity_monitor.py --help
```

## Tech Stack

- **Language:** Python 3
- **Libraries:** hashlib, socket, threading, os
- **Concepts:** Cryptography, network protocols, file system monitoring, brute-force algorithms

## Disclaimer

These tools are intended for **educational purposes and authorized security testing only**. Unauthorized use against systems you do not own or have permission to test is illegal.

## Author

[NovaCode37](https://github.com/NovaCode37)
