import numpy as np
exec(open('/projects/sandbox/fsqca_route_a.py').read().split('print("=" * 104)')[0])
CONDS = CANDIDATES['set5']

print("NECESSITY, correct formulas: consistency = sum min(X,Y)/sum Y ; coverage = sum min(X,Y)/sum X")
for outcome, olab in [(False, 'HIGH GLP'), (True, 'LOW GLP (~GLP)')]:
    print(f"\n=== {olab} ===")
    print(f"{'condition':10s} {'DEV cons':>9s} {'DEV cov':>8s} | {'EME cons':>9s} {'EME cov':>8s}")
    for lab, neg in [('', False), ('~', True)]:
        for k in CONDS:
            out = f"{lab + k:10s}"
            for gi, g in enumerate(['developing', 'emerging']):
                m = grp == g
                F, _ = build(m, 'p95', CONDS)
                X = (1 - F[k]) if neg else F[k]
                Y = (1 - F['GLP']) if outcome else F['GLP']
                mn = np.minimum(X, Y).sum()
                out += f" {mn/Y.sum():9.3f} {mn/X.sum():8.3f} |" if gi == 0 else f" {mn/Y.sum():9.3f} {mn/X.sum():8.3f}"
            print(out)
        print()
