"""
Master pipeline for 'Marketing Without Growth'.

Usage:
    python run_all.py                # full run (Monte Carlo at MC_REPS)
    python run_all.py --quick        # fast run for development
    python run_all.py --skip-mc      # everything except the Monte Carlo study

Everything is deterministic given config.SEED.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

from config import BOOT_REPS, EXP3A_N_PER_CELL, EXP3B_N, EXP3C_N_PER_CELL, MC_REPS, OUT_DIR, TAB_DIR
import abm_market
import experiment_analysis
import figures
import measurement
import moderated_mediation
import sem_micro
from dgp import (flip_point, study2_survey, study3a_factorial, study3b_stringency,
                 study3c_sacrifice)


def banner(txt: str):
    print("\n" + "=" * 92)
    print(txt)
    print("=" * 92)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--skip-mc", action="store_true")
    args = ap.parse_args()

    mc_reps = 40 if args.quick else MC_REPS
    boot_reps = 500 if args.quick else BOOT_REPS
    exp_reps = 400 if args.quick else 2500
    perm_metric = 30 if args.quick else 150
    perm_paths = 60 if args.quick else 400

    t0 = time.time()
    summary: dict = {}

    banner("DATA GENERATION")
    df2 = study2_survey()
    d3a = study3a_factorial(n_per_cell=EXP3A_N_PER_CELL)
    d3b = study3b_stringency(n=EXP3B_N)
    d3c = study3c_sacrifice(n_per_cell=EXP3C_N_PER_CELL)
    print(f"Study 2 survey        N = {len(df2)}  ({df2['country'].value_counts().to_dict()})")
    print(f"Study 3A factorial    N = {len(d3a)}  (2x2x2, {EXP3A_N_PER_CELL}/cell)")
    print(f"Study 3B dose         N = {len(d3b)}  (7 stringency levels)")
    print(f"Study 3C sacrifice    N = {len(d3c)}  (2x2, {EXP3C_N_PER_CELL}/cell)")
    print(f"Analytic flip point at mean precarity: S* = {flip_point(0.0):.4f}")
    df2.to_csv(f"{OUT_DIR}/data_study2_survey.csv", index=False)
    d3a.to_csv(f"{OUT_DIR}/data_study3a.csv", index=False)
    d3b.to_csv(f"{OUT_DIR}/data_study3b.csv", index=False)
    d3c.to_csv(f"{OUT_DIR}/data_study3c.csv", index=False)

    res: dict = {}

    if not args.skip_mc:
        banner("STUDY 1  -  MEASUREMENT, RECOVERY, POWER")
        res["s1"] = measurement.run(df2, reps=mc_reps)
        summary["study1"] = {
            "cfa_CFI": float(res["s1"]["cfa_fit"]["CFI"].iloc[0]),
            "cfa_TLI": float(res["s1"]["cfa_fit"]["TLI"].iloc[0]),
            "cfa_RMSEA": float(res["s1"]["cfa_fit"]["RMSEA"].iloc[0]),
            "cfa_chi2_df": float(res["s1"]["cfa_fit"]["chi2/df"].iloc[0]),
            "min_AVE": float(res["s1"]["reliability"]["AVE"].min()),
            "min_CR": float(res["s1"]["reliability"]["CR_omega"].min()),
            "max_HTMT": float(res["s1"]["max_htmt"]),
            # %bias is meaningless for the predicted-null path, whose estimand is ~0; report the
            # absolute bias in coefficient units, and restrict %bias to non-trivial estimands.
            "max_abs_bias_at_1600": float(
                res["s1"]["recovery"].query("N==1600")["bias"].abs().max()),
            "max_abs_pct_bias_at_1600_nontrivial": float(
                res["s1"]["recovery"].query("N==1600 and abs(true) > 0.10")["pct_bias"].abs().max()),
            "mean_coverage_at_1600": float(
                res["s1"]["recovery"].query("N==1600")["coverage_95"].mean()),
            "min_coverage_at_1600": float(
                res["s1"]["recovery"].query("N==1600")["coverage_95"].min()),
            "mc_reps": mc_reps,
        }

    banner("STUDY 2  -  STRUCTURAL MODEL AND CROSS-NATIONAL INVARIANCE")
    res["s2"] = sem_micro.run(df2, n_perm_metric=perm_metric, n_perm_paths=perm_paths)
    res["s2mm"] = moderated_mediation.run(df2, reps=boot_reps)
    summary["study2"] = {
        "sem_CFI": float(res["s2"]["sem_fit"]["CFI"].iloc[0]),
        "sem_TLI": float(res["s2"]["sem_fit"]["TLI"].iloc[0]),
        "sem_RMSEA": float(res["s2"]["sem_fit"]["RMSEA"].iloc[0]),
        "CS_r2": float(res["s2"]["sem_r2"].query("latent=='CS'")["r2"].iloc[0]),
        "n_hypothesized_terms": int(len(res["s2"]["reduced"])),
        "n_supported": int(res["s2"]["reduced"]["supported"].sum()),
        "metric_invariance_p": float(res["s2"]["invariance"]["perm_p"]),
        "n_heterogeneous_paths": int(res["s2"]["multigroup"]["heterogeneous"].sum()),
        "n_indirect_effects_excluding_zero": int(res["s2mm"]["effects"]["excludes_zero"].sum()),
        "n_indirect_effects": int(len(res["s2mm"]["effects"])),
    }

    banner("STUDY 3  -  EXPERIMENTS: ARCHITECTURE, THE FLIP POINT, SUFFICIENCY-WASHING")
    res["s3"] = experiment_analysis.run(d3a, d3b, d3c, reps=exp_reps)
    q = res["s3"]["s3b"]["quadratic"]
    pd_ = res["s3"]["s3b"]["peak_difference"]
    summary["study3"] = {
        "3A_contrast_d": float(res["s3"]["s3a"]["contrast"]["cohens_d"]),
        "3A_contrast_p": float(res["s3"]["s3a"]["contrast"]["p"]),
        "3B_b_quadratic": float(q["b_quadratic"]),
        "3B_p_quadratic": float(q["p_quadratic"]),
        "3B_peak": float(q["peak_boot_median"]),
        "3B_peak_ci": [float(q["peak_ci_lo"]), float(q["peak_ci_hi"])],
        "3B_analytic_peak": float(q["analytic_flip_point_at_mean_precarity"]),
        "3B_inverted_U_supported": bool(res["s3"]["s3b"]["two_lines"]["inverted_U_supported"]),
        "3B_peak_shift_high_minus_low": float(pd_["difference_S_star"]),
        "3B_peak_shift_ci": [float(pd_["ci_lo"]), float(pd_["ci_hi"])],
        "3B_H8_supported": bool(pd_["H8_supported"]),
        "3C_effect_low_sacrifice": float(
            res["s3"]["s3c"]["simple_effects"].query("sacrifice=='low'")
            ["effect_of_demarketing_intensity"].iloc[0]),
        "3C_p_low_sacrifice": float(
            res["s3"]["s3c"]["simple_effects"].query("sacrifice=='low'")["p"].iloc[0]),
        "3C_effect_high_sacrifice": float(
            res["s3"]["s3c"]["simple_effects"].query("sacrifice=='high'")
            ["effect_of_demarketing_intensity"].iloc[0]),
        "3C_p_high_sacrifice": float(
            res["s3"]["s3c"]["simple_effects"].query("sacrifice=='high'")["p"].iloc[0]),
    }

    banner("STUDY 4  -  MARKET-SYSTEMS MODEL OF DEMARKETING PROPAGATION")
    res["s4"] = abm_market.run(full=not args.quick)
    surf = res["s4"]["surface"]
    comp = res["s4"]["complementarity"]
    scen = res["s4"]["scenarios"]
    ineq = res["s4"]["inequality"]
    summary["study4"] = {
        "regimes_observed": sorted(surf["regime"].unique().tolist()),
        "scenario_regimes": dict(zip(scen["scenario"], scen["regime"])),
        "futility_leakage": float(scen.query("scenario=='futility'")["leakage"].iloc[0]),
        "tipping_reduction": float(scen.query("scenario=='tipping'")["throughput_reduction"].iloc[0]),
        "tipping_leakage": float(scen.query("scenario=='tipping'")["leakage"].iloc[0]),
        "backlash_reduction": float(scen.query("scenario=='backlash'")["throughput_reduction"].iloc[0]),
        "PMV_rate_low_lambda_low_r_policy0": float(
            comp.query("policy==0.0 and lambda_hi==False and r_hi==False")["PMV_rate"].iloc[0]),
        "PMV_rate_high_lambda_low_r_policy0": float(
            comp.query("policy==0.0 and lambda_hi==True and r_hi==False")["PMV_rate"].iloc[0]),
        "PMV_rate_low_lambda_high_r_policy0": float(
            comp.query("policy==0.0 and lambda_hi==False and r_hi==True")["PMV_rate"].iloc[0]),
        "PMV_rate_high_lambda_high_r_policy0": float(
            comp.query("policy==0.0 and lambda_hi==True and r_hi==True")["PMV_rate"].iloc[0]),
        "interior_optimum_found": bool(
            abm_market.interior_optimum_summary(res["s4"]["credibility_viability"])
            ["interior_optimum"].any()),
        "lambda_star_at_precarity_0": float(
            ineq.query("precarity_mean==0.0 and precarity_sd==1.0")["lambda_star"].iloc[0]),
        "lambda_star_at_precarity_1": float(
            ineq.query("precarity_mean==1.0 and precarity_sd==1.0")["lambda_star"].iloc[0]),
        "viability_unattainable_above_precarity": float(
            ineq[ineq["lambda_star"].isna()]["precarity_mean"].min()),
    }

    banner("FIGURES")
    figures.make_all(res)

    banner("HEADLINE NUMBERS")
    print(json.dumps(summary, indent=2, default=str))
    with open(f"{OUT_DIR}/summary.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)

    print(f"\nTotal runtime: {time.time() - t0:.1f}s")
    print(f"Tables -> {TAB_DIR}")
    print(f"Figures -> {OUT_DIR}/figures")
    return res, summary


if __name__ == "__main__":
    main()
