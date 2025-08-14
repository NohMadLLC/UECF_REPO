```markdown
# Universal Evidence Convergence Framework (UECF) – Public Repository

**Version:** 1.0  
**Author:** Breezon Brown (NohMad Research / NohMad LLC)  
**License:** MIT (see LICENSE file)  
**Related Publications:**  
- Main manuscript: *The Universal Evidence Convergence Framework (UECF): A Methodology for Transparent, Equitable, and Rigorous Truth Evaluation*  
- Supplements: S1 (Appendix F & scoring), S2 (Automated Scoring Stress Test), S3 (Threshold Calibration Backtest)

---

## 1. Purpose

This repository contains the complete dataset, algorithm specification, and codebase required to reproduce all tables, figures, and metrics from the UECF study. It implements the automated binary criteria from Appendix F (Supplement S1) across all four main case studies and the 30-case threshold backtest.

---

## 2. Repo Layout

```

UECF\_REPO/
README.md
LICENSE
data/
case\_studies/
exodus\_binary\_checks.csv
clovis\_binary\_checks.csv
polynesian\_binary\_checks.csv
prophecy\_binary\_checks.csv
backtest/
backtest\_30cases.csv
code/
scoring\_pipeline.py
extract\_metadata.py
parse\_citations.py
compute\_confidence.py
make\_roc.py
outputs/
s2\_extraction\_audit\_logs/
s3\_threshold\_backtest\_metrics.csv
roc\_curve.png

````

---

## 3. Automated Binary Criteria (Appendix F, Embedded)

| **Metric** | **Criterion** | **Description** | **Pass Condition** | **Points** |
|------------|---------------|-----------------|--------------------|------------|
| **Empirical Robustness** (0–5) | Peer reviewed | Publication in vetted, peer-reviewed venue | Indexed journal/conference whitelist | +1 |
|            | Independent replication ≥ 2 | Reproduced by ≥ 2 independent teams | Distinct affiliations | +1 |
|            | Direct physical evidence | Material artefact or direct measurement | Tagged as physical | +1 |
|            | Confidence ≥ 95% | Explicit CI ≥ 95% or equivalent | Regex match in text | +1 |
|            | Data public | Raw/processed data accessible | Download link present | +1 |
| **Falsifiability** (0–5) | Specific dates/measurements | Contains concrete dated/measured claims | NLP date/unit detection | +1 |
|            | Testing method stated | Protocol to verify claim included | Methods section | +1 |
|            | Counterfactuals stated | States disproof conditions | “unless”, “if not” clauses | +1 |
|            | Multiple disprovables | ≥ 2 independent falsifiers | e.g., date + locus | +1 |
|            | Independently testable | Third parties can reproduce | Accessible tools/data | +1 |
| **Independence** (0–3) | Distinct authorship/source | Non-overlapping first/senior authors | Metadata match | +1 |
|            | No shared funding | Distinct grants/sponsors | Parse acknowledgments | +1 |
|            | No top-3 reference overlap | Distinct upstream literature | Citation graph diff | +1 |
| **Cross-Corroboration** (0, 2, 4) | ≥ 2 unrelated categories | Agreement across different evidence categories | Category map check | +2 |
|            | Independent literature confirmation | Agreement replicated in independent literature thread | Disjoint citation set | +2 |

**Total possible per stream:** 17 points (w) + independence multiplier (d) up to 3 → 51 points per stream for confidence scaling.

---

## 4. Running the Pipeline

### 4.1 Prerequisites
- Python 3.8+
- Required packages: `pandas`, `numpy`, `matplotlib`, `networkx`

```bash
pip install pandas numpy matplotlib networkx
````

---

### 4.2 Reproducing Case Study Scores (S1)

```bash
python code/scoring_pipeline.py data/case_studies/exodus_binary_checks.csv
python code/scoring_pipeline.py data/case_studies/clovis_binary_checks.csv
python code/scoring_pipeline.py data/case_studies/polynesian_binary_checks.csv
python code/scoring_pipeline.py data/case_studies/prophecy_binary_checks.csv
```

* Outputs per-stream binary flags, `(w,d)` values, and final confidence/tier.

---

### 4.3 Regenerating the Stress Test (S2)

```bash
python code/scoring_pipeline.py --stress-test data/case_studies/exodus_binary_checks.csv
```

* Produces ablation and independence shuffle results in `outputs/s2_extraction_audit_logs/`.

---

### 4.4 Reproducing the Threshold Backtest (S3)

```bash
python code/compute_confidence.py data/backtest/backtest_30cases.csv
python code/make_roc.py outputs/s3_threshold_backtest_metrics.csv outputs/roc_curve.png
```

* Generates ROC curve in `outputs/roc_curve.png` and metrics in `outputs/s3_threshold_backtest_metrics.csv`.

---

## 5. Versioning & Audit Trail

* **Commit hash**: Always cite the commit hash when using outputs in publications.
* **Criteria changes**: Any edits to binary criteria must be logged in `README.md` and rerun against all case studies and the backtest.
* **Assumption Impact Scoring (AIS)**: Re-run AIS whenever criteria or scoring logic changes, and publish delta results.

---

## 6. Contact

For technical issues, open a GitHub Issue in `UECF_REPO`. For methodological questions, contact **NohMad Research** email Nohmad.business@gmail.com .

---

```

