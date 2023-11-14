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
    "hdinsight-on-aks clusterpool wait",
)
class Wait(AAZWaitCommand):
    """Place the CLI in a waiting state until a condition is met.
    """

    _aaz_info = {
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.hdinsight/clusterpools/{}", "2023-06-01-preview"],
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
        _args_schema.cluster_pool_name = AAZStrArg(
            options=["-n", "--name", "--cluster-pool-name"],
            help="The name of the cluster pool.",
            required=True,
            id_part="name",
        )
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.ClusterPoolsGet(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=False)
        return result

    class ClusterPoolsGet(AAZHttpOperation):
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
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HDInsight/clusterpools/{clusterPoolName}",
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
                    "clusterPoolName", self.ctx.args.cluster_pool_name,
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
                    "api-version", "2023-06-01-preview",
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
                flags={"client_flatten": True},
            )
            _schema_on_200.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _schema_on_200.tags = AAZDictType()
            _schema_on_200.type = AAZStrType(
                flags={"read_only": True},
            )

            properties = cls._schema_on_200.properties
            properties.aks_cluster_profile = AAZObjectType(
                serialized_name="aksClusterProfile",
                flags={"read_only": True},
            )
            properties.aks_managed_resource_group_name = AAZStrType(
                serialized_name="aksManagedResourceGroupName",
                flags={"read_only": True},
            )
            properties.cluster_pool_profile = AAZObjectType(
                serialized_name="clusterPoolProfile",
            )
            properties.compute_profile = AAZObjectType(
                serialized_name="computeProfile",
                flags={"required": True},
            )
            properties.deployment_id = AAZStrType(
                serialized_name="deploymentId",
                flags={"read_only": True},
            )
            properties.log_analytics_profile = AAZObjectType(
                serialized_name="logAnalyticsProfile",
            )
            properties.managed_resource_group_name = AAZStrType(
                serialized_name="managedResourceGroupName",
            )
            properties.network_profile = AAZObjectType(
                serialized_name="networkProfile",
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            properties.status = AAZStrType(
                flags={"read_only": True},
            )

            aks_cluster_profile = cls._schema_on_200.properties.aks_cluster_profile
            aks_cluster_profile.aks_cluster_agent_pool_identity_profile = AAZObjectType(
                serialized_name="aksClusterAgentPoolIdentityProfile",
            )
            aks_cluster_profile.aks_cluster_resource_id = AAZStrType(
                serialized_name="aksClusterResourceId",
            )
            aks_cluster_profile.aks_version = AAZStrType(
                serialized_name="aksVersion",
                flags={"read_only": True},
            )

            aks_cluster_agent_pool_identity_profile = cls._schema_on_200.properties.aks_cluster_profile.aks_cluster_agent_pool_identity_profile
            aks_cluster_agent_pool_identity_profile.msi_client_id = AAZStrType(
                serialized_name="msiClientId",
                flags={"required": True},
            )
            aks_cluster_agent_pool_identity_profile.msi_object_id = AAZStrType(
                serialized_name="msiObjectId",
                flags={"required": True},
            )
            aks_cluster_agent_pool_identity_profile.msi_resource_id = AAZStrType(
                serialized_name="msiResourceId",
                flags={"required": True},
            )

            cluster_pool_profile = cls._schema_on_200.properties.cluster_pool_profile
            cluster_pool_profile.cluster_pool_version = AAZStrType(
                serialized_name="clusterPoolVersion",
                flags={"required": True},
            )

            compute_profile = cls._schema_on_200.properties.compute_profile
            compute_profile.count = AAZIntType(
                flags={"read_only": True},
            )
            compute_profile.vm_size = AAZStrType(
                serialized_name="vmSize",
                flags={"required": True},
            )

            log_analytics_profile = cls._schema_on_200.properties.log_analytics_profile
            log_analytics_profile.enabled = AAZBoolType(
                flags={"required": True},
            )
            log_analytics_profile.workspace_id = AAZStrType(
                serialized_name="workspaceId",
            )

            network_profile = cls._schema_on_200.properties.network_profile
            network_profile.subnet_id = AAZStrType(
                serialized_name="subnetId",
                flags={"required": True},
            )

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


class _WaitHelper:
    """Helper class for Wait"""


__all__ = ["Wait"]
