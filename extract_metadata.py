#!/usr/bin/env python3
"""
extract_metadata.py
Extracts metadata flags for UECF binary criteria from source metadata JSON or PDF text.
Outputs a CSV with columns matching CRITERIA in scoring_pipeline.py.
"""

import argparse
import csv
import json
import re
from pathlib import Path

# Simple keyword patterns for detection (expand as needed)
PATTERNS = {
    "peer_reviewed": ["journal", "peer reviewed", "conference proceedings"],
    "replicated_2plus": ["replicated", "independent replication", "confirmatory"],
    "direct_physical": ["artefact", "specimen", "sample", "measurement", "excavation"],
    "confidence_95plus": [r"95% confidence", r"p\s*<\s*0\.05"],
    "data_public": ["doi.org", "supplementary data", "repository"],
    "specific_dates": [r"\b\d{4}\b", r"\bBCE\b", r"\bCE\b"],
    "test_method": ["method", "protocol", "procedure"],
    "counterfactuals": ["unless", "if not", "would fail"],
    "multi_disprovables": ["date and location", "two independent variables"],
    "indep_testable": ["accessible", "publicly available", "replicable"],
    "distinct_auth": [],  # Handled via metadata fields
    "no_shared_funding": [],  # Handled via metadata fields
    "no_top3_overlap": [],  # Handled via citation graph
    "two_cats_plus2": [],  # Requires category mapping
    "indep_lit_plus2": []  # Requires citation analysis
}

def extract_flags_from_text(text):
    flags = {key: 0 for key in PATTERNS}
    for key, patterns in PATTERNS.items():
        for pat in patterns:
            if re.search(pat, text, re.IGNORECASE):
                flags[key] = 1
                break
    return flags

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to text or JSON metadata")
    parser.add_argument("--output", required=True, help="Path to output CSV")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    records = []

    if input_path.suffix.lower() == ".json":
        with open(input_path, "r") as f:
            data = json.load(f)
        for rec in data:
            flags = extract_flags_from_text(rec.get("text", ""))
            flags["distinct_auth"] = int(rec.get("distinct_auth", 0))
            flags["no_shared_funding"] = int(rec.get("no_shared_funding", 0))
            flags["no_top3_overlap"] = int(rec.get("no_top3_overlap", 0))
            records.append({"stream": rec.get("stream", "Unknown"), **flags})
    else:
        # Treat as raw text file
        with open(input_path, "r") as f:
            text = f.read()
        flags = extract_flags_from_text(text)
        records.append({"stream": input_path.stem, **flags})

    fieldnames = ["stream"] + list(PATTERNS.keys())
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in records:
            writer.writerow(row)

    print(f"[extract_metadata] Wrote {len(records)} records to {output_path}")

if __name__ == "__main__":
    main()
