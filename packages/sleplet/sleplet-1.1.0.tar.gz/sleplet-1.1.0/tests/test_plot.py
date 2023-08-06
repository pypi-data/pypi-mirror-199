import cmocean
import numpy as np
from numpy.testing import assert_equal

from sleplet.utils.plot_methods import (
    calc_nearest_grid_point,
    calc_plot_resolution,
    convert_colourscale,
)

L = 128
PHI_0 = np.pi / 6
PL_ENTRIES = 255
THETA_MAX = np.pi / 3


def test_resolution_values() -> None:
    """
    verifies the correct resolution is chosen for a given bandlimit
    """
    arguments = [1, 10, 100, 1000]
    output = [64, 80, 800, 2000]
    for c, arg in enumerate(arguments):
        assert_equal(calc_plot_resolution(arg), output[c])


def test_create_colourscale() -> None:
    """
    test creates a plotly compatible colourscale
    """
    colourscale = convert_colourscale(cmocean.cm.ice, pl_entries=PL_ENTRIES)
    assert_equal(len(colourscale), PL_ENTRIES)


def test_find_nearest_grid_point() -> None:
    """
    test to find nearest grid point to provided angles
    """
    alpha, beta = calc_nearest_grid_point(L, PHI_0 / np.pi, THETA_MAX / np.pi)
    assert_equal(alpha, 0.5154175447295755)
    assert_equal(beta, 1.055378782065321)
