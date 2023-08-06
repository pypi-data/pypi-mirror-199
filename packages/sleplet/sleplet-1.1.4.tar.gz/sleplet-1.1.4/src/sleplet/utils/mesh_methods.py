from pathlib import Path

import numpy as np
import tomli
from igl import average_onto_faces, cotmatrix, read_triangle_mesh, upsample
from numpy import typing as npt
from scipy.sparse import linalg as LA_sparse  # noqa: N812

from sleplet import logger
from sleplet.data.setup_pooch import find_on_pooch_then_local
from sleplet.utils.integration_methods import integrate_whole_mesh

_data_path = Path(__file__).resolve().parents[1] / "data"


def average_functions_on_vertices_to_faces(
    faces: npt.NDArray[np.int_],
    functions_on_vertices: npt.NDArray[np.complex_ | np.float_],
) -> npt.NDArray[np.float_]:
    """
    the integrals require all functions to be defined on faces
    this method handles an arbitrary number of functions
    """
    logger.info("converting function on vertices to faces")
    # handle the case of a 1D array
    array_is_1d = len(functions_on_vertices.shape) == 1
    if array_is_1d:
        functions_on_vertices = functions_on_vertices.reshape(1, -1)

    functions_on_faces = np.zeros((functions_on_vertices.shape[0], faces.shape[0]))
    for i, f in enumerate(functions_on_vertices):
        functions_on_faces[i] = average_onto_faces(faces, f)

    # put the vector back in 1D form
    if array_is_1d:
        functions_on_faces = functions_on_faces.reshape(-1)
    return functions_on_faces


def create_mesh_region(
    mesh_config: dict, vertices: npt.NDArray[np.float_]
) -> npt.NDArray[np.bool_]:
    """
    creates the boolean region for the given mesh
    """
    return (
        (vertices[:, 0] >= mesh_config["XMIN"])
        & (vertices[:, 0] <= mesh_config["XMAX"])
        & (vertices[:, 1] >= mesh_config["YMIN"])
        & (vertices[:, 1] <= mesh_config["YMAX"])
        & (vertices[:, 2] >= mesh_config["ZMIN"])
        & (vertices[:, 2] <= mesh_config["ZMAX"])
    )


def extract_mesh_config(mesh_name: str) -> dict:
    """
    reads in the given mesh region settings file
    """
    with open(_data_path / f"meshes_regions_{mesh_name}.toml", "rb") as f:
        return tomli.load(f)


def mesh_eigendecomposition(
    name: str,
    vertices: npt.NDArray[np.float_],
    faces: npt.NDArray[np.int_],
    *,
    number_basis_functions: int | None = None,
) -> tuple[npt.NDArray[np.float_], npt.NDArray[np.float_], int]:
    """
    computes the eigendecomposition of the mesh represented
    as a graph if already computed then it loads the data
    """
    # determine number of basis functions
    if number_basis_functions is None:
        number_basis_functions = vertices.shape[0] // 4
    logger.info(
        f"finding {number_basis_functions}/{vertices.shape[0]} "
        f"basis functions of {name} mesh"
    )

    # create filenames
    eigd_loc = f"meshes_laplacians_basis_functions_{name}_b{number_basis_functions}"
    eval_loc = f"{eigd_loc}_eigenvalues.npy"
    evec_loc = f"{eigd_loc}_eigenvectors.npy"

    try:
        eigenvalues = np.load(find_on_pooch_then_local(eval_loc))
        eigenvectors = np.load(find_on_pooch_then_local(evec_loc))
    except TypeError:
        laplacian = _mesh_laplacian(vertices, faces)
        eigenvalues, eigenvectors = LA_sparse.eigsh(
            laplacian, k=number_basis_functions, which="LM", sigma=0
        )
        eigenvectors = _orthonormalise_basis_functions(vertices, faces, eigenvectors.T)
        logger.info("saving binaries...")
        np.save(_data_path / eval_loc, eigenvalues)
        np.save(_data_path / evec_loc, eigenvectors)
    return eigenvalues, eigenvectors, number_basis_functions


def read_mesh(mesh_config: dict) -> tuple[npt.NDArray[np.float_], npt.NDArray[np.int_]]:
    """
    reads in the given mesh
    """
    vertices, faces = read_triangle_mesh(
        str(_data_path / f"meshes_polygons_{mesh_config['FILENAME']}")
    )
    return upsample(vertices, faces, number_of_subdivs=mesh_config["UPSAMPLE"])


def _mesh_laplacian(
    vertices: npt.NDArray[np.float_], faces: npt.NDArray[np.int_]
) -> npt.NDArray[np.float_]:
    """
    computes the cotagent mesh laplacian
    """
    return -cotmatrix(vertices, faces)


def _orthonormalise_basis_functions(
    vertices: npt.NDArray[np.float_],
    faces: npt.NDArray[np.int_],
    basis_functions: npt.NDArray[np.float_],
) -> npt.NDArray[np.float_]:
    """
    for computing the Slepian D matrix the basis functions must be orthonormal
    """
    logger.info("orthonormalising basis functions")
    factor = np.zeros(basis_functions.shape[0])
    for i, phi_i in enumerate(basis_functions):
        factor[i] = integrate_whole_mesh(vertices, faces, phi_i, phi_i)
    normalisation = np.sqrt(factor).reshape(-1, 1)
    return basis_functions / normalisation
