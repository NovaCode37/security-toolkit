#!/usr/bin/env python3

import argparse
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

COMMON_PORTS = {
    20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 111: "RPCbind", 135: "MSRPC",
    139: "NetBIOS", 143: "IMAP", 443: "HTTPS", 445: "SMB", 993: "IMAPS",
    995: "POP3S", 1723: "PPTP", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 5900: "VNC", 6379: "Redis", 8080: "HTTP-Proxy",
    8443: "HTTPS-Alt", 27017: "MongoDB",
}

def parse_ports(port_str: str) -> list[int]:
    ports = []
    for part in port_str.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            s, e = int(start), int(end)
            if s < 1 or e > 65535 or s > e:
                raise ValueError(f"Invalid port range: {part}")
            ports.extend(range(s, e + 1))
        else:
            p = int(part)
            if p < 1 or p > 65535:
                raise ValueError(f"Invalid port number: {p}")
            ports.append(p)
    if not ports:
        raise ValueError("No ports specified")
    return sorted(set(ports))

def grab_banner(sock: socket.socket, timeout: float) -> str:
    try:
        sock.settimeout(timeout)
        banner = sock.recv(1024).decode("utf-8", errors="replace").strip()
        if not banner:
            sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
            banner = sock.recv(1024).decode("utf-8", errors="replace").strip()
        return banner[:120]
    except Exception:
        return ""

def scan_port(target: str, port: int, timeout: float, do_banner: bool,) -> dict | None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        if result == 0:
            service = COMMON_PORTS.get(port, "unknown")
            banner = ""
            if do_banner:
                banner = grab_banner(sock, timeout)
            return {"port": port, "service": service, "banner": banner}
    except (socket.timeout, OSError):
        pass
    finally:
        sock.close()
    return None

def resolve_target(target: str) -> str:
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        raise ValueError(f"Cannot resolve hostname: {target}")

def main():
    parser = argparse.ArgumentParser(
        description="TCP Port Scanner — multi-threaded scanner with banner grabbing"
    )
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", default="1-1024",
                        help="Port range: 80 | 1-1024 | 22,80,443")
    parser.add_argument("-t", "--threads", type=int, default=100,
                        help="Number of threads (default: 100)")
    parser.add_argument("-T", "--timeout", type=float, default=1.0,
                        help="Connection timeout in seconds (default: 1.0)")
    parser.add_argument("--banner", action="store_true",
                        help="Attempt banner grabbing on open ports")
    args = parser.parse_args()

    try:
        target_ip = resolve_target(args.target)
    except ValueError as e:
        print(f"[!] {e}")
        sys.exit(1)

    try:
        ports = parse_ports(args.ports)
    except ValueError as e:
        print(f"[!] {e}")
        sys.exit(1)

    print("=" * 60)
    print("TCP Port Scanner")
    print(f"Target: {args.target} ({target_ip})")
    print(f"Ports: {len(ports)} ports ({args.ports})")
    print(f"Threads: {args.threads}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    start_time = time.time()
    open_ports = []

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {
            executor.submit(scan_port, target_ip, port, args.timeout, args.banner): port
            for port in ports
        }
        for future in as_completed(futures):
            result = future.result()
            if result:
                open_ports.append(result)
                banner_info = f" | {result['banner']}" if result["banner"] else ""
                print(f"[OPEN] {result['port']:>5}/tcp {result['service']:<15}{banner_info}")

    elapsed = time.time() - start_time
    open_ports.sort(key=lambda x: x["port"])

    print("-" * 60)
    print(f"Scan completed in {elapsed:.2f}s — {len(open_ports)} open port(s) found")
    print("=" * 60)

    if open_ports:
        print(f"\n{'PORT':<10}{'SERVICE':<15}{'BANNER'}")
        print("-" * 50)
        for p in open_ports:
            banner = p["banner"] if p["banner"] else "-"
            print(f"{p['port']:<10}{p['service']:<15}{banner}")

if __name__ == "__main__":
    main()
