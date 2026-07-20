"""
A3 statistical analysis - Group 19 (Flocking: separation weight vs. ANND)

Design note: the SAME 10 seeds are used in every condition, so each seed is a
matched starting configuration measured under all five separation weights.
That makes this a WITHIN-SUBJECTS (repeated-measures) design, not independent
groups -- so we use the repeated-measures form of the ANOVA, confirm it with
the non-parametric Friedman test, and use PAIRED pairwise tests.
"""

import numpy as np
from scipy import stats
from itertools import combinations

# --- Raw results: separation weight -> ANND per seed (seed order 0..9) ---
results = {
    0.1: [18.50, 17.92, 20.28, 20.48, 16.83, 20.49, 12.73, 25.34, 17.97, 17.60],
    0.3: [19.52, 19.63, 21.38, 21.57, 18.82, 21.57, 17.75, 26.83, 19.62, 18.97],
    0.5: [20.69, 21.21, 22.22, 21.72, 20.59, 23.15, 16.34, 27.81, 21.48, 20.03],
    0.7: [20.85, 20.43, 23.29, 24.38, 20.23, 24.10, 18.84, 28.15, 24.71, 20.10],
    1.0: [22.52, 23.96, 27.81, 26.69, 24.72, 25.62, 23.32, 27.53, 27.94, 22.10],
}
conds = list(results.keys())
M = np.array([results[c] for c in conds])      # 5 conditions x 10 seeds
k, n = M.shape

# --- 1. Summary statistics (sample SD, ddof=1) ---
print("=" * 60, "\nSUMMARY (sample SD)\n", "=" * 60, sep="")
for c in conds:
    d = np.array(results[c])
    print(f"sep={c}  mean={d.mean():6.2f}  sd={d.std(ddof=1):5.2f}  "
          f"min={d.min():.2f}  max={d.max():.2f}")

# --- 2. Justify repeated-measures: are conditions correlated across seeds? ---
print("\n" + "=" * 60, "\nMATCHED-DESIGN CHECK (Pearson r across seeds)\n", "=" * 60, sep="")
print("Near 0 = independent; high = matched by seed (=> repeated-measures).")
for a, b in combinations(conds, 2):
    r, _ = stats.pearsonr(results[a], results[b])
    print(f"  {a} vs {b}: r = {r:.2f}")

# --- 3. Assumption checks ---
print("\n" + "=" * 60, "\nASSUMPTION CHECKS\n", "=" * 60, sep="")
resid = np.concatenate([np.array(results[c]) - np.mean(results[c]) for c in conds])
W, pW = stats.shapiro(resid)
L, pL = stats.levene(*[results[c] for c in conds])
print(f"Shapiro-Wilk (normality of residuals): W={W:.3f}, p={pW:.4f}")
print(f"Levene (equal variances):              stat={L:.3f}, p={pL:.4f}")

# --- 4. Omnibus tests ---
print("\n" + "=" * 60, "\nOMNIBUS TESTS\n", "=" * 60, sep="")

# 4a. Repeated-measures ANOVA (computed directly; partitions out seed variance)
grand = M.mean()
SS_total = ((M - grand) ** 2).sum()
SS_cond = n * ((M.mean(axis=1) - grand) ** 2).sum()
SS_subj = k * ((M.mean(axis=0) - grand) ** 2).sum()
SS_err = SS_total - SS_cond - SS_subj
df_cond, df_err = k - 1, (k - 1) * (n - 1)
F_rm = (SS_cond / df_cond) / (SS_err / df_err)
p_rm = stats.f.sf(F_rm, df_cond, df_err)
print(f"Repeated-measures ANOVA: F({df_cond},{df_err}) = {F_rm:.2f}, p = {p_rm:.2e}")

# 4b. Non-parametric backup (robust to the mild non-normality)
chi, p_fr = stats.friedmanchisquare(*[results[c] for c in conds])
print(f"Friedman (non-parametric backup): chi2 = {chi:.2f}, p = {p_fr:.2e}")

# 4c. Independent one-way ANOVA (the A2 plan) for transparency / comparison
F_i, p_i = stats.f_oneway(*[results[c] for c in conds])
print(f"[for comparison] independent one-way ANOVA: F = {F_i:.2f}, p = {p_i:.2e}")

# --- 5. Pairwise: paired Wilcoxon (non-parametric), Bonferroni corrected ---
print("\n" + "=" * 60, "\nPAIRWISE (paired Wilcoxon, Bonferroni x10)\n", "=" * 60, sep="")
m = len(list(combinations(conds, 2)))
for a, b in combinations(conds, 2):
    _, p = stats.wilcoxon(results[a], results[b])
    cp = min(p * m, 1.0)
    print(f"  {a} vs {b}:  p = {p:.4f}   corrected = {cp:.4f}   "
          f"{'SIGNIFICANT' if cp < 0.05 else 'n.s.'}")

# --- 6. Trend: regression of ANND on separation weight (all 50 points) ---
print("\n" + "=" * 60, "\nTREND (linear regression, all runs)\n", "=" * 60, sep="")
xs = np.concatenate([[c] * n for c in conds])
ys = M.flatten()
sl, ic, r, p, se = stats.linregress(xs, ys)
print(f"slope = {sl:.2f} px per unit separation weight, R^2 = {r**2:.2f}, p = {p:.2e}")
