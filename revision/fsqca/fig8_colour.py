import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon, Rectangle, FancyArrowPatch

plt.rcParams.update({'font.family': 'DejaVu Sans'})

NAVY, RED, GREY, BORDER = '#2C3E50', '#C0392B', '#95A5A6', '#7F8C8D'
FAM = {
    'RP':   ('#AED6F1', '#2E75B6'),
    'SP':   ('#AED6F1', '#2E75B6'),
    'DI':   ('#A9DFBF', '#1E8449'),
    'CBI':  ('#A9DFBF', '#1E8449'),
    'KSR':  ('#A9DFBF', '#1E8449'),
    'TMC':  ('#F5CBA7', '#E67E22'),
    'GSCI': ('#D7BDE2', '#7D3C98'),
}
NAME = {
    'RP': 'Regulatory &\nPolicy Pressure',
    'SP': 'Stakeholder &\nCustomer Pressure',
    'DI': 'Digital Infra.\nReadiness',
    'CBI': 'Perceived Economic\nFeasibility',
    'KSR': 'Knowledge &\nSkill Readiness',
    'TMC': 'Top Management\nCommitment',
    'GSCI': 'Green Supply\nChain Integration',
}

# (panel title, [(code, role)], consistency, raw cov, unique cov)
# role: 'core' | 'periph' | 'coreabs'
PANELS = [
    ('Developing C1', [('GSCI', 'core'), ('TMC', 'core'), ('CBI', 'periph')], 0.864, 0.448, 0.431),
    ('Developing C2', [('GSCI', 'core'), ('TMC', 'core'), ('DI', 'periph')], 0.867, 0.472, 0.399),
    ('Developing C3', [('TMC', 'core'), ('RP', 'core'), ('CBI', 'coreabs')], 0.871, 0.468, 0.408),
    ('Emerging C1', [('GSCI', 'core'), ('TMC', 'core'), ('DI', 'periph')], 0.832, 0.542, 0.463),
    ('Emerging C2', [('GSCI', 'core'), ('TMC', 'core'), ('RP', 'periph')], 0.850, 0.481, 0.406),
]

fig = plt.figure(figsize=(19.2, 9.6))
ML, MR, MT, MB, GX, GY = 0.010, 0.010, 0.012, 0.012, 0.011, 0.014
PW = (1 - ML - MR - 2 * GX) / 3
PH = (1 - MT - MB - GY) / 2


def cell(r, c):
    left = ML + c * (PW + GX)
    bot = 1 - MT - PH - r * (PH + GY)
    ax = fig.add_axes([left, bot, PW, PH])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color(BORDER); s.set_linewidth(1.1)
    return ax


def hexagon(cx, cy, w, h):
    k = w * 0.20
    return [(cx - w / 2, cy), (cx - w / 2 + k, cy + h / 2), (cx + w / 2 - k, cy + h / 2),
            (cx + w / 2, cy), (cx + w / 2 - k, cy - h / 2), (cx - w / 2 + k, cy - h / 2)]


def draw_panel(ax, title, conds, cons, raw, uniq):
    ax.add_patch(Rectangle((0, 0.885), 1, 0.115, transform=ax.transAxes,
                           facecolor=NAVY, edgecolor='none', zorder=5))
    ax.text(0.018, 0.9425, title, transform=ax.transAxes, color='white',
            fontsize=15, fontweight='bold', va='center', ha='left', zorder=6)

    solid = [c for c in conds if c[1] in ('core', 'coreabs')]
    dashed = [c for c in conds if c[1] == 'periph']
    ys_solid = {1: [0.63], 2: [0.755, 0.545], 3: [0.775, 0.575, 0.375]}[len(solid)]
    ys_dash = {0: [], 1: [0.215], 2: [0.28, 0.145]}[len(dashed)]

    HX, HY, HW, HH = 0.735, 0.555, 0.275, 0.20
    ax.add_patch(Polygon(hexagon(HX, HY, HW, HH), closed=True,
                         facecolor='#EFD87A', edgecolor='#B7950B', lw=2.0, zorder=4))
    ax.text(HX, HY + 0.033, 'GLP', ha='center', va='center', fontsize=13,
            fontweight='bold', zorder=5)
    ax.text(HX, HY - 0.038, 'High Green\nLogistics Perf.', ha='center', va='center',
            fontsize=8.6, linespacing=1.35, zorder=5)

    def hex_edge(dy):
        """point on the hexagon's left boundary at vertical offset dy"""
        k = HW * 0.20
        x = HX - HW / 2 + k * min(abs(dy) / (HH / 2), 1.0)
        return (x - 0.006, HY + dy)

    items = list(zip(solid, ys_solid)) + list(zip(dashed, ys_dash))
    items.sort(key=lambda it: -it[1])
    n = len(items)
    offs = [0.0] if n == 1 else [0.058 - i * (0.116 / (n - 1)) for i in range(n)]
    dymap = {id(it): o for it, o in zip(items, offs)}

    for it in items:
        (code, role), y = it
        tip = hex_edge(dymap[id(it)])
        fill, edge = FAM[code]
        if role == 'periph':
            e = Ellipse((0.245, y), 0.395, 0.175, facecolor='white', edgecolor=edge,
                        lw=2.0, ls=(0, (5.5, 3.0)), zorder=3)
            lbl, half = '(peripheral)', 0.395 / 2
        elif role == 'coreabs':
            e = Ellipse((0.245, y), 0.395, 0.175, facecolor='white', edgecolor=edge,
                        lw=2.6, zorder=3)
            lbl, half = '(core, absent)', 0.395 / 2
        else:
            e = Ellipse((0.245, y), 0.345, 0.175, facecolor=fill, edgecolor=edge,
                        lw=2.2, zorder=3)
            lbl, half = '(core)', 0.345 / 2
        ax.add_patch(e)
        pre = '~' if role == 'coreabs' else ''
        ax.text(0.238, y + 0.038, pre + code, ha='right', va='center',
                fontsize=12.5, fontweight='bold', zorder=5)
        ax.text(0.252, y + 0.036, lbl, ha='left', va='center', fontsize=8.4, zorder=5)
        ax.text(0.245, y - 0.040, NAME[code], ha='center', va='center',
                fontsize=8.2, linespacing=1.35, zorder=5)

        start = (0.245 + half * 0.87, y)
        if role == 'periph':
            ax.add_patch(FancyArrowPatch(start, tip, arrowstyle='-|>', mutation_scale=17,
                                         lw=2.0, color=GREY, ls=(0, (5.5, 3.0)),
                                         shrinkA=0, shrinkB=1, zorder=2))
        else:
            ax.add_patch(FancyArrowPatch(start, tip, arrowstyle='-|>', mutation_scale=17,
                                         lw=1.9, color=RED, shrinkA=0, shrinkB=1, zorder=2))

    ax.text(0.018, 0.045, f'Consistency = {cons:.3f}     Raw coverage = {raw:.3f}'
                          f'     Unique coverage = {uniq:.3f}',
            transform=ax.transAxes, fontsize=10.8, va='center', ha='left')


for i, p in enumerate(PANELS):
    draw_panel(cell(i // 3, i % 3), *p)

# ---------------- legend cell ----------------
ax = cell(1, 2)
X0, X1, XS = 0.055, 0.965, 0.235
rows = [
    ('solid', 'Core condition (parsimonious + intermediate)', None),
    ('dashed', 'Peripheral condition (intermediate only)', None),
    ('unfilled', 'Core condition absent from the recipe', None),
    (None, 'External pressures (RP, SP)', '#AED6F1'),
    (None, 'Capabilities (DI, CBI, KSR)', '#A9DFBF'),
    (None, 'Management (TMC)', '#F5CBA7'),
    (None, 'Integration (GSCI)', '#D7BDE2'),
    (None, 'Outcome hexagon (high GLP)', '#EFD87A'),
]
TOP, RH = 0.855, 0.0735
TITLE_H = 0.075
ax.add_patch(Rectangle((X0, TOP - TITLE_H), X1 - X0, TITLE_H, facecolor='white',
                       edgecolor='black', lw=1.0))
ax.text((X0 + X1) / 2, TOP - TITLE_H / 2, 'Legend', ha='center', va='center',
        fontsize=14, fontweight='bold')
y = TOP - TITLE_H
for word, txt, swatch in rows:
    ax.add_patch(Rectangle((X0, y - RH), XS - X0, RH, facecolor='white',
                           edgecolor='black', lw=1.0))
    ax.add_patch(Rectangle((XS, y - RH), X1 - XS, RH, facecolor='white',
                           edgecolor='black', lw=1.0))
    if swatch:
        ax.add_patch(Rectangle((X0 + 0.012, y - RH + 0.012), XS - X0 - 0.024, RH - 0.024,
                               facecolor=swatch, edgecolor='#555555', lw=0.8))
    else:
        ax.text((X0 + XS) / 2, y - RH / 2, word, ha='center', va='center',
                fontsize=11.5, fontweight='bold')
    ax.text(XS + 0.022, y - RH / 2, txt, ha='left', va='center', fontsize=12.2)
    y -= RH
ax.add_patch(Rectangle((X0, y - 0.135), X1 - X0, 0.135, facecolor='white',
                       edgecolor='black', lw=1.0))
ax.text((X0 + X1) / 2, y - 0.135 / 2,
        'Red arrows mark core contributions and grey dashed arrows peripheral ones.\n'
        'A condition shown as absent enters the recipe in negated form.\n'
        'Ellipse = enabler condition; hexagon = outcome.',
        ha='center', va='center', fontsize=9.6, linespacing=1.5)

out = '/projects/sandbox/MetaV/Figure8_configuration_paths_revised.png'
plt.savefig(out, dpi=170, facecolor='white')
print('written', out)
