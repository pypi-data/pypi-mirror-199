import numpy
from ..transformation import apply_transformations
from ..io.input_stack import InputStackNumpy
from ..io.output_stack import OutputStackNumpy
from .data import data_for_registration
from ..transformation.numpy_backend import NumpyHomography


def test_apply_transformations():
    istack, active, passive = data_for_registration.images("translation", plot=0)

    forward = [NumpyHomography(M) for M in passive]
    backward = [NumpyHomography(M) for M in active]

    data1 = list()
    with OutputStackNumpy(data1) as ostack:
        apply_transformations(istack, ostack, forward)

    data2 = list()
    with OutputStackNumpy(data2) as ostack:
        with InputStackNumpy(data1) as istack2:
            apply_transformations(istack2, ostack, backward)

    istack = numpy.asarray(istack)
    ostack = numpy.asarray(data2)
    idx = numpy.isnan(ostack)
    ostack[idx] = istack[idx]

    numpy.testing.assert_allclose(istack, ostack)
