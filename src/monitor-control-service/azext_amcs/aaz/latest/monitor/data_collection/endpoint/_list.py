# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: skip-file
# flake8: noqa

from azure.cli.core.aaz import *


@register_command(
    "monitor data-collection endpoint list",
)
class List(AAZCommand):
    """List all data collection endpoints in the specified subscription

    :example: List data collection endpoints by resource group
        az monitor data-collection endpoint list --resource-group "myResourceGroup"

    :example: List data collection endpoints by subscription
        az monitor data-collection endpoint list
    """

    _aaz_info = {
        "version": "2023-03-11",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/providers/microsoft.insights/datacollectionendpoints", "2023-03-11"],
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.insights/datacollectionendpoints", "2023-03-11"],
        ]
    }

    AZ_SUPPORT_PAGINATION = True

    def _handler(self, command_args):
        super()._handler(command_args)
        return self.build_paging(self._execute_operations, self._output)

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.resource_group = AAZResourceGroupNameArg()
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        condition_0 = has_value(self.ctx.args.resource_group) and has_value(self.ctx.subscription_id)
        condition_1 = has_value(self.ctx.subscription_id) and has_value(self.ctx.args.resource_group) is not True
        if condition_0:
            self.DataCollectionEndpointsListByResourceGroup(ctx=self.ctx)()
        if condition_1:
            self.DataCollectionEndpointsListBySubscription(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance.value, client_flatten=True)
        next_link = self.deserialize_output(self.ctx.vars.instance.next_link)
        return result, next_link

    class DataCollectionEndpointsListByResourceGroup(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [200]:
                return self.on_200(session)

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Insights/dataCollectionEndpoints",
                **self.url_parameters
            )

        @property
        def method(self):
            return "GET"

        @property
        def error_format(self):
            return "MgmtErrorFormat"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2023-03-11",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        def on_200(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200
            )

        _schema_on_200 = None

        @classmethod
        def _build_schema_on_200(cls):
            if cls._schema_on_200 is not None:
                return cls._schema_on_200

            cls._schema_on_200 = AAZObjectType()

            _schema_on_200 = cls._schema_on_200
            _schema_on_200.next_link = AAZStrType(
                serialized_name="nextLink",
            )
            _schema_on_200.value = AAZListType(
                flags={"required": True},
            )

            value = cls._schema_on_200.value
            value.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element
            _element.etag = AAZStrType(
                flags={"read_only": True},
            )
            _element.id = AAZStrType(
                flags={"read_only": True},
            )
            _element.identity = AAZObjectType()
            _element.kind = AAZStrType()
            _element.location = AAZStrType(
                flags={"required": True},
            )
            _element.name = AAZStrType(
                flags={"read_only": True},
            )
            _element.properties = AAZObjectType(
                flags={"client_flatten": True},
            )
            _element.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _element.tags = AAZDictType()
            _element.type = AAZStrType(
                flags={"read_only": True},
            )

            identity = cls._schema_on_200.value.Element.identity
            identity.principal_id = AAZStrType(
                serialized_name="principalId",
                flags={"read_only": True},
            )
            identity.tenant_id = AAZStrType(
                serialized_name="tenantId",
                flags={"read_only": True},
            )
            identity.type = AAZStrType(
                flags={"required": True},
            )
            identity.user_assigned_identities = AAZDictType(
                serialized_name="userAssignedIdentities",
            )

            user_assigned_identities = cls._schema_on_200.value.Element.identity.user_assigned_identities
            user_assigned_identities.Element = AAZObjectType(
                nullable=True,
            )

            _element = cls._schema_on_200.value.Element.identity.user_assigned_identities.Element
            _element.client_id = AAZStrType(
                serialized_name="clientId",
                flags={"read_only": True},
            )
            _element.principal_id = AAZStrType(
                serialized_name="principalId",
                flags={"read_only": True},
            )

            properties = cls._schema_on_200.value.Element.properties
            properties.configuration_access = AAZObjectType(
                serialized_name="configurationAccess",
            )
            properties.description = AAZStrType()
            properties.failover_configuration = AAZObjectType(
                serialized_name="failoverConfiguration",
                flags={"read_only": True},
            )
            properties.immutable_id = AAZStrType(
                serialized_name="immutableId",
            )
            properties.logs_ingestion = AAZObjectType(
                serialized_name="logsIngestion",
            )
            properties.metadata = AAZObjectType(
                flags={"read_only": True},
            )
            properties.metrics_ingestion = AAZObjectType(
                serialized_name="metricsIngestion",
            )
            properties.network_acls = AAZObjectType(
                serialized_name="networkAcls",
            )
            properties.private_link_scoped_resources = AAZListType(
                serialized_name="privateLinkScopedResources",
                flags={"read_only": True},
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )

            configuration_access = cls._schema_on_200.value.Element.properties.configuration_access
            configuration_access.endpoint = AAZStrType(
                flags={"read_only": True},
            )

            failover_configuration = cls._schema_on_200.value.Element.properties.failover_configuration
            failover_configuration.active_location = AAZStrType(
                serialized_name="activeLocation",
            )
            failover_configuration.locations = AAZListType()

            locations = cls._schema_on_200.value.Element.properties.failover_configuration.locations
            locations.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element.properties.failover_configuration.locations.Element
            _element.location = AAZStrType()
            _element.provisioning_status = AAZStrType(
                serialized_name="provisioningStatus",
            )

            logs_ingestion = cls._schema_on_200.value.Element.properties.logs_ingestion
            logs_ingestion.endpoint = AAZStrType(
                flags={"read_only": True},
            )

            metadata = cls._schema_on_200.value.Element.properties.metadata
            metadata.provisioned_by = AAZStrType(
                serialized_name="provisionedBy",
                flags={"read_only": True},
            )
            metadata.provisioned_by_immutable_id = AAZStrType(
                serialized_name="provisionedByImmutableId",
                flags={"read_only": True},
            )
            metadata.provisioned_by_resource_id = AAZStrType(
                serialized_name="provisionedByResourceId",
                flags={"read_only": True},
            )

            metrics_ingestion = cls._schema_on_200.value.Element.properties.metrics_ingestion
            metrics_ingestion.endpoint = AAZStrType(
                flags={"read_only": True},
            )

            network_acls = cls._schema_on_200.value.Element.properties.network_acls
            network_acls.public_network_access = AAZStrType(
                serialized_name="publicNetworkAccess",
            )

            private_link_scoped_resources = cls._schema_on_200.value.Element.properties.private_link_scoped_resources
            private_link_scoped_resources.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element.properties.private_link_scoped_resources.Element
            _element.resource_id = AAZStrType(
                serialized_name="resourceId",
            )
            _element.scope_id = AAZStrType(
                serialized_name="scopeId",
            )

            system_data = cls._schema_on_200.value.Element.system_data
            system_data.created_at = AAZStrType(
                serialized_name="createdAt",
            )
            system_data.created_by = AAZStrType(
                serialized_name="createdBy",
            )
            system_data.created_by_type = AAZStrType(
                serialized_name="createdByType",
            )
            system_data.last_modified_at = AAZStrType(
                serialized_name="lastModifiedAt",
            )
            system_data.last_modified_by = AAZStrType(
                serialized_name="lastModifiedBy",
            )
            system_data.last_modified_by_type = AAZStrType(
                serialized_name="lastModifiedByType",
            )

            tags = cls._schema_on_200.value.Element.tags
            tags.Element = AAZStrType()

            return cls._schema_on_200

    class DataCollectionEndpointsListBySubscription(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [200]:
                return self.on_200(session)

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/providers/Microsoft.Insights/dataCollectionEndpoints",
                **self.url_parameters
            )

        @property
        def method(self):
            return "GET"

        @property
        def error_format(self):
            return "MgmtErrorFormat"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2023-03-11",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        def on_200(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200
            )

        _schema_on_200 = None

        @classmethod
        def _build_schema_on_200(cls):
            if cls._schema_on_200 is not None:
                return cls._schema_on_200

            cls._schema_on_200 = AAZObjectType()

            _schema_on_200 = cls._schema_on_200
            _schema_on_200.next_link = AAZStrType(
                serialized_name="nextLink",
            )
            _schema_on_200.value = AAZListType(
                flags={"required": True},
            )

            value = cls._schema_on_200.value
            value.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element
            _element.etag = AAZStrType(
                flags={"read_only": True},
            )
            _element.id = AAZStrType(
                flags={"read_only": True},
            )
            _element.identity = AAZObjectType()
            _element.kind = AAZStrType()
            _element.location = AAZStrType(
                flags={"required": True},
            )
            _element.name = AAZStrType(
                flags={"read_only": True},
            )
            _element.properties = AAZObjectType(
                flags={"client_flatten": True},
            )
            _element.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _element.tags = AAZDictType()
            _element.type = AAZStrType(
                flags={"read_only": True},
            )

            identity = cls._schema_on_200.value.Element.identity
            identity.principal_id = AAZStrType(
                serialized_name="principalId",
                flags={"read_only": True},
            )
            identity.tenant_id = AAZStrType(
                serialized_name="tenantId",
                flags={"read_only": True},
            )
            identity.type = AAZStrType(
                flags={"required": True},
            )
            identity.user_assigned_identities = AAZDictType(
                serialized_name="userAssignedIdentities",
            )

            user_assigned_identities = cls._schema_on_200.value.Element.identity.user_assigned_identities
            user_assigned_identities.Element = AAZObjectType(
                nullable=True,
            )

            _element = cls._schema_on_200.value.Element.identity.user_assigned_identities.Element
            _element.client_id = AAZStrType(
                serialized_name="clientId",
                flags={"read_only": True},
            )
            _element.principal_id = AAZStrType(
                serialized_name="principalId",
                flags={"read_only": True},
            )

            properties = cls._schema_on_200.value.Element.properties
            properties.configuration_access = AAZObjectType(
                serialized_name="configurationAccess",
            )
            properties.description = AAZStrType()
            properties.failover_configuration = AAZObjectType(
                serialized_name="failoverConfiguration",
                flags={"read_only": True},
            )
            properties.immutable_id = AAZStrType(
                serialized_name="immutableId",
            )
            properties.logs_ingestion = AAZObjectType(
                serialized_name="logsIngestion",
            )
            properties.metadata = AAZObjectType(
                flags={"read_only": True},
            )
            properties.metrics_ingestion = AAZObjectType(
                serialized_name="metricsIngestion",
            )
            properties.network_acls = AAZObjectType(
                serialized_name="networkAcls",
            )
            properties.private_link_scoped_resources = AAZListType(
                serialized_name="privateLinkScopedResources",
                flags={"read_only": True},
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )

            configuration_access = cls._schema_on_200.value.Element.properties.configuration_access
            configuration_access.endpoint = AAZStrType(
                flags={"read_only": True},
            )

            failover_configuration = cls._schema_on_200.value.Element.properties.failover_configuration
            failover_configuration.active_location = AAZStrType(
                serialized_name="activeLocation",
            )
            failover_configuration.locations = AAZListType()

            locations = cls._schema_on_200.value.Element.properties.failover_configuration.locations
            locations.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element.properties.failover_configuration.locations.Element
            _element.location = AAZStrType()
            _element.provisioning_status = AAZStrType(
                serialized_name="provisioningStatus",
            )

            logs_ingestion = cls._schema_on_200.value.Element.properties.logs_ingestion
            logs_ingestion.endpoint = AAZStrType(
                flags={"read_only": True},
            )

            metadata = cls._schema_on_200.value.Element.properties.metadata
            metadata.provisioned_by = AAZStrType(
                serialized_name="provisionedBy",
                flags={"read_only": True},
            )
            metadata.provisioned_by_immutable_id = AAZStrType(
                serialized_name="provisionedByImmutableId",
                flags={"read_only": True},
            )
            metadata.provisioned_by_resource_id = AAZStrType(
                serialized_name="provisionedByResourceId",
                flags={"read_only": True},
            )

            metrics_ingestion = cls._schema_on_200.value.Element.properties.metrics_ingestion
            metrics_ingestion.endpoint = AAZStrType(
                flags={"read_only": True},
            )

            network_acls = cls._schema_on_200.value.Element.properties.network_acls
            network_acls.public_network_access = AAZStrType(
                serialized_name="publicNetworkAccess",
            )

            private_link_scoped_resources = cls._schema_on_200.value.Element.properties.private_link_scoped_resources
            private_link_scoped_resources.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element.properties.private_link_scoped_resources.Element
            _element.resource_id = AAZStrType(
                serialized_name="resourceId",
            )
            _element.scope_id = AAZStrType(
                serialized_name="scopeId",
            )

            system_data = cls._schema_on_200.value.Element.system_data
            system_data.created_at = AAZStrType(
                serialized_name="createdAt",
            )
            system_data.created_by = AAZStrType(
                serialized_name="createdBy",
            )
            system_data.created_by_type = AAZStrType(
                serialized_name="createdByType",
            )
            system_data.last_modified_at = AAZStrType(
                serialized_name="lastModifiedAt",
            )
            system_data.last_modified_by = AAZStrType(
                serialized_name="lastModifiedBy",
            )
            system_data.last_modified_by_type = AAZStrType(
                serialized_name="lastModifiedByType",
            )

            tags = cls._schema_on_200.value.Element.tags
            tags.Element = AAZStrType()

            return cls._schema_on_200


class _ListHelper:
    """Helper class for List"""


__all__ = ["List"]
