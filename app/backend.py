from __future__ import annotations

import aiida.plugins.entry_point as ep
from aiida import orm
from aiida.manage.configuration import load_profile
from aiida.plugins.factories import BaseFactory
from flask import Blueprint, Flask, jsonify, request

_ = load_profile()

app = Flask(__name__)
aiida_bp = Blueprint(
    "aiida",
    __name__,
    url_prefix="/",
)


@aiida_bp.route("/types", methods=["GET"])
def get_aiida_types():
    return jsonify(NODE_TYPES)


@aiida_bp.route("/relationships/<group>/<entry_point>", methods=["GET"])
def get_aiida_relationships(group: str, entry_point: str):
    """docstring"""
    node = BaseFactory(group, entry_point)
    return (
        NODE_RELATIONSHIPS
        if issubclass(node, orm.Node)  # type: ignore
        else GROUP_RELATIONSHIPS
        if issubclass(node, orm.Group)  # type: ignore
        else []
    )


@aiida_bp.route("/query", methods=["GET"])
def get_aiida_query_results():
    """docstring"""
    qb_dict = request.get_json()
    results = orm.QueryBuilder.from_dict(qb_dict).all(flat=True)
    return jsonify(results)


app.register_blueprint(aiida_bp)

NODE_TYPES = [
    {
        "name": entry_point.attr,
        "group": entry_point.group,
        "entry_point": entry_point.name,
    }
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
]

NODE_RELATIONSHIPS = [
    "Outgoing",
    "Incoming",
    "Group",
]

GROUP_RELATIONSHIPS = [
    "Node",
    "User",
]


if __name__ == "__main__":
    app.run(port=5000)
