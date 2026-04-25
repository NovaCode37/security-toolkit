# TCP Port Scanner

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Type](https://img.shields.io/badge/Type-Security%20Tool-red)
![Topic](https://img.shields.io/badge/Topic-Network%20Reconnaissance%20%7C%20Penetration%20Testing-darkgreen)

A multi-threaded TCP port scanner with service identification and banner grabbing. Built for network reconnaissance and authorized security assessments.

## Features

- **Multi-threaded scanning** — configurable thread count for fast parallel scans
- **Service identification** — recognizes 24 common services (SSH, HTTP, RDP, MySQL, MongoDB, etc.)
- **Banner grabbing** — attempts to retrieve service banners on open ports (`--banner`)
- **Flexible port input** — supports ranges (`1-1024`), comma lists (`22,80,443`), or single ports
- **Hostname resolution** — accepts both IP addresses and domain names
- **Clean summary table** — sorted results with port / service / banner columns

## Usage

```bash
# Scan default ports 1–1024
python port_scanner.py 192.168.1.1

# Scan specific ports
python port_scanner.py 10.0.0.5 -p 22,80,443,8080,3306

# Scan a range with banner grabbing
python port_scanner.py example.com -p 1-65535 --banner

# Tune performance
python port_scanner.py 192.168.1.1 -p 1-10000 --threads 200 --timeout 0.5
```

## Sample Output

```
============================================================
  TCP Port Scanner
  Target : 192.168.1.1 (192.168.1.1)
  Ports  : 1024 ports (1-1024)
  Threads: 100
  Started: 2025-11-14 19:45:02
============================================================
  [OPEN]    22/tcp  SSH
  [OPEN]    80/tcp  HTTP             HTTP/1.1 200 OK...
  [OPEN]   443/tcp  HTTPS
  [OPEN]  3306/tcp  MySQL
------------------------------------------------------------
  Scan completed in 3.87s — 4 open port(s) found

PORT       SERVICE         BANNER
--------------------------------------------------
22         SSH             -
80         HTTP            HTTP/1.1 200 OK Server: nginx/1.24
443        HTTPS           -
3306       MySQL           5.7.39-MySQL Community Server
```

## Known Services

SSH · FTP · Telnet · SMTP · DNS · HTTP · HTTPS · SMB · RDP · MySQL · PostgreSQL · Redis · MongoDB · VNC · and more

## Arguments

| Flag | Default | Description |
|---|---|---|
| `target` | — | IP address or hostname |
| `-p` / `--ports` | `1-1024` | Port(s) to scan |
| `-t` / `--threads` | `100` | Concurrent threads |
| `-T` / `--timeout` | `1.0s` | Per-port connection timeout |
| `--banner` | off | Enable banner grabbing |

## Requirements

```
Python 3.10+  — standard library only (socket, concurrent.futures)
```

## Ethical Use

Only scan systems you own or have **explicit written permission** to test. Unauthorized port scanning may violate local laws and terms of service.
