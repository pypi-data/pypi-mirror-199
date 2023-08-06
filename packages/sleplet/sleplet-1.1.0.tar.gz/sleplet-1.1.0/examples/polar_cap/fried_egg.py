import numpy as np

from sleplet import logger
from sleplet.functions.fp.slepian import Slepian
from sleplet.plotting.create_plot_sphere import Plot
from sleplet.utils.region import Region
from sleplet.utils.slepian_methods import slepian_inverse

L = 16
NORMALISE = False
RANKS = 16
THETA_MAX = 40


def main() -> None:
    """
    create fig 5.4 from Spatiospectral Concentration on a Sphere by Simons et al 2006
    """
    region = Region(theta_max=np.deg2rad(THETA_MAX))
    for r in range(RANKS):
        logger.info(f"plotting rank={r}")
        slepian_function = Slepian(L, rank=r, region=region)
        f = slepian_inverse(slepian_function.coefficients, L, slepian_function.slepian)
        Plot(
            f,
            L,
            slepian_function.name,
            normalise=NORMALISE,
            region=slepian_function.region,
        ).execute()


if __name__ == "__main__":
    main()
