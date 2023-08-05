from __future__ import annotations

import ckan.plugins.toolkit as tk
from ckan import model
from ckan.logic import validate

from ckanext.toolbelt.decorators import Collector

from . import schema

action, get_actions = Collector("flakes_feedback").split()


@action
@validate(schema.feedback_create)
def feedback_create(context, data_dict):
    tk.check_access("flakes_feedback_feedback_create", context, data_dict)

    pkg = model.Package.get(data_dict["package_id"])
    if not pkg:
        raise tk.ObjectNotFound("Package not found")

    flake = tk.get_action("flakes_flake_override")(
        context,
        {
            "name": _name(pkg.id),
            "data": data_dict["data"],
            "extras": {"flakes_feedback": {"type": "package", "id": pkg.id}},
        },
    )

    return flake


@action
@validate(schema.feedback_update)
def feedback_update(context, data_dict):
    tk.check_access("flakes_feedback_feedback_update", context, data_dict)

    try:
        flake = tk.get_action("flakes_flake_update")(context, data_dict)
    except tk.ObjectNotFound as e:
        raise tk.ObjectNotFound("Feedback not found") from e

    return flake


@action
@validate(schema.feedback_delete)
def feedback_delete(context, data_dict):
    tk.check_access("flakes_feedback_feedback_delete", context, data_dict)

    try:
        flake = tk.get_action("flakes_flake_delete")(context, {"id": data_dict["id"]})
    except tk.ObjectNotFound as e:
        raise tk.ObjectNotFound("Feedback not found") from e

    return flake


@action
@tk.side_effect_free
@validate(schema.feedback_list)
def feedback_list(context, data_dict):
    tk.check_access("flakes_feedback_feedback_list", context, data_dict)

    pkg = model.Package.get(data_dict["package_id"])

    flakes = tk.get_action("flakes_flake_list")(
        dict(context, ignore_auth=True),
        {
            "author_id": None,
            "extras": {"flakes_feedback": {"type": "package", "id": pkg.id}},
        },
    )

    return flakes


@action
@tk.side_effect_free
@validate(schema.feedback_show)
def feedback_show(context, data_dict):
    tk.check_access("flakes_feedback_feedback_show", context, data_dict)

    try:
        flake = tk.get_action("flakes_flake_show")(
            dict(context, ignore_auth=True), {"id": data_dict["id"]}
        )
    except tk.ObjectNotFound as e:
        raise tk.ObjectNotFound("Feedback not found") from e

    return flake


@action
@tk.side_effect_free
@validate(schema.feedback_lookup)
def feedback_lookup(context, data_dict):
    tk.check_access("flakes_feedback_feedback_list", context, data_dict)

    pkg = model.Package.get(data_dict["package_id"])
    if not pkg:
        raise tk.ObjectNotFound("Package not found")

    try:
        flake = tk.get_action("flakes_flake_lookup")(context, {"name": _name(pkg.id)})
    except tk.ObjectNotFound as e:
        raise tk.ObjectNotFound("Feedback not found") from e

    return flake


def _name(id_: str):
    return f"ckanext:flakes_feedback:feedback:package:{id_}"
