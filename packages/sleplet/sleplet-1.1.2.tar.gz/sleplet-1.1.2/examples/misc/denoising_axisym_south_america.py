from sleplet.functions.flm.axisymmetric_wavelets import AxisymmetricWavelets
from sleplet.functions.flm.south_america import SouthAmerica
from sleplet.plotting.create_plot_sphere import Plot
from sleplet.utils.denoising import denoising_axisym
from sleplet.utils.plot_methods import find_max_amplitude

B = 2
J_MIN = 0
L = 128
N_SIGMA = 3
NORMALISE = False
SNR_IN = 10


def main() -> None:
    """
    contrast denosiing with an Earth map versus South America map
    """
    # create map & noised map
    fun = SouthAmerica(L)
    fun_noised = SouthAmerica(L, noise=SNR_IN)

    # create wavelets
    aw = AxisymmetricWavelets(L, B=B, j_min=J_MIN)

    # fix amplitude
    amplitude = find_max_amplitude(fun)

    f, _, _ = denoising_axisym(fun, fun_noised, aw, SNR_IN, N_SIGMA)
    name = f"{fun.name}_denoised_axisym"
    Plot(f, L, name, amplitude=amplitude, normalise=NORMALISE).execute()


if __name__ == "__main__":
    main()
