"""Figure 9: integrated framework synthesising structural, mediated and configurational results."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon, Rectangle, FancyArrowPatch, FancyBboxPatch
from matplotlib.lines import Line2D

plt.rcParams.update({'font.family': 'DejaVu Sans'})

NAVY, RED, GREY, INK = '#2C3E50', '#C0392B', '#95A5A6', '#1C2833'
BLUE, BLUE_E = '#AED6F1', '#2E75B6'
GREEN, GREEN_E = '#A9DFBF', '#1E8449'
ORNG, ORNG_E = '#F5CBA7', '#E67E22'
PURP, PURP_E = '#D7BDE2', '#7D3C98'
YELL, YELL_E = '#EFD87A', '#B7950B'
PANEL_BG = '#FCFCFD'

# ---- values (change here if Table 6 is revised) ----------------------------
BETA = {('RP', 'TMC'): '0.44***', ('SP', 'TMC'): '0.29***', ('KSR', 'DI'): '0.61***',
        ('TMC', 'GSCI'): '0.38***', ('DI', 'GSCI'): '0.41***', ('CBI', 'GSCI'): '0.16 ns',
        ('GSCI', 'GLP'): '0.49***', ('TMC', 'GLP'): '0.27***'}
IND = {'RP': (0.177, True, 0.048, False), 'SP': (0.056, False, 0.038, False),
       'KSR': (0.040, False, 0.089, True), 'DI': (0.076, False, 0.166, True),
       'TMC': (0.098, True, 0.102, True), 'CBI': (0.071, False, 0.038, False)}
CONDS = ['GSCI', 'TMC', 'DI', 'CBI', 'RP']
RECIPES = [
    ('Dev C1', 'developing', {'GSCI': 'C', 'TMC': 'C', 'CBI': 'p'}, 0.864, 0.448),
    ('Dev C2', 'developing', {'GSCI': 'C', 'TMC': 'C', 'DI': 'p'}, 0.867, 0.472),
    ('Dev C3', 'developing', {'TMC': 'C', 'CBI': 'A', 'RP': 'C'}, 0.871, 0.468),
    ('Eme C1', 'emerging', {'GSCI': 'C', 'TMC': 'C', 'DI': 'p'}, 0.832, 0.542),
    ('Eme C2', 'emerging', {'GSCI': 'C', 'TMC': 'C', 'RP': 'p'}, 0.850, 0.481),
]
NAME = {'RP': 'Regulatory &\nPolicy Pressure', 'SP': 'Stakeholder &\nCustomer Pressure',
        'KSR': 'Knowledge &\nSkill Readiness', 'TMC': 'Top Management\nCommitment',
        'DI': 'Digital Infra.\nReadiness', 'CBI': 'Perceived Economic\nFeasibility',
        'GSCI': 'Green Supply\nChain Integration', 'GLP': 'Green Logistics\nPerformance'}
FAM = {'RP': (BLUE, BLUE_E), 'SP': (BLUE, BLUE_E), 'KSR': (GREEN, GREEN_E),
       'DI': (GREEN, GREEN_E), 'CBI': (GREEN, GREEN_E), 'TMC': (ORNG, ORNG_E),
       'GSCI': (PURP, PURP_E)}

fig = plt.figure(figsize=(16.4, 11.2))
fig.patch.set_facecolor('white')


def panel(rect, title, sub=None):
    ax = fig.add_axes(rect)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color('#B9C2C9'); s.set_linewidth(1.1)
    ax.set_facecolor(PANEL_BG)
    ax.add_patch(Rectangle((0, 0.918), 1, 0.082, transform=ax.transAxes,
                           facecolor=NAVY, edgecolor='none', zorder=6))
    ax.text(0.014, 0.959, title, transform=ax.transAxes, color='white',
            fontsize=13.5, fontweight='bold', va='center', zorder=7)
    if sub:
        ax.text(0.986, 0.959, sub, transform=ax.transAxes, color='#D6DBDF',
                fontsize=10, va='center', ha='right', zorder=7, style='italic')
    return ax


def node(ax, code, x, y, w=0.148, h=0.115, big=False):
    f, e = FAM[code]
    ax.add_patch(Ellipse((x, y), w, h, facecolor=f, edgecolor=e,
                         lw=2.6 if big else 2.0, zorder=4))
    ax.text(x, y + 0.021, code, ha='center', va='center', fontsize=12.5,
            fontweight='bold', zorder=5)
    ax.text(x, y - 0.028, NAME[code], ha='center', va='center', fontsize=7.4,
            linespacing=1.3, zorder=5)
    return (x, y, w, h)


def hexnode(ax, x, y, w=0.175, h=0.145):
    k = w * 0.20
    pts = [(x - w/2, y), (x - w/2 + k, y + h/2), (x + w/2 - k, y + h/2),
           (x + w/2, y), (x + w/2 - k, y - h/2), (x - w/2 + k, y - h/2)]
    ax.add_patch(Polygon(pts, closed=True, facecolor=YELL, edgecolor=YELL_E,
                         lw=2.8, zorder=4))
    ax.text(x, y + 0.026, 'GLP', ha='center', va='center', fontsize=13.5,
            fontweight='bold', zorder=5)
    ax.text(x, y - 0.030, NAME['GLP'], ha='center', va='center', fontsize=7.6,
            linespacing=1.3, zorder=5)
    return (x, y, w, h)


def arrow(ax, a, b, label=None, ns=False, rad=0.0, lo=0.5, dx=0.0, dy=0.0, fs=9.4):
    ax1, ay1, aw1, ah1 = a
    bx, by, bw, bh = b
    import math
    ang = math.atan2(by - ay1, bx - ax1)
    p0 = (ax1 + (aw1 / 2) * math.cos(ang) * 0.98, ay1 + (ah1 / 2) * math.sin(ang) * 0.98)
    p1 = (bx - (bw / 2) * math.cos(ang) * 0.99, by - (bh / 2) * math.sin(ang) * 0.99)
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle='-|>', mutation_scale=18,
                                 lw=1.7 if not ns else 1.5,
                                 color=GREY if ns else RED,
                                 ls=(0, (5, 3)) if ns else 'solid',
                                 connectionstyle=f'arc3,rad={rad}',
                                 shrinkA=0, shrinkB=1, zorder=3))
    if label:
        mx = p0[0] + (p1[0] - p0[0]) * lo + dx
        my = p0[1] + (p1[1] - p0[1]) * lo + dy - rad * 0.16
        ax.text(mx, my, label, ha='center', va='center', fontsize=fs,
                fontweight='bold' if not ns else 'normal',
                color=INK if not ns else '#707B7C', zorder=6,
                bbox=dict(boxstyle='round,pad=0.22', facecolor='white',
                          edgecolor='none', alpha=0.94))


# ============================ PANEL A =====================================
axA = panel([0.028, 0.455, 0.944, 0.485], 'A   Estimated sequential mechanism',
            'pooled sample, n = 220 · standardised path coefficients')

rp = node(axA, 'RP', 0.105, 0.775)
sp = node(axA, 'SP', 0.105, 0.575)
ksr = node(axA, 'KSR', 0.105, 0.285)
tmc = node(axA, 'TMC', 0.345, 0.675, big=True)
di = node(axA, 'DI', 0.345, 0.285)
cbi = node(axA, 'CBI', 0.345, 0.095)
gsci = node(axA, 'GSCI', 0.605, 0.420, big=True)
glp = hexnode(axA, 0.855, 0.545)

arrow(axA, rp, tmc, BETA[('RP', 'TMC')], lo=0.52, dy=0.030)
arrow(axA, sp, tmc, BETA[('SP', 'TMC')], lo=0.52, dy=-0.030)
arrow(axA, ksr, di, BETA[('KSR', 'DI')], lo=0.5, dy=0.032)
arrow(axA, tmc, gsci, BETA[('TMC', 'GSCI')], lo=0.5, dy=0.030)
arrow(axA, di, gsci, BETA[('DI', 'GSCI')], lo=0.5, dy=-0.032)
arrow(axA, cbi, gsci, BETA[('CBI', 'GSCI')], ns=True, lo=0.5, dy=-0.028)
arrow(axA, gsci, glp, BETA[('GSCI', 'GLP')], lo=0.5, dy=0.030)
arrow(axA, tmc, glp, BETA[('TMC', 'GLP')], rad=-0.30, lo=0.5, dy=0.075)

# group-difference badges
for (bx, by, txt) in [(0.222, 0.845, 'Dev > Eme'), (0.424, 0.404, 'Eme > Dev')]:
    axA.add_patch(FancyBboxPatch((bx - 0.055, by - 0.026), 0.110, 0.052,
                                 boxstyle='round,pad=0.008', facecolor='#FDEBD0',
                                 edgecolor='#CA6F1E', lw=1.3, zorder=7))
    axA.text(bx, by, '◆ ' + txt, ha='center', va='center', fontsize=8.6,
             fontweight='bold', color='#943126', zorder=8)

axA.add_patch(Rectangle((0.735, 0.055), 0.245, 0.115, facecolor='white',
                        edgecolor='#D5DBDB', lw=1.0, zorder=4))
axA.text(0.7575, 0.1375, 'Mediation form', fontsize=9.4, fontweight='bold',
         va='center', zorder=5)
axA.text(0.7575, 0.104, 'Full  ·  SP, KSR, DI, CBI', fontsize=8.6, va='center', zorder=5)
axA.text(0.7575, 0.076, 'Partial  ·  RP', fontsize=8.6, va='center', zorder=5)

# ============================ PANEL B =====================================
axB = panel([0.028, 0.055, 0.455, 0.365], 'B   Where each mediated chain operates',
            'total indirect effect on GLP')
axB.text(0.055, 0.845, 'Antecedent', fontsize=10, fontweight='bold')
axB.text(0.455, 0.845, 'Developing', fontsize=10, fontweight='bold', ha='center')
axB.text(0.700, 0.845, 'Emerging', fontsize=10, fontweight='bold', ha='center')
axB.text(0.905, 0.845, 'Pattern', fontsize=10, fontweight='bold', ha='center')
axB.plot([0.045, 0.965], [0.808, 0.808], color='#AEB6BF', lw=1.2)

ys = [0.735, 0.630, 0.525, 0.420, 0.315, 0.210]
for (code, y) in zip(['RP', 'SP', 'KSR', 'DI', 'TMC', 'CBI'], ys):
    dv, ds, ev, es = IND[code]
    f, e = FAM[code]
    axB.add_patch(Rectangle((0.048, y - 0.030), 0.022, 0.060, facecolor=f,
                            edgecolor=e, lw=1.2))
    axB.text(0.085, y, code, fontsize=10.5, fontweight='bold', va='center')
    for xc, v, s in [(0.455, dv, ds), (0.700, ev, es)]:
        axB.scatter(xc - 0.075, y, s=132 if s else 116,
                    c=RED if s else 'white', edgecolors=RED if s else '#AEB6BF',
                    linewidths=1.8, zorder=4)
        axB.text(xc + 0.030, y, f'{v:.3f}', fontsize=9.6, va='center', ha='center',
                 fontweight='bold' if s else 'normal',
                 color=INK if s else '#909497')
    pat = ('Developing only' if ds and not es else 'Emerging only' if es and not ds
           else 'Both contexts' if ds and es else 'Neither')
    axB.text(0.905, y, pat, fontsize=8.8, va='center', ha='center',
             color=INK if (ds or es) else '#909497',
             style='normal' if (ds or es) else 'italic')
axB.plot([0.045, 0.965], [0.165, 0.165], color='#D5DBDB', lw=1.0)
axB.text(0.5, 0.115, 'Filled marker denotes a significant indirect effect at p < 0.05',
         fontsize=8.8, ha='center', color='#5D6D7E')
axB.text(0.5, 0.062, 'The regulatory chain and the digital chain are context-exclusive',
         fontsize=9.2, ha='center', fontweight='bold', color='#943126')

# ============================ PANEL C =====================================
axC = panel([0.517, 0.055, 0.455, 0.365], 'C   Sufficient configurations',
            'fsQCA · intermediate solution')
x0 = 0.300
xs = [x0 + i * 0.118 for i in range(len(CONDS))]
for xc, c in zip(xs, CONDS):
    axC.text(xc, 0.845, c, fontsize=9.8, fontweight='bold', ha='center')
axC.text(0.075, 0.845, 'Recipe', fontsize=10, fontweight='bold')
axC.text(0.905, 0.845, 'Cons.', fontsize=9.8, fontweight='bold', ha='center')
axC.plot([0.045, 0.965], [0.808, 0.808], color='#AEB6BF', lw=1.2)

ry = [0.730, 0.632, 0.534, 0.398, 0.300]
for (lab, grp, spec, cons, cov), y in zip(RECIPES, ry):
    axC.text(0.075, y, lab, fontsize=10, fontweight='bold', va='center',
             color='#1A5276' if grp == 'developing' else '#7E5109')
    for xc, c in zip(xs, CONDS):
        st = spec.get(c)
        if st == 'C':
            axC.scatter(xc, y, s=170, c=INK, edgecolors=INK, zorder=4)
        elif st == 'p':
            axC.scatter(xc, y, s=66, c=INK, edgecolors=INK, zorder=4)
        elif st == 'A':
            axC.scatter(xc, y, s=170, facecolors='white', edgecolors=INK,
                        linewidths=2.0, zorder=4)
            axC.plot([xc], [y], marker='x', ms=7.5, mew=1.9, color=INK, zorder=5)
        else:
            axC.plot([xc], [y], marker='x', ms=5.5, mew=1.2, color='#CACFD2', zorder=3)
    axC.text(0.905, y, f'{cons:.3f}', fontsize=9.4, va='center', ha='center')
axC.plot([0.045, 0.965], [0.462, 0.462], color='#D5DBDB', lw=1.0, ls=(0, (4, 3)))
axC.text(0.5, 0.205, 'Integration and managerial commitment are core in four of five recipes',
         fontsize=8.9, ha='center', color='#5D6D7E')
axC.text(0.5, 0.148, 'Dev C1 needs cost easing · Dev C3 needs its absence, offset by regulation',
         fontsize=9.2, ha='center', fontweight='bold', color='#943126')
axC.text(0.5, 0.075, '● core present    • peripheral present    ⊗ core absent    × don\'t care',
         fontsize=9.0, ha='center', color=INK)

# ============================ header / footer =============================
fig.text(0.028, 0.975, 'An integrated framework of green logistics enablement '
                       'in developing and emerging economies',
         fontsize=17, fontweight='bold', color=NAVY, va='center')
fig.text(0.028, 0.950, 'Symmetric net effects, mediated chains and equifinal '
                       'configurations, estimated on the same sample',
         fontsize=10.5, color='#5D6D7E', va='center', style='italic')
fig.text(0.972, 0.017, 'Source: authors.', fontsize=9, ha='right', color='#7F8C8D')
fig.text(0.028, 0.017, 'Solid red arrows denote significant paths and grey dashed '
                       'arrows non-significant paths. ◆ marks a path differing '
                       'significantly between groups.',
         fontsize=9, color='#7F8C8D')

out = '/projects/sandbox/MetaV/Figure9_integrated_framework.png'
plt.savefig(out, dpi=190, facecolor='white')
print('written', out)
