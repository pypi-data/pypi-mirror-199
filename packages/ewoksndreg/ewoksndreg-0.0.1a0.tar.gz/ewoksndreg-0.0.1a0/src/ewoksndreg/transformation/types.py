try:
    from enum import StrEnum
except ImportError:
    from strenum import StrEnum

TransformationType = StrEnum(
    "TransformationType",
    [
        "identity",
        "translation",
        "proper_rigid",
        "rigid",
        "similarity",
        "affine",
        "projective",
    ],
)
