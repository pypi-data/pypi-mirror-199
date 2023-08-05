from ewokscore.task import Task
from ..io.input_stack import input_context
from ..intensities import registration

__all__ = ["Reg2DIntensities"]


class Reg2DIntensities(
    Task,
    input_names=["imagestack", "mapper", "transformation_type"],
    optional_input_names=["inputs_are_stacks", "reference"],
    output_names=["transformations"],
):
    def run(self):
        mapper = registration.IntensityMapping.get_subclass(self.inputs.mapper)(
            self.inputs.transformation_type
        )
        with input_context(
            self.inputs.imagestack,
            inputs_are_stacks=self.get_input_value("inputs_are_stacks", None),
        ) as stack:
            self.outputs.transformations = registration.calculate_transformations(
                stack,
                mapper,
                reference=self.get_input_value("reference", 0),
            )
