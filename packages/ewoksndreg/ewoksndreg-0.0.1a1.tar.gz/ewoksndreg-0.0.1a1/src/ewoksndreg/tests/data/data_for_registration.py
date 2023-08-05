"""Data to test registration"""

from typing import Tuple, List
import numpy

try:
    from skimage import data
    from skimage.transform import warp
    from skimage.transform import SimilarityTransform
    from skimage.transform import AffineTransform
    from skimage.color import rgb2gray
except ImportError:
    data = None

from ...transformation.types import TransformationType


def images(
    transfo_type: TransformationType,
    shape: Tuple[int] = (200, 220),
    nimages: int = 4,
    plot: float = 0,
    name: str = "astronaut",
) -> Tuple[List[numpy.ndarray], List[numpy.ndarray], List[numpy.ndarray]]:
    if data is None:
        raise ModuleNotFoundError("No module named 'skimage'")
    load_image = getattr(data, name)
    image0 = load_image()
    if image0.ndim > 2:
        image0 = rgb2gray(image0)
    image0 = image0[::-1, :]
    full_shape = numpy.array(image0.shape)
    if all(shape):
        sub_shape = numpy.minimum(numpy.array(shape), full_shape)
    else:
        sub_shape = full_shape
    center = (full_shape / 2).astype(int)
    d = (sub_shape / 2).astype(int)
    idx0 = center - d
    idx1 = center + d
    idx = tuple(slice(i0, i1) for i0, i1 in zip(idx0, idx1))

    if transfo_type == TransformationType.identity:
        tform = SimilarityTransform()
    elif transfo_type == TransformationType.translation:
        tform = SimilarityTransform(translation=[2, 3])
    elif transfo_type == TransformationType.proper_rigid:
        tform = SimilarityTransform(rotation=numpy.radians(4))
    elif transfo_type == TransformationType.rigid:
        tform = SimilarityTransform(rotation=numpy.radians(4), scale=[1, -1])
    elif transfo_type == TransformationType.similarity:
        tform = SimilarityTransform(scale=1.05)
    elif transfo_type == TransformationType.affine:
        tform = AffineTransform(shear=numpy.radians(4))
    else:
        raise NotImplementedError(transfo_type)

    tbefore = SimilarityTransform(translation=-center)
    tafter = SimilarityTransform(translation=center)
    tform0 = tbefore + tform + tafter

    image1 = image0.copy()
    tform1 = tform0
    images = [image1[idx]]
    passive = [numpy.identity(3)]
    active = [numpy.identity(3)]
    if plot:
        import matplotlib.pyplot as plt

        fig = plt.figure()
        plt.imshow(images[-1], origin="lower")
        plt.pause(plot)
    for _ in range(1, nimages):
        image1 = warp(image1, tform0, order=3)
        images.append(image1[idx])
        active.append(indexing_order(tform1.params))
        passive.append(indexing_order(numpy.linalg.inv(tform1.params)))
        if plot:
            fig.clear()
            plt.imshow(images[-1], origin="lower")
            plt.pause(plot)
        tform1 = tform1 + tform0
    return images, active, passive


def indexing_order(matrix: numpy.ndarray) -> numpy.ndarray:
    matrix = matrix.copy()
    matrix[:2, :2] = matrix[:2, :2].T
    matrix[:2, 2] = matrix[:2, 2][::-1]
    return matrix
