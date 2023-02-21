# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long

from azure.cli.core.azclierror import (ValidationError, ResourceNotFoundError)
from knack.log import get_logger

from ._clients import ContainerAppClient
from ._ssh_utils import ping_container_app
from ._utils import safe_get
from ._constants import ACR_IMAGE_SUFFIX


logger = get_logger(__name__)


def _is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def validate_memory(namespace):
    if namespace.memory is not None:
        valid = False

        if not namespace.memory.endswith("Gi"):
            namespace.memory = namespace.memory.rstrip()
            namespace.memory += "Gi"

        valid = _is_number(namespace.memory[:-2])

        if not valid:
            raise ValidationError("Usage error: --memory must be a number ending with \"Gi\"")


def validate_cpu(namespace):
    if namespace.cpu:
        cpu = namespace.cpu
        try:
            float(cpu)
        except ValueError as e:
            raise ValidationError("Usage error: --cpu must be a number eg. \"0.5\"") from e


def validate_env_name_or_id(cmd, namespace):
    from azure.cli.core.commands.client_factory import get_subscription_id
    from msrestazure.tools import is_valid_resource_id, resource_id

    if not namespace.env or not namespace.resource_group_name:
        return

    # Set environment type
    environment_type = None

    if namespace.__dict__.get("environment_type"):
        environment_type = namespace.environment_type

    if namespace.env:
        if "connectedEnvironments" in namespace.env:
            environment_type = "connected"
        if "managedEnvironments" in namespace.env:
            environment_type = "managed"
    if namespace.__dict__.get("custom_location") or namespace.__dict__.get("connected_cluster_id"):
        environment_type = "connected"
    # Validate resource id / format resource id
    if environment_type == "connected":
        if not is_valid_resource_id(namespace.env):
            namespace.env = resource_id(
                subscription=get_subscription_id(cmd.cli_ctx),
                resource_group=namespace.resource_group_name,
                namespace='Microsoft.App',
                type='connectedEnvironments',
                name=namespace.env
            )
    elif environment_type == "managed":
        if not is_valid_resource_id(namespace.env):
            namespace.env = resource_id(
                subscription=get_subscription_id(cmd.cli_ctx),
                resource_group=namespace.resource_group_name,
                namespace='Microsoft.App',
                type='managedEnvironments',
                name=namespace.env
            )


def validate_custom_location_name_or_id(cmd, namespace):
    from azure.cli.core.commands.client_factory import get_subscription_id
    from msrestazure.tools import is_valid_resource_id, resource_id

    if not namespace.custom_location or not namespace.resource_group_name:
        return

    if not is_valid_resource_id(namespace.custom_location):
        namespace.custom_location = resource_id(
            subscription=get_subscription_id(cmd.cli_ctx),
            resource_group=namespace.resource_group_name,
            namespace='Microsoft.ExtendedLocation',
            type='customLocations',
            name=namespace.custom_location
        )


def validate_registry_server(namespace):
    if "create" in namespace.command.lower():
        if namespace.registry_server:
            if not namespace.registry_user or not namespace.registry_pass:
                if ACR_IMAGE_SUFFIX not in namespace.registry_server:
                    raise ValidationError("Usage error: --registry-server, --registry-password and --registry-username are required together if not using Azure Container Registry")


def validate_registry_user(namespace):
    if "create" in namespace.command.lower():
        if namespace.registry_user:
            if not namespace.registry_server or (not namespace.registry_pass and ACR_IMAGE_SUFFIX not in namespace.registry_server):
                raise ValidationError("Usage error: --registry-server, --registry-password and --registry-username are required together if not using Azure Container Registry")


def validate_registry_pass(namespace):
    if "create" in namespace.command.lower():
        if namespace.registry_pass:
            if not namespace.registry_server or (not namespace.registry_user and ACR_IMAGE_SUFFIX not in namespace.registry_server):
                raise ValidationError("Usage error: --registry-server, --registry-password and --registry-username are required together if not using Azure Container Registry")


def validate_target_port(namespace):
    if "create" in namespace.command.lower():
        if namespace.target_port:
            if not namespace.ingress:
                raise ValidationError("Usage error: must specify --ingress with --target-port")


def validate_ingress(namespace):
    if "create" in namespace.command.lower():
        if namespace.ingress:
            if not namespace.target_port:
                raise ValidationError("Usage error: must specify --target-port with --ingress")


def _set_ssh_defaults(cmd, namespace):
    app = ContainerAppClient.show(cmd, namespace.resource_group_name, namespace.name)
    if not app:
        raise ResourceNotFoundError("Could not find a container app")
    replicas = []
    if not namespace.revision:
        namespace.revision = app.get("properties", {}).get("latestRevisionName")
        if not namespace.revision:
            raise ResourceNotFoundError("Could not find a revision")
    if not namespace.replica:
        # VVV this may not be necessary according to Anthony Chu
        try:
            ping_container_app(app)  # needed to get an alive replica
        except Exception as e:
            logger.warning("Failed to ping container app with error '%s' \nPlease ensure there is an alive replica. ", str(e))
        replicas = ContainerAppClient.list_replicas(cmd=cmd,
                                                    resource_group_name=namespace.resource_group_name,
                                                    container_app_name=namespace.name,
                                                    revision_name=namespace.revision)
        if not replicas:
            raise ResourceNotFoundError("Could not find a replica for this app")
        namespace.replica = replicas[0]["name"]
    if not namespace.container:
        revision = ContainerAppClient.show_revision(cmd, resource_group_name=namespace.resource_group_name,
                                                    container_app_name=namespace.name,
                                                    name=namespace.revision)
        revision_containers = safe_get(revision, "properties", "template", "containers")
        if revision_containers:
            namespace.container = revision_containers[0]["name"]


def _validate_revision_exists(cmd, namespace):
    revision = ContainerAppClient.show_revision(cmd, resource_group_name=namespace.resource_group_name,
                                                container_app_name=namespace.name, name=namespace.revision)
    if not revision:
        raise ResourceNotFoundError("Could not find revision")


def _validate_replica_exists(cmd, namespace):
    replica = ContainerAppClient.get_replica(cmd=cmd,
                                             resource_group_name=namespace.resource_group_name,
                                             container_app_name=namespace.name,
                                             revision_name=namespace.revision,
                                             replica_name=namespace.replica)
    if not replica:
        raise ResourceNotFoundError("Could not find replica")


def _validate_container_exists(cmd, namespace):
    replica_containers = ContainerAppClient.get_replica(cmd=cmd,
                                                        resource_group_name=namespace.resource_group_name,
                                                        container_app_name=namespace.name,
                                                        revision_name=namespace.revision,
                                                        replica_name=namespace.replica)["properties"]["containers"]
    matches = [r for r in replica_containers if r["name"].lower() == namespace.container.lower()]
    if not matches:
        raise ResourceNotFoundError("Could not find container")


def _validate_container_connected(cmd, namespace):
    containerapp = ContainerAppClient.show(cmd, namespace.resource_group_name, namespace.name)
    if "connected" in containerapp["properties"]["environmentId"]:
        raise ValidationError("Containerapps hosted on connected environments do not support this command.")


# also used to validate logstream
def validate_ssh(cmd, namespace):
    _set_ssh_defaults(cmd, namespace)
    _validate_revision_exists(cmd, namespace)
    _validate_replica_exists(cmd, namespace)
    _validate_container_exists(cmd, namespace)


def validate_exec(cmd, namespace):
    _validate_container_connected(cmd, namespace)
    validate_ssh(cmd, namespace)