"""Homography abstraction.

A homography transformation can be represented be the following change-of-frame matrix

    $$
    F=\\begin{bmatrix}
    C_{n\\times n}&T_{n\\times 1}\\\\
    P_{1\\times n}&1
    \\end{bmatrix}
    $$

Different transformation types can be distinguished based on the properties of the translation vector $T$, change-of-basis matrix $C$ and projection vector $P$

    * translation:
        * $C$ is the identity matrix and $P$ are all zeros
    * proper rigid (euclidian) transformation:
        * $P$ are all zeros
        * $C$ is any orthogonal matrix ($C^T=C^{-1}$) with determinant $\\det{C}=+1$
        * preserves angles, distances and handedness
        * translation + rotation
    * rigid (euclidian) transformation:
        * $P$ are all zeros
        * $C$ is any orthogonal matrix ($C^T=C^{-1}$)
        * preserves angles and distances
        * proper rigid transformation + reflection
    * similarity transformation:
        * $P$ are all zeros
        * $C=rA$ where A any orthogonal matrix ($A^T=A^{-1}$) and $r>0$
        * preserves angles and ratios between distances
        * rigid transformation + isotropic scaling
    * affine transformation:
        * $P$ are all zeros
        * $C$ is any invertible matrix (i.e. linear transformation)
        * preserves parallelism
        * similarity transformation + non-isotropic scaling and shear
    * projective transformation (homography):
        * $C$ is any invertible matrix (i.e. linear transformation)
        * preserves collinearity
        * affine transformation + projection
"""

from typing import Optional
import numpy
from .types import TransformationType
from .base import Transformation


def type_from_matrix(matrix: numpy.ndarray) -> TransformationType:
    """
    :param active: shape `(N+1, N+1)` or `(K, N+1, N+1)`
    :returns: transformation type
    """
    N = matrix.shape[0] - 1
    if matrix.shape != (N + 1, N + 1):
        raise ValueError("must be a square matrix")
    if numpy.allclose(matrix, numpy.identity(N + 1)):
        return TransformationType.identity
    if matrix[-1, -1] != 1 or not numpy.allclose(matrix[-1, 0:-1], 0):
        return TransformationType.projective
    C = matrix[:-1, :-1]
    if numpy.allclose(C, numpy.identity(N)):
        if numpy.allclose(matrix[-1, :-1], 0):
            return TransformationType.translation
        else:
            return TransformationType.rigid
    C_T = C.T
    C_I = numpy.linalg.inv(C)
    if numpy.allclose(C_T, C_I):
        if numpy.allclose(numpy.linalg.det(C), 1):
            return TransformationType.proper_rigid
        else:
            return TransformationType.rigid
    C_I[C_I == 0] = 1
    r = C_T / C_I
    if numpy.allclose(r, r.mean()):
        return TransformationType.similarity
    return TransformationType.affine


class Homography(Transformation, register=False):
    def __init__(
        self, passive: numpy.ndarray, transfo_type: Optional[TransformationType] = None
    ) -> None:
        if transfo_type is None:
            transfo_type = type_from_matrix(passive)
        self._passive = passive
        self._active = None
        super().__init__(transfo_type)

    @property
    def passive(self) -> numpy.ndarray:
        return self._passive

    @property
    def active(self) -> numpy.ndarray:
        if self._active is None:
            self._active = numpy.linalg.inv(self._passive)
        return self._active
