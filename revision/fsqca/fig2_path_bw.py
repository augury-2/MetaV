"""Figure 2: structural path diagram, monochrome, publication grade."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon, Rectangle, FancyArrowPatch
import math

plt.rcParams.update({'font.family': 'DejaVu Serif'})
BK = '#000000'
WH, G1, G2, G3 = 'white', '#F2F2F2', '#E4E4E4', '#D6D6D6'

NODE = {   # code: (x, y, label, fill, lw, dashed)
    'CBI':  (0.455, 0.885, 'Perceived Economic\nFeasibility', WH, 1.3, True),
    'KSR':  (0.135, 0.560, 'Knowledge &\nSkill Readiness', WH, 1.3, False),
    'DI':   (0.455, 0.560, 'Digital Infrastructure\nReadiness', G1, 2.0, False),
    'GSCI': (0.720, 0.500, 'Green Supply\nChain Integration', G2, 2.0, False),
    'SP':   (0.135, 0.290, 'Stakeholder &\nCustomer Pressure', WH, 1.3, False),
    'TMC':  (0.455, 0.290, 'Top Management\nCommitment', G1, 2.0, False),
    'RP':   (0.135, 0.075, 'Regulatory &\nPolicy Pressure', WH, 1.3, False),
}
EW, EH = 0.176, 0.136
GLP = (0.925, 0.330, 'Green Logistics\nPerformance')
HW, HH = 0.150, 0.168
EDGES = [('KSR', 'DI', 'H5', (0.295, 0.588)), ('SP', 'TMC', 'H2', (0.295, 0.318)),
         ('RP', 'TMC', 'H1', (0.293, 0.210)), ('CBI', 'GSCI', 'H6', (0.612, 0.706)),
         ('DI', 'GSCI', 'H4', (0.588, 0.562)), ('TMC', 'GSCI', 'H3', (0.556, 0.424)),
         ('GSCI', 'GLP', 'H7', (0.828, 0.452)), ('TMC', 'GLP', 'H8', (0.692, 0.342))]

fig = plt.figure(figsize=(14.2, 8.6))
ax = fig.add_axes([0.010, 0.055, 0.980, 0.900])
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')


def pos(c):
    return (GLP[0], GLP[1]) if c == 'GLP' else (NODE[c][0], NODE[c][1])


def dims(c):
    return (HW, HH) if c == 'GLP' else (EW, EH)


for c, (x, y, lab, fill, lw, dsh) in NODE.items():
    ax.add_patch(Ellipse((x, y), EW, EH, facecolor=fill, edgecolor=BK, lw=lw,
                         ls=(0, (5, 2.6)) if dsh else 'solid', zorder=4))
    ax.text(x, y + 0.030, c, ha='center', va='center', fontsize=13,
            fontweight='bold', zorder=5)
    ax.text(x, y - 0.026, lab, ha='center', va='center', fontsize=8.4,
            linespacing=1.40, zorder=5)

gx, gy, glab = GLP
k = HW * 0.24
ax.add_patch(Polygon([(gx - HW/2, gy), (gx - HW/2 + k, gy + HH/2),
                      (gx + HW/2 - k, gy + HH/2), (gx + HW/2, gy),
                      (gx + HW/2 - k, gy - HH/2), (gx - HW/2 + k, gy - HH/2)],
                     closed=True, facecolor=G3, edgecolor=BK, lw=2.4, zorder=4))
ax.text(gx, gy + 0.032, 'GLP', ha='center', va='center', fontsize=13.5,
        fontweight='bold', zorder=5)
ax.text(gx, gy - 0.026, glab, ha='center', va='center', fontsize=8.4,
        linespacing=1.40, zorder=5)


def rim(c, ang):
    x, y = pos(c); w, h = dims(c)
    if c == 'GLP':
        ca, sa = math.cos(ang), math.sin(ang)
        t = min(w/2/abs(ca) if abs(ca) > 1e-9 else 1e9,
                h/2/abs(sa) if abs(sa) > 1e-9 else 1e9)
        return (x + t*ca*1.01, y + t*sa*1.01)
    return (x + (w/2)*math.cos(ang)*1.01, y + (h/2)*math.sin(ang)*1.01)


for s, t, hyp, lp in EDGES:
    sx, sy = pos(s); tx, ty = pos(t)
    ang = math.atan2(ty - sy, tx - sx)
    p0, p1 = rim(s, ang), rim(t, ang + math.pi)
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle='-|>', mutation_scale=18,
                                 lw=1.4, color=BK, shrinkA=0, shrinkB=1.4, zorder=3))
    ax.text(lp[0], lp[1], f'{hyp} (+)', ha='center', va='center', fontsize=10.2,
            zorder=6, bbox=dict(boxstyle='round,pad=0.26', facecolor='white',
                                edgecolor='none'))

# ------------------------------- legend -------------------------------
LX, LY, LW = 0.008, 0.985, 0.300
RH, HDR = 0.036, 0.044
ROWS = [('External pressures (RP, SP)', WH, 1.3, False),
        ('Capability conditions (KSR, DI)', G1, 1.3, False),
        ('Enabling condition (CBI)', WH, 1.3, True),
        ('Managerial commitment (TMC)', G1, 2.0, False),
        ('Integration capability (GSCI)', G2, 2.0, False),
        ('Outcome (GLP)', G3, 2.4, False)]
ax.add_patch(Rectangle((LX, LY - HDR), LW, HDR, facecolor=WH, edgecolor=BK, lw=1.2, zorder=5))
ax.text(LX + LW/2, LY - HDR/2, 'Legend', ha='center', va='center',
        fontsize=11, fontweight='bold', zorder=6)
for i, (txt, fill, lw, dsh) in enumerate(ROWS):
    ry = LY - HDR - i*RH
    ax.add_patch(Rectangle((LX, ry - RH), LW, RH, facecolor=WH, edgecolor=BK, lw=1.0, zorder=5))
    ax.add_patch(Rectangle((LX + 0.011, ry - RH + 0.008), 0.038, RH - 0.016,
                           facecolor=fill, edgecolor=BK, lw=lw,
                           ls=(0, (3.5, 2.0)) if dsh else 'solid', zorder=6))
    ax.text(LX + 0.062, ry - RH/2, txt, ha='left', va='center', fontsize=8.7, zorder=6)
ny = LY - HDR - len(ROWS)*RH
ax.add_patch(Rectangle((LX, ny - 0.048), LW, 0.048, facecolor=WH, edgecolor=BK, lw=1.0, zorder=5))
ax.text(LX + LW/2, ny - 0.024,
        'Ellipse = enabler condition; hexagon = outcome.\n'
        'Heavier borders denote endogenous constructs.',
        ha='center', va='center', fontsize=7.9, linespacing=1.50, zorder=6)

fig.text(0.010, 0.026, 'Note. The dashed outline marks perceived economic feasibility as '
                       'an enabling condition rather than a firm capability, since the '
                       'easing of a constraint permits integration without producing it.',
         fontsize=8.8, color='#333333')
fig.text(0.990, 0.026, 'Source: authors.', fontsize=8.8, ha='right', color='#333333')

out = '/projects/sandbox/MetaV/Figure2_path_diagram_bw.png'
plt.savefig(out, dpi=300, facecolor='white')
print('written', out)
