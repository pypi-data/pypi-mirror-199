from typing import Optional, Sequence, List
from ..io.input_stack import InputStack
from ..transformation.base import Transformation
from .base import IntensityMapping


def calculate_transformations(
    input_stack: InputStack,
    mapper: IntensityMapping,
    include: Optional[Sequence[int]] = None,
    reference: int = 0,
) -> List[Transformation]:
    if include is None:
        include = list(range(len(input_stack)))
    ref_image = input_stack[reference]
    transformations = list()
    for i in include:
        new_image = input_stack[i]
        if i == reference:
            transformations.append(mapper.identity())
        else:
            transformations.append(mapper.calculate(new_image, ref_image))
    return transformations
