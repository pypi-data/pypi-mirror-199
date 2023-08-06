import numpy as np
from numpy import typing as npt
from pydantic.dataclasses import dataclass

from sleplet.meshes.harmonic_coefficients.mesh_field import MeshField
from sleplet.meshes.mesh_harmonic_coefficients import MeshHarmonicCoefficients
from sleplet.utils.noise import compute_snr, create_mesh_noise
from sleplet.utils.string_methods import filename_args
from sleplet.utils.validation import Validation


@dataclass(config=Validation, kw_only=True)
class MeshNoiseField(MeshHarmonicCoefficients):
    SNR: float = 10

    def __post_init_post_parse__(self) -> None:
        super().__post_init_post_parse__()

    def _create_coefficients(self) -> npt.NDArray[np.complex_ | np.float_]:
        mf = MeshField(self.mesh)
        noise = create_mesh_noise(mf.coefficients, self.SNR)
        compute_snr(mf.coefficients, noise, "Harmonic")
        return noise

    def _create_name(self) -> str:
        return f"{self.mesh.name}_noise_field{filename_args(self.SNR, 'snr')}"

    def _set_reality(self) -> bool:
        return True

    def _set_spin(self) -> int:
        return 0

    def _setup_args(self) -> None:
        if isinstance(self.extra_args, list):
            num_args = 1
            if len(self.extra_args) != num_args:
                raise ValueError(f"The number of extra arguments should be {num_args}")
            self.SNR = self.extra_args[0]
