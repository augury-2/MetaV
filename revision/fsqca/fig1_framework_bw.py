"""Figure 1: conceptual framework, monochrome, publication grade."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import math

plt.rcParams.update({'font.family': 'DejaVu Serif', 'mathtext.fontset': 'dejavuserif'})
BLACK, GREY_L, GREY_M = '#000000', '#F0F0F0', '#7A7A7A'

NAME = {
    'RP':   ('RP',   'Regulatory &\nPolicy Pressure'),
    'SP':   ('SP',   'Stakeholder &\nCustomer Pressure'),
    'KSR':  ('KSR',  'Knowledge &\nSkill Readiness'),
    'TMC':  ('TMC',  'Top Management\nCommitment'),
    'DI':   ('DI',   'Digital Infrastructure\nReadiness'),
    'CBI':  ('CBI',  'Perceived Economic\nFeasibility'),
    'GSCI': ('GSCI', 'Green Supply Chain\nIntegration'),
    'GLP':  ('GLP',  'Green Logistics\nPerformance'),
}
POS = {'RP': (0.105, 0.860), 'SP': (0.105, 0.655), 'KSR': (0.105, 0.300),
       'TMC': (0.415, 0.775), 'DI': (0.415, 0.335), 'CBI': (0.415, 0.105),
       'GSCI': (0.685, 0.470), 'GLP': (0.905, 0.700)}
W, H = 0.176, 0.150
ENDO = {'TMC', 'DI', 'GSCI', 'GLP'}
EDGES = [                                   # src, tgt, hyp, label xy, rad
    ('RP', 'TMC', 'H1', (0.260, 0.862), 0.0),
    ('SP', 'TMC', 'H2', (0.260, 0.672), 0.0),
    ('KSR', 'DI', 'H5', (0.260, 0.352), 0.0),
    ('TMC', 'GSCI', 'H3', (0.550, 0.667), 0.0),
    ('DI', 'GSCI', 'H4', (0.550, 0.360), 0.0),
    ('CBI', 'GSCI', 'H6', (0.556, 0.246), 0.0),
    ('GSCI', 'GLP', 'H7', (0.772, 0.628), 0.0),
    ('TMC', 'GLP', 'H8', (0.660, 0.886), -0.20),
]

fig = plt.figure(figsize=(13.6, 8.0))
ax = fig.add_axes([0.012, 0.070, 0.976, 0.870])
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')


def node(c):
    x, y = POS[c]; code, label = NAME[c]
    ax.add_patch(FancyBboxPatch((x - W/2, y - H/2), W, H,
                                boxstyle='round,pad=0.004,rounding_size=0.026',
                                facecolor=GREY_L if c == 'GLP' else 'white',
                                edgecolor=BLACK, lw=2.0 if c in ENDO else 1.25,
                                zorder=4))
    ax.text(x, y + 0.036, code, ha='center', va='center', fontsize=14,
            fontweight='bold', color=BLACK, zorder=5)
    ax.text(x, y - 0.030, label, ha='center', va='center', fontsize=8.8,
            linespacing=1.44, color=BLACK, zorder=5)


def edge_pt(c, ang):
    x, y = POS[c]; ca, sa = math.cos(ang), math.sin(ang)
    t = min(W/2/abs(ca) if abs(ca) > 1e-9 else 1e9,
            H/2/abs(sa) if abs(sa) > 1e-9 else 1e9)
    return (x + t*ca*1.012, y + t*sa*1.012)


def arrow(s, t, hyp, lp, rad):
    sx, sy = POS[s]; tx, ty = POS[t]
    ang = math.atan2(ty - sy, tx - sx)
    if rad:
        p0 = (sx + W/2 * 0.62, sy + H/2 * 1.012)
        p1 = edge_pt(t, ang + math.pi + 0.55)
    else:
        p0, p1 = edge_pt(s, ang), edge_pt(t, ang + math.pi)
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle='-|>', mutation_scale=17,
                                 lw=1.35, color=BLACK,
                                 connectionstyle=f'arc3,rad={rad}',
                                 shrinkA=0, shrinkB=1.2, zorder=3))
    ax.text(lp[0], lp[1], f'{hyp} (+)', ha='center', va='center', fontsize=10.4,
            style='italic', color=BLACK, zorder=6,
            bbox=dict(boxstyle='round,pad=0.28', facecolor='white', edgecolor='none'))


for c in POS:
    node(c)
for e in EDGES:
    arrow(*e)

BANDS = [(0.105, 'Antecedent conditions', 0.012, 0.198),
         (0.415, 'Mediating and enabling conditions', 0.300, 0.530),
         (0.795, 'Integration and outcome', 0.590, 0.988)]
for xc, txt, xa, xb in BANDS:
    ax.text(xc, 0.978, txt, ha='center', va='center', fontsize=9.8,
            style='italic', color=GREY_M)
    ax.plot([xa, xb], [0.955, 0.955], color='#C4C4C4', lw=0.8, zorder=1)

fig.text(0.012, 0.030, 'Note. Heavier borders denote endogenous constructs. All eight '
                       'hypotheses predict a positive association.',
         fontsize=8.8, color='#333333')
fig.text(0.012, 0.010, 'H6 is specified as weaker than H3 and H4, since easing a '
                       'constraint permits integration without producing it.',
         fontsize=8.8, color='#333333')
fig.text(0.988, 0.010, 'Source: authors.', fontsize=8.8, ha='right', color='#333333')

out = '/projects/sandbox/MetaV/Figure1_conceptual_framework_bw.png'
plt.savefig(out, dpi=300, facecolor='white')
print('written', out)
