from __future__ import annotations

import datetime
import typing as t
from collections import OrderedDict

import aiida.plugins.entry_point as ep
from aiida import orm
from aiida.plugins.factories import BaseFactory
from yaml import safe_load

if t.TYPE_CHECKING:
    from qb_widget.models.node import NodeModel


class AiiDAService:
    """docstring"""

    @staticmethod
    def get_results(nodes: list[NodeModel]) -> list[t.Any]:
        """docstring"""
        if not (query := get_query_from_node_models(nodes)):
            return []
        qb = orm.QueryBuilder()
        for node, args in query:
            qb.append(node, **args)  # type: ignore
        qb.limit(1000)
        return qb.all(flat=True)

    @staticmethod
    def get_node_types() -> dict[str, NodeType]:
        """docstring"""
        return NODE_TYPES

    @staticmethod
    def get_relationship_types(node_type: NodeType) -> list[str]:
        """docstring"""
        if not node_type.name:
            return []
        node = get_entry_point(node_type)
        return (
            NODE_RELATIONSHIPS
            if issubclass(node, orm.Node)
            else GROUP_RELATIONSHIPS
            if issubclass(node, orm.Group)
            else []
        )

    @staticmethod
    def get_fields(node_type: NodeType) -> list[str]:
        """docstring"""
        if not node_type.name:
            return []
        node = get_entry_point(node_type)
        return list(node.fields._dict.keys())

    @staticmethod
    def get_field(node_type: NodeType, field_name: str) -> orm.QbField:
        """docstring"""
        node = get_entry_point(node_type)
        return node.fields[field_name]

    @staticmethod
    def get_operators(
        node_type: NodeType,
        field_name: str,
        is_attr_field: bool = False,
    ) -> list[str]:
        """docstring"""
        if not node_type or not field_name:
            return []
        if is_attr_field:
            return _ATTRIBUTE_OPERATORS
        node = get_entry_point(node_type)
        field = node.fields[field_name]
        if field.key == "value":
            if isinstance(node, orm.Str):
                return _LITERAL_OPERATORS
            if issubclass(node, orm.NumericType):
                return _NUMERICAL_OPERATORS
            if isinstance(node, orm.List):
                return _ITERABLE_OPERATORS
            if isinstance(node, orm.Dict):
                return _DICTIONARY_OPERATORS
        dtype = field.dtype
        if dtype is str:
            return _LITERAL_OPERATORS
        if dtype in (int, float, datetime.date, datetime.datetime):
            return _NUMERICAL_OPERATORS
        if dtype in (list, tuple):
            return _ITERABLE_OPERATORS
        if dtype is dict:
            return _DICTIONARY_OPERATORS
        return _GENERAL_OPERATORS

    @staticmethod
    def validate_filter(
        node_type: NodeType,
        filter_args: dict[str, str],
    ) -> bool:
        """docstring"""
        node = get_entry_point(node_type)
        field = node.fields[filter_args.pop("field")]
        _, operator, value = filter_args.values()

        if "in" in operator:
            value = f"[{value}]"
        elif field.key == "value":
            if isinstance(node, orm.Str):
                pass  # HANDLE
            if issubclass(node, orm.NumericType) and not is_numeric(value):
                return False
            if isinstance(node, orm.Bool) and not is_boolean(value):
                return False
            if isinstance(node, orm.List) and not is_iterable(value):
                return False
        else:
            if field.dtype is str:
                # TODO needs work (handle ', ", and combo cases)
                value = f"'{value}'"

            try:
                cast = cast_filter_value(value)
                if not isinstance(cast, field.dtype):
                    return False
            except Exception:
                return False

        try:
            cast = cast_filter_value(value)
        except Exception:
            return False

        return True


def get_entry_point(node_type: NodeType):
    """docstring"""
    return BaseFactory(
        node_type.group,
        node_type.entry_point,
    )


def cast_filter_value(value: str) -> t.Any:
    """docstring"""
    cast = safe_load(value)
    if isinstance(cast, datetime.date):
        cast = datetime.datetime.combine(cast, datetime.time.min)
    return cast


def is_numeric(value: str) -> bool:
    """docstring"""
    return value.isnumeric()


def is_boolean(value: str) -> bool:
    """docstring"""
    return value.capitalize() in _BOOLEANS


def is_iterable(value: str) -> bool:
    """docstring"""
    try:
        safe_load(value)
    except Exception:
        return False
    return True


def get_query_from_node_models(nodes: list[NodeModel]) -> list[tuple[orm.Node, dict]]:
    """docstring"""
    return [(get_entry_point(node.type), {}) for node in nodes]  # type: ignore


class NodeType:
    """docstring"""

    def __init__(
        self,
        name: str = "",
        group: str = "",
        entry_point: str = "",
    ):
        self.name = name
        self.group = group
        self.entry_point = entry_point

    def __str__(self) -> str:
        return f"{self.group}:{self.name}"


NODE_TYPES = {
    entry_point.attr: NodeType(
        entry_point.attr,
        entry_point.group,
        entry_point.name,
    )
    for group in filter(
        lambda ep: "aiida." in ep,
        ep.get_entry_point_groups(),
    )
    for entry_point in ep.get_entry_points(group)
    if group
    in (
        "aiida.node",
        "aiida.data",
        "aiida.groups",
    )
}

NODE_RELATIONSHIPS = [
    "Outgoing",
    "Incoming",
    "Group",
]

GROUP_RELATIONSHIPS = [
    "Node",
    "User",
]

_BOOLEANS = {
    "True": True,
    "False": False,
}

_GENERAL_OPERATORS = [
    "==",
    "in",
]

_NUMERICAL_OPERATORS = [
    *_GENERAL_OPERATORS,
    ">",
    "<",
    "<=",
    ">=",
]

_LITERAL_OPERATORS = [
    *_GENERAL_OPERATORS,
    "like",
    "ilike",
]

_ITERABLE_OPERATORS = [
    *_GENERAL_OPERATORS,
    "of_length",
    "shorter",
    "longer",
    "contains",
]

_DICTIONARY_OPERATORS = [
    *_GENERAL_OPERATORS,
    "has_key",
]

_ATTRIBUTE_OPERATORS = list(
    OrderedDict.fromkeys(
        [
            *_NUMERICAL_OPERATORS,
            *_LITERAL_OPERATORS,
            *_ITERABLE_OPERATORS,
            *_DICTIONARY_OPERATORS,
            "of_type",
        ]
    )
)
