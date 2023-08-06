from pathlib import Path

import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

from sleplet.slepian.slepian_region.slepian_arbitrary import SlepianArbitrary
from sleplet.utils.plot_methods import save_plot

fig_path = Path(__file__).resolve().parents[2] / "src" / "sleplet" / "figures"
sns.set(context="paper")

COLOURS = ["b", "k"]
L = 128
REGIONS = ["africa", "south_america"]
X_POS = [19, -16]
ZORDER = [2, 1]


def main() -> None:
    """
    plots the tiling of the Slepian line
    """
    for c, region in enumerate(REGIONS):
        slepian = SlepianArbitrary(L, region)
        p_range = np.arange(0, L**2)
        plt.semilogx(
            p_range,
            slepian.eigenvalues,
            f"{COLOURS[c]}.",
            label=" ".join(region.title().split("_")),
            zorder=ZORDER[c],
        )
        plt.axvline(slepian.N, color=COLOURS[c], ls="--", alpha=0.8)
        plt.annotate(
            f"N={slepian.N}",
            xy=(slepian.N, 1),
            xytext=(X_POS[c], 3),
            ha="center",
            textcoords="offset points",
            annotation_clip=False,
            color=COLOURS[c],
        )
    ticks = 2 ** np.arange(np.log2(L**2) + 1, dtype=int)
    plt.xticks(ticks, ticks)
    plt.xlabel(r"$p$")
    plt.ylabel(r"$\mu$")
    plt.legend(loc=3)
    save_plot(fig_path, f"combined_eigenvalues_L{L}")


if __name__ == "__main__":
    main()
