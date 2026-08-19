"""Replacement for Figure 5: definitive structural results figure."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle, FancyArrowPatch
from matplotlib.lines import Line2D
import math

plt.rcParams.update({'font.family': 'DejaVu Sans'})
NAVY, RED, GREY, INK = '#2C3E50', '#B03A2E', '#A6ACAF', '#17202A'
ORNG_B, ORNG_F = '#CA6F1E', '#FDF2E3'
FAM = {'RP': ('#AED6F1', '#2E75B6'), 'SP': ('#AED6F1', '#2E75B6'),
       'KSR': ('#A9DFBF', '#1E8449'), 'DI': ('#A9DFBF', '#1E8449'),
       'CBI': ('#A9DFBF', '#1E8449'), 'TMC': ('#F5CBA7', '#E67E22'),
       'GSCI': ('#D7BDE2', '#7D3C98'), 'GLP': ('#EFD87A', '#B7950B')}
NAME = {'RP': 'Regulatory &\nPolicy Pressure', 'SP': 'Stakeholder &\nCustomer Pressure',
        'KSR': 'Knowledge &\nSkill Readiness', 'TMC': 'Top Management\nCommitment',
        'DI': 'Digital Infrastructure\nReadiness', 'CBI': 'Perceived Economic\nFeasibility',
        'GSCI': 'Green Supply Chain\nIntegration', 'GLP': 'Green Logistics\nPerformance'}
R2 = {'TMC': '0.41', 'DI': '0.37', 'GSCI': '0.57', 'GLP': '0.59'}
# hyp: (src, tgt, pooled, stars, dev, eme, diff, delta, p)
ROWS = [
    ('H1', 'RP', 'TMC', '0.44', '***', '0.52', '0.33', True, '0.19', '0.021'),
    ('H2', 'SP', 'TMC', '0.29', '***', '0.31', '0.27', False, '0.04', '0.612'),
    ('H3', 'TMC', 'GSCI', '0.38', '***', '0.34', '0.42', False, '-0.08', '0.288'),
    ('H4', 'DI', 'GSCI', '0.41', '***', '0.27', '0.54', True, '-0.27', '0.004'),
    ('H5', 'KSR', 'DI', '0.61', '***', '0.55', '0.66', False, '-0.11', '0.144'),
    ('H6', 'CBI', 'GSCI', '0.16', 'ns', '0.21', '0.12', False, '0.09', '0.331'),
    ('H7', 'GSCI', 'GLP', '0.49', '***', '0.46', '0.52', False, '-0.06', '0.402'),
    ('H8', 'TMC', 'GLP', '0.27', '***', '0.30', '0.24', False, '0.06', '0.466'),
]
E = {(r[1], r[2]): r for r in ROWS}
POS = {'RP': (0.070, 0.880), 'SP': (0.070, 0.600), 'KSR': (0.070, 0.200),
       'TMC': (0.355, 0.740), 'DI': (0.355, 0.300), 'CBI': (0.355, 0.100),
       'GSCI': (0.640, 0.440), 'GLP': (0.895, 0.700)}
NW, NH, GW, GH = 0.140, 0.160, 0.165, 0.185
LAB = {('RP', 'TMC'): (0.2125, 0.868), ('SP', 'TMC'): (0.2125, 0.612),
       ('KSR', 'DI'): (0.2125, 0.308), ('TMC', 'GSCI'): (0.4975, 0.645),
       ('DI', 'GSCI'): (0.4975, 0.312), ('CBI', 'GSCI'): (0.4975, 0.212),
       ('GSCI', 'GLP'): (0.745, 0.640), ('TMC', 'GLP'): (0.620, 0.800)}

fig = plt.figure(figsize=(15.8, 12.2))
axd = fig.add_axes([0.016, 0.345, 0.968, 0.575]); axd.set_xlim(0, 1); axd.set_ylim(0, 1); axd.axis('off')
axt = fig.add_axes([0.016, 0.022, 0.968, 0.300]); axt.set_xlim(0, 1); axt.set_ylim(0, 1); axt.axis('off')


def dims(c):
    return (GW, GH) if c == 'GLP' else (NW, NH)


def node(c):
    x, y = POS[c]; f, e = FAM[c]; endo = c in R2; w, h = dims(c)
    if c == 'GLP':
        k = w * 0.19
        axd.add_patch(Polygon([(x-w/2, y), (x-w/2+k, y+h/2), (x+w/2-k, y+h/2),
                               (x+w/2, y), (x+w/2-k, y-h/2), (x-w/2+k, y-h/2)],
                              closed=True, facecolor=f, edgecolor=e, lw=2.8, zorder=4))
    else:
        axd.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
                                     boxstyle='round,pad=0.004,rounding_size=0.022',
                                     facecolor=f, edgecolor=e,
                                     lw=2.5 if endo else 1.9, zorder=4))
    axd.text(x, y + 0.042, c, ha='center', va='center', fontsize=13,
             fontweight='bold', zorder=5)
    axd.text(x, y - 0.008, NAME[c], ha='center', va='center', fontsize=7.7,
             linespacing=1.30, zorder=5)
    if endo:
        axd.text(x, y - 0.058, f'$R^2$ = {R2[c]}', ha='center', va='center',
                 fontsize=9.0, style='italic', color='#515A5A', zorder=5)


def edge(c, ang):
    x, y = POS[c]; w, h = dims(c); ca, sa = math.cos(ang), math.sin(ang)
    t = min(w/2/abs(ca) if abs(ca) > 1e-9 else 1e9, h/2/abs(sa) if abs(sa) > 1e-9 else 1e9)
    return (x + t*ca*1.02, y + t*sa*1.02)


def arrow(a, b):
    hyp, s, t, pooled, stars, dv, ev, diff, dl, pv = E[(a, b)]
    ns = stars == 'ns'
    ax_, ay_ = POS[a]; bx_, by_ = POS[b]
    ang = math.atan2(by_-ay_, bx_-ax_)
    p0, p1 = edge(a, ang), edge(b, ang + math.pi)
    axd.add_patch(FancyArrowPatch(p0, p1, arrowstyle='-|>', mutation_scale=19,
                                  lw=2.3 if not ns else 1.6,
                                  color=RED if not ns else GREY,
                                  ls='solid' if not ns else (0, (5.5, 3.2)),
                                  shrinkA=0, shrinkB=1.5, zorder=3))
    mx, my = LAB[(a, b)]
    txt = ('◆ ' if diff else '') + f'{hyp}  {pooled}' + (stars if not ns else ' n.s.')
    w = 0.020 + 0.0082 * len(txt)
    axd.add_patch(FancyBboxPatch((mx-w/2, my-0.029), w, 0.058,
                                 boxstyle='round,pad=0.003,rounding_size=0.013',
                                 facecolor=ORNG_F if diff else 'white',
                                 edgecolor=ORNG_B if diff else '#CFD6DA',
                                 lw=1.4 if diff else 1.0, zorder=6))
    axd.text(mx, my, txt, ha='center', va='center', fontsize=10.0, fontweight='bold',
             zorder=7, color='#943126' if diff else (INK if not ns else '#6E7B7B'))


for c in POS:
    node(c)
for k in LAB:
    arrow(*k)

# -------------------------- lower tables --------------------------
def frame(x, w, title):
    axt.add_patch(FancyBboxPatch((x, 0.03), w, 0.94,
                                 boxstyle='round,pad=0.004,rounding_size=0.030',
                                 facecolor='#FBFCFC', edgecolor='#B9C2C9',
                                 lw=1.2, zorder=4))
    axt.add_patch(Rectangle((x, 0.845), w, 0.125, facecolor=NAVY, zorder=5))
    axt.text(x + 0.014, 0.9075, title, color='white', fontsize=11.2,
             fontweight='bold', va='center', zorder=6)


frame(0.005, 0.478, 'Path coefficients by economy group')
c1 = [0.035, 0.082, 0.245, 0.318, 0.393, 0.455]
for cx, hd, al in zip(c1, ['', 'Path', 'Dev.', 'Eme.', 'Diff.', 'p'],
                      ['left', 'left', 'center', 'center', 'center', 'center']):
    if hd:
        axt.text(cx, 0.785, hd, fontsize=9.4, fontweight='bold', ha=al,
                 va='center', zorder=6, color='#34495E')
axt.plot([0.020, 0.470], [0.755, 0.755], color='#CFD6DA', lw=1.0, zorder=6)
for i, r in enumerate(ROWS):
    hyp, s, t, pooled, stars, dv, ev, diff, dl, pv = r
    yy = 0.705 - i*0.078
    axt.text(c1[0], yy, hyp, fontsize=9.2, fontweight='bold', va='center',
             ha='left', zorder=6, color='#943126' if diff else INK)
    axt.text(c1[1], yy, f'{s} → {t}', fontsize=9.2, va='center', ha='left', zorder=6)
    axt.text(c1[2], yy, dv, fontsize=9.2, va='center', ha='center', zorder=6,
             fontweight='bold' if diff else 'normal')
    axt.text(c1[3], yy, ev, fontsize=9.2, va='center', ha='center', zorder=6,
             fontweight='bold' if diff else 'normal')
    axt.text(c1[4], yy, dl, fontsize=9.2, va='center', ha='center', zorder=6)
    axt.text(c1[5], yy, ('◆ ' if diff else '') + pv, fontsize=9.2, va='center',
             ha='center', zorder=6, fontweight='bold' if diff else 'normal',
             color='#943126' if diff else '#5D6D7E')
axt.text(0.020, 0.075, '◆ difference significant at p < 0.05 by permutation test',
         fontsize=8.6, color='#5D6D7E', va='center', zorder=6)

IE = [('RP', '0.212', True, 'partial'), ('SP', '0.234', True, 'full'),
      ('KSR', '0.134', True, 'full'), ('DI', '0.173', True, 'full'),
      ('TMC', '0.145', True, 'partial'), ('CBI', '0.017', False, 'none')]
frame(0.517, 0.478, 'Total indirect effect on performance')
c2 = [0.556, 0.700, 0.790, 0.930]
for cx, hd, al in zip(c2, ['Antecedent', 'Indirect', 'Sig.', 'Mediation'],
                      ['left', 'center', 'center', 'center']):
    axt.text(cx, 0.785, hd, fontsize=9.4, fontweight='bold', ha=al,
             va='center', zorder=6, color='#34495E')
axt.plot([0.532, 0.982], [0.755, 0.755], color='#CFD6DA', lw=1.0, zorder=6)
for i, (c, v, sig, form) in enumerate(IE):
    yy = 0.700 - i*0.103
    f, e = FAM[c]
    axt.add_patch(Rectangle((0.532, yy-0.028), 0.016, 0.056, facecolor=f,
                            edgecolor=e, lw=1.0, zorder=6))
    axt.text(c2[0], yy, c, fontsize=9.6, fontweight='bold', va='center', zorder=6)
    axt.text(c2[1], yy, v, fontsize=9.6, va='center', ha='center', zorder=6,
             fontweight='bold' if sig else 'normal', color=INK if sig else '#909497')
    axt.text(c2[2], yy, '***' if sig else 'n.s.', fontsize=9.0, va='center',
             ha='center', zorder=6, color=INK if sig else '#909497')
    axt.text(c2[3], yy, form, fontsize=9.0, va='center', ha='center', zorder=6,
             color='#566573' if sig else '#909497',
             style='normal' if sig else 'italic')
axt.text(0.532, 0.075, 'Bootstrapped with 5,000 subsamples, percentile intervals',
         fontsize=8.6, color='#5D6D7E', va='center', zorder=6)

fig.text(0.016, 0.972, 'Estimated structural model of green logistics enablement',
         fontsize=18, fontweight='bold', color=NAVY, va='center')
fig.text(0.016, 0.945, 'Pooled sample n = 220 · developing n = 100 · emerging n = 120 · '
                       'standardised coefficients · *** p < 0.001',
         fontsize=10.6, color='#5D6D7E', va='center', style='italic')
leg = [Line2D([], [], color=RED, lw=2.3, label='Significant path'),
       Line2D([], [], color=GREY, lw=1.6, ls=(0, (5.5, 3.2)), label='Non-significant path'),
       Line2D([], [], marker='s', ls='', ms=9, mfc='#AED6F1', mec='#2E75B6', label='External pressure'),
       Line2D([], [], marker='s', ls='', ms=9, mfc='#A9DFBF', mec='#1E8449', label='Capability condition'),
       Line2D([], [], marker='s', ls='', ms=9, mfc='#F5CBA7', mec='#E67E22', label='Managerial commitment'),
       Line2D([], [], marker='s', ls='', ms=9, mfc='#D7BDE2', mec='#7D3C98', label='Integration capability'),
       Line2D([], [], marker='h', ls='', ms=11, mfc='#EFD87A', mec='#B7950B', label='Outcome')]
fig.legend(handles=leg, loc='upper right', bbox_to_anchor=(0.988, 0.998), ncol=2,
           frameon=False, fontsize=9.6, handletextpad=0.6, columnspacing=1.5)
fig.text(0.986, 0.006, 'Source: authors.', fontsize=9, ha='right', color='#7F8C8D')

out = '/projects/sandbox/MetaV/Figure5_structural_model_revised.png'
plt.savefig(out, dpi=200, facecolor='white')
print('written', out)
