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
    "mobile-network pcdp create",
)
class Create(AAZCommand):
    """Create a packet core data plane.

    :example: Create Packet Core Data Plane
        az mobile-network pcdp create -n pcdp-name -g rg --pccp-name pccp-name --access-interface "{name:N2,ipv4Address:10.28.128.2,ipv4Subnet:10.28.128.0/24,ipv4Gateway:10.28.128.1}"
    """

    _aaz_info = {
        "version": "2023-09-01",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.mobilenetwork/packetcorecontrolplanes/{}/packetcoredataplanes/{}", "2023-09-01"],
        ]
    }

    AZ_SUPPORT_NO_WAIT = True

    def _handler(self, command_args):
        super()._handler(command_args)
        return self.build_lro_poller(self._execute_operations, self._output)

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.pccp_name = AAZStrArg(
            options=["--pccp-name"],
            help="The name of the packet core control plane.",
            required=True,
            fmt=AAZStrArgFormat(
                pattern="^[a-zA-Z0-9][a-zA-Z0-9_-]*$",
                max_length=64,
            ),
        )
        _args_schema.pcdp_name = AAZStrArg(
            options=["-n", "--name", "--pcdp-name"],
            help="The name of the packet core data plane.",
            required=True,
            fmt=AAZStrArgFormat(
                pattern="^[a-zA-Z0-9][a-zA-Z0-9_-]*$",
                max_length=64,
            ),
        )
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )

        # define Arg Group "Parameters"

        _args_schema = cls._args_schema
        _args_schema.location = AAZResourceLocationArg(
            arg_group="Parameters",
            help="The geo-location where the resource lives",
            required=True,
            fmt=AAZResourceLocationArgFormat(
                resource_group_arg="resource_group",
            ),
        )
        _args_schema.tags = AAZDictArg(
            options=["--tags"],
            arg_group="Parameters",
            help="Resource tags.",
        )

        tags = cls._args_schema.tags
        tags.Element = AAZStrArg()

        # define Arg Group "Properties"

        _args_schema = cls._args_schema
        _args_schema.access_interface = AAZObjectArg(
            options=["--access-interface"],
            arg_group="Properties",
            help="The user plane interface on the access network. For 5G networks, this is the N3 interface. For 4G networks, this is the S1-U interface.",
            required=True,
        )

        access_interface = cls._args_schema.access_interface
        access_interface.ipv4_address = AAZStrArg(
            options=["ipv4-address"],
            help="The IPv4 address.",
            fmt=AAZStrArgFormat(
                pattern="^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$",
            ),
        )
        access_interface.ipv4_gateway = AAZStrArg(
            options=["ipv4-gateway"],
            help="The default IPv4 gateway (router).",
            fmt=AAZStrArgFormat(
                pattern="^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$",
            ),
        )
        access_interface.ipv4_subnet = AAZStrArg(
            options=["ipv4-subnet"],
            help="The IPv4 subnet.",
            fmt=AAZStrArgFormat(
                pattern="^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])(\/([0-9]|[1-2][0-9]|3[0-2]))$",
            ),
        )
        access_interface.name = AAZStrArg(
            options=["name"],
            help="The logical name for this interface. This should match one of the interfaces configured on your Azure Stack Edge device.",
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        yield self.PacketCoreDataPlanesCreateOrUpdate(ctx=self.ctx)()
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

    class PacketCoreDataPlanesCreateOrUpdate(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [202]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200_201,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )
            if session.http_response.status_code in [200, 201]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200_201,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MobileNetwork/packetCoreControlPlanes/{packetCoreControlPlaneName}/packetCoreDataPlanes/{packetCoreDataPlaneName}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "PUT"

        @property
        def error_format(self):
            return "MgmtErrorFormat"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "packetCoreControlPlaneName", self.ctx.args.pccp_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "packetCoreDataPlaneName", self.ctx.args.pcdp_name,
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
                    "api-version", "2023-09-01",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Content-Type", "application/json",
                ),
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        @property
        def content(self):
            _content_value, _builder = self.new_content_builder(
                self.ctx.args,
                typ=AAZObjectType,
                typ_kwargs={"flags": {"required": True, "client_flatten": True}}
            )
            _builder.set_prop("location", AAZStrType, ".location", typ_kwargs={"flags": {"required": True}})
            _builder.set_prop("properties", AAZObjectType, ".", typ_kwargs={"flags": {"required": True, "client_flatten": True}})
            _builder.set_prop("tags", AAZDictType, ".tags")

            properties = _builder.get(".properties")
            if properties is not None:
                properties.set_prop("userPlaneAccessInterface", AAZObjectType, ".access_interface", typ_kwargs={"flags": {"required": True}})

            user_plane_access_interface = _builder.get(".properties.userPlaneAccessInterface")
            if user_plane_access_interface is not None:
                user_plane_access_interface.set_prop("ipv4Address", AAZStrType, ".ipv4_address")
                user_plane_access_interface.set_prop("ipv4Gateway", AAZStrType, ".ipv4_gateway")
                user_plane_access_interface.set_prop("ipv4Subnet", AAZStrType, ".ipv4_subnet")
                user_plane_access_interface.set_prop("name", AAZStrType, ".name")

            tags = _builder.get(".tags")
            if tags is not None:
                tags.set_elements(AAZStrType, ".")

            return self.serialize_content(_content_value)

        def on_200_201(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200_201
            )

        _schema_on_200_201 = None

        @classmethod
        def _build_schema_on_200_201(cls):
            if cls._schema_on_200_201 is not None:
                return cls._schema_on_200_201

            cls._schema_on_200_201 = AAZObjectType()

            _schema_on_200_201 = cls._schema_on_200_201
            _schema_on_200_201.id = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200_201.location = AAZStrType(
                flags={"required": True},
            )
            _schema_on_200_201.name = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200_201.properties = AAZObjectType(
                flags={"required": True, "client_flatten": True},
            )
            _schema_on_200_201.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _schema_on_200_201.tags = AAZDictType()
            _schema_on_200_201.type = AAZStrType(
                flags={"read_only": True},
            )

            properties = cls._schema_on_200_201.properties
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            properties.user_plane_access_interface = AAZObjectType(
                serialized_name="userPlaneAccessInterface",
                flags={"required": True},
            )
            properties.user_plane_access_virtual_ipv4_addresses = AAZListType(
                serialized_name="userPlaneAccessVirtualIpv4Addresses",
            )

            user_plane_access_interface = cls._schema_on_200_201.properties.user_plane_access_interface
            user_plane_access_interface.ipv4_address = AAZStrType(
                serialized_name="ipv4Address",
            )
            user_plane_access_interface.ipv4_gateway = AAZStrType(
                serialized_name="ipv4Gateway",
            )
            user_plane_access_interface.ipv4_subnet = AAZStrType(
                serialized_name="ipv4Subnet",
            )
            user_plane_access_interface.name = AAZStrType()

            user_plane_access_virtual_ipv4_addresses = cls._schema_on_200_201.properties.user_plane_access_virtual_ipv4_addresses
            user_plane_access_virtual_ipv4_addresses.Element = AAZStrType()

            system_data = cls._schema_on_200_201.system_data
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

            tags = cls._schema_on_200_201.tags
            tags.Element = AAZStrType()

            return cls._schema_on_200_201


class _CreateHelper:
    """Helper class for Create"""


__all__ = ["Create"]
