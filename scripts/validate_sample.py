#!/usr/bin/env python3
"""Validate FICTIONAL normalized management input; no Azure access or dependencies."""
import json
import sys
from pathlib import Path

REQUIRED = {"MonthlyIncidentTrend", "IncidentDrivers"}


def validate(document):
    investigations = document.get("investigations", [])
    chart_evidence = document.get("chart_evidence", [])
    if not isinstance(investigations, list) or not 1 <= len(investigations) <= 10:
        raise ValueError("Expected 1 to 10 investigation records")
    if not isinstance(chart_evidence, list):
        raise ValueError("Expected chart_evidence array")
    seen = {}
    for item in investigations:
        alias = item.get("workspace_alias")
        if not alias or not item.get("customer_name") or not str(item.get("investigation", "")).strip():
            raise ValueError("Missing workspace identity or investigation narrative")
        if alias in seen:
            raise ValueError(f"Duplicate investigation workspace: {alias}")
        seen[alias] = set()
    for item in chart_evidence:
        alias, tool = item.get("workspace_alias"), item.get("tool")
        if alias not in seen:
            raise ValueError(f"Unknown chart workspace: {alias}")
        if tool not in REQUIRED or tool in seen[alias]:
            raise ValueError(f"Unexpected or duplicate tool for {alias}: {tool}")
        if item.get("status") != "Success":
            raise ValueError(f"Failed mandatory tool for {alias}: {tool}")
        if not isinstance(item.get("rows"), list):
            raise ValueError(f"Tool rows missing for {alias}: {tool}")
        seen[alias].add(tool)
    for alias, tools in seen.items():
        if tools != REQUIRED:
            raise ValueError(f"Missing mandatory evidence for {alias}: {REQUIRED - tools}")
    return {"customers": len(investigations), "mandatory_records": len(chart_evidence)}


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "examples" / "management-evidence.example.json"
    try:
        result = validate(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"VALIDATION FAILED: {exc}", file=sys.stderr)
        sys.exit(1)
    print(f"VALIDATED synthetic sample: {result['customers']} customers, {result['mandatory_records']} mandatory tool records")
