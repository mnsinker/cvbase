from compiler.entities.annotation_config import AnnotationConfig
from compiler.entities.value_format import ValueFormat

ANNOTATION_CONFIGS = [
    AnnotationConfig(
        key="career_spine",
        value_format=ValueFormat.LIST
    ),
    AnnotationConfig(
        key="advanced_themes",
        value_format=ValueFormat.LIST
    ),
    AnnotationConfig(
        key="excluded_visibility",
        value_format=ValueFormat.BOOL
    )
]