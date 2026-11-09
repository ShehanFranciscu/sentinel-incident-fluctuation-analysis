#!/usr/bin/env python3
"""Conservative offline check of sanitized public sample files; stdlib only.

Run before publication and in CI. This is intentionally not a complete
PII detector and cannot determine whether a non-obvious identifier is confidential.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_TYPES = {".md", ".txt", ".json", ".py", ".js", ".yml", ".yaml", ".dot", ".svg", ".gitignore"}
EXCLUDED_DIRS = {".git", "__pycache__", ".venv", "venv", ".pytest_cache"}
FORBIDDEN_SUFFIXES = {".pdf", ".csv", ".xlsx", ".xls", ".docx", ".pptx", ".pfx", ".p12", ".pem", ".key", ".zip"}
FORBIDDEN_FILENAMES = {".env", "secrets.json", "local.settings.json", "id_rsa", "id_ed25519"}
FORBIDDEN_DIRS = {"private", "run-history", "reports", "production-export", "customers"}
SYNTHETIC_UUIDS = {
    "00000000-0000-0000-0000-000000000001",
    "00000000-0000-0000-0000-000000000002",
}
PATTERNS = {
    "email address": re.compile(r"(?i)\b[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}\b"),
    "IPv4 address": re.compile(r"\b(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}\b"),
    "private key": re.compile(r"-----BEGIN (?:[A-Z ]+)?PRIVATE KEY-----"),
    "bearer token": re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/-]{20,}"),
    "GitHub token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    "JWT token": re.compile(r"\beyJ[A-Za-z0-9_-]{15,}\.eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{10,}\b"),
}
UUID_RE = re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b")

def scan():
    findings = []
    count = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in EXCLUDED_DIRS for part in path.relative_to(ROOT).parts):
            continue
        count += 1
        rel = path.relative_to(ROOT)
        if path.suffix.lower() in FORBIDDEN_SUFFIXES or path.name in FORBIDDEN_FILENAMES:
            findings.append(f"{rel}: sensitive or disallowed file type/name")
        if any(p in FORBIDDEN_DIRS for p in rel.parts):
            findings.append(f"{rel}: disallowed directory")
        if path.suffix.lower() not in TEXT_TYPES and path.name != ".gitignore":
            continue
        try:
            data = path.read_text(encoding="utf-8")
        except UnicodeError:
            findings.append(f"{rel}: non-UTF8 text content")
            continue
        for label, regex in PATTERNS.items():
            for match in regex.finditer(data):
                findings.append(f"{rel}: possible {label} at line {data.count(chr(10), 0, match.start()) + 1}")
        for match in UUID_RE.finditer(data):
            if match.group(0).lower() not in SYNTHETIC_UUIDS:
                findings.append(f"{rel}: non-demo UUID at line {data.count(chr(10), 0, match.start()) + 1}")
    return count, findings

if __name__ == "__main__":
    count, findings = scan()
    if findings:
        print(f"FAILED public release scan ({len(findings)} finding(s)):", file=sys.stderr)
        for issue in findings:
            print("  - " + issue, file=sys.stderr)
        sys.exit(1)
    print(f"PASS: scanned {count} files; no matches to configured suspicious patterns")
    print("Manual review remains required; automated scans cannot guarantee anonymity.")
