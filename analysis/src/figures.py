"""
Figure generation for the manuscript. All figures are written to ../output/figures/.

Fig 1  Conceptual model (dual-route architecture)
Fig 2  The flip point: Route A saturation vs Route B acceleration, and the resulting inverted-U
Fig 3  Empirical dose-response with the analytic prediction overlaid
Fig 4  Flip point by precarity (Johnson-Neyman style)
Fig 5  Limit-architecture cell means (Study 3A)
Fig 6  Sufficiency-washing interaction (Study 3C)
Fig 7  Power curves (Study 1C)
Fig 8  Market regimes over time (Study 4A)
Fig 9  Tipping surface / phase diagram in (lambda, r) space by policy (Study 4B)
Fig 10 lambda* frontier and the policy-for-culture substitution (Study 4B)
Fig 11 Inequality raises the contagion threshold (Study 4D, P20)
Fig 12 Reconfiguration sweep and the disconfirmation of the credibility-viability tradeoff
"""
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from config import FIG_DIR
from dgp import (cs_stringency_profile, flip_point, route_a_gain, route_b_cost)

plt.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 150, "font.size": 9,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlesize": 10, "axes.labelsize": 9, "legend.fontsize": 8,
    "figure.constrained_layout.use": True,
})

C_A = "#1b6ca8"      # Route A (autonomy-identity)
C_B = "#c0392b"      # Route B (deprivation-reactance)
C_N = "#2d3436"      # net
C_P = "#16a085"      # policy / macro


# ======================================================================================
def fig1_conceptual_model():
    fig, ax = plt.subplots(figsize=(12.5, 7.0))
    ax.axis("off")
    ax.set_xlim(0, 100); ax.set_ylim(0, 70)

    def box(x, y, w, h, text, fc, ec, fs=8, weight="normal"):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.0",
                                    fc=fc, ec=ec, lw=1.2))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, weight=weight)

    def arrow(p1, p2, color=C_N, style="-", lw=1.15, label=None, lx=0.5, dy=1.3,
              rad=0.0):
        ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=11,
                                     color=color, lw=lw, linestyle=style,
                                     shrinkA=2, shrinkB=3,
                                     connectionstyle=f"arc3,rad={rad}"))
        if label:
            x = p1[0] + lx * (p2[0] - p1[0]); y = p1[1] + lx * (p2[1] - p1[1])
            ax.text(x, y + dy, label, ha="center", fontsize=7.2, color=color,
                    style="italic",
                    bbox=dict(fc="white", ec="none", alpha=0.85, pad=0.6))

    # ---------------- antecedents ----------------
    box(1, 42, 19, 20, "LIMIT ARCHITECTURE\n\nAgency: chosen / imposed\nLocus: collective / individual\n"
                       "Frame: sufficiency / reduction\nStringency: $S$", "#eaf2f8", C_A, 8, "bold")
    box(1, 10, 19, 16, "DEMARKETING ACT\n\nIntensity\nSacrifice signal\nBusiness-model\nreconfiguration",
        "#fdf2e9", "#d35400", 8, "bold")

    # ---------------- Route A ----------------
    box(26, 54, 16, 8, "Perceived\nautonomy", "#eaf2f8", C_A)
    box(26, 42, 16, 8, "Collective\nefficacy", "#eaf2f8", C_A)
    box(48, 54, 16, 8, "Restraint identity\naffirmation", "#eaf2f8", C_A)
    box(48, 42, 16, 8, "Restraint\nsignaling value", "#eaf2f8", C_A)
    # ---------------- Route B ----------------
    box(26, 22, 16, 8, "Anticipated\ndeprivation", "#fdedec", C_B)
    box(48, 22, 16, 8, "Psychological\nreactance", "#fdedec", C_B)

    # ---------------- focal ----------------
    box(70, 36, 15, 12, "CHOSEN\nSUFFICIENCY", "#f4f6f7", C_N, 10, "bold")

    # ---------------- outcomes ----------------
    box(88, 56, 11.5, 8, "Sufficiency\ncommitment\nbehavior", "#eafaf1", C_P, 7.5)
    box(88, 45, 11.5, 8, "Brand\nsufficiency\nequity", "#eafaf1", C_P, 7.5)
    box(88, 34, 11.5, 8, "Sufficiency\npolicy\nsupport", "#eafaf1", C_P, 7.5)
    box(88, 23, 11.5, 8, "Compensatory\ndisplacement", "#fdedec", C_B, 7.5)

    # ---------------- Route A arrows ----------------
    arrow((20, 56), (26, 58), C_A, label="H1 +")
    arrow((20, 50), (26, 46), C_A, label="H2 +")
    arrow((42, 58), (48, 58), C_A, label="H4 +")
    arrow((34, 54), (34, 50), C_A, style=":", lw=0.9)          # PA -> CE covariance
    arrow((42, 48), (48, 55), C_A)                              # CE -> RIA
    arrow((57, 54), (57, 50), C_A, label="H5 +", lx=0.5, dy=-2.0)
    arrow((64, 57), (70, 46), C_A)
    arrow((64, 45), (70, 43), C_A, label="H4 +")
    arrow((42, 43), (70, 40), C_A, rad=-0.10)

    # ---------------- Route B arrows ----------------
    arrow((20, 46), (26, 28), C_B, label="H3/H9 +", lx=0.35)
    arrow((42, 26), (48, 26), C_B, label="H10 +")
    arrow((64, 26), (70, 37), C_B, label="H6 \u2212", lx=0.6)
    arrow((34, 22), (71, 36.5), C_B, style=":", rad=0.12)

    # ---------------- firm side ----------------
    arrow((20, 20), (28, 22), "#d35400")
    ax.add_patch(FancyArrowPatch((20, 14), (93.7, 45), arrowstyle="-|>", mutation_scale=11,
                                 color="#d35400", lw=1.15, linestyle=":",
                                 connectionstyle="arc3,rad=0.22", shrinkA=2, shrinkB=3))
    ax.text(56, 9.0, "H13: demarketing intensity \u00d7 sacrifice signal", fontsize=7.4,
            color="#d35400", style="italic", ha="center",
            bbox=dict(fc="white", ec="none", alpha=0.85, pad=0.6))

    # ---------------- outcome arrows ----------------
    arrow((85, 45), (88, 59), C_P, label="H11 +", lx=0.55, dy=0.8)
    arrow((85, 43), (88, 49), C_P)
    arrow((85, 41), (88, 38), C_P, label="H14 +", lx=0.55, dy=0.8)
    arrow((85, 38), (88, 28), C_B, label="H12 \u2212", lx=0.6, dy=0.8)

    # ---------------- annotations ----------------
    ax.text(50, 67.2, "MODERATORS    economic precarity (M2)  \u00b7  cultural collectivism (M1)  \u00b7  "
                      "category symbolic intensity (M3)  \u00b7  community embeddedness (M4)  \u00b7  "
                      "growth-paradigm endorsement (M5)",
            ha="center", fontsize=7.6, style="italic", color="#555")
    ax.text(45, 34.5, "ROUTE A  (autonomy\u2013identity: sovereignty-expanding)", color=C_A,
            fontsize=8.6, ha="center", weight="bold")
    ax.text(45, 17.5, "ROUTE B  (deprivation\u2013reactance: sovereignty-contracting)", color=C_B,
            fontsize=8.6, ha="center", weight="bold")
    ax.text(50, 1.0, "Chosen sufficiency is the NET RESULTANT of two competing appraisal routes. "
                     "Because Route A saturates in stringency while Route B accelerates,\nthe net "
                     "effect is inverted-U with a flip point $S^*$ that falls as economic precarity "
                     "rises.", fontsize=8.2, ha="center", style="italic")
    ax.set_title("Figure 1. The Sufficiency\u2013Sovereignty Model: a dual-route account of "
                 "consumption under limits", fontsize=11.5, weight="bold")
    fig.savefig(f"{FIG_DIR}/fig1_conceptual_model.png", bbox_inches="tight")
    plt.close(fig)


def _fig1_old():
    fig, ax = plt.subplots(figsize=(11, 6.2))
    ax.axis("off")
    ax.set_xlim(0, 100); ax.set_ylim(0, 62)

    def box(x, y, w, h, text, fc, ec, fs=8, weight="normal"):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5,rounding_size=1.2",
                                    fc=fc, ec=ec, lw=1.2))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
                weight=weight, wrap=True)

    def arrow(x1, y1, x2, y2, color=C_N, style="-", lw=1.1, label=None, sign=""):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                     mutation_scale=11, color=color, lw=lw,
                                     linestyle=style, shrinkA=1, shrinkB=1))
        if label:
            ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 1.1, f"{label}{sign}", ha="center",
                    fontsize=7, color=color, style="italic")

    # antecedents
    box(1, 36, 17, 20, "LIMIT ARCHITECTURE\n\nAgency: chosen / imposed\nLocus: collective / individual\n"
                       "Frame: sufficiency / reduction\nStringency: S", "#eaf2f8", C_A, 8, "bold")
    box(1, 12, 17, 18, "DEMARKETING ACT\n\nIntensity\nSacrifice signal\nBusiness-model\nreconfiguration",
        "#fdf2e9", "#d35400", 8, "bold")

    # Route A
    box(24, 47, 15, 8, "Perceived\nautonomy", "#eaf2f8", C_A)
    box(24, 36, 15, 8, "Collective\nefficacy", "#eaf2f8", C_A)
    box(43, 47, 15, 8, "Restraint identity\naffirmation", "#eaf2f8", C_A)
    box(43, 36, 15, 8, "Restraint\nsignaling value", "#eaf2f8", C_A)
    # Route B
    box(24, 20, 15, 8, "Anticipated\ndeprivation", "#fdedec", C_B)
    box(43, 20, 15, 8, "Psychological\nreactance", "#fdedec", C_B)

    # focal
    box(62, 32, 16, 12, "CHOSEN\nSUFFICIENCY", "#f4f6f7", C_N, 10, "bold")

    # outcomes
    box(82, 48, 17, 8, "Sufficiency\ncommitment behavior", "#eafaf1", C_P)
    box(82, 37, 17, 8, "Brand sufficiency\nequity", "#eafaf1", C_P)
    box(82, 26, 17, 8, "Sufficiency\npolicy support", "#eafaf1", C_P)
    box(82, 15, 17, 8, "Compensatory\ndisplacement", "#fdedec", C_B)

    # arrows Route A
    arrow(18, 50, 24, 51, C_A, label="H1", sign=" +")
    arrow(18, 44, 24, 40, C_A, label="H2", sign=" +")
    arrow(39, 51, 43, 51, C_A, label="H4", sign=" +")
    arrow(39, 40, 43, 44, C_A)
    arrow(50, 47, 50, 44, C_A, label="H5", sign=" +")
    arrow(58, 49, 62, 42, C_A, sign="")
    arrow(58, 39, 62, 38, C_A, label="H4", sign=" +")
    arrow(39, 37, 62, 35, C_A, label="", sign="")
    # arrows Route B
    arrow(18, 40, 24, 27, C_B, label="H3/H9", sign=" +")
    arrow(39, 24, 43, 24, C_B, label="H10", sign=" +")
    arrow(58, 24, 62, 33, C_B, label="H6", sign=" \u2212")
    arrow(30, 20, 64, 32, C_B, style=":", label="", sign="")
    # firm side
    arrow(18, 21, 26, 22, "#d35400", label="", sign="")
    arrow(18, 24, 82, 41, "#d35400", style=":", label="H13 (x sacrifice)", sign="")
    # outcomes
    arrow(78, 41, 82, 50, C_P, label="H11", sign=" +")
    arrow(78, 38, 82, 41, C_P)
    arrow(78, 36, 82, 30, C_P, label="H14", sign=" +")
    arrow(78, 33, 82, 19, C_B, label="H12", sign=" \u2212")

    # moderators
    ax.text(50, 58.5, "MODERATORS   precarity (M2)  \u00b7  collectivism (M1)  \u00b7  category symbolic "
                      "intensity (M3)  \u00b7  community embeddedness (M4)  \u00b7  growth-paradigm "
                      "endorsement (M5)",
            ha="center", fontsize=7.5, style="italic", color="#555")
    ax.text(31, 58.5 - 26, "", ha="center")
    ax.text(50, 8, "ROUTE A  (autonomy\u2013identity: sovereignty-expanding)", color=C_A,
            fontsize=8.5, ha="center", weight="bold")
    ax.text(50, 5, "ROUTE B  (deprivation\u2013reactance: sovereignty-contracting)", color=C_B,
            fontsize=8.5, ha="center", weight="bold")
    ax.text(50, 1.6, "Chosen sufficiency is the NET RESULTANT of two competing appraisal routes; "
                     "the flip point S* is where Route B overtakes Route A.",
            fontsize=8, ha="center", style="italic")
    ax.set_title("Figure 1. The Sufficiency\u2013Sovereignty Model: a dual-route account of "
                 "consumption under limits", fontsize=11, weight="bold")
    fig.savefig(f"{FIG_DIR}/fig1_conceptual_model.png", bbox_inches="tight")
    plt.close(fig)


# ======================================================================================
def fig2_flip_mechanism():
    S = np.linspace(0, 1, 400)
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.6))

    ax = axes[0]
    ax.plot(S, route_a_gain(S), color=C_A, lw=2, label="Route A gain: identity affirmation\n"
                                                       r"$\alpha(1-e^{-\theta S})$  (saturating)")
    ax.plot(S, route_b_cost(S, 0.0), color=C_B, lw=2,
            label="Route B cost: anticipated deprivation\n"
                  r"$b S + \beta S^2$  (accelerating)")
    ax.set_xlabel("Limit stringency $S$ (share of baseline throughput forgone)")
    ax.set_ylabel("Route activation")
    ax.set_title("(a) Why a flip point must exist")
    ax.legend(frameon=False, loc="upper left")

    ax = axes[1]
    for prec, ls, lab in [(-1.0, "--", "low precarity ($-1$ SD)"),
                          (0.0, "-", "mean precarity"),
                          (1.0, ":", "high precarity ($+1$ SD)")]:
        y = cs_stringency_profile(S, prec)
        ax.plot(S, y, color=C_N, ls=ls, lw=1.8, label=lab)
        s = flip_point(prec)
        ax.plot([s], [cs_stringency_profile(s, prec)], "o", color=C_B, ms=6)
        ax.annotate(f"$S^*$={s:.2f}", (s, cs_stringency_profile(s, prec)),
                    textcoords="offset points", xytext=(4, 6), fontsize=7.5, color=C_B)
    ax.axhline(0, color="#aaa", lw=0.7)
    ax.set_xlabel("Limit stringency $S$")
    ax.set_ylabel("Net effect on chosen sufficiency")
    ax.set_title("(b) The inverted-U and the shifting flip point")
    ax.legend(frameon=False, loc="lower left")
    fig.suptitle("Figure 2. The flip point: precarity moves the sufficiency optimum "
                 "($\\partial S^*/\\partial$ precarity $< 0$)", fontsize=10, weight="bold")
    fig.savefig(f"{FIG_DIR}/fig2_flip_mechanism.png", bbox_inches="tight")
    plt.close(fig)


# ======================================================================================
def fig3_dose_response(dose: pd.DataFrame, quad: dict, theory: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.6))

    ax = axes[0]
    ax.errorbar(dose["stringency"], dose["CS"], yerr=1.96 * dose["CS_se"], fmt="o-",
                color=C_N, capsize=3, lw=1.4, ms=5, label="observed cell means (\u00b195% CI)")
    xs = np.linspace(dose["stringency"].min(), dose["stringency"].max(), 200)
    intercept = dose["CS"].mean() - (quad["b_linear"] * dose["stringency"].mean()
                                    + quad["b_quadratic"] * (dose["stringency"] ** 2).mean())
    ax.plot(xs, intercept + quad["b_linear"] * xs + quad["b_quadratic"] * xs ** 2,
            color=C_A, lw=1.6, label="fitted quadratic")
    ax.axvline(quad["peak_boot_median"], color=C_B, ls="--", lw=1.2)
    ax.axvspan(quad["peak_ci_lo"], quad["peak_ci_hi"], color=C_B, alpha=0.12)
    ax.annotate(f"$\\hat S^*$ = {quad['peak_boot_median']:.2f}\n"
                f"[{quad['peak_ci_lo']:.2f}, {quad['peak_ci_hi']:.2f}]",
                (quad["peak_boot_median"], dose["CS"].min()),
                textcoords="offset points", xytext=(6, 2), fontsize=7.5, color=C_B)
    ax.set_xlabel("Limit stringency (manipulated)")
    ax.set_ylabel("Chosen sufficiency (SD units)")
    ax.set_title("(a) Study 3B dose\u2013response")
    ax.legend(frameon=False, loc="lower left")

    ax = axes[1]
    ax.plot(dose["stringency"], dose["RIA"], "o-", color=C_A, lw=1.5, ms=4,
            label="Restraint identity affirmation (Route A)")
    ax.plot(dose["stringency"], dose["AD"], "s-", color=C_B, lw=1.5, ms=4,
            label="Anticipated deprivation (Route B)")
    ax.plot(dose["stringency"], dose["CS"], "^-", color=C_N, lw=1.8, ms=5,
            label="Chosen sufficiency (net)")
    ax.axhline(0, color="#aaa", lw=0.7)
    ax.set_xlabel("Limit stringency (manipulated)")
    ax.set_ylabel("Mediator / outcome (SD units)")
    ax.set_title("(b) The two routes move differently")
    ax.legend(frameon=False, loc="upper left")
    fig.suptitle("Figure 3. Route A saturates while Route B accelerates, producing an "
                 "inverted-U in chosen sufficiency", fontsize=10, weight="bold")
    fig.savefig(f"{FIG_DIR}/fig3_dose_response.png", bbox_inches="tight")
    plt.close(fig)


# ======================================================================================
def fig4_flip_by_precarity(by_prec: pd.DataFrame, jn: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.6))

    ax = axes[0]
    x = np.arange(len(by_prec))
    ax.errorbar(x, by_prec["peak_boot_median"],
                yerr=[by_prec["peak_boot_median"] - by_prec["peak_ci_lo"],
                      by_prec["peak_ci_hi"] - by_prec["peak_boot_median"]],
                fmt="o", color=C_N, capsize=4, ms=6, label="estimated $S^*$ (95% CI)")
    ax.plot(x, by_prec["analytic_flip_point"], "D--", color=C_A, ms=5,
            label="analytic $S^*$ implied by theory")
    ax.set_xticks(x)
    ax.set_xticklabels([f"{t}\n(z={m:+.2f})" for t, m in
                        zip(by_prec["precarity_tercile"], by_prec["mean_precarity"])])
    ax.set_xlabel("Economic precarity tercile")
    ax.set_ylabel("Flip point $S^*$")
    ax.set_title("(a) The precarious flip earlier")
    ax.legend(frameon=False)

    ax = axes[1]
    ax.plot(jn["mod_value"], jn["effect"], color=C_N, lw=1.8)
    ax.fill_between(jn["mod_value"], jn["effect"] - 1.96 * jn["se"],
                    jn["effect"] + 1.96 * jn["se"], color=C_N, alpha=0.15)
    ax.axhline(0, color="#aaa", lw=0.8)
    for b in jn.attrs.get("jn_boundaries", []):
        if jn["mod_value"].min() <= b <= jn["mod_value"].max():
            ax.axvline(b, color=C_B, ls="--", lw=1.1)
            ax.annotate(f"JN = {b:.2f}", (b, ax.get_ylim()[1] * 0.75),
                        textcoords="offset points", xytext=(4, 0), fontsize=7.5, color=C_B)
    ax.set_xlabel("Economic precarity (z)")
    ax.set_ylabel("Conditional effect of stringency on\nchosen sufficiency")
    ax.set_title("(b) Johnson\u2013Neyman region of significance")
    fig.suptitle("Figure 4. Precarity is the binding boundary condition on chosen sufficiency",
                 fontsize=10, weight="bold")
    fig.savefig(f"{FIG_DIR}/fig4_flip_by_precarity.png", bbox_inches="tight")
    plt.close(fig)


# ======================================================================================
def fig5_architecture_cells(cells: pd.DataFrame, marg: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.6))

    ax = axes[0]
    lab, val, err = [], [], []
    for _, r in cells.sort_values("CS_mean").iterrows():
        lab.append(f"{'chosen' if r['agency'] else 'imposed'}/"
                   f"{'coll' if r['locus'] else 'indiv'}/"
                   f"{'suff' if r['frame'] else 'reduc'}")
        val.append(r["CS_mean"]); err.append(1.96 * r["CS_se"])
    colors = [C_B if v < 0 else C_A for v in val]
    ax.barh(lab, val, xerr=err, color=colors, alpha=0.85, capsize=3)
    ax.axvline(0, color="#666", lw=0.8)
    ax.set_xlabel("Chosen sufficiency (SD units)")
    ax.set_title("(a) All eight limit architectures")

    ax = axes[1]
    piv = marg.pivot(index="factor", columns="dv", values="cohens_d")
    piv = piv.reindex(["agency", "locus", "frame"])
    w = 0.26
    x = np.arange(len(piv))
    for i, (dv, c, lb) in enumerate([("PA_c", C_A, "Perceived autonomy"),
                                     ("AD_c", C_B, "Anticipated deprivation"),
                                     ("CS_c", C_N, "Chosen sufficiency")]):
        ax.bar(x + (i - 1) * w, piv[dv], w, color=c, alpha=0.85, label=lb)
    ax.axhline(0, color="#666", lw=0.8)
    ax.set_xticks(x); ax.set_xticklabels(["agency", "locus", "frame"])
    ax.set_ylabel("Cohen's $d$")
    ax.set_xlabel("Limit-architecture dimension")
    ax.set_title("(b) Each lever works through a different route")
    ax.legend(frameon=False)
    fig.suptitle("Figure 5. Limit architecture is a designable space with route-specific levers",
                 fontsize=10, weight="bold")
    fig.savefig(f"{FIG_DIR}/fig5_architecture_cells.png", bbox_inches="tight")
    plt.close(fig)


# ======================================================================================
def fig6_sufficiency_washing(cells: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    for sac, c, lab in [(0, C_B, "low sacrifice signal"), (1, C_A, "high sacrifice signal")]:
        g = cells[cells["sacrifice_hi"] == sac].sort_values("intensity_hi")
        ax.errorbar([0, 1], g["BSE"], yerr=1.96 * g["se"], fmt="o-", color=c,
                    capsize=4, lw=1.8, ms=6, label=lab)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["low", "high"])
    ax.set_xlabel("Demarketing intensity")
    ax.set_ylabel("Brand sufficiency equity (SD units)")
    ax.axhline(0, color="#aaa", lw=0.7)
    ax.legend(frameon=False)
    ax.set_title("Figure 6. Demarketing builds brand equity only when it is\n"
                 "visibly costly: the sufficiency-washing penalty", fontsize=9.5, weight="bold")
    fig.savefig(f"{FIG_DIR}/fig6_sufficiency_washing.png", bbox_inches="tight")
    plt.close(fig)


# ======================================================================================
def fig7_power(recovery: pd.DataFrame, paths: list[str] | None = None):
    paths = paths or ["PA<-agency", "RIA<-PA", "CS<-RIA", "CS<-PR",
                      "CS<-stringency2", "AD<-stringency:precarity",
                      "SCB<-CS:community", "BSE<-int:sac", "SPS<-CS:growth_endorse"]
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    cmap = plt.get_cmap("tab10")
    for i, p in enumerate(paths):
        g = recovery[recovery["path"] == p].sort_values("N")
        if len(g):
            ax.plot(g["N"], g["power"], "o-", ms=4, lw=1.4, color=cmap(i % 10), label=p)
    ax.axhline(0.80, color=C_B, ls="--", lw=1.2)
    ax.text(recovery["N"].max(), 0.815, "80% power", ha="right", fontsize=7.5, color=C_B)
    ax.set_xlabel("Sample size $N$")
    ax.set_ylabel("Directional power (p < .05, correct sign)")
    ax.set_ylim(0, 1.02)
    ax.legend(frameon=False, fontsize=7, ncol=1, loc="lower right")
    ax.set_title("Figure 7. Power curves for focal paths: a design specification\n"
                 "for the confirmatory field study", fontsize=9.5, weight="bold")
    fig.savefig(f"{FIG_DIR}/fig7_power_curves.png", bbox_inches="tight")
    plt.close(fig)


# ======================================================================================
def fig8_regimes(series: dict[str, pd.DataFrame]):
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.4))
    cmap = {"futility": "#7f8c8d", "collapse": "#c0392b", "niche": "#f39c12",
            "tipping": "#16a085", "backlash": "#8e44ad"}
    for name, df in series.items():
        c = cmap.get(name, "#333")
        axes[0].plot(df["t"], df["Q_total"] / df["Q_total"].iloc[0], color=c, lw=1.6, label=name)
        axes[1].plot(df["t"], df["cs_mean"], color=c, lw=1.6, label=name)
        axes[2].plot(df["t"], df["prop_rate"], color=c, lw=1.6, label=name)
    axes[0].set_ylabel("Category throughput (indexed to $t_0$)")
    axes[0].set_title("(a) Aggregate throughput")
    axes[1].set_ylabel("Mean chosen sufficiency")
    axes[1].set_title("(b) Consumer sufficiency")
    axes[2].set_ylabel("Share of supply practising demarketing")
    axes[2].set_title("(c) Demarketing propagation")
    for ax in axes:
        ax.set_xlabel("Period")
    axes[0].legend(frameon=False, fontsize=7.5)
    fig.suptitle("Figure 8. Five market-system regimes generated by the same model",
                 fontsize=10, weight="bold")
    fig.savefig(f"{FIG_DIR}/fig8_regimes.png", bbox_inches="tight")
    plt.close(fig)


# ======================================================================================
def fig9_phase_diagram(surface: pd.DataFrame):
    pols = sorted(surface["policy"].unique())
    fig, axes = plt.subplots(1, len(pols), figsize=(3.6 * len(pols), 3.5), squeeze=False)
    order = ["backlash", "collapse", "futility", "strained", "niche", "tipping"]
    colors = ["#8e44ad", "#c0392b", "#bdc3c7", "#f39c12", "#f1c40f", "#16a085"]
    cmapd = dict(zip(order, colors))
    for k, pol in enumerate(pols):
        ax = axes[0][k]
        g = surface[surface["policy"] == pol]
        piv = g.pivot(index="r_demarketer", columns="lambda_social", values="regime")
        num = piv.apply(lambda col: col.map(lambda v: order.index(v) if v in order else np.nan))
        ax.imshow(num.to_numpy(), origin="lower", aspect="auto", cmap=
                  matplotlib.colors.ListedColormap(colors), vmin=-0.5, vmax=len(order) - 0.5,
                  extent=[g["lambda_social"].min(), g["lambda_social"].max(),
                          g["r_demarketer"].min(), g["r_demarketer"].max()])
        ax.set_xlabel("Social multiplier on sufficiency  $\\lambda$")
        if k == 0:
            ax.set_ylabel("Business-model reconfiguration  $r$")
        ax.set_title(f"policy intensity = {pol:g}")
    handles = [plt.Line2D([0], [0], marker="s", ls="", color=cmapd[o], label=o) for o in order]
    fig.legend(handles=handles, frameon=False, ncol=6, loc="lower center", fontsize=8,
               bbox_to_anchor=(0.5, -0.10))
    fig.suptitle("Figure 9. Phase diagram of market-system regimes: institutional scaffolding "
                 "enlarges the viable region", fontsize=10, weight="bold")
    fig.savefig(f"{FIG_DIR}/fig9_phase_diagram.png", bbox_inches="tight")
    plt.close(fig)


# ======================================================================================
def fig10_lambda_star(lstar: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(5.6, 3.8))
    for pol, c, m in zip(sorted(lstar["policy"].unique()),
                         ["#c0392b", "#f39c12", "#16a085"], ["o", "s", "^"]):
        g = lstar[lstar["policy"] == pol].sort_values("r_demarketer")
        ax.plot(g["r_demarketer"], g["lambda_star"], marker=m, color=c, lw=1.6,
                label=f"policy = {pol:g}")
    ax.set_xlabel("Business-model reconfiguration  $r$")
    ax.set_ylabel("$\\lambda^*$  (minimum social multiplier\nfor post-growth market viability)")
    ax.set_title("Figure 10. $\\lambda^*(r)$: reconfiguration and institutions are\n"
                 "substitutes for cultural change \u2014 gaps mean viability is unattainable",
                 fontsize=9.5, weight="bold")
    ax.legend(frameon=False)
    fig.savefig(f"{FIG_DIR}/fig10_lambda_star.png", bbox_inches="tight")
    plt.close(fig)


# ======================================================================================
def fig11_inequality(ineq: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.6))
    xhi = float(ineq["precarity_mean"].max())

    ax = axes[0]
    # the region in which no feasible lambda attains viability
    attainable = ineq[ineq["lambda_star"].notna()]["precarity_mean"]
    cut = (attainable.max() + ineq[ineq["lambda_star"].isna()]["precarity_mean"].min()) / 2
    ax.axvspan(cut, xhi + 0.2, color="#c0392b", alpha=0.10, lw=0)
    for sd, c, m, ls in zip(sorted(ineq["precarity_sd"].unique()),
                            ["#1b6ca8", "#f39c12", "#c0392b"], ["o", "s", "^"],
                            ["-", "--", ":"]):
        g = ineq[ineq["precarity_sd"] == sd].sort_values("precarity_mean")
        ax.plot(g["precarity_mean"], g["lambda_star"], marker=m, color=c, lw=1.6, ls=ls,
                ms=6, mfc="none" if sd != 0.6 else None, label=f"precarity SD = {sd:g}")
    ax.set_xlim(-0.15, xhi + 0.2)
    ax.set_xlabel("Mean economic precarity (z)")
    ax.set_ylabel("$\\lambda^*$ required for viability")
    ax.set_title("(a) Precarity raises the contagion threshold")
    ax.legend(frameon=False, loc="upper left", fontsize=7.5)
    ymid = sum(ax.get_ylim()) / 2
    ax.annotate("no $\\lambda$ attains\nviability", ((cut + xhi + 0.2) / 2, ymid),
                fontsize=8, color="#c0392b", ha="center", va="center", weight="bold")
    ax.annotate("the three dispersion levels coincide:\nat these means it is the LEVEL of precarity,\n"
                "not its spread, that sets $\\lambda^*$",
                (0.30, 0.05), xycoords="axes fraction", fontsize=6.8, color="#555",
                style="italic", va="bottom")

    ax = axes[1]
    for sd, c, m, ls in zip(sorted(ineq["precarity_sd"].unique()),
                            ["#1b6ca8", "#f39c12", "#c0392b"], ["o", "s", "^"],
                            ["-", "--", ":"]):
        g = ineq[ineq["precarity_sd"] == sd].sort_values("precarity_mean")
        ax.plot(g["precarity_mean"], g["share_below_flip_point"], marker=m, color=c, lw=1.6,
                ls=ls, ms=6, label=f"precarity SD = {sd:g}")
    ax.set_xlim(-0.15, xhi + 0.2)
    ax.set_xlabel("Mean economic precarity (z)")
    ax.set_ylabel("Share of consumers past their flip point")
    ax.set_title("(b) The micro mechanism behind it")
    ax.legend(frameon=False, fontsize=7.5)
    ax.annotate("dispersion does bind here: at a mean of 0,\nspread raises the share past the "
                "flip point\nfrom .000 to .062",
                (0.03, 0.72), xycoords="axes fraction", fontsize=6.8, color="#555",
                style="italic")
    fig.suptitle("Figure 11. Distributive justice is a precondition of sufficiency policy, "
                 "not a parallel concern (P20)", fontsize=10, weight="bold")
    fig.savefig(f"{FIG_DIR}/fig11_inequality.png", bbox_inches="tight")
    plt.close(fig)


# ======================================================================================
def fig12_reconfiguration(cvt: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.5))
    ax = axes[0]
    for phi, c in zip(sorted(cvt["phi_credibility_erosion"].unique()),
                      ["#1b6ca8", "#16a085", "#f39c12", "#c0392b"]):
        g = cvt[cvt["phi_credibility_erosion"] == phi].sort_values("r_demarketer")
        ax.plot(g["r_demarketer"], g["throughput_reduction"], color=c, lw=1.6,
                label=f"$\\phi$ = {phi:g}")
    ax.set_xlabel("Business-model reconfiguration  $r$")
    ax.set_ylabel("Throughput reduction")
    ax.set_title("(a) No interior optimum at any $\\phi$")
    ax.legend(frameon=False, title="credibility erosion", title_fontsize=7.5)

    ax = axes[1]
    g = cvt[cvt["phi_credibility_erosion"] == 0.4].sort_values("r_demarketer")
    ax.plot(g["r_demarketer"], g["relative_profit_demarketers"], color=C_A, lw=1.8,
            label="demarketer profit\n(relative to business as usual)")
    ax.axhline(1.0, color="#666", ls="--", lw=1.0)
    ax2 = ax.twinx()
    ax2.plot(g["r_demarketer"], g["throughput_reduction"], color=C_B, lw=1.8, ls="--",
             label="throughput reduction")
    ax2.set_ylabel("Throughput reduction", color=C_B)
    ax.set_xlabel("Business-model reconfiguration  $r$")
    ax.set_ylabel("Relative profit", color=C_A)
    ax.set_title("(b) Viability and reduction rise together")
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, frameon=False, loc="upper left", fontsize=7.5)
    fig.suptitle("Figure 12. A conjecture the model rejects: decoupling revenue from volume "
                 "does not undermine sufficiency credibility enough to matter",
                 fontsize=10, weight="bold")
    fig.savefig(f"{FIG_DIR}/fig12_reconfiguration.png", bbox_inches="tight")
    plt.close(fig)


# ======================================================================================
def make_all(res: dict):
    print("[figures] rendering ...")
    fig1_conceptual_model()
    fig2_flip_mechanism()
    if "s3" in res:
        fig3_dose_response(res["s3"]["s3b"]["dose"], res["s3"]["s3b"]["quadratic"],
                           res["s3"]["s3b"]["theory_curve"])
        fig4_flip_by_precarity(res["s3"]["s3b"]["by_precarity"], res["s2mm"]["jn"])
        fig5_architecture_cells(res["s3"]["s3a"]["cells"], res["s3"]["s3a"]["marginals"])
        fig6_sufficiency_washing(res["s3"]["s3c"]["cells"])
    if "s1" in res:
        fig7_power(res["s1"]["recovery"])
    if "s4" in res:
        fig8_regimes(res["s4"]["series"])
        fig9_phase_diagram(res["s4"]["surface"])
        fig10_lambda_star(res["s4"]["lambda_star"])
        fig11_inequality(res["s4"]["inequality"])
        fig12_reconfiguration(res["s4"]["credibility_viability"])
    print(f"[figures] written to {FIG_DIR}")
