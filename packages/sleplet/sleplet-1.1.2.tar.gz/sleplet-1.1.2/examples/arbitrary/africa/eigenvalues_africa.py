from pathlib import Path

import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

from sleplet.slepian.slepian_region.slepian_arbitrary import SlepianArbitrary
from sleplet.utils.plot_methods import save_plot

fig_path = Path(__file__).resolve().parents[3] / "src" / "sleplet" / "figures"
sns.set(context="paper")

L = 128


def main() -> None:
    """
    plots the tiling of the Slepian line
    """
    slepian = SlepianArbitrary(L, "africa")
    p_range = np.arange(0, L**2)
    plt.semilogx(p_range, slepian.eigenvalues, "k.")
    plt.axvline(slepian.N, c="k", ls="--", alpha=0.8)
    plt.annotate(
        f"N={slepian.N}",
        xy=(slepian.N, 1),
        xytext=(19, 3),
        ha="center",
        textcoords="offset points",
        annotation_clip=False,
    )
    ticks = 2 ** np.arange(np.log2(L**2) + 1, dtype=int)
    plt.xticks(ticks, ticks)
    plt.xlabel(r"$p$")
    plt.ylabel(r"$\mu$")
    save_plot(fig_path, f"africa_eigenvalues_L{L}")


if __name__ == "__main__":
    main()
