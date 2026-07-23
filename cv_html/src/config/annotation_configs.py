from compiler.entities.annotation_config import AnnotationConfig
from compiler.entities.value_format import ValueFormat

CV_ANNOTATIONS = [
    AnnotationConfig(
        key="excluded_visibility",
        value_format=ValueFormat.BOOL,
    )
]