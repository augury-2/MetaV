import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyArrowPatch
from matplotlib.lines import Line2D

plt.rcParams.update({'font.family': 'serif', 'font.size': 10.5})

CONFIGS = [
    ('Dev C1', [('GSCI', 'core'), ('TMC', 'core'), ('CBI', 'periph')], 0.864, 0.448, 0.431),
    ('Dev C2', [('GSCI', 'core'), ('TMC', 'core'), ('DI', 'periph')], 0.867, 0.472, 0.399),
    ('Dev C3', [('TMC', 'core'), ('RP', 'core'), ('~CBI', 'coreabs')], 0.871, 0.468, 0.408),
    ('Eme C1', [('GSCI', 'core'), ('TMC', 'core'), ('DI', 'periph')], 0.832, 0.542, 0.463),
    ('Eme C2', [('GSCI', 'core'), ('TMC', 'core'), ('RP', 'periph')], 0.850, 0.481, 0.406),
]

fig = plt.figure(figsize=(11.2, 6.9))

L, W, GAP, H = 0.045, 0.29, 0.015, 0.300
B1, B2 = 0.565, 0.135
POS = [(B1, 0), (B1, 1), (B1, 2), (B2, 0), (B2, 1)]

for (name, conds, cons, raw, uniq), (b, c) in zip(CONFIGS, POS):
    ax = fig.add_axes([L + c * (W + GAP), b, W, H])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    ys = [0.80, 0.50, 0.20]

    for (lab, kind), y in zip(conds, ys):
        if kind == 'periph':
            e = Ellipse((0.235, y), 0.38, 0.21, facecolor='0.94', edgecolor='0.20',
                        lw=1.4, ls=(0, (4, 2.2)), zorder=3)
            fw = 'normal'
        elif kind == 'coreabs':
            e = Ellipse((0.235, y), 0.38, 0.21, facecolor='white', edgecolor='0.15',
                        lw=2.4, zorder=3)
            fw = 'bold'
        else:
            e = Ellipse((0.235, y), 0.38, 0.21, facecolor='0.82', edgecolor='0.15',
                        lw=2.4, zorder=3)
            fw = 'bold'
        ax.add_patch(e)
        ax.text(0.235, y, lab, ha='center', va='center', fontsize=11,
                fontweight=fw, zorder=4)
        ax.add_patch(FancyArrowPatch((0.432, y), (0.655, 0.50), arrowstyle='-|>',
                                     mutation_scale=13, lw=1.2, color='0.30',
                                     shrinkA=0, shrinkB=2, zorder=2))

    ax.add_patch(Ellipse((0.815, 0.50), 0.31, 0.25, facecolor='0.30',
                         edgecolor='0.10', lw=1.6, zorder=3))
    ax.text(0.815, 0.50, 'GLP', ha='center', va='center', color='white',
            fontsize=11, fontweight='bold', zorder=4)

    ax.text(0.5, 1.105, name, ha='center', va='bottom', fontsize=12,
            fontweight='bold', transform=ax.transAxes)
    ax.text(0.5, 1.010, f'cons. {cons:.3f}    raw cov. {raw:.3f}    '
                        f'uniq. cov. {uniq:.3f}',
            ha='center', va='bottom', fontsize=8.2, color='0.32',
            transform=ax.transAxes)

for ylab, yline, txt in [(0.955, 0.947, 'Developing economies  (n = 100)'),
                         (0.525, 0.517, 'Emerging economies  (n = 120)')]:
    fig.text(L, ylab, txt, fontsize=11.5, fontweight='bold', color='0.20',
             va='bottom')
    fig.add_artist(Line2D([L, 0.955], [yline, yline], color='0.80', lw=0.9))

leg = [
    Line2D([], [], marker='o', ls='', ms=13, mfc='0.82', mec='0.15', mew=2.0,
           label='Core condition present'),
    Line2D([], [], marker='o', ls='', ms=13, mfc='0.94', mec='0.20', mew=1.2,
           label='Peripheral condition present'),
    Line2D([], [], marker='o', ls='', ms=13, mfc='white', mec='0.15', mew=2.0,
           label='Core condition absent'),
    Line2D([], [], marker='o', ls='', ms=13, mfc='0.30', mec='0.10', label='Outcome'),
]
fig.legend(handles=leg, loc='lower center', bbox_to_anchor=(0.5, 0.018),
           ncol=4, frameon=False, fontsize=10, handletextpad=0.6, columnspacing=2.2)

out = '/projects/sandbox/MetaV/Figure8_configuration_paths_revised.png'
plt.savefig(out, dpi=300, facecolor='white')
print('written', out)
