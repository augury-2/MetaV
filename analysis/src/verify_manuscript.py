"""
Verification harness: checks that every numeric claim made in paper/MANUSCRIPT.md matches the
figures actually produced in analysis/output/.

Run:  python verify_manuscript.py
Exit code 0 = all claims verified; 1 = at least one mismatch.
"""
from __future__ import annotations

import json
import sys

import pandas as pd

from config import OUT_DIR, TAB_DIR

FAILS: list[str] = []
CHECKS = 0


def chk(label: str, actual, expected, tol: float = 0.0005):
    global CHECKS
    CHECKS += 1
    if isinstance(expected, str) or isinstance(expected, bool):
        ok = actual == expected
    elif expected is None:
        ok = actual is None or (isinstance(actual, float) and pd.isna(actual))
    else:
        ok = abs(float(actual) - float(expected)) <= tol
    status = "ok  " if ok else "FAIL"
    print(f"  [{status}] {label}: actual={actual!r} claimed={expected!r}")
    if not ok:
        FAILS.append(label)


def t(name: str) -> pd.DataFrame:
    return pd.read_csv(f"{TAB_DIR}/{name}")


def main():
    S = json.load(open(f"{OUT_DIR}/summary.json"))

    print("\n--- Study 1: measurement ---")
    fit = t("t1_cfa_fit.csv").iloc[0]
    chk("CFA chi2", round(fit["chi2"], 2), 1626.03, 0.01)
    chk("CFA df", int(fit["DoF"]), 1119)
    chk("CFA chi2/df", round(fit["chi2/df"], 2), 1.45, 0.005)
    chk("CFA CFI", round(fit["CFI"], 3), 0.985, 0.0005)
    chk("CFA TLI", round(fit["TLI"], 3), 0.983, 0.0005)
    chk("CFA NFI", round(fit["NFI"], 3), 0.953, 0.0005)
    chk("CFA RMSEA", round(fit["RMSEA"], 3), 0.017, 0.0005)
    chk("CFA GFI", round(fit["GFI"], 3), 0.953, 0.0005)
    chk("CFA AGFI", round(fit["AGFI"], 3), 0.947, 0.0005)

    from config import MEASURES
    chk("n constructs in measurement model", len(MEASURES), 15)
    chk("n items", sum(v["n_items"] for v in MEASURES.values()), 51)

    rel = t("t2_reliability_ave.csv")
    chk("alpha min", round(rel["alpha"].min(), 3), 0.767, 0.0005)
    chk("alpha max", round(rel["alpha"].max(), 3), 0.860, 0.0005)
    chk("CR min", round(rel["CR_omega"].min(), 3), 0.767, 0.0005)
    chk("CR max", round(rel["CR_omega"].max(), 3), 0.859, 0.0005)
    chk("AVE min", round(rel["AVE"].min(), 3), 0.525, 0.0005)
    chk("AVE max", round(rel["AVE"].max(), 3), 0.604, 0.0005)
    chk("loading min", round(rel["min_loading"].min(), 3), 0.672, 0.0005)
    chk("loading max", round(rel["max_loading"].max(), 3), 0.839, 0.0005)
    chk("all AVE > .50", bool(rel["AVE_ok"].all()), True)

    chk("max HTMT", round(S["study1"]["max_HTMT"], 3), 0.673, 0.0005)
    h = pd.read_csv(f"{TAB_DIR}/t3_htmt.csv", index_col=0)["CS"]
    chk("HTMT CS-VS", round(h["VS"], 3), 0.531, 0.0005)
    chk("HTMT CS-FRUG", round(h["FRUG"], 3), 0.345, 0.0005)
    chk("HTMT CS-MAT", round(h["MAT"], 3), 0.344, 0.0005)
    chk("HTMT CS-CR", round(h["CR"], 3), 0.120, 0.0005)

    print("\n--- Study 1: recovery and power ---")
    chk("max |bias| @1600", round(S["study1"]["max_abs_bias_at_1600"], 3), 0.085, 0.0005)
    chk("mean coverage @1600", round(S["study1"]["mean_coverage_at_1600"], 3), 0.958, 0.0005)
    chk("min coverage @1600", round(S["study1"]["min_coverage_at_1600"], 3), 0.926, 0.0005)
    chk("MC reps", S["study1"]["mc_reps"], 500)

    rec = t("t4_mc_recovery.csv")
    r16 = rec[rec["N"] == 1600].set_index("path")
    chk("int:sac estimand", round(r16.loc["BSE<-int:sac", "true"], 3), 0.224, 0.0005)
    chk("int:sac bias", round(r16.loc["BSE<-int:sac", "bias"], 3), 0.085, 0.0005)

    p = t("t5_power_curves.csv").set_index("path")
    chk("terms >=80% power @1600", int((p["1600"] >= 0.80).sum()), 26)
    chk("n focal terms", len(p), 28)
    chk("max required N", round(p["N_for_80pct"].max()), 1115, 1)
    chk("int:sac power @1600", round(p.loc["BSE<-int:sac", "1600"], 2), 0.21, 0.005)
    chk("int:sac power @2400", round(p.loc["BSE<-int:sac", "2400"], 3), 0.254, 0.0005)
    chk("null path power @1600", round(p.loc["BSE<-intensity|no_sacrifice", "1600"], 3), 0.054, 0.0005)
    chk("AD<-stringency2 required N", round(p.loc["AD<-stringency2", "N_for_80pct"]), 732, 1)
    chk("CS<-stringency2 required N", round(p.loc["CS<-stringency2", "N_for_80pct"]), 709, 1)
    chk("CS<-stringency required N", round(p.loc["CS<-stringency", "N_for_80pct"]), 1115, 1)

    print("\n--- Study 2 ---")
    chk("SEM CFI", round(S["study2"]["sem_CFI"], 3), 0.975, 0.0005)
    chk("SEM TLI", round(S["study2"]["sem_TLI"], 3), 0.973, 0.0005)
    chk("SEM RMSEA", round(S["study2"]["sem_RMSEA"], 3), 0.021, 0.0005)
    chk("CS R2", round(S["study2"]["CS_r2"], 3), 0.583, 0.0005)
    chk("terms supported", S["study2"]["n_supported"], 28)
    chk("n terms", S["study2"]["n_hypothesized_terms"], 28)
    chk("metric invariance p", round(S["study2"]["metric_invariance_p"], 2), 0.38, 0.005)
    chk("heterogeneous paths", S["study2"]["n_heterogeneous_paths"], 0)
    chk("indirect effects excl zero", S["study2"]["n_indirect_effects_excluding_zero"], 36)

    r2 = t("t6c_sem_r2.csv").set_index("latent")["r2"]
    for lv, v in [("PA", .263), ("CE", .155), ("RIA", .273), ("RSV", .447), ("AD", .552),
                  ("PR", .434), ("SCB", .293), ("BSE", .203), ("SPS", .203), ("CDC", .246)]:
        chk(f"R2 {lv}", round(r2[lv], 3), v, 0.0005)

    sp = t("t6b_sem_paths.csv").set_index(["dv", "predictor"])["beta_std"]
    for k, v in [(("PA", "agency"), .388), (("PA", "locus"), .185), (("PA", "frame"), .139),
                 (("PA", "stringency"), -.071), (("PA", "precarity"), -.236),
                 (("CE", "locus"), .336), (("CE", "community"), .200),
                 (("RIA", "PA"), .410), (("RIA", "frame"), .162), (("RIA", "CE"), .136),
                 (("RIA", "growth_endorse"), -.168),
                 (("RSV", "RIA"), .433), (("RSV", "symbolic"), .504),
                 (("AD", "agency"), -.176), (("AD", "frame"), -.138),
                 (("AD", "stringency"), .461), (("AD", "precarity"), .511),
                 (("AD", "symbolic"), .136), (("PR", "AD"), .649),
                 (("CS", "RIA"), .296), (("CS", "RSV"), .334), (("CS", "CE"), .221),
                 (("CS", "PR"), -.284), (("CS", "AD"), -.187),
                 (("SCB", "CS"), .506), (("BSE", "CS"), .282), (("BSE", "PR"), -.229),
                 (("SPS", "CS"), .370), (("SPS", "CE"), .168),
                 (("CDC", "CS"), -.261), (("CDC", "PR"), .269), (("CDC", "symbolic"), .217)]:
        chk(f"beta {k[0]}<-{k[1]}", round(sp[k], 3), v, 0.0011)

    red = t("t6d_reduced_form.csv").set_index("path")
    chk("null path b", round(red.loc["BSE<-intensity|no_sacrifice", "b"], 3), -0.057, 0.0011)
    chk("null path p", round(red.loc["BSE<-intensity|no_sacrifice", "p"], 3), 0.729, 0.0011)

    e = t("t7_bootstrap_effects.csv").set_index("effect")
    def eff(name, est, lo, hi):
        chk(f"{name} est", round(e.loc[name, "estimate"], 3), est, 0.0011)
        chk(f"{name} CI", (round(e.loc[name, "ci_lo"], 3), round(e.loc[name, "ci_hi"], 3)),
            None if lo is None else None) if False else None
        chk(f"{name} lo", round(e.loc[name, "ci_lo"], 3), lo, 0.0011)
        chk(f"{name} hi", round(e.loc[name, "ci_hi"], 3), hi, 0.0011)
    eff("H4_serial_agency_PA_RIA_CS", .089, .071, .109)
    eff("H4_serial_agency_PA_RIA_RSV_CS", .013, .009, .018)
    eff("H1_routeB_agency_AD_PR_CS", .049, .036, .062)
    eff("H1_routeB_agency_AD_CS", .067, .048, .088)
    eff("H1_net_agency_to_CS", .218, .185, .253)
    eff("H3_frame_via_RIA", .102, .074, .133)
    eff("H3_frame_via_AD_PR", .035, .023, .047)
    eff("H3_frame_via_AD_direct", .048, .032, .066)
    eff("H3_frame_net", .184, .147, .223)
    eff("H2_index_modmed", .036, .024, .049)
    eff("H2_cond_locus_CE_CS@lowColl", .078, .055, .104)
    eff("H2_cond_locus_CE_CS@meanColl", .114, .087, .143)
    eff("H2_cond_locus_CE_CS@highColl", .150, .115, .186)
    eff("H9_index_modmed", -.249, -.302, -.201)
    eff("H9_cond_stringency_AD_PR_CS@lowPrec", -.327, -.399, -.259)
    eff("H9_cond_stringency_AD_PR_CS@meanPrec", -.576, -.656, -.498)
    eff("H9_cond_stringency_AD_PR_CS@highPrec", -.826, -.938, -.717)
    eff("H10_RIA_to_CS@lowSym", .208, .153, .264)
    eff("H10_RIA_to_CS@highSym", .452, .398, .510)
    eff("H10_AD_to_PR@lowSym", .428, .371, .483)
    eff("H10_AD_to_PR@highSym", .678, .622, .735)
    eff("H10_polarization_gap_RouteA", .244, .170, .321)
    eff("H10_polarization_gap_RouteB", .250, .171, .330)
    eff("H11_index_mod", .135, .094, .175)
    eff("H11_cond_CS_to_SCB@lowComm", .234, .170, .298)
    eff("H11_cond_CS_to_SCB@highComm", .503, .445, .560)
    eff("H12_index_mod", -.094, -.137, -.051)
    eff("H12_cond_CS_to_CDC@lowComm", -.091, -.163, -.020)
    eff("H12_cond_CS_to_CDC@highComm", -.278, -.338, -.218)
    eff("H14_index_mod", -.104, -.149, -.062)
    eff("H14_cond_CS_to_SPS@lowGrowth", .392, .329, .455)
    eff("H14_cond_CS_to_SPS@highGrowth", .183, .120, .247)

    print("\n--- Study 2: Johnson-Neyman and multigroup ---")
    jn = t("t8_johnson_neyman_stringency_precarity.csv")
    sig_neg = jn[(jn["significant"]) & (jn["effect"] < 0)]
    chk("JN neg threshold", round(sig_neg["mod_value"].min(), 3), -0.203, 0.0011)
    d2 = pd.read_csv(f"{OUT_DIR}/data_study2_survey.csv")
    chk("sample share above JN neg bound", round(100 * (d2["precarity"] > -0.203).mean(), 1), 54.6, 0.05)
    chk("sample share below JN pos bound", round(100 * (d2["precarity"] > -1.371).mean(), 1), 88.1, 0.05)

    cfg = t("t9a_configural_fit.csv").set_index("country")
    for c, cfi, rm in [("DE", .986, .019), ("FR", .982, .021), ("SE", .974, .026), ("BR", .978, .025)]:
        chk(f"configural CFI {c}", round(cfg.loc[c, "CFI"], 3), cfi, 0.0005)
        chk(f"configural RMSEA {c}", round(cfg.loc[c, "RMSEA"], 3), rm, 0.0005)
    mg = t("t9c_multigroup_paths.csv")
    chk("min heterogeneity p", round(mg["perm_p_heterogeneity"].min(), 3), 0.085, 0.0011)

    print("\n--- Study 3A ---")
    a = t("t10a_study3a_anova.csv")
    a = a[a["dv"] == "CS_c"].set_index("term")
    chk("3A agency F", round(a.loc["C(agency)", "F"], 2), 22.72, 0.005)
    chk("3A agency eta2p", round(a.loc["C(agency)", "partial_eta_sq"], 3), 0.019, 0.0005)
    chk("3A locus F", round(a.loc["C(locus)", "F"], 2), 5.07, 0.005)
    chk("3A locus p", round(a.loc["C(locus)", "PR(>F)"], 3), 0.024, 0.0005)
    chk("3A frame F", round(a.loc["C(frame)", "F"], 2), 7.87, 0.005)
    chk("3A frame p", round(a.loc["C(frame)", "PR(>F)"], 3), 0.005, 0.0005)
    chk("3A residual df", int(a.loc["Residual", "df"]), 1192)
    inter = a.loc[[i for i in a.index if ":" in i], "PR(>F)"]
    chk("3A no interaction p<.19", bool((inter > 0.19).all()), True)

    m = t("t10c_study3a_marginals.csv").set_index(["factor", "dv"])
    for k, v in [(("agency", "CS_c"), .274), (("agency", "PA_c"), .687), (("agency", "AD_c"), -.448),
                 (("locus", "CS_c"), .129), (("locus", "PA_c"), .222), (("locus", "AD_c"), .018),
                 (("frame", "CS_c"), .160), (("frame", "PA_c"), .204), (("frame", "AD_c"), -.245)]:
        chk(f"3A d {k[0]}->{k[1]}", round(m.loc[k, "cohens_d"], 3), v, 0.0011)
    chk("3A locus->AD p", round(m.loc[("locus", "AD_c"), "p"], 3), 0.751, 0.0011)

    cells = t("t10b_study3a_cells.csv")
    best = cells.query("agency==1 and locus==1 and frame==1")["CS_mean"].iloc[0]
    worst = cells.query("agency==0 and locus==0 and frame==0")["CS_mean"].iloc[0]
    chk("3A best cell M", round(best, 3), 0.277, 0.0011)
    chk("3A worst cell M", round(worst, 3), -0.238, 0.0011)
    chk("3A contrast d", round(S["study3"]["3A_contrast_d"], 3), 0.516, 0.0011)

    print("\n--- Study 3B ---")
    q = t("t11a_flip_quadratic.csv").iloc[0]
    chk("3B b_quad", round(q["b_quadratic"], 3), -2.507, 0.0011)
    chk("3B adj b_quad", round(q["adj_b_quadratic"], 3), -2.355, 0.0011)
    chk("3B adj R2", round(q["adj_r2"], 3), 0.186, 0.0011)
    chk("3B peak", round(q["peak_boot_median"], 3), 0.406, 0.0011)
    chk("3B peak lo", round(q["peak_ci_lo"], 3), 0.368, 0.0011)
    chk("3B peak hi", round(q["peak_ci_hi"], 3), 0.436, 0.0011)
    chk("3B analytic peak", round(q["analytic_flip_point_at_mean_precarity"], 3), 0.353, 0.0011)

    tl = t("t11b_two_lines.csv").iloc[0]
    chk("3B slope_low", round(tl["slope_low"], 3), 1.166, 0.0011)
    chk("3B slope_high", round(tl["slope_high"], 3), -1.347, 0.0011)
    chk("3B inverted U", bool(tl["inverted_U_supported"]), True)

    dose = t("t11c_dose_response.csv").set_index("stringency")
    for s, cs, ria, ad in [(0.05, -.131, -.878, -.488), (0.15, .095, -.349, -.484),
                           (0.30, .189, .016, -.277), (0.45, .207, .258, -.188),
                           (0.60, .129, .341, .155), (0.75, -.111, .324, .445),
                           (0.90, -.377, .288, .838)]:
        chk(f"3B dose CS @{s}", round(dose.loc[s, "CS"], 3), cs, 0.0011)
        chk(f"3B dose RIA @{s}", round(dose.loc[s, "RIA"], 3), ria, 0.0011)
        chk(f"3B dose AD @{s}", round(dose.loc[s, "AD"], 3), ad, 0.0011)

    bp = t("t11d_flip_by_precarity.csv").set_index("precarity_tercile")
    for terc, mz, bq, pk, an in [("low", -1.12, -1.394, .510, .474),
                                 ("mid", 0.02, -2.864, .420, .352),
                                 ("high", 1.11, -3.309, .352, .299)]:
        chk(f"3B {terc} mean z", round(bp.loc[terc, "mean_precarity"], 2), mz, 0.005)
        chk(f"3B {terc} b_quad", round(bp.loc[terc, "b_quadratic"], 3), bq, 0.0011)
        chk(f"3B {terc} peak", round(bp.loc[terc, "peak_boot_median"], 3), pk, 0.0011)
        chk(f"3B {terc} analytic", round(bp.loc[terc, "analytic_flip_point"], 3), an, 0.0011)

    pd_ = t("t11g_peak_difference.csv").iloc[0]
    chk("3B peak diff", round(pd_["difference_S_star"], 4), -0.0965, 0.0002)
    chk("3B peak diff lo", round(pd_["ci_lo"], 3), -0.178, 0.0011)
    chk("3B peak diff hi", round(pd_["ci_hi"], 3), -0.019, 0.0011)
    chk("3B peak diff p", round(pd_["boot_p_one_sided_negative"], 4), 0.0096, 0.0002)
    chk("3B analytic diff", round(pd_["analytic_difference"], 3), -0.115, 0.0011)

    ps = t("t11e_peak_shift.csv").iloc[0]
    chk("3B str2xprec b", round(ps["b_str2_x_prec"], 3), -0.790, 0.0011)
    chk("3B str2xprec p", round(ps["p_str2_x_prec"], 3), 0.006, 0.0011)
    chk("3B str-x-prec b", round(ps["b_str_x_prec"], 3), 0.352, 0.0011)
    chk("3B str-x-prec p", round(ps["p_str_x_prec"], 3), 0.213, 0.0011)

    th = pd.read_csv(f"{TAB_DIR}/t11h_two_lines_halves.csv", index_col=0)
    chk("3B low-prec breakpoint", round(th.loc["low_precarity", "breakpoint"], 3), 0.470, 0.0011)
    chk("3B high-prec breakpoint", round(th.loc["high_precarity", "breakpoint"], 3), 0.374, 0.0011)
    chk("3B low-prec slope_high", round(th.loc["low_precarity", "slope_high"], 3), -0.840, 0.0011)
    chk("3B high-prec slope_high", round(th.loc["high_precarity", "slope_high"], 3), -1.841, 0.0011)

    print("\n--- Study 3C ---")
    a3 = t("t12a_study3c_anova.csv").set_index("term")
    key = [i for i in a3.index if ":" in i][0]
    chk("3C interaction F", round(a3.loc[key, "F"], 2), 13.60, 0.005)
    chk("3C interaction p", round(a3.loc[key, "PR(>F)"], 4), 0.0002, 0.00005)
    chk("3C interaction eta2p", round(a3.loc[key, "partial_eta_sq"], 3), 0.021, 0.0005)
    chk("3C residual df", int(a3.loc["Residual", "df"]), 636)
    c3 = t("t12b_study3c_cells.csv").set_index(["intensity_hi", "sacrifice_hi"])["BSE"]
    for k, v in [((0, 0), -.014), ((0, 1), -.178), ((1, 0), -.109), ((1, 1), .301)]:
        chk(f"3C cell {k}", round(c3[k], 3), v, 0.0011)
    se = t("t12c_study3c_simple.csv").set_index("sacrifice")
    chk("3C low sac effect", round(se.loc["low", "effect_of_demarketing_intensity"], 3), -0.096, 0.0011)
    chk("3C low sac p", round(se.loc["low", "p"], 3), 0.389, 0.0011)
    chk("3C low sac d", round(se.loc["low", "cohens_d"], 3), -0.096, 0.0011)
    chk("3C high sac effect", round(se.loc["high", "effect_of_demarketing_intensity"], 3), 0.479, 0.0011)
    chk("3C high sac t", round(se.loc["high", "t"], 2), 4.37, 0.005)
    chk("3C high sac d", round(se.loc["high", "cohens_d"], 3), 0.489, 0.0011)

    print("\n--- Study 4 ---")
    sc = t("t13a_abm_scenarios.csv").set_index("scenario")
    for name, reg, dq, lk, rp, pr in [
            ("futility", "futility", .011, .740, .322, .000),
            ("collapse", "collapse", .000, 1.000, .000, .125),
            ("niche", "niche", .100, .418, 1.935, .250),
            ("tipping", "tipping", .391, -1.443, 5.683, .750),
            ("backlash", "backlash", -.236, 1.500, 1.805, .250)]:
        chk(f"S4 {name} regime", sc.loc[name, "regime"], reg)
        chk(f"S4 {name} dQ", round(sc.loc[name, "throughput_reduction"], 3), dq, 0.0011)
        chk(f"S4 {name} leakage", round(sc.loc[name, "leakage"], 3), lk, 0.0011)
        chk(f"S4 {name} rel profit", round(sc.loc[name, "relative_profit_demarketers"], 3), rp, 0.0011)
        chk(f"S4 {name} prop", round(sc.loc[name, "prop_rate"], 3), pr, 0.0011)
    chk("S4 collapse exits", int(sc.loc["collapse", "n_exits_demarketers"]), 1)
    chk("S4 backlash rebound", round(sc.loc["backlash", "rebound_mean_treat"], 3), 0.538, 0.0011)
    chk("S4 backlash past flip", round(sc.loc["backlash", "share_micro_negative"], 3), 0.847, 0.0011)
    chk("S4 tipping cs", round(sc.loc["tipping", "cs_mean_treat"], 3), 0.781, 0.0011)

    surf = t("t14a_tipping_surface.csv")
    freq = pd.crosstab(surf["policy"], surf["regime"], normalize="index")
    for pol, vals in [(0.0, {"futility": .383, "collapse": .198, "niche": .136,
                            "strained": .012, "tipping": .272}),
                      (0.3, {"futility": .086, "collapse": .173, "niche": .062,
                             "strained": .173, "tipping": .506}),
                      (0.6, {"futility": .000, "collapse": .185, "niche": .012,
                             "strained": .111, "tipping": .691})]:
        for reg, v in vals.items():
            chk(f"S4 freq policy={pol} {reg}", round(freq.loc[pol, reg], 3), v, 0.0011)
    chk("S4 n sweep cells", len(surf), 243)

    comp = t("t14c_complementarity.csv").query("policy==0.0").set_index(["lambda_hi", "r_hi"])
    for k, pmv, red, lk in [((False, False), .00, .018, .768), ((True, False), .25, .081, .108),
                            ((False, True), .50, .118, .166), ((True, True), 1.00, .297, -1.079)]:
        chk(f"S4 PMV rate {k}", round(comp.loc[k, "PMV_rate"], 2), pmv, 0.005)
        chk(f"S4 mean reduction {k}", round(comp.loc[k, "mean_reduction"], 3), red, 0.0011)
        chk(f"S4 mean leakage {k}", round(comp.loc[k, "mean_leakage"], 3), lk, 0.0011)

    ls = t("t14b_lambda_star.csv").set_index(["policy", "r_demarketer"])["lambda_star"]
    for (pol, r), v in [((0.0, 0.250), .600), ((0.0, 0.375), .525), ((0.0, 0.500), .525),
                        ((0.0, 0.625), .375), ((0.0, 0.750), .300), ((0.0, 0.875), .075),
                        ((0.0, 1.000), .000),
                        ((0.3, 0.250), .525), ((0.3, 0.375), .450), ((0.3, 0.500), .300),
                        ((0.3, 0.625), .000),
                        ((0.6, 0.125), .525), ((0.6, 0.250), .375), ((0.6, 0.375), .225),
                        ((0.6, 0.500), .000)]:
        chk(f"S4 lambda* policy={pol} r={r}", round(ls[(pol, r)], 3), v, 0.0011)
    for pol in (0.0, 0.3, 0.6):
        chk(f"S4 lambda* undefined policy={pol} r=0", bool(pd.isna(ls[(pol, 0.0)])), True)
    for pol in (0.0, 0.3):
        chk(f"S4 lambda* undefined policy={pol} r=0.125", bool(pd.isna(ls[(pol, 0.125)])), True)

    io = t("t15b_interior_optimum.csv").set_index("phi_credibility_erosion")
    for phi, argmax, mx in [(0.0, 1.0, .417), (0.4, 1.0, .350), (0.8, 1.0, .274), (1.0, 1.0, .209)]:
        chk(f"S4 argmax r phi={phi}", round(io.loc[phi, "r_argmax"], 2), argmax, 0.005)
        chk(f"S4 max reduction phi={phi}", round(io.loc[phi, "max_reduction"], 3), mx, 0.0011)
        chk(f"S4 interior phi={phi}", bool(io.loc[phi, "interior_optimum"]), False)

    iq = t("t16_inequality.csv")
    iq1 = iq[iq["precarity_sd"] == 1.0].set_index("precarity_mean")
    for mu, lam, shr, ss in [(0.0, .56, .016, .353), (0.5, .60, .050, .325),
                             (1.0, .64, .124, .303), (1.5, .68, .258, .285)]:
        chk(f"S4 lambda* precarity={mu}", round(iq1.loc[mu, "lambda_star"], 3), lam, 0.0011)
        chk(f"S4 share past flip precarity={mu}", round(iq1.loc[mu, "share_below_flip_point"], 3), shr, 0.0011)
        chk(f"S4 mean S* precarity={mu}", round(iq1.loc[mu, "mean_flip_point_S_star"], 3), ss, 0.0011)
    for mu in (2.0, 2.5):
        chk(f"S4 unattainable at precarity={mu}", bool(iq1.loc[mu, "lambda_star"] != iq1.loc[mu, "lambda_star"]), True)
    chk("S4 share past flip precarity=2.0", round(iq1.loc[2.0, "share_below_flip_point"], 3), 0.444, 0.0011)
    chk("S4 share past flip precarity=2.5", round(iq1.loc[2.5, "share_below_flip_point"], 3), 0.640, 0.0011)
    chk("S4 max reduction precarity=0", round(iq1.loc[0.0, "max_throughput_reduction"], 2), 0.21, 0.005)
    chk("S4 max reduction precarity=2.0", round(iq1.loc[2.0, "max_throughput_reduction"], 3), 0.018, 0.0011)
    iq0 = iq[iq["precarity_mean"] == 0.0].set_index("precarity_sd")
    chk("S4 share past flip sd=0.6", round(iq0.loc[0.6, "share_below_flip_point"], 3), 0.000, 0.0011)
    chk("S4 share past flip sd=1.4", round(iq0.loc[1.4, "share_below_flip_point"], 3), 0.062, 0.0011)
    chk("S4 lambda* stable in sd at mu=0", bool((iq0["lambda_star"] == 0.56).all()), True)

    sens = t("t17_sensitivity.csv")
    chk("S4 sensitivity all tipping", bool((sens["regime"] == "tipping").all()), True)
    chk("S4 sensitivity all PMV", bool(sens["PMV"].all()), True)
    chk("S4 n perturbations", len(sens), 32)
    ss = sens.set_index(["parameter", "direction"])["d_throughput_reduction"]
    chk("S4 sens d_demarketer +20%", round(ss[("d_demarketer", "+20%")], 3), 0.072, 0.0011)
    chk("S4 sens d_demarketer -20%", round(ss[("d_demarketer", "-20%")], 3), -0.059, 0.0011)
    chk("S4 sens imitation_rate -20%", round(ss[("imitation_rate", "-20%")], 3), -0.021, 0.0011)

    print("\n" + "=" * 70)
    print(f"{CHECKS - len(FAILS)}/{CHECKS} claims verified")
    if FAILS:
        print(f"\n{len(FAILS)} MISMATCHES:")
        for f in FAILS:
            print(f"  - {f}")
        return 1
    print("All manuscript claims match the analysis output.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
