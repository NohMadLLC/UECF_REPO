# scoring_pipeline.py
# UECF Supplement S1 – Automated Scoring
# Reads a binary criteria CSV (Appendix F format) for one case study
# and outputs per-stream scores and overall confidence/tier.

import argparse
import pandas as pd
import json
from pathlib import Path

# Appendix F binary criteria – must be present in the CSV
CRITERIA = [
    "peer_reviewed", "replicated_ge2", "physical_evidence",
    "conf_95_or_higher", "data_public",
    "specific_dates", "test_method", "counterfactuals",
    "multi_disprovables", "indep_testable",
    "distinct_authorship", "no_shared_funding", "no_top3_reference_overlap",
    "crosscat_plus2", "indep_lit_plus2"
]

# Metric groupings and caps
ROBUSTNESS = CRITERIA[0:5]           # max 5
FALSIFIABILITY = CRITERIA[5:10]      # max 5
INDEPENDENCE = CRITERIA[10:13]       # max 3
CROSSCORR = CRITERIA[13:15]          # each worth +2, max 4
MAX_R, MAX_F, MAX_D, MAX_C = 5, 5, 3, 4
STREAM_MAX = 17
DENOM_PER_STREAM = STREAM_MAX * MAX_D  # 51

TIERS = [
    ("Verified", 85.0000001, 100.0),
    ("Plausible", 60.0, 85.0),
    ("Speculative", -1e9, 60.0)
]

def load_binary_checks(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = [c for c in CRITERIA if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    for c in CRITERIA:
        df[c] = df[c].astype(int)
        if not set(df[c].unique()).issubset({0, 1}):
            raise ValueError(f"Column {c} must be 0/1")
    return df

def score_streams(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["r"] = out[ROBUSTNESS].sum(axis=1).clip(upper=MAX_R)
    out["f"] = out[FALSIFIABILITY].sum(axis=1).clip(upper=MAX_F)
    out["d"] = out[INDEPENDENCE].sum(axis=1).clip(upper=MAX_D)
    out["c"] = (out[CROSSCORR].sum(axis=1) * 2).clip(upper=MAX_C)
    out["w"] = (out["r"] + out["f"] + out["d"] + out["c"]).clip(upper=STREAM_MAX)
    return out

def compute_confidence(df: pd.DataFrame) -> dict:
    N = len(df)
    numerator = float((df["w"] * df["d"]).sum())
    denominator = DENOM_PER_STREAM * N
    confidence = 100.0 * numerator / denominator
    tier = None
    for name, lo, hi in TIERS:
        if confidence > lo and confidence <= hi:
            tier = name
            break
    if abs(confidence - 85.0) < 1e-12 or abs(confidence - 60.0) < 1e-12:
        tier = "Plausible"
    return {
        "N": N,
        "numerator": numerator,
        "denominator": denominator,
        "confidence": confidence,
        "tier": tier
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Binary checks CSV for a single case")
    ap.add_argument("--outdir", required=False, default="outputs", help="Directory for outputs")
    args = ap.parse_args()

    inpath = Path(args.input)
    outdir = Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)
    case_name = inpath.stem

    df = load_binary_checks(inpath)
    scored = score_streams(df)
    scored.to_csv(outdir / f"{case_name}_per_stream.csv", index=False)

    summary = compute_confidence(scored)
    with open(outdir / f"{case_name}_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
