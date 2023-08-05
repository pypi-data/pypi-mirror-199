import numpy
import pytest
from ..intensities import registration
from ..io.input_stack import InputStackNumpy
from .data import data_for_registration


_MAPPERS = {
    f"mapper{'_'.join(k)}": v
    for k, v in registration.IntensityMapping.get_subclass_items()
}


@pytest.mark.parametrize("mapper", _MAPPERS)
@pytest.mark.parametrize("transfo_type", ["translation"])
def test_intensity_registration(transfo_type, mapper):
    istack, active1, passive1 = data_for_registration.images(transfo_type, plot=0)
    istack = InputStackNumpy(istack)

    mapper = _MAPPERS[mapper](transfo_type)

    transformations = registration.calculate_transformations(istack, mapper)

    active2 = numpy.stack([tr.active for tr in transformations])
    passive2 = numpy.stack([tr.passive for tr in transformations])

    numpy.testing.assert_allclose(active1, active2, rtol=0.01)
    numpy.testing.assert_allclose(passive1, passive2, rtol=0.01)
