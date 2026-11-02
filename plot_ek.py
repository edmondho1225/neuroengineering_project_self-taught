"""Plot K+ equilibrium potential (E_K) three ways, saved as PNGs.

(a) E_K vs log10(K_out/K_in) straight line (Nernst linearity)
(b) 3D surface: E_K(K_in, K_out)
(c) 2D contour / heatmap: E_K(K_in, K_out)
"""

import numpy as np
import matplotlib.pyplot as plt

from nernst import ek_mv, slope_mv_per_decade

T = 37.0
SLOPE = slope_mv_per_decade(T)

# --- (a) straight line ------------------------------------------------------
K_in_fixed = 140.0
ratio = np.logspace(-2.0, 0.0, 200)        # K_out/K_in from 0.01 to 1
E_a = SLOPE * np.log10(ratio)

phys_ratio = 4.0 / K_in_fixed
phys_E = ek_mv(K_in_fixed, 4.0, T)

fig, ax = plt.subplots(figsize=(6.5, 5))
ax.plot(np.log10(ratio), E_a, color="tab:blue", lw=2)
ax.axhline(0, color="gray", lw=0.8, ls="--")
ax.axvline(0, color="gray", lw=0.8, ls="--")
ax.plot(np.log10(phys_ratio), phys_E, "ro",
        label="physiological K_out=4, K_in=140")
ax.annotate("E_K = %.1f mV" % phys_E,
            xy=(np.log10(phys_ratio), phys_E),
            xytext=(np.log10(phys_ratio) + 0.1, phys_E + 12),
            arrowprops=dict(arrowstyle="->"))
ax.set_xlabel("log10(K_out / K_in)")
ax.set_ylabel("E_K (mV)")
ax.set_title("Nernst line at 37 C  (slope = %.2f mV/decade)" % SLOPE)
ax.legend(loc="lower right")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("plot_a.png", dpi=150)
plt.close(fig)

# --- (b) 3D surface and (c) contour/heatmap ---------------------------------
K_in_grid = np.linspace(100.0, 160.0, 80)
K_out_grid = np.linspace(2.0, 10.0, 80)
K_in_mesh, K_out_mesh = np.meshgrid(K_in_grid, K_out_grid)
E_mesh = SLOPE * np.log10(K_out_mesh / K_in_mesh)

# (b) 3D surface
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection="3d")
surf = ax.plot_surface(K_in_mesh, K_out_mesh, E_mesh, cmap="viridis",
                       edgecolor="none")
ax.set_xlabel("K_in (mmol/L)")
ax.set_ylabel("K_out (mmol/L)")
ax.set_zlabel("E_K (mV)")
ax.set_title("E_K as a function of K_in and K_out (37 C)")
fig.colorbar(surf, ax=ax, shrink=0.6, label="E_K (mV)")
fig.tight_layout()
fig.savefig("plot_b.png", dpi=150)
plt.close(fig)

# (c) contour / heatmap
fig, ax = plt.subplots(figsize=(7, 6))
levels = np.arange(-120, 5, 10)
cf = ax.contourf(K_in_mesh, K_out_mesh, E_mesh, levels=levels, cmap="viridis")
cs = ax.contour(K_in_mesh, K_out_mesh, E_mesh, levels=levels,
                colors="black", linewidths=0.5)
ax.clabel(cs, fmt="%d mV", fontsize=7)
ax.plot(140.0, 4.0, "ro")
ax.annotate("K_in=140, K_out=4\nE=%.1f mV" % phys_E, xy=(140.0, 4.0),
            xytext=(118.0, 8.0), arrowprops=dict(arrowstyle="->"))
ax.set_xlabel("K_in (mmol/L)")
ax.set_ylabel("K_out (mmol/L)")
ax.set_title("E_K (mV) contour map (37 C)")
fig.colorbar(cf, ax=ax, label="E_K (mV)")
fig.tight_layout()
fig.savefig("plot_c.png", dpi=150)
plt.close(fig)

print("Saved plot_a.png, plot_b.png, plot_c.png")
