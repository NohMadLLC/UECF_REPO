#!/usr/bin/env python3
"""
parse_citations.py
Analyzes citation lists to determine overlap, funding, and independent literature threads.
Outputs a CSV with independence-related flags for scoring.
"""

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

def parse_citation_data(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
    return data

def compute_independence_flags(data):
    results = []
    author_groups = defaultdict(set)
    funder_groups = defaultdict(set)
    ref_groups = defaultdict(list)

    for rec in data:
        stream = rec["stream"]
        authors = set(rec.get("authors", []))
        funders = set(rec.get("funders", []))
        top3_refs = rec.get("top3_refs", [])
        thread_id = rec.get("thread_id", None)

        author_groups[stream] = authors
        funder_groups[stream] = funders
        ref_groups[stream] = top3_refs

    streams = list(author_groups.keys())

    for s in streams:
        distinct_auth = 1
        no_shared_funding = 1
        no_top3_overlap = 1

        for t in streams:
            if s == t:
                continue
            if author_groups[s] & author_groups[t]:
                distinct_auth = 0
            if funder_groups[s] & funder_groups[t]:
                no_shared_funding = 0
            if any(r in ref_groups[t] for r in ref_groups[s]):
                no_top3_overlap = 0

        results.append({
            "stream": s,
            "distinct_auth": distinct_auth,
            "no_shared_funding": no_shared_funding,
            "no_top3_overlap": no_top3_overlap
        })
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to citation JSON file")
    parser.add_argument("--output", required=True, help="Output CSV path")
    args = parser.parse_args()

    data = parse_citation_data(args.input)
    flags = compute_independence_flags(data)

    fieldnames = ["stream", "distinct_auth", "no_shared_funding", "no_top3_overlap"]
    with open(args.output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in flags:
            writer.writerow(row)

    print(f"[parse_citations] Wrote independence flags to {args.output}")

if __name__ == "__main__":
    main()
