#!/usr/bin/env python3

import argparse
import hashlib
import sys
import time

HASH_LENGTHS = {
    32: "md5",
    40: "sha1",
    64: "sha256",
    128: "sha512",
}

BUILTIN_WORDS = [
    "password", "123456", "12345678", "qwerty", "abc123", "monkey",
    "1234567", "letmein", "trustno1", "dragon", "baseball", "master",
    "michael", "football", "shadow", "jennifer", "111111", "2000",
    "jordan", "superman", "harley", "1234567890", "robert", "hunter",
    "admin", "root", "toor", "pass", "test", "guest", "welcome",
    "login", "password1", "iloveyou", "princess", "sunshine", "charlie",
    "donald", "secret", "access", "hello", "server", "computer",
]

def detect_hash_type(hash_str: str) -> str | None:
    return HASH_LENGTHS.get(len(hash_str))

def compute_hash(word: str, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    h.update(word.encode("utf-8"))
    return h.hexdigest()

def apply_rules(word: str) -> list[str]:
    mutations = [word]
    mutations.append(word.capitalize())
    mutations.append(word.upper())
    for suffix in ["1", "12", "123", "1234", "!", "!!", "01", "69", "007"]:
        mutations.append(word + suffix)
        mutations.append(word.capitalize() + suffix)
    for prefix in ["1", "123"]:
        mutations.append(prefix + word)
    leet = word.replace("a", "@").replace("e", "3").replace("i", "1")
    leet = leet.replace("o", "0").replace("s", "$").replace("t", "7")
    if leet != word:
        mutations.append(leet)
    mutations.append(word[::-1])
    return list(set(mutations))

def load_wordlist(path: str) -> list[str]:
    words = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            word = line.strip()
            if word:
                words.append(word)
    return words

def crack_hash(target_hash: str, algorithm: str, words: list[str],
               use_rules: bool = False) -> tuple[str | None, int]:
    target_hash = target_hash.lower().strip()
    attempts = 0

    for word in words:
        candidates = apply_rules(word) if use_rules else [word]
        for candidate in candidates:
            attempts += 1
            if compute_hash(candidate, algorithm) == target_hash:
                return candidate, attempts
    return None, attempts

def main():
    parser = argparse.ArgumentParser(
        description="Hash Cracker — dictionary attack with rule-based mutations"
    )
    parser.add_argument("hash", nargs="?", help="Hash to crack")
    parser.add_argument("-f", "--file", help="File with hashes (one per line)")
    parser.add_argument("-w", "--wordlist", help="Path to wordlist file")
    parser.add_argument("-a", "--algorithm",
                        choices=["md5", "sha1", "sha256", "sha512"],
                        help="Hash algorithm (auto-detected if not specified)")
    parser.add_argument("--rules", action="store_true",
                        help="Apply rule-based word mutations")
    args = parser.parse_args()

    if not args.hash and not args.file:
        parser.error("Provide a hash or --file with hashes")

    if args.wordlist:
        try:
            words = load_wordlist(args.wordlist)
        except FileNotFoundError:
            print(f"[!] Wordlist not found: {args.wordlist}")
            sys.exit(1)
        print(f"[*] Loaded wordlist: {len(words)} words from {args.wordlist}")
    else:
        words = BUILTIN_WORDS
        print(f"[*] Using built-in wordlist: {len(words)} words")

    if args.rules:
        print("[*] Rule-based mutations: ENABLED")

    hashes = []
    if args.file:
        try:
            with open(args.file, "r") as f:
                hashes = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"[!] File not found: {args.file}")
            sys.exit(1)
    else:
        hashes = [args.hash]

    print(f"[*] Hashes to crack: {len(hashes)}")
    print("=" * 55)

    cracked = 0
    total_start = time.time()

    for target in hashes:
        target = target.strip().lower()
        algo = args.algorithm or detect_hash_type(target)
        if not algo:
            print(f"  [?] Cannot detect algorithm for: {target[:20]}...")
            continue

        start = time.time()
        result, attempts = crack_hash(target, algo, words, args.rules)
        elapsed = time.time() - start
        speed = attempts / elapsed if elapsed > 0 else 0

        if result:
            cracked += 1
            print(f"  [+] CRACKED  {target[:16]}...  =>  {result}")
            print(f"      Algorithm: {algo.upper()} | {attempts:,} attempts | {elapsed:.2f}s | {speed:,.0f} H/s")
        else:
            print(f"  [-] FAILED   {target[:16]}...")
            print(f"      Algorithm: {algo.upper()} | {attempts:,} attempts | {elapsed:.2f}s")

    total_elapsed = time.time() - total_start
    print("=" * 55)
    print(f"  Results: {cracked}/{len(hashes)} cracked in {total_elapsed:.2f}s")

if __name__ == "__main__":
    main()
