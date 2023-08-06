from argparse import ArgumentParser

import numpy as np

from sleplet import logger
from sleplet.meshes.classes.mesh import Mesh
from sleplet.meshes.slepian_coefficients.mesh_slepian_field import MeshSlepianField
from sleplet.meshes.slepian_coefficients.mesh_slepian_wavelets import (
    MeshSlepianWavelets,
)
from sleplet.plotting.create_plot_mesh import Plot
from sleplet.scripts.plotting_on_mesh import valid_meshes
from sleplet.utils.class_lists import MESHES
from sleplet.utils.denoising import denoising_mesh_slepian
from sleplet.utils.slepian_methods import slepian_mesh_inverse
from sleplet.utils.string_methods import filename_args

B = 3
J_MIN = 2
N_SIGMA = 1
NORMALISE = False
SNR_IN = -5


def main(mesh_name: str, snr: float, sigma: int) -> None:
    """
    denoising demo using Slepian wavelets
    """
    logger.info(f"SNR={snr}, n_sigma={sigma}")
    # setup
    mesh = Mesh(mesh_name, zoom=True)

    # create map & noised map
    fun = MeshSlepianField(mesh)
    fun_noised = MeshSlepianField(mesh, noise=snr)

    # create wavelets
    smw = MeshSlepianWavelets(mesh, B=B, j_min=J_MIN)

    # fix amplitude
    amplitude = np.abs(
        slepian_mesh_inverse(fun_noised.mesh_slepian, fun.coefficients)
    ).max()

    f = denoising_mesh_slepian(fun, fun_noised, smw, snr, sigma)
    name = f"{mesh_name}{filename_args(snr, 'snr')}{filename_args(sigma,'n')}_denoised"
    Plot(mesh, name, f, amplitude=amplitude, normalise=NORMALISE, region=True).execute()


if __name__ == "__main__":
    parser = ArgumentParser(description="denoising")
    parser.add_argument(
        "function",
        type=valid_meshes,
        choices=MESHES,
        help="mesh to plot",
    )
    parser.add_argument(
        "--noise",
        "-n",
        type=int,
        default=SNR_IN,
    )
    parser.add_argument(
        "--sigma",
        "-s",
        type=int,
        default=N_SIGMA,
    )
    args = parser.parse_args()
    main(args.function, args.noise, args.sigma)
