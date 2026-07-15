from compiler.annotations.parsers import _parse_string, _parse_list, _parse_bool
from compiler.entities.value_format import ValueFormat


_VALUE_PARSERS = {
    ValueFormat.STRING: _parse_string,
    ValueFormat.LIST: _parse_list,
    ValueFormat.BOOL: _parse_bool,
}
