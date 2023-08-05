from ewokscore.task import Task
from ..transformation.numpy_backend import NumpyHomography
from ..tests.data import data_for_registration


__all__ = ["Example2DStack"]


class Example2DStack(
    Task,
    input_names=["name", "transformation_type"],
    optional_input_names=["shape", "nimages"],
    output_names=["imagestack", "transformations"],
):
    def run(self):
        values = self.input_values
        transformation_type = values.pop("transformation_type")
        istack, _, passive = data_for_registration.images(transformation_type, **values)
        self.outputs.imagestack = istack
        self.outputs.transformations = [NumpyHomography(M) for M in passive]
