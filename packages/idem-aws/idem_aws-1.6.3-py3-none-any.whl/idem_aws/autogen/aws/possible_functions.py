"""List of possible functions for known operations."""

DESCRIBE_FUNCTIONS = ("get", "search", "describe")

LIST_FUNCTIONS = ("list", "describe", "search")

DELETE_FUNCTIONS = (
    "delete",
    "disassociate",
    "reject",
    "deallocate",
    "unassign",
    "deregister",
    "deprovision",
    "revoke",
    "release",
    "terminate",
    "cancel",
    "disable",
)

CREATE_FUNCTIONS = (
    "create",
    "associate",
    "accept",
    "allocate",
    "assign",
    "register",
    "provision",
    "authorize",
    "run",
    "enable",
    "upload",
    "put",
    "publish",
    "request",
    "put",
    "add",
)

UPDATE_FUNCTIONS = ("modify",)

ADD_TAG_FUNCTIONS = (
    "add_tags",
    "tag_resource",
    "create_tags",
    "add_tags_to_resource",
)

REMOVE_TAG_FUNCTIONS = (
    "remove_tags",
    "untag_resource",
    "delete_tags",
    "remove_tags_from_resource",
)

SINGLE_TAG_UPDATE_FUNCTIONS = (
    "change_tags_for_resource",
    "change_tags",
)

LIST_TAG_FUNCTIONS = (
    "list_tags",
    "get_tags",
    "describe_tags",
    "list_tags_for_resource",
)
