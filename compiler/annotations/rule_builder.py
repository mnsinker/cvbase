from compiler.entities.annotation_config import AnnotationConfig
from compiler.entities.annotation_rule import AnnotationRule
from compiler.annotations.value_parsers import _VALUE_PARSERS

def build_annotation_rules(configs: list[AnnotationConfig]) -> dict[str, AnnotationRule]:
    """convert annotations configs into runtime annotation rules"""
    return {
        config.key: AnnotationRule(key=config.key, parser=_VALUE_PARSERS[config.value_format])
        for config in configs
    }