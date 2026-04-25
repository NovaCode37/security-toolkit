#!/usr/bin/env python3

import argparse
import math
import re
import string
import sys

COMMON_PASSWORDS = {
    "123456", "password", "12345678", "qwerty", "123456789", "12345",
    "1234", "111111", "1234567", "dragon", "123123", "baseball", "abc123",
    "football", "monkey", "letmein", "shadow", "master", "666666",
    "qwertyuiop", "123321", "mustang", "1234567890", "michael", "654321",
    "superman", "1qaz2wsx", "7777777", "121212", "000000", "qazwsx",
    "123qwe", "killer", "trustno1", "jordan", "jennifer", "zxcvbnm",
    "asdfgh", "hunter", "buster", "soccer", "harley", "batman", "andrew",
    "tigger", "sunshine", "iloveyou", "2000", "charlie", "robert",
    "thomas", "hockey", "ranger", "daniel", "starwars", "klaster",
    "112233", "george", "computer", "michelle", "jessica", "pepper",
    "1111", "zxcvbn", "555555", "11111111", "131313", "freedom", "777777",
    "pass", "maggie", "159753", "aaaaaa", "ginger", "princess", "joshua",
    "cheese", "amanda", "summer", "love", "ashley", "nicole", "chelsea",
    "biteme", "matthew", "access", "yankees", "987654321", "dallas",
    "austin", "thunder", "taylor", "matrix", "admin", "root", "password1",
    "welcome", "welcome1", "p@ssw0rd", "passw0rd",
}

KEYBOARD_SEQUENCES = [
    "qwertyuiop", "asdfghjkl", "zxcvbnm",
    "1234567890", "0987654321",
    "qwerty", "asdfgh", "zxcvbn",
    "qazwsx", "1qaz2wsx", "1q2w3e4r",
]

LEET_MAP = {"@": "a", "0": "o", "1": "l", "3": "e", "4": "a", "5": "s", "7": "t", "$": "s", "!": "i"}

def calculate_entropy(password: str) -> float:
    charset_size = 0
    if any(c in string.ascii_lowercase for c in password):
        charset_size += 26
    if any(c in string.ascii_uppercase for c in password):
        charset_size += 26
    if any(c in string.digits for c in password):
        charset_size += 10
    if any(c in string.punctuation for c in password):
        charset_size += 32

    if any(c not in string.ascii_letters + string.digits + string.punctuation for c in password):
        charset_size += 128

    if charset_size == 0:
        return 0.0

    entropy = len(password) * math.log2(charset_size)
    return round(entropy, 2)

def detect_patterns(password: str) -> list[str]:
    issues = []
    lower = password.lower()

    if lower in COMMON_PASSWORDS:
        issues.append("Found in common passwords list")

    deleet = lower
    for leet_char, orig_char in LEET_MAP.items():
        deleet = deleet.replace(leet_char, orig_char)
    if deleet != lower and deleet in COMMON_PASSWORDS:
        issues.append("Common password with leet-speak substitution")

    if re.search(r"(.)\1{2,}", password):
        issues.append("Contains repeated characters (3+)")

    for seq_len in range(4, len(password) + 1):
        for i in range(len(password) - seq_len + 1):
            substr = password[i:i + seq_len]
            if substr.isdigit():
                nums = [int(c) for c in substr]
                diffs = [nums[j + 1] - nums[j] for j in range(len(nums) - 1)]
                if len(set(diffs)) == 1 and diffs[0] in (-1, 1):
                    issues.append(f"Sequential numbers detected: {substr}")
                    break
        else:
            continue
        break

    for seq in KEYBOARD_SEQUENCES:
        if seq in lower:
            issues.append(f"Keyboard sequence detected: {seq}")
            break

    if password.isalpha():
        if password.islower():
            issues.append("All lowercase letters")
        elif password.isupper():
            issues.append("All uppercase letters")

    if password.isdigit():
        issues.append("Only numeric characters")

    if re.search(r"(19|20)\d{2}", password):
        issues.append("Contains year pattern (possible date)")

    return issues

def analyze_password(password: str) -> dict:
    if not password:
        return {
            "password": "",
            "length": 0,
            "entropy": 0.0,
            "charset": {
                "uppercase": False,
                "lowercase": False,
                "digits": False,
                "special": False,
                "types_count": 0,
            },
            "score": 0,
            "strength": "VERY WEAK",
            "crack_time": "instant",
            "issues": ["Password is empty"],
        }

    length = len(password)
    entropy = calculate_entropy(password)
    has_upper = bool(re.search(r"[A-Z]", password))
    has_lower = bool(re.search(r"[a-z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_special = bool(re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?`~]", password))
    char_types = sum([has_upper, has_lower, has_digit, has_special])
    issues = detect_patterns(password)

    score = 0
    score += min(length * 3, 30)
    score += min(int(entropy / 4), 30)
    score += char_types * 5
    score -= len(issues) * 15

    score = max(0, min(100, score))

    if score >= 80:
        strength = "STRONG"
    elif score >= 60:
        strength = "GOOD"
    elif score >= 40:
        strength = "MODERATE"
    elif score >= 20:
        strength = "WEAK"
    else:
        strength = "VERY WEAK"

    if entropy > 0:
        seconds = (2 ** entropy) / 10_000_000_000
        if seconds < 1:
            crack_time = "< 1 second"
        elif seconds < 60:
            crack_time = f"{seconds:.1f} seconds"
        elif seconds < 3600:
            crack_time = f"{seconds / 60:.1f} minutes"
        elif seconds < 86400:
            crack_time = f"{seconds / 3600:.1f} hours"
        elif seconds < 31536000:
            crack_time = f"{seconds / 86400:.1f} days"
        elif seconds < 31536000 * 1000:
            crack_time = f"{seconds / 31536000:.1f} years"
        else:
            crack_time = f"{seconds / 31536000:.2e} years"
    else:
        crack_time = "instant"

    return {
        "password": password,
        "length": length,
        "entropy": entropy,
        "charset": {
            "uppercase": has_upper,
            "lowercase": has_lower,
            "digits": has_digit,
            "special": has_special,
            "types_count": char_types,
        },
        "score": round(score),
        "strength": strength,
        "crack_time": crack_time,
        "issues": issues,
    }

def print_report(analysis: dict):
    pw_len = len(analysis["password"])
    if pw_len <= 2:
        masked = "*" * pw_len
    else:
        masked = analysis["password"][:2] + "*" * (pw_len - 2)

    strength_colors = {
        "VERY WEAK": "🔴", "WEAK": "🟠", "MODERATE": "🟡",
        "GOOD": "🟢", "STRONG": "🟢",
    }
    icon = strength_colors.get(analysis["strength"], "⚪")

    print(f"\n{'=' * 50}")
    print(f"  Password Analysis: {masked}")
    print(f"{'=' * 50}")
    print(f"  Length          : {analysis['length']} characters")
    print(f"  Entropy         : {analysis['entropy']} bits")
    print(f"  Score           : {analysis['score']}/100")
    print(f"  Strength        : {icon} {analysis['strength']}")
    print(f"  Crack Time (BF) : {analysis['crack_time']}")
    print(f"  Character Types : {analysis['charset']['types_count']}/4", end="")
    types = []
    if analysis["charset"]["uppercase"]:
        types.append("A-Z")
    if analysis["charset"]["lowercase"]:
        types.append("a-z")
    if analysis["charset"]["digits"]:
        types.append("0-9")
    if analysis["charset"]["special"]:
        types.append("!@#")
    print(f" ({', '.join(types)})")

    if analysis["issues"]:
        print(f"\n  Issues Found:")
        for issue in analysis["issues"]:
            print(f"    [!] {issue}")
    else:
        print(f"\n  No known weaknesses detected.")
    print(f"{'=' * 50}\n")

def main():
    parser = argparse.ArgumentParser(description="Password Strength Analyzer")
    parser.add_argument("-p", "--password", help="Password to analyze")
    parser.add_argument("-f", "--file", help="File with passwords (one per line)")
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                passwords = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"[!] File not found: {args.file}")
            sys.exit(1)
        for pw in passwords:
            result = analyze_password(pw)
            print_report(result)
    elif args.password:
        result = analyze_password(args.password)
        print_report(result)
    else:
        print("Password Strength Analyzer")
        print("-" * 30)
        while True:
            try:
                pw = input("Enter password (or 'quit'): ")
                if pw.lower() == "quit":
                    break
                result = analyze_password(pw)
                print_report(result)
            except (KeyboardInterrupt, EOFError):
                print("\nBye!")
                break

if __name__ == "__main__":
    main()
