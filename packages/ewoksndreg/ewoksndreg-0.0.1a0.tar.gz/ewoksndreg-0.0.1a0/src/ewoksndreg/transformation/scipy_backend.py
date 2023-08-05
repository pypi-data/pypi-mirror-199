from typing import Optional, Sequence, Dict
import numpy
from scipy.ndimage import affine_transform, shift
from .homography import Homography
from .numpy_backend import homography_transform_coordinates

__all__ = ["ScipyHomography"]


class ScipyHomography(
    Homography, registry_id=Homography.RegistryId("Homography", "Scipy")
):
    def __init__(self, *args, warp_options: Optional[Dict] = None, **kw) -> None:
        if warp_options is None:
            warp_options = dict()
        self._warp_options = warp_options
        super().__init__(*args, **kw)

    def apply_coordinates(self, coord: Sequence[numpy.ndarray]) -> numpy.ndarray:
        """
        :param coord: shape `(N, M)`
        :returns: shape `(N, M)`
        """
        return homography_transform_coordinates(self.active, coord)

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
        # TODO: offset, shape
        if self.type == self.type.identity:
            return data
        if self.type == self.type.translation:
            return shift(data, -self.passive[:2, 2], **kw)
        if self.type in (self.type.rigid, self.type.similarity, self.type.affine):
            return affine_transform(
                data, self.passive[0:2, 0:2], offset=self.passive[:2, 2], **kw
            )
        raise NotImplementedError
