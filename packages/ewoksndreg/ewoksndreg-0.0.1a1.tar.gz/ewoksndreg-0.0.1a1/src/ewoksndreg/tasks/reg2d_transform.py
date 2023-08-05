from ewokscore.task import Task
from ..io.input_stack import input_context
from ..io.output_stack import output_context
from ..transformation import apply_transformations

__all__ = ["Reg2DTransform"]


class Reg2DTransform(
    Task,
    input_names=["imagestack", "transformations"],
    optional_input_names=["url", "inputs_are_stacks"],
    output_names=["imagestack"],
):
    def run(self):
        url = self.get_input_value("url", None)
        with output_context(url=url) as ostack:
            with input_context(
                self.inputs.imagestack,
                inputs_are_stacks=self.get_input_value("inputs_are_stacks", None),
            ) as istack:
                apply_transformations(istack, ostack, self.inputs.transformations)
            if url:
                self.outputs.imagestack = url
            else:
                self.outputs.imagestack = ostack.data
