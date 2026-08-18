import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

plt.rcParams.update({'font.family': 'serif', 'font.size': 11})

CONDS = ['GSCI', 'TMC', 'DI', 'CBI', 'RP']
COLS = ['Dev C1', 'Dev C2', 'Dev C3', 'Eme C1', 'Eme C2']

# 'CP' core present, 'PP' peripheral present, 'CA' core absent,
# 'PA' peripheral absent, 'DC' don't care
M = {
    'Dev C1': {'GSCI': 'CP', 'TMC': 'CP', 'DI': 'DC', 'CBI': 'PP', 'RP': 'DC'},
    'Dev C2': {'GSCI': 'CP', 'TMC': 'CP', 'DI': 'PP', 'CBI': 'DC', 'RP': 'DC'},
    'Dev C3': {'GSCI': 'DC', 'TMC': 'CP', 'DI': 'DC', 'CBI': 'CA', 'RP': 'CP'},
    'Eme C1': {'GSCI': 'CP', 'TMC': 'CP', 'DI': 'PP', 'CBI': 'DC', 'RP': 'DC'},
    'Eme C2': {'GSCI': 'CP', 'TMC': 'CP', 'DI': 'DC', 'CBI': 'DC', 'RP': 'PP'},
}

fig, ax = plt.subplots(figsize=(9.2, 5.0))
ny = len(CONDS)

for xi, c in enumerate(COLS):
    ax.plot([xi, xi], [-0.5, ny - 0.5], color='0.88', lw=1, zorder=0)

for xi, c in enumerate(COLS):
    for yi, cond in enumerate(CONDS):
        y = ny - 1 - yi
        s = M[c][cond]
        if s == 'CP':
            ax.scatter(xi, y, s=330, c='0.15', edgecolors='0.15', zorder=3)
        elif s == 'PP':
            ax.scatter(xi, y, s=125, c='0.15', edgecolors='0.15', zorder=3)
        elif s == 'CA':
            ax.scatter(xi, y, s=330, facecolors='white', edgecolors='0.15',
                       linewidths=1.6, zorder=3)
            ax.plot([xi], [y], marker='x', ms=9, mew=1.6, color='0.15', zorder=4)
        elif s == 'PA':
            ax.scatter(xi, y, s=125, facecolors='white', edgecolors='0.15',
                       linewidths=1.4, zorder=3)
        else:
            ax.plot([xi], [y], marker='x', ms=7, mew=1.3, color='0.70', zorder=2)

ax.axvline(2.5, color='0.45', ls='--', lw=1.2, zorder=1)

ax.set_xlim(-0.6, len(COLS) - 0.4)
ax.set_ylim(-0.6, ny - 0.4)
ax.set_xticks(range(len(COLS)))
ax.set_xticklabels(COLS)
ax.set_yticks(range(ny))
ax.set_yticklabels(CONDS[::-1])
ax.tick_params(axis='both', length=3)
ax.set_title('Configurations for high green logistics performance', pad=14)
for sp in ax.spines.values():
    sp.set_color('0.25')

leg = [
    Line2D([], [], marker='o', ls='', ms=13, mfc='0.15', mec='0.15', label='Core present'),
    Line2D([], [], marker='o', ls='', ms=8, mfc='0.15', mec='0.15', label='Peripheral present'),
    Line2D([], [], marker='o', ls='', ms=13, mfc='white', mec='0.15', mew=1.6, label='Core absent'),
    Line2D([], [], marker='x', ls='', ms=8, mec='0.70', mew=1.3, label="Don't care"),
]
ax.legend(handles=leg, loc='upper center', bbox_to_anchor=(0.5, -0.13),
          ncol=4, frameon=False, handletextpad=0.5, columnspacing=2.0)

plt.tight_layout()
out = '/projects/sandbox/MetaV/Figure7_configurations_revised.png'
plt.savefig(out, dpi=300, bbox_inches='tight', facecolor='white')
print('written', out)
