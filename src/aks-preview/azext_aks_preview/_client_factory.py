# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.commands.client_factory import get_mgmt_service_client
from azure.cli.core.commands.parameters import get_resources_in_subscription
from azure.cli.core.profiles import ResourceType
from azure.cli.core.profiles import CustomResourceType
from azure.mgmt.msi import ManagedServiceIdentityClient
from knack.util import CLIError

CUSTOM_MGMT_AKS_PREVIEW = CustomResourceType('azext_aks_preview.vendored_sdks.azure_mgmt_preview_aks',
                                             'ContainerServiceClient')


def get_container_service_client(cli_ctx, **_):
    return get_mgmt_service_client(cli_ctx, CUSTOM_MGMT_AKS_PREVIEW)


def cf_trustedaccess_role(cli_ctx, *_):
    return get_container_service_client(cli_ctx).trusted_access_roles


def cf_container_services(cli_ctx, *_):
    return get_container_service_client(cli_ctx).container_services


def cf_managed_clusters(cli_ctx, *_):
    return get_container_service_client(cli_ctx).managed_clusters


def cf_agent_pools(cli_ctx, *_):
    return get_container_service_client(cli_ctx).agent_pools


def cf_maintenance_configurations(cli_ctx, *_):
    return get_container_service_client(cli_ctx).maintenance_configurations


def cf_nodepool_snapshots(cli_ctx, *_):
    return get_container_service_client(cli_ctx).snapshots


# TODO: remove this
def cf_nodepool_snapshots_client(cli_ctx, subscription_id=None):
    return get_mgmt_service_client(cli_ctx, CUSTOM_MGMT_AKS_PREVIEW, subscription_id=subscription_id).snapshots


def cf_mc_snapshots(cli_ctx, *_):
    return get_container_service_client(cli_ctx).managed_cluster_snapshots


# TODO: remove this
def cf_mc_snapshots_client(cli_ctx, subscription_id=None):
    return get_mgmt_service_client(cli_ctx, CUSTOM_MGMT_AKS_PREVIEW, subscription_id=subscription_id).managed_cluster_snapshots


def cf_compute_service(cli_ctx, *_):
    return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_COMPUTE)


def cf_resource_groups(cli_ctx, subscription_id=None):
    return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_RESOURCE_RESOURCES,
                                   subscription_id=subscription_id).resource_groups


def cf_resources(cli_ctx, subscription_id=None):
    return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_RESOURCE_RESOURCES,
                                   subscription_id=subscription_id).resources


def cf_container_registry_service(cli_ctx, subscription_id=None):
    return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_CONTAINERREGISTRY,
                                   subscription_id=subscription_id)


def cf_storage(cli_ctx, subscription_id=None):
    return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_STORAGE, subscription_id=subscription_id)


def get_auth_management_client(cli_ctx, scope=None, **_):
    import re

    subscription_id = None
    if scope:
        matched = re.match('/subscriptions/(?P<subscription>[^/]*)/', scope)
        if matched:
            subscription_id = matched.groupdict()['subscription']
        else:
            raise CLIError("{} does not contain subscription Id.".format(scope))
    return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_AUTHORIZATION, subscription_id=subscription_id)


def get_graph_rbac_management_client(cli_ctx, **_):
    from azure.cli.core.commands.client_factory import configure_common_settings
    from azure.cli.core._profile import Profile
    from azure.graphrbac import GraphRbacManagementClient

    profile = Profile(cli_ctx=cli_ctx)
    cred, _, tenant_id = profile.get_login_credentials(
        resource=cli_ctx.cloud.endpoints.active_directory_graph_resource_id)
    client = GraphRbacManagementClient(
        cred, tenant_id,
        base_url=cli_ctx.cloud.endpoints.active_directory_graph_resource_id)
    configure_common_settings(cli_ctx, client)
    return client


# pylint: disable=inconsistent-return-statements
def get_resource_by_name(cli_ctx, resource_name, resource_type):
    """Returns the ARM resource in the current subscription with resource_name.
    :param str resource_name: The name of resource
    :param str resource_type: The type of resource
    """
    result = get_resources_in_subscription(cli_ctx, resource_type)
    elements = [item for item in result if item.name.lower() == resource_name.lower()]

    if not elements:
        from azure.cli.core._profile import Profile
        profile = Profile(cli_ctx=cli_ctx)
        message = "The resource with name '{}' and type '{}' could not be found".format(
            resource_name, resource_type)
        try:
            subscription = profile.get_subscription(
                cli_ctx.data['subscription_id'])
            raise CLIError(
                "{} in subscription '{} ({})'.".format(message, subscription['name'], subscription['id']))
        except (KeyError, TypeError):
            raise CLIError(
                "{} in the current subscription.".format(message))

    elif len(elements) == 1:
        return elements[0]
    else:
        raise CLIError(
            "More than one resources with type '{}' are found with name '{}'.".format(
                resource_type, resource_name))


def get_msi_client(cli_ctx, subscription_id=None):
    return get_mgmt_service_client(cli_ctx, ManagedServiceIdentityClient,
                                   subscription_id=subscription_id)
