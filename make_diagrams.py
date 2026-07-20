"""
Three diagrams for the A3 slides (Group 19):
  diagram_variance.png        - slide 5: why repeated-measures (variance partition)
  diagram_pairwise.png        - slide 6: which conditions differ (paired Wilcoxon, Bonferroni)
  diagram_interpretation.png  - slide 7: what increasing ANND looks like (cohesive -> dispersed)

Run: python make_diagrams.py   (needs numpy + matplotlib)
"""
import numpy as np
import matplotlib.pyplot as plt

DARK = "#222222"

# ANND per seed (seed order 0..9) for each separation weight
results = {
    0.1: [18.50, 17.92, 20.28, 20.48, 16.83, 20.49, 12.73, 25.34, 17.97, 17.60],
    0.3: [19.52, 19.63, 21.38, 21.57, 18.82, 21.57, 17.75, 26.83, 19.62, 18.97],
    0.5: [20.69, 21.21, 22.22, 21.72, 20.59, 23.15, 16.34, 27.81, 21.48, 20.03],
    0.7: [20.85, 20.43, 23.29, 24.38, 20.23, 24.10, 18.84, 28.15, 24.71, 20.10],
    1.0: [22.52, 23.96, 27.81, 26.69, 24.72, 25.62, 23.32, 27.53, 27.94, 22.10],
}
conds = list(results.keys())


def variance_partition():
    """Justifies repeated-measures: most variance is between seeds, which RM removes."""
    sep, seed, resid = 226.9, 294.0, 51.2          # SS components
    parts = np.array([sep, seed, resid]); parts = parts / parts.sum() * 100
    fig, ax = plt.subplots(figsize=(9, 3.4))
    colors = ['#4F9DDE', '#E0A458', '#9aa0a6']
    names = ['Separation\neffect', 'Between-seed\nvariance', 'Residual']
    left = 0
    for p, c, nm in zip(parts, colors, names):
        ax.barh(0, p, left=left, color=c, edgecolor='white', height=0.5)
        ax.text(left + p / 2, 0, f"{p:.0f}%", ha='center', va='center', color='white', fontsize=13, fontweight='bold')
        ax.text(left + p / 2, -0.40, nm, ha='center', va='top', color=DARK, fontsize=10)
        left += p
    ax.text(50, 0.75, "Same seeds reused in every condition \u2192 over half the variance is just between seeds",
            ha='center', color=DARK, fontsize=11, fontweight='bold')
    ax.text(50, -0.95, "Independent ANOVA leaves seed variance in the error term  \u2192  F = 7.4",
            ha='center', color='#8a6d3b', fontsize=10.5)
    ax.text(50, -1.18, "Repeated-measures ANOVA removes it  \u2192  F = 39.9",
            ha='center', color='#1f6f3f', fontsize=10.5, fontweight='bold')
    ax.set_xlim(0, 100); ax.set_ylim(-1.35, 1.0); ax.axis('off')
    fig.tight_layout(); fig.savefig('diagram_variance.png', dpi=200); plt.close(fig)


def pairwise_matrix():
    """Which conditions differ. NS = the two smallest middle steps."""
    NS = {(2, 1), (3, 2)}          # (row i, col j) with i > j that are NOT significant
    n = len(conds)
    fig, ax = plt.subplots(figsize=(6, 5.6))
    for i in range(n):
        for j in range(n):
            if i > j:
                sig = (i, j) not in NS
                ax.add_patch(plt.Rectangle((j, n - 1 - i), 1, 1,
                             facecolor='#3FA66A' if sig else '#b9bdc1', edgecolor='white', lw=1.6))
                ax.text(j + 0.5, n - 1 - i + 0.5, '\u2713' if sig else 'n.s.', ha='center', va='center',
                        color='white', fontsize=15 if sig else 10, fontweight='bold')
            elif i == j:
                ax.add_patch(plt.Rectangle((j, n - 1 - i), 1, 1, facecolor='#f0f0f0', edgecolor='white', lw=1.6))
    ax.set_xlim(0, n); ax.set_ylim(0, n); ax.set_aspect('equal')
    ax.set_xticks([k + 0.5 for k in range(n)]); ax.set_xticklabels(conds, color=DARK)
    ax.set_yticks([k + 0.5 for k in range(n)]); ax.set_yticklabels(conds[::-1], color=DARK)
    ax.set_xlabel("Separation weight", color=DARK); ax.set_ylabel("Separation weight", color=DARK)
    ax.tick_params(colors=DARK, length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title("Pairwise differences (paired Wilcoxon, Bonferroni)\n8 / 10 pairs significant", color=DARK, fontsize=12)
    fig.tight_layout(); fig.savefig('diagram_pairwise.png', dpi=200); plt.close(fig)


def interpretation():
    """What increasing ANND means: the flock goes from cohesive to dispersed."""
    rng = np.random.default_rng(3)
    fig, axs = plt.subplots(1, 3, figsize=(11, 4.2))
    spreads = [1.0, 1.5, 2.15]
    titles = ['Low separation (w = 0.1)\nANND \u2248 18.8 px  \u2014  cohesive',
              'Medium (w = 0.5)\nANND \u2248 21.5 px',
              'High separation (w = 1.0)\nANND \u2248 25.2 px  \u2014  dispersed']
    for ax, sp, t in zip(axs, spreads, titles):
        pts = rng.normal(0, sp, size=(45, 2))
        ax.scatter(pts[:, 0], pts[:, 1], s=35, color='#4F9DDE', edgecolor='white', linewidth=0.5, alpha=0.95)
        ax.set_xlim(-6, 6); ax.set_ylim(-6, 6); ax.set_aspect('equal'); ax.axis('off')
        ax.set_title(t, color=DARK, fontsize=10.5)
    fig.suptitle('Increasing separation weight spreads the flock out', color=DARK, fontsize=12, y=1.02)
    fig.tight_layout(); fig.savefig('diagram_interpretation.png', dpi=200, bbox_inches='tight'); plt.close(fig)


if __name__ == "__main__":
    variance_partition()
    pairwise_matrix()
    interpretation()
    print("Saved diagram_variance.png, diagram_pairwise.png, diagram_interpretation.png")
