import numpy as np
import matplotlib.pyplot as plt

# ANND per seed (seed order 0..9) for each separation weight
results = {
    0.1: [18.50, 17.92, 20.28, 20.48, 16.83, 20.49, 12.73, 25.34, 17.97, 17.60],
    0.3: [19.52, 19.63, 21.38, 21.57, 18.82, 21.57, 17.75, 26.83, 19.62, 18.97],
    0.5: [20.69, 21.21, 22.22, 21.72, 20.59, 23.15, 16.34, 27.81, 21.48, 20.03],
    0.7: [20.85, 20.43, 23.29, 24.38, 20.23, 24.10, 18.84, 28.15, 24.71, 20.10],
    1.0: [22.52, 23.96, 27.81, 26.69, 24.72, 25.62, 23.32, 27.53, 27.94, 22.10],
}

x = list(results.keys())
M = np.array([results[c] for c in x])        # 5 conditions x 10 seeds
means = M.mean(axis=1)
sds = M.std(axis=1, ddof=1)                   # sample SD

fig, ax = plt.subplots(figsize=(8, 5))

# faint line per seed (each seed across the five conditions)
for seed in range(M.shape[1]):
    ax.plot(x, M[:, seed], color='grey', alpha=0.35, lw=1, marker='o', ms=3, zorder=1)

# bold mean +/- SD on top
ax.errorbar(x, means, yerr=sds, fmt='o-', color='steelblue', lw=2.5,
            capsize=5, ms=7, zorder=3, label='Mean \u00b1 SD (n=10)')
ax.plot([], [], color='grey', alpha=0.5, lw=1, label='Individual seeds')

ax.set_xlabel("Separation Weight")
ax.set_ylabel("Average Nearest-Neighbour Distance (px)")
ax.set_title("Effect of Separation Weight on Flock Cohesion")
ax.set_xticks(x)
ax.grid(True, ls='--', alpha=0.5)
ax.legend(frameon=False)

plt.tight_layout()
plt.savefig("results_per_seed.png", dpi=150)
plt.show()
print("Saved results_per_seed.png")
