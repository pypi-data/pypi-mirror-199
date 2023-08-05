from typing import Optional, Sequence, Dict
import numpy
from skimage.transform import warp
from skimage.transform import EuclideanTransform
from skimage.transform import SimilarityTransform
from skimage.transform import AffineTransform
from skimage.transform import ProjectiveTransform
from .homography import Homography
from .lstsq import calc_translation

__all__ = ["SciKitImageHomography"]


class ShiftTransform(ProjectiveTransform):
    def __init__(self, matrix=None, translation=None, dimensionality=2):
        params_given = translation is not None

        if params_given and matrix is not None:
            raise ValueError(
                "You cannot specify the transformation matrix and"
                " the implicit parameters at the same time."
            )
        elif matrix is not None:
            if matrix.shape[0] != matrix.shape[1]:
                raise ValueError("Invalid shape of transformation matrix.")
            self.params = matrix
        elif params_given:
            if translation is None:
                translation = (0,) * dimensionality
            self.params[0:dimensionality, dimensionality] = translation
        else:
            # default to an identity transform
            self.params = numpy.eye(dimensionality + 1)

    def estimate(self, src: numpy.ndarray, dst: numpy.ndarray) -> bool:
        self.params[...] = calc_translation(src.T, dst.T)

    @property
    def translation(self):
        return self.params[0:2, 2]


class SciKitImageHomography(
    Homography, registry_id=Homography.RegistryId("Homography", "SciKitImage")
):
    def __init__(self, *args, warp_options: Optional[Dict] = None, **kw) -> None:
        if warp_options is None:
            warp_options = dict()
        self._warp_options = warp_options

        super().__init__(*args, **kw)
        if self.transfo_type == self.transfo_type.translation:
            self._sc_passive = EuclideanTransform(matrix=self.passive)
        elif self.transfo_type == self.transfo_type.proper_rigid:
            self._sc_passive = EuclideanTransform(matrix=self.passive)
        elif self.transfo_type == self.transfo_type.rigid:
            self._sc_passive = EuclideanTransform(matrix=self.passive)
        elif self.transfo_type == self.transfo_type.similarity:
            self._sc_passive = SimilarityTransform(matrix=self.passive)
        elif self.transfo_type == self.transfo_type.affine:
            self._sc_passive = AffineTransform(matrix=self.passive)
        elif self.transfo_type == self.transfo_type.projective:
            self._sc_passive = ProjectiveTransform(matrix=self.passive)
        else:
            raise ValueError(f"'{self.transfo_type}' not supported")
        self._sc_active = self._sc_passive.inverse

    def apply_coordinates(self, coord: Sequence[numpy.ndarray]) -> numpy.ndarray:
        """
        :param coord: shape `(N, M)`
        :returns: shape `(N, M)`
        """
        return self._sc_active(coord)

    def apply_data(
        self,
        data: numpy.ndarray,
        offset: Optional[numpy.ndarray] = None,
        shape: Optional[numpy.ndarray] = None,
        cval=numpy.nan,
    ) -> numpy.ndarray:
        """
        :param data: shape `(N1, N2, ..., M1, M2, ...)` with `len((N1, N2, ...)) = N`
        :param offset: shape `(N,)`
        :param shape: shape `(N,) = [N1', N2', ...]`
        :param cval: missing value
        :returns: shape `(N1', N2', ..., M1, M2, ...)`
        """
        kw = dict(self._warp_options)
        if shape is not None:
            kw["output_shape"] = shape
        if offset is not None:
            kw["offset"] = offset
        if cval is not None:
            kw["cval"] = cval
        # TODO: offset
        return warp(data, self._sc_passive, **self._warp_options)
