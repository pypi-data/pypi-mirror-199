import numpy as np
import pyssht as ssht
from numpy import typing as npt

from sleplet import logger
from sleplet.meshes.classes.mesh_slepian import MeshSlepian
from sleplet.meshes.classes.mesh_slepian_decomposition import MeshSlepianDecomposition
from sleplet.slepian.slepian_decomposition import SlepianDecomposition
from sleplet.slepian.slepian_functions import SlepianFunctions
from sleplet.slepian.slepian_region.slepian_arbitrary import SlepianArbitrary
from sleplet.slepian.slepian_region.slepian_limit_lat_lon import SlepianLimitLatLon
from sleplet.slepian.slepian_region.slepian_polar_cap import SlepianPolarCap
from sleplet.utils.harmonic_methods import boost_coefficient_resolution, mesh_inverse
from sleplet.utils.region import Region
from sleplet.utils.vars import SAMPLING_SCHEME


def choose_slepian_method(L: int, region: Region) -> SlepianFunctions:
    """
    initialise Slepian object depending on input
    """
    match region.region_type:
        case "polar":
            logger.info("polar cap region detected")
            return SlepianPolarCap(L, region.theta_max, gap=region.gap)

        case "lim_lat_lon":
            logger.info("limited latitude longitude region detected")
            return SlepianLimitLatLon(
                L,
                theta_min=region.theta_min,
                theta_max=region.theta_max,
                phi_min=region.phi_min,
                phi_max=region.phi_max,
            )

        case "arbitrary":
            logger.info("mask specified in file detected")
            return SlepianArbitrary(L, region.mask_name)

        case _:
            raise ValueError(f"{region.region_type} is an invalid region type")


def slepian_inverse(
    f_p: npt.NDArray[np.complex_ | np.float_], L: int, slepian: SlepianFunctions
) -> npt.NDArray[np.complex_]:
    """
    computes the Slepian inverse transform up to the Shannon number
    """
    f_p_reshape = f_p[: slepian.N, np.newaxis, np.newaxis]
    s_p = compute_s_p_omega(L, slepian)
    return (f_p_reshape * s_p).sum(axis=0)


def slepian_forward(
    L: int,
    slepian: SlepianFunctions,
    *,
    f: npt.NDArray[np.complex_] | None = None,
    flm: npt.NDArray[np.complex_ | np.float_] | None = None,
    mask: npt.NDArray[np.float_] | None = None,
    n_coeffs: int | None = None,
) -> npt.NDArray[np.complex_]:
    """
    computes the Slepian forward transform for all coefficients
    """
    sd = SlepianDecomposition(L, slepian, f=f, flm=flm, mask=mask)
    n_coeffs = slepian.N if n_coeffs is None else n_coeffs
    return sd.decompose_all(n_coeffs)


def compute_s_p_omega(L: int, slepian: SlepianFunctions) -> npt.NDArray[np.complex_]:
    """
    method to calculate Sp(omega) for a given region
    """
    n_theta, n_phi = ssht.sample_shape(L, Method=SAMPLING_SCHEME)
    sp = np.zeros((slepian.N, n_theta, n_phi), dtype=np.complex_)
    for p in range(slepian.N):
        if p % L == 0:
            logger.info(f"compute Sp(omega) p={p+1}/{slepian.N}")
        sp[p] = ssht.inverse(slepian.eigenvectors[p], L, Method=SAMPLING_SCHEME)
    return sp


def compute_s_p_omega_prime(
    L: int, alpha: float, beta: float, slepian: SlepianFunctions
) -> npt.NDArray[np.complex_]:
    """
    method to pick out the desired angle from Sp(omega)
    """
    sp_omega = compute_s_p_omega(L, slepian)
    p = ssht.theta_to_index(beta, L, Method=SAMPLING_SCHEME)
    q = ssht.phi_to_index(alpha, L, Method=SAMPLING_SCHEME)
    sp_omega_prime = sp_omega[:, p, q]
    # pad with zeros so it has the expected shape
    boost = L**2 - slepian.N
    return boost_coefficient_resolution(sp_omega_prime, boost)


def slepian_mesh_forward(
    mesh_slepian: MeshSlepian,
    *,
    u: npt.NDArray[np.complex_ | np.float_] | None = None,
    u_i: npt.NDArray[np.complex_ | np.float_] | None = None,
    mask: bool = False,
    n_coeffs: int | None = None,
) -> npt.NDArray[np.float_]:
    """
    computes the Slepian forward transform for all coefficients
    """
    sd = MeshSlepianDecomposition(
        mesh_slepian,
        u=u,
        u_i=u_i,
        mask=mask,
    )
    n_coeffs = mesh_slepian.N if n_coeffs is None else n_coeffs
    return sd.decompose_all(n_coeffs)


def slepian_mesh_inverse(
    mesh_slepian: MeshSlepian,
    f_p: npt.NDArray[np.complex_ | np.float_],
) -> npt.NDArray[np.complex_ | np.float_]:
    """
    computes the Slepian inverse transform on the mesh up to the Shannon number
    """
    f_p_reshape = f_p[: mesh_slepian.N, np.newaxis]
    s_p = compute_mesh_s_p_pixel(mesh_slepian)
    return (f_p_reshape * s_p).sum(axis=0)


def compute_mesh_s_p_pixel(mesh_slepian: MeshSlepian) -> npt.NDArray[np.float_]:
    """
    method to calculate Sp(omega) for a given region
    """
    sp = np.zeros((mesh_slepian.N, mesh_slepian.mesh.vertices.shape[0]))
    for p in range(mesh_slepian.N):
        sp[p] = mesh_inverse(mesh_slepian.mesh, mesh_slepian.slepian_functions[p])
    return sp
