import pytest
from .data import data_for_registration


@pytest.mark.parametrize(
    "transfo_type", ["translation", "rigid", "similarity", "affine"]
)
def test_images(transfo_type):
    data_for_registration.images(transfo_type, plot=0)
