from pathlib import Path

import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from scipy.interpolate import pchip

from sleplet.utils.plot_methods import save_plot
from sleplet.utils.wavelet_methods import create_kappas

fig_path = Path(__file__).resolve().parents[2] / "src" / "sleplet" / "figures"
sns.set(context="paper")

B = 3
J_MIN = 2
L = 128
STEP = 0.01


def main() -> None:
    """
    plots the tiling of the harmonic line
    """
    xlim = L
    x = np.arange(xlim)
    xi = np.arange(0, xlim - 1 + STEP, STEP)
    kappas = create_kappas(xlim, B, J_MIN)
    yi = pchip(x, kappas[0])
    plt.semilogx(xi, yi(xi), label=r"$\Phi_{\ell0}$")
    for j, k in enumerate(kappas[1:]):
        yi = pchip(x, k)
        plt.semilogx(xi, yi(xi), label=rf"$\Psi^{{{j+J_MIN}}}_{{\ell0}}$")
    plt.xlim(1, xlim)
    ticks = 2 ** np.arange(np.log2(xlim) + 1, dtype=int)
    plt.xticks(ticks, ticks)
    plt.xlabel(r"$\ell$")
    plt.legend(loc=6)
    save_plot(fig_path, f"axisymmetric_tiling_L{L}")


if __name__ == "__main__":
    main()
