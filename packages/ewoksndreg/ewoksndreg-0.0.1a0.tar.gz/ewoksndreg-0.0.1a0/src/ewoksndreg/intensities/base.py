import numpy
from ..transformation.base import Transformation
from ..registry import Registered


__all__ = ["IntensityMapping"]


class IntensityMapping(Registered, register=False):
    def identity(self) -> Transformation:
        raise NotImplementedError

    def calculate(
        self, from_image: numpy.ndarray, to_image: numpy.ndarray
    ) -> Transformation:
        raise NotImplementedError
