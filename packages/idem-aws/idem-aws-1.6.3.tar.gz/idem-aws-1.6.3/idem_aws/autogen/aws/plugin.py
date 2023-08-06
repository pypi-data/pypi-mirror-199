"""Build plugin metadata which can be used by pop-create for plugin code generation"""
from typing import Any
from typing import Dict

from dict_tools.data import NamespaceDict


def parse_exec_plugin(
    hub,
    ctx,
    shared_resource_data: dict,
) -> Dict[str, Any]:
    aws_service_name = shared_resource_data.get("aws_service_name")
    resource_name = shared_resource_data.get("resource_name")

    plugin = {
        "doc": f"Exec module for managing {aws_service_name}.{resource_name} in AWS",
        "imports": [
            "import copy",
            "from dataclasses import field",
            "from dataclasses import make_dataclass",
            "from typing import *",
        ],
        "func_alias": {"list_": "list"},
        "functions": NamespaceDict(
            get=hub.pop_create.aws.plugin.generate_get(
                ctx, resource_name, shared_resource_data
            ),
            list=hub.pop_create.aws.plugin.generate_list(
                resource_name, shared_resource_data
            ),
            create=hub.pop_create.aws.plugin.generate_present(
                ctx, resource_name, shared_resource_data
            ),
            update=hub.pop_create.aws.plugin.generate_update(
                ctx, resource_name, shared_resource_data
            ),
            delete=hub.pop_create.aws.plugin.generate_absent(
                ctx, resource_name, shared_resource_data
            ),
        ),
    }

    if ctx.create_plugin == "auto_state":
        plugin["contracts"] = ["auto_state", "soft_fail"]

    return plugin


def parse_state_plugin(
    hub,
    ctx,
    shared_resource_data: dict,
) -> Dict[str, Any]:
    aws_service_name = shared_resource_data.get("aws_service_name")
    resource_name = shared_resource_data.get("resource_name")

    plugin = {
        "doc": f"State module for managing {aws_service_name}.{resource_name} in AWS",
        "imports": [
            "import copy",
            "from dataclasses import field",
            "from dataclasses import make_dataclass",
            "from typing import *",
        ],
        "contracts": ["resource"],
        "functions": NamespaceDict(
            present=hub.pop_create.aws.plugin.generate_present(
                ctx, resource_name, shared_resource_data
            ),
            absent=hub.pop_create.aws.plugin.generate_absent(
                ctx, resource_name, shared_resource_data
            ),
            describe=hub.pop_create.aws.plugin.generate_list(
                resource_name, shared_resource_data
            ),
        ),
    }

    return plugin


def generate_list(hub, resource_name, shared_resource_data):
    describe_function_definition = shared_resource_data["list"]
    params = describe_function_definition.get("params", {})
    return {
        "doc": f"List all {resource_name} resources for the given account. \n{describe_function_definition.get('doc', '')}",
        "params": params,
        "hardcoded": dict(
            **describe_function_definition.get("hardcoded", {}),
        ),
    }


def generate_present(hub, ctx, resource_name, shared_resource_data):
    create_function_definition = shared_resource_data["create"]
    params = create_function_definition.get("params", {})
    if "Tags" not in params.keys():
        params["tags"] = hub.pop_create.aws.template.TAGS_PARAMETER.copy()
    hub.pop_create.aws.plugin.resolve_resource_id_and_name_params(ctx, params)
    return {
        "doc": f"{create_function_definition.get('doc', '')}",
        "params": params,
        "hardcoded": dict(
            **create_function_definition.get("hardcoded", {}),
        ),
    }


def generate_absent(hub, ctx, resource_name, shared_resource_data):
    delete_function_definition = shared_resource_data["delete"]
    # In most cases, absent/delete only needs name and resource_id params
    # This will make sure that all these params are not added in function definition
    params = {}
    hub.pop_create.aws.plugin.resolve_resource_id_and_name_params(ctx, params)
    return {
        "doc": f"{delete_function_definition.get('doc', '')}",
        "params": params,
        "hardcoded": dict(
            **delete_function_definition.get("hardcoded", {}),
        ),
    }


def generate_get(hub, ctx, resource_name, shared_resource_data):
    get_function_definition = shared_resource_data["get"]
    params = get_function_definition.get("params", {})
    hub.pop_create.aws.plugin.resolve_resource_id_and_name_params(ctx, params)
    return {
        "doc": f"Get {resource_name} resources for the given account. \n{get_function_definition.get('doc', '')}",
        "params": params,
        "hardcoded": dict(
            **get_function_definition.get("hardcoded", {}),
        ),
    }


def generate_update(hub, ctx, resource_name, shared_resource_data):
    update_function_definition = shared_resource_data["update"]
    params = update_function_definition.get("params", {})
    if "tags" not in params.keys():
        params["tags"] = hub.pop_create.aws.template.TAGS_PARAMETER.copy()
    hub.pop_create.aws.plugin.resolve_resource_id_and_name_params(ctx, params)
    return {
        "doc": f"{update_function_definition.get('doc', '')}",
        "params": params,
        "hardcoded": dict(
            **update_function_definition.get("hardcoded", {}),
        ),
    }


def resolve_resource_id_and_name_params(hub, ctx, params: dict):
    # auto_state already puts name and resource_id by default in header params
    if ctx.create_plugin == "state_modules":
        params["resource_id"] = hub.pop_create.aws.template.RESOURCE_ID_PARAMETER.copy()
        if "Name" not in params.keys():
            # If we come here that means name was not present in AWS function definition
            params["Name"] = hub.pop_create.aws.template.NAME_PARAMETER.copy()
