#!/usr/bin/env python3
"""
compute_confidence.py
Reads per-stream scores (w, d) and calculates UECF overall confidence + tier.
"""

import argparse
import csv
from pathlib import Path

def compute_confidence(scores):
    N = len(scores)
    total_possible = 51 * N  # 17 max weight * 3 max independence
    numerator = sum(w * d for w, d in scores)
    conf = (numerator / total_possible) * 100
    return conf

def classify_tier(conf):
    if conf > 85:
        return "VERIFIED"
    elif conf >= 60:
        return "PLAUSIBLE"
    else:
        return "SPECULATIVE"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="CSV with columns: stream,w,d")
    parser.add_argument("--output", required=True, help="Output metrics CSV")
    args = parser.parse_args()

    scores = []
    with open(args.input, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            w = int(row["w"])
            d = int(row["d"])
            scores.append((w, d))

    conf = compute_confidence(scores)
    tier = classify_tier(conf)

    with open(args.output, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["confidence", "tier"])
        writer.writerow([f"{conf:.2f}", tier])

    print(f"[compute_confidence] Confidence={conf:.2f}% Tier={tier}")

if __name__ == "__main__":
    main()
