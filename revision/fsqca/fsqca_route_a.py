"""Route A: reduced condition set, full fsQCA with robustness."""
import numpy as np, openpyxl, math, itertools
from collections import defaultdict

PATH = '/projects/sandbox/MetaV/data BSD Collected.xlsx'
CONS = {'GSCI': 5, 'RP': 4, 'DI': 5, 'TMC': 4, 'SP': 4, 'CBI': 4, 'KSR': 4, 'GLP': 4}
ws = openpyxl.load_workbook(PATH, data_only=True)['Data']
hdr = [c.value for c in ws[1]]
raw = [dict(zip(hdr, [ws.cell(row=r, column=c).value for c in range(1, len(hdr) + 1)]))
       for r in range(2, ws.max_row + 1)]
raw = [r for r in raw if r.get('respondent_id') is not None]
S = {k: np.array([sum(r[f"{k}{i}"] for i in range(1, CONS[k] + 1)) / CONS[k] for r in raw]) for k in CONS}
grp = np.array([r['group'] for r in raw])
SC = math.log(0.95 / 0.05)

CANDIDATES = {
    'set5': ['GSCI', 'TMC', 'DI', 'CBI', 'RP'],
    'set4a': ['GSCI', 'TMC', 'DI', 'CBI'],
    'set4b': ['GSCI', 'TMC', 'DI', 'RP'],
}


def calib(x, full, cross, out):
    m = np.empty(len(x))
    for i, v in enumerate(x):
        if v >= cross:
            d = (v - cross) / (full - cross) if full > cross else 0.0
            lo = d * SC
        else:
            d = (cross - v) / (cross - out) if cross > out else 0.0
            lo = -d * SC
        m[i] = 1 / (1 + math.exp(-max(min(lo, 12), -12)))
    return np.clip(m, 0.001, 0.999)


def anch(k, mask, scheme):
    x = S[k][mask]
    if scheme == 'p95':  return (np.percentile(x, 95), np.percentile(x, 50), np.percentile(x, 5))
    if scheme == 'p90':  return (np.percentile(x, 90), np.percentile(x, 50), np.percentile(x, 10))
    if scheme == 'p80':  return (np.percentile(x, 80), np.percentile(x, 50), np.percentile(x, 20))
    if scheme == 'msd':  return (x.mean() + x.std(), x.mean(), x.mean() - x.std())
    if scheme == 'p95x': return (np.percentile(x, 95), x.mean(), np.percentile(x, 5))


def build(mask, scheme, conds):
    A = {k: anch(k, mask, scheme) for k in conds + ['GLP']}
    return {k: calib(S[k][mask], *A[k]) for k in conds + ['GLP']}, A


def tmem(F, term, conds):
    v = np.ones(len(F[conds[0]]))
    for i, c in enumerate(conds):
        if term[i] == '1':   v = np.minimum(v, F[c])
        elif term[i] == '0': v = np.minimum(v, 1 - F[c])
    return v


def consis(X, Y):
    return np.minimum(X, Y).sum() / X.sum() if X.sum() > 0 else 0.0


def pri(X, Y):
    a = np.minimum(X, Y).sum()
    b = np.minimum(X, np.minimum(Y, 1 - Y)).sum()
    return (a - b) / (X.sum() - b) if (X.sum() - b) > 1e-9 else 0.0


def combine(a, b, n):
    d = -1
    for i in range(n):
        if a[i] != b[i]:
            if a[i] == '-' or b[i] == '-' or d != -1: return None
            d = i
    return None if d == -1 else a[:d] + ('-',) + a[d + 1:]


def primes(mt, dc, n):
    cur = set(mt) | set(dc); allp = set()
    while cur:
        nxt, used = set(), set()
        cl = list(cur)
        for i in range(len(cl)):
            for j in range(i + 1, len(cl)):
                c = combine(cl[i], cl[j], n)
                if c is not None: nxt.add(c); used.add(cl[i]); used.add(cl[j])
        allp |= (cur - used); cur = nxt
    return allp


def cov(p, m, n):
    return all(p[i] == '-' or p[i] == m[i] for i in range(n))


def mincover(ps, mt, n):
    ps = list(ps); rem = set(mt); ch = []
    for m in list(rem):
        c = [p for p in ps if cov(p, m, n)]
        if len(c) == 1 and c[0] not in ch: ch.append(c[0])
    rem -= {m for m in rem if any(cov(p, m, n) for p in ch)}
    while rem:
        best = max(ps, key=lambda p: sum(1 for m in rem if cov(p, m, n)))
        if sum(1 for m in rem if cov(best, m, n)) == 0: break
        ch.append(best); rem -= {m for m in rem if cov(best, m, n)}
    return ch


def truthtable(F, conds, freq, thr, prithr=0.5):
    n = len(conds); N = len(F[conds[0]]); Y = F['GLP']
    cnt = defaultdict(int)
    for i in range(N):
        cnt[tuple('1' if F[c][i] > 0.5 else '0' for c in conds)] += 1
    rows, pos, neg = [], [], []
    for corner, k in sorted(cnt.items(), key=lambda kv: -kv[1]):
        cm = tmem(F, corner, conds)
        cs, pr = consis(cm, Y), pri(cm, Y)
        keep = k >= freq
        out = 1 if (keep and cs >= thr and pr >= prithr) else 0
        rows.append((corner, k, cs, pr, out, keep))
        if keep: (pos if out else neg).append(corner)
    return rows, pos, neg, cnt


def solve(F, conds, pos, neg, mode):
    n = len(conds)
    allc = [tuple(b) for b in itertools.product('01', repeat=n)]
    if mode == 'parsimonious':
        dc = [c for c in allc if c not in pos and c not in neg]
    elif mode == 'complex':
        dc = []
    else:  # intermediate: easy counterfactuals only (presence expected to help)
        dc = []
        for c in allc:
            if c in pos or c in neg: continue
            for p in pos:
                if all(c[i] >= p[i] for i in range(n)):  # '1' >= '0'
                    dc.append(c); break
    P = [p for p in primes(pos, dc, n) if not any(cov(p, m, n) for m in neg)]
    if not P: return []
    return mincover(P, pos, n)


def fmt(t, conds):
    p = [(c if t[i] == '1' else '~' + c) for i, c in enumerate(conds) if t[i] != '-']
    return '*'.join(p) if p else '(empty)'


def report(F, conds, sol, label):
    Y = F['GLP']
    if not sol:
        print(f"    {label}: no solution"); return
    sm = np.zeros(len(Y))
    for t in sol: sm = np.maximum(sm, tmem(F, t, conds))
    print(f"    {label}: solcons {consis(sm, Y):.3f}  solcov {np.minimum(sm, Y).sum()/Y.sum():.3f}")
    for t in sol:
        tm = tmem(F, t, conds)
        uniq = tm.copy()
        for o in sol:
            if o != t: uniq = np.minimum(uniq, 1 - tmem(F, o, conds))
        print(f"        {fmt(t, conds):40s} cons {consis(tm, Y):.3f} raw {np.minimum(tm, Y).sum()/Y.sum():.3f} "
              f"uniq {np.minimum(uniq, Y).sum()/Y.sum():.3f}")


print("=" * 104)
print("STEP 1  CASE COVERAGE OF RETAINED ROWS, BY CONDITION SET  (within-group p95/50/5)")
print("=" * 104)
print(f"{'set':7s} {'group':11s} {'corners':>8s} {'maxn':>5s} " +
      "  ".join(f"f>={f}".rjust(9) for f in [2, 3, 4]))
for name, conds in CANDIDATES.items():
    for g in ['developing', 'emerging']:
        m = grp == g
        F, A = build(m, 'p95', conds)
        cnt = defaultdict(int)
        for i in range(m.sum()):
            cnt[tuple('1' if F[c][i] > 0.5 else '0' for c in conds)] += 1
        line = f"{name:7s} {g:11s} {len(cnt):8d} {max(cnt.values()):5d} "
        for f in [2, 3, 4]:
            cases = sum(v for v in cnt.values() if v >= f)
            line += f"  {cases:3d}/{m.sum():3d} {100*cases/m.sum():3.0f}%"
        print(line)



CONDS = CANDIDATES['set5']
print()
print("=" * 104)
print("STEP 2  CALIBRATION ANCHORS, WITHIN GROUP, 95th/50th/5th PERCENTILE")
print("=" * 104)
for g in ['developing', 'emerging']:
    m = grp == g
    F, A = build(m, 'p95', CONDS)
    print(f"\n  {g} (n={m.sum()})")
    for k in CONDS + ['GLP']:
        print(f"    {k:5s} full {A[k][0]:.2f}  crossover {A[k][1]:.2f}  non-member {A[k][2]:.2f}"
              f"   members>0.5: {(F[k] > 0.5).sum():3d}")

print()
print("=" * 104)
print("STEP 3  NECESSITY  (threshold 0.90)")
print("=" * 104)
print(f"{'condition':12s} {'DEV cons':>9s} {'DEV cov':>8s} | {'EME cons':>9s} {'EME cov':>8s}")
for lab, neg in [('', False), ('~', True)]:
    for k in CONDS:
        out = f"{lab + k:12s}"
        for gi, g in enumerate(['developing', 'emerging']):
            m = grp == g
            F, _ = build(m, 'p95', CONDS)
            X = (1 - F[k]) if neg else F[k]
            c = consis(X, F['GLP']); cv = np.minimum(X, F['GLP']).sum() / X.sum()
            out += f" {c:9.3f} {cv:8.3f} |" if gi == 0 else f" {c:9.3f} {cv:8.3f}"
        print(out)
    print()
print("  necessity for the NEGATED outcome ~GLP")
print(f"{'condition':12s} {'DEV cons':>9s} {'DEV cov':>8s} | {'EME cons':>9s} {'EME cov':>8s}")
for lab, neg in [('', False), ('~', True)]:
    for k in CONDS:
        out = f"{lab + k:12s}"
        for gi, g in enumerate(['developing', 'emerging']):
            m = grp == g
            F, _ = build(m, 'p95', CONDS)
            X = (1 - F[k]) if neg else F[k]
            c = consis(X, 1 - F['GLP']); cv = np.minimum(X, 1 - F['GLP']).sum() / X.sum()
            out += f" {c:9.3f} {cv:8.3f} |" if gi == 0 else f" {c:9.3f} {cv:8.3f}"
        print(out)
    print()

print("=" * 104)
print("STEP 4  TRUTH TABLE  freq>=3, raw consistency 0.80, PRI 0.50")
print("=" * 104)
SOLS = {}
for g in ['developing', 'emerging']:
    m = grp == g
    F, _ = build(m, 'p95', CONDS)
    rows, pos, neg, cnt = truthtable(F, CONDS, 3, 0.80)
    print(f"\n  {g}   " + " ".join(f"{c:>5s}" for c in CONDS) + "     n   cons    PRI  out")
    for corner, k, cs, pr, out, keep in rows:
        if not keep: continue
        print("        " + " ".join(f"{b:>5s}" for b in corner) + f" {k:5d} {cs:6.3f} {pr:6.3f}  {out}")
    print(f"    rows above cutoff: {sum(1 for r in rows if r[5])}   coded 1: {len(pos)}   coded 0: {len(neg)}")
    print(f"    STEP 5  solutions")
    for mode in ['complex', 'intermediate', 'parsimonious']:
        sol = solve(F, CONDS, pos, neg, mode)
        SOLS[(g, mode)] = sol
        report(F, CONDS, sol, mode)

print()
print("=" * 104)
print("STEP 6  CORE vs PERIPHERAL  (core = in parsimonious and intermediate; Fiss 2011)")
print("=" * 104)
for g in ['developing', 'emerging']:
    inter = SOLS[(g, 'intermediate')]; pars = SOLS[(g, 'parsimonious')]
    print(f"\n  {g}")
    for t in inter:
        core, periph = [], []
        for i, c in enumerate(CONDS):
            if t[i] == '-': continue
            lit = (c if t[i] == '1' else '~' + c)
            inpars = any(p[i] == t[i] for p in pars)
            (core if inpars else periph).append(lit)
        print(f"    {fmt(t, CONDS):38s} core: {', '.join(core) or '-':28s} peripheral: {', '.join(periph) or '-'}")

print()
print("=" * 104)
print("STEP 7  ROBUSTNESS  calibration x frequency x consistency   (intermediate solution)")
print("=" * 104)
for g in ['developing', 'emerging']:
    m = grp == g
    print(f"\n### {g}")
    print(f"{'calib':6s} {'freq':>4s} {'cons':>5s} {'nterm':>6s} {'solcons':>8s} {'solcov':>7s}  solution")
    for scheme in ['p95', 'p90', 'p80', 'msd', 'p95x']:
        F, _ = build(m, scheme, CONDS)
        for freq in [2, 3, 4]:
            for thr in [0.75, 0.80, 0.85]:
                rows, pos, neg, cnt = truthtable(F, CONDS, freq, thr)
                sol = solve(F, CONDS, pos, neg, 'intermediate')
                if sol:
                    sm = np.zeros(m.sum())
                    for t in sol: sm = np.maximum(sm, tmem(F, t, CONDS))
                    sc = consis(sm, F['GLP']); cv = np.minimum(sm, F['GLP']).sum() / F['GLP'].sum()
                else:
                    sc = cv = 0.0
                txt = " + ".join(fmt(t, CONDS) for t in sol)[:62] or "none"
                print(f"{scheme:6s} {freq:4d} {thr:5.2f} {len(sol):6d} {sc:8.3f} {cv:7.3f}  {txt}")

print()
print("=" * 104)
print("STEP 8  KEY CLAIM STABILITY ACROSS ALL SPECIFICATIONS")
print("=" * 104)
tally = {}
for g in ['developing', 'emerging']:
    m = grp == g
    F0 = None
    hits = defaultdict(int); tot = 0
    for scheme in ['p95', 'p90', 'p80', 'msd', 'p95x']:
        F, _ = build(m, scheme, CONDS)
        for freq in [2, 3, 4]:
            for thr in [0.75, 0.80, 0.85]:
                rows, pos, neg, cnt = truthtable(F, CONDS, freq, thr)
                sol = solve(F, CONDS, pos, neg, 'intermediate')
                if not sol: continue
                tot += 1
                for i, c in enumerate(CONDS):
                    if any(t[i] == '1' for t in sol): hits[c] += 1
                    if any(t[i] == '0' for t in sol): hits['~' + c] += 1
    tally[g] = (hits, tot)
    print(f"\n  {g}: {tot} specifications yielding a solution")
    for c in CONDS:
        print(f"    {c:6s} present in {hits[c]:3d}/{tot} ({100*hits[c]/max(tot,1):3.0f}%)   "
              f"absent in {hits['~'+c]:3d}/{tot} ({100*hits['~'+c]/max(tot,1):3.0f}%)")
