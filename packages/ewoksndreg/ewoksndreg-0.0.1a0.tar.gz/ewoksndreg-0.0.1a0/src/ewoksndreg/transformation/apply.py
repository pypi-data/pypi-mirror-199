from typing import Optional, Sequence, List
from ..io.input_stack import InputStack
from ..io.output_stack import OutputStack
from .base import Transformation


def apply_transformations(
    input_stack: InputStack,
    output_stack: OutputStack,
    transformations: List[Transformation],
    include: Optional[Sequence[int]] = None,
):
    if include is None:
        include = range(len(transformations))
    else:
        if len(include) != len(transformations):
            raise ValueError(
                "Number of transformations and number of items to transform must be the same"
            )
    for i in include:
        output_stack.add_point(
            transformations[i].apply_data(input_stack[i], offset=None, shape=None)
        )
