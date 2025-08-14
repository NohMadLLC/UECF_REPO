#!/usr/bin/env python3
"""
make_roc.py
Generates ROC curve points and plot for the UECF backtest dataset.
"""

import argparse
import csv
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

def load_backtest_data(path):
    y_true = []
    y_score = []
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            y_true.append(1 if row["actual_outcome"].lower() == "true" else 0)
            y_score.append(float(row["uecf_confidence"]))
    return y_true, y_score

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to backtest CSV")
    parser.add_argument("--out_png", required=True, help="Output PNG path")
    parser.add_argument("--out_csv", required=True, help="Output CSV of ROC points")
    args = parser.parse_args()

    y_true, y_score = load_backtest_data(args.input)
    fpr, tpr, _ = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)

    with open(args.out_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["fpr", "tpr"])
        for a, b in zip(fpr, tpr):
            writer.writerow([a, b])

    plt.figure()
    plt.plot(fpr, tpr, color="blue", lw=2, label=f"ROC curve (AUC = {roc_auc:.2f})")
    plt.plot([0, 1], [0, 1], color="grey", lw=1, linestyle="--")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("UECF Backtest ROC Curve")
    plt.legend(loc="lower right")
    plt.savefig(args.out_png, dpi=300)

    print(f"[make_roc] Saved ROC curve to {args.out_png} and points to {args.out_csv}")

if __name__ == "__main__":
    main()
