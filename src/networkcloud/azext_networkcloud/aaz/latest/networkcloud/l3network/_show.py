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
    "networkcloud l3network show",
    is_preview=True,
)
class Show(AAZCommand):
    """Get properties of the provided layer 3 (L3) network.

    :example: Get L3 network
        az networkcloud l3network show --name "l2NetworkName" --resource-group "resourceGroupName"
    """

    _aaz_info = {
        "version": "2024-06-01-preview",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.networkcloud/l3networks/{}", "2024-06-01-preview"],
        ]
    }

    def _handler(self, command_args):
        super()._handler(command_args)
        self._execute_operations()
        return self._output()

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.l3_network_name = AAZStrArg(
            options=["-n", "--name", "--l3-network-name"],
            help="The name of the L3 network.",
            required=True,
            id_part="name",
            fmt=AAZStrArgFormat(
                pattern="^([a-zA-Z0-9][a-zA-Z0-9-_]{0,28}[a-zA-Z0-9])$",
            ),
        )
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.L3NetworksGet(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)
        return result

    class L3NetworksGet(AAZHttpOperation):
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
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.NetworkCloud/l3Networks/{l3NetworkName}",
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
                    "l3NetworkName", self.ctx.args.l3_network_name,
                    required=True,
                ),
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
                    "api-version", "2024-06-01-preview",
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
            _schema_on_200.extended_location = AAZObjectType(
                serialized_name="extendedLocation",
                flags={"required": True},
            )
            _schema_on_200.id = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200.location = AAZStrType(
                flags={"required": True},
            )
            _schema_on_200.name = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200.properties = AAZObjectType(
                flags={"required": True, "client_flatten": True},
            )
            _schema_on_200.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _schema_on_200.tags = AAZDictType()
            _schema_on_200.type = AAZStrType(
                flags={"read_only": True},
            )

            extended_location = cls._schema_on_200.extended_location
            extended_location.name = AAZStrType(
                flags={"required": True},
            )
            extended_location.type = AAZStrType(
                flags={"required": True},
            )

            properties = cls._schema_on_200.properties
            properties.associated_resource_ids = AAZListType(
                serialized_name="associatedResourceIds",
                flags={"read_only": True},
            )
            properties.cluster_id = AAZStrType(
                serialized_name="clusterId",
                flags={"read_only": True},
            )
            properties.detailed_status = AAZStrType(
                serialized_name="detailedStatus",
                flags={"read_only": True},
            )
            properties.detailed_status_message = AAZStrType(
                serialized_name="detailedStatusMessage",
                flags={"read_only": True},
            )
            properties.hybrid_aks_clusters_associated_ids = AAZListType(
                serialized_name="hybridAksClustersAssociatedIds",
                flags={"read_only": True},
            )
            properties.hybrid_aks_ipam_enabled = AAZStrType(
                serialized_name="hybridAksIpamEnabled",
            )
            properties.hybrid_aks_plugin_type = AAZStrType(
                serialized_name="hybridAksPluginType",
            )
            properties.interface_name = AAZStrType(
                serialized_name="interfaceName",
            )
            properties.ip_allocation_type = AAZStrType(
                serialized_name="ipAllocationType",
            )
            properties.ipv4_connected_prefix = AAZStrType(
                serialized_name="ipv4ConnectedPrefix",
            )
            properties.ipv6_connected_prefix = AAZStrType(
                serialized_name="ipv6ConnectedPrefix",
            )
            properties.l3_isolation_domain_id = AAZStrType(
                serialized_name="l3IsolationDomainId",
                flags={"required": True},
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            properties.virtual_machines_associated_ids = AAZListType(
                serialized_name="virtualMachinesAssociatedIds",
                flags={"read_only": True},
            )
            properties.vlan = AAZIntType(
                flags={"required": True},
            )

            associated_resource_ids = cls._schema_on_200.properties.associated_resource_ids
            associated_resource_ids.Element = AAZStrType()

            hybrid_aks_clusters_associated_ids = cls._schema_on_200.properties.hybrid_aks_clusters_associated_ids
            hybrid_aks_clusters_associated_ids.Element = AAZStrType()

            virtual_machines_associated_ids = cls._schema_on_200.properties.virtual_machines_associated_ids
            virtual_machines_associated_ids.Element = AAZStrType()

            system_data = cls._schema_on_200.system_data
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

            tags = cls._schema_on_200.tags
            tags.Element = AAZStrType()

            return cls._schema_on_200


class _ShowHelper:
    """Helper class for Show"""


__all__ = ["Show"]
