# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=protected-access, line-too-long, too-many-branches, raise-missing-from, consider-using-f-string

from collections import defaultdict
from knack.util import to_snake_case
from azure.cli.core.aaz import has_value, AAZStrArg
from azure.cli.core.azclierror import ValidationError
from azure.cli.core.commands.validators import validate_file_or_dict
from azure.cli.command_modules.monitor.actions import AAZCustomListArg

from .aaz.latest.monitor.data_collection.endpoint import Create as _EndpointCreate
from .aaz.latest.monitor.data_collection.rule import Create as _RuleCreate, Update as _RuleUpdate, Show as RuleShow

try:
    from .manual.custom import *  # noqa: F403
except ImportError as e:
    if e.name.endswith('manual.custom'):
        pass
    else:
        raise e


class EndpointCreate(_EndpointCreate):

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        args_schema = super()._build_arguments_schema(*args, **kwargs)
        args_schema.public_network_access._required = True
        return args_schema


def monitor_data_collection_rule_show(client,
                                      resource_group_name,
                                      data_collection_rule_name):
    return client.get(resource_group_name=resource_group_name,
                      data_collection_rule_name=data_collection_rule_name)


def monitor_data_collection_endpoint_show(client,
                                          resource_group_name,
                                          data_collection_endpoint_name):
    return client.get(resource_group_name=resource_group_name,
                      data_collection_endpoint_name=data_collection_endpoint_name)


def monitor_data_collection_rule_association_list(cmd, resource_group_name=None, data_collection_rule_name=None,
                                                  data_collection_endpoint_name=None, resource_uri=None):
    if resource_group_name and data_collection_rule_name is not None:
        from .aaz.latest.monitor.data_collection.rule.association import List as ListByRule
        return ListByRule(cli_ctx=cmd.cli_ctx)(command_args={
            "data_collection_rule_name": data_collection_rule_name,
            "resource_group": resource_group_name,
        })
    if resource_group_name and data_collection_endpoint_name is not None:
        from .aaz.latest.monitor.data_collection.endpoint.association import List as ListByEndpoint
        return ListByEndpoint(cli_ctx=cmd.cli_ctx)(command_args={
            "data_collection_endpoint_name": data_collection_rule_name,
            "resource_group": resource_group_name,
        })
    from .aaz.latest.monitor.data_collection.rule.association import ListByResource
    return ListByResource(cli_ctx=cmd.cli_ctx)(command_args={"resource_uri": resource_uri})


class RuleCreate(_RuleCreate):

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        args_schema = super()._build_arguments_schema(*args, **kwargs)
        args_schema.rule_file = AAZStrArg(
            options=["--rule-file"],
            required=False,
            help='The json file for rule parameters. If provided, corresponding parameter will be overwrited by value from rule file' + '''
            Usage:   --rule-file sample.json
            rule json file should be rule parameters organized as json format, like below:
        {
            "properties": {
                "destinations": {
                    "azureMonitorMetrics": {
                        "name": "azureMonitorMetrics-default"
                    }
                },
                "dataFlows": [
                    {
                        "streams": [
                            "Microsoft-InsightsMetrics"
                        ],
                        "destinations": [
                            "azureMonitorMetrics-default"
                        ]
                    }
                ]
            }
        }.
        ''',
        )
        return args_schema

    def pre_operations(self):
        args = self.ctx.args
        if not has_value(args.rule_file):
            return
        rule_file = args.rule_file.to_serialized_data()
        from azure.cli.core.util import get_file_json
        from azure.cli.core.azclierror import FileOperationError, UnclassifiedUserFault

        try:
            json_data = get_file_json(rule_file)
        except FileNotFoundError:
            raise FileOperationError("No such file: " + str(rule_file))
        except IsADirectoryError:
            raise FileOperationError("Is a directory: " + str(rule_file))
        except PermissionError:
            raise FileOperationError("Permission denied: " + str(rule_file))
        except OSError as err:
            raise UnclassifiedUserFault(err)
        for key_prop in json_data:
            if key_prop == 'properties':
                data = json_data['properties']
            else:
                data = json_data
        for key in data:
            arg_key = to_snake_case(key)
            if hasattr(args, arg_key):
                setattr(args, arg_key, data[key])


def process_data_flows_remain(args):
    if not has_value(args.data_flows_remain):
        return
    properties = defaultdict(list)
    for x in args.data_flows_remain:
        if has_value(x):
            if '=' in x.to_serialized_data():
                key, value = x.to_serialized_data().split('=', 1)
                properties[key].append(value)
            else:
                raise ValidationError('--data-flows format: [KEY=VALUE ...]')

    properties = dict(properties)
    data_flows = {}
    for k, v in properties.items():
        kl = k.lower()
        if kl == 'streams':
            data_flows['streams'] = v
        elif kl == 'destinations':
            data_flows['destinations'] = v
    args.data_flows.append(data_flows)


def process_data_source_extension(args):
    if not has_value(args.extensions):
        return
    extension_value = validate_file_or_dict(args.extensions.to_serialized_data())
    if extension_value is not None:
        args.data_sources.extensions.append(extension_value)


def process_data_source_performance_counters(args):
    if not has_value(args.performance_counters):
        return
    properties = defaultdict(list)
    for x in args.performance_counters:
        if has_value(x):
            if '=' in x.to_serialized_data():
                key, value = x.to_serialized_data().split('=', 1)
                properties[key].append(value)
            else:
                raise ValidationError('--performance-counters format: [KEY=VALUE ...]')
    properties = dict(properties)
    performance_counter = {}
    for k, v in properties.items():
        kl = k.lower()
        if kl == 'streams':
            performance_counter['streams'] = v
        elif kl == 'sampling-frequency':
            try:
                performance_counter['sampling_frequency_in_seconds'] = int(v[0])
            except ValueError:
                raise ValidationError('invalid sampling-frequency={}'.format(v[0]))
        elif kl == 'counter-specifiers':
            performance_counter['counter_specifiers'] = v
        elif kl == 'name':
            performance_counter['name'] = v[0]
    args.data_sources.performance_counters.append(performance_counter)


def process_data_source_syslog(args):
    if not has_value(args.syslog):
        return
    properties = defaultdict(list)
    for x in args.syslog:
        if has_value(x):
            if '=' in x.to_serialized_data():
                key, value = x.to_serialized_data().split('=', 1)
                properties[key].append(value)
            else:
                raise ValidationError('--syslog format: [KEY=VALUE ...]')
    properties = dict(properties)
    syslog = {}
    for k, v in properties.items():
        kl = k.lower()
        if kl == 'streams':
            syslog['streams'] = v
        elif kl == 'facility-names':
            syslog['facility_names'] = v
        elif kl == 'log-levels':
            syslog['log_levels'] = v
        elif kl == 'name':
            syslog['name'] = v[0]
    args.data_sources.syslog.append(syslog)


def process_data_source_windows_event_logs(args):
    if not has_value(args.windows_event_logs):
        return
    properties = defaultdict(list)
    for x in args.windows_event_logs:
        if has_value(x):
            if '=' in x.to_serialized_data():
                key, value = x.to_serialized_data().split('=', 1)
                properties[key].append(value)
            else:
                raise ValidationError('--windows-event-logs format: [KEY=VALUE ...]')
    properties = dict(properties)
    windows_event_logs = {}
    for k, v in properties.items():
        kl = k.lower()
        if kl == 'streams':
            windows_event_logs['streams'] = v
        elif kl == 'x-path-queries':
            windows_event_logs['x_path_queries'] = v
        elif kl == 'name':
            windows_event_logs['name'] = v[0]
    args.data_sources.windows_event_logs.append(windows_event_logs)


def process_destination_log_analytics(args):
    if not has_value(args.log_analytics):
        return
    properties = defaultdict(list)
    for x in args.log_analytics:
        if has_value(x):
            if '=' in x.to_serialized_data():
                key, value = x.to_serialized_data().split('=', 1)
                properties[key].append(value)
            else:
                raise ValidationError('--log-analytics format: [KEY=VALUE ...]')
    properties = dict(properties)
    log_analytics = {}
    for k, v in properties.items():
        kl = k.lower()
        if kl == 'resource-id':
            log_analytics['workspace_resource_id'] = v[0]
        elif kl == 'name':
            log_analytics['name'] = v[0]
    args.destinations.log_analytics.append(log_analytics)


def process_destination_monitor_metrics(args):
    if not has_value(args.monitor_metrics):
        return
    properties = defaultdict(list)
    for x in args.monitor_metrics:
        if has_value(x):
            if '=' in x.to_serialized_data():
                key, value = x.to_serialized_data().split('=', 1)
                properties[key].append(value)
            else:
                raise ValidationError('--monitor-metrics format: [KEY=VALUE ...]')
    properties = dict(properties)
    azure_monitor_metrics = {}
    for k, v in properties.items():
        kl = k.lower()
        if kl == 'name':
            azure_monitor_metrics['name'] = v[0]
    args.destinations.azure_monitor_metrics = azure_monitor_metrics


class RuleUpdate(_RuleUpdate):

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        args_schema = super()._build_arguments_schema(*args, **kwargs)
        args_schema.data_flows_remain = AAZCustomListArg(
            options=["--data-flows", "--data-flows-remain"],
            arg_group="Data Flow",
            help="The specification of data flows." + '''
        Usage: --data-flows streams=XX1 streams=XX2 destinations=XX1 destinations=XX2
        streams: Required. List of streams for this data flow.
        destinations: Required. List of destinations for this data flow.
        Multiple actions can be specified by using more than one --data-flows argument.
        '''
        )
        args_schema.data_flows_remain.Element = AAZStrArg()

        args_schema.extensions = AAZStrArg(
            options=["--extensions"],
            arg_group="Data Sources",
            help="The list of Azure VM extension data source configurations. Expected value: json-string/@json-file.",
        )

        args_schema.performance_counters = AAZCustomListArg(
            options=["--performance-counters"],
            arg_group="Data Sources",
            help="The list of performance counter data source configurations." + '''
            Usage: --performance-counters streams=XX1 streams=XX2 sampling-frequency=XX counter-specifiers=XX1 counter-specifiers=XX2 name=XX
            streams: Required. List of streams that this data source will be sent to. A stream indicates what schema will be used for this data and usually what table in Log Analytics the data will be sent to.
            sampling-frequency: Required. The number of seconds between consecutive counter measurements(samples).
            counter-specifiers: Required. A list of specifier names of the performance counters you want to collect. Use a wildcard (*) to collect a counter for all instances. To get a list of performance counters on Windows, run the command 'typeperf'.
            name: Required. A friendly name for the data source.  This name should be unique across all data sources (regardless of type) within the data collection rule.
            Multiple actions can be specified by using more than one --performance-counters argument.
            ''',
        )
        args_schema.performance_counters.Element = AAZStrArg()

        args_schema.syslog = AAZCustomListArg(
            options=["--syslog"],
            arg_group="Data Sources",
            help="The list of Syslog data source configurations." + '''
            Usage: --syslog streams=XX1 streams=XX2 facility-names=XX1 facility-names=XX2 log-levels=XX1 log-levels=XX2 name=XX
            streams: Required. List of streams that this data source will be sent to. A stream indicates what schema will be used for this data and usually what table in Log Analytics the data will be sent to.
            facility-names: Required. The list of facility names.
            log-levels: The log levels to collect.
            name: Required. A friendly name for the data source.  This name should be unique across all data sources (regardless of type) within the data collection rule.
            Multiple actions can be specified by using more than one --syslog argument.
            '''
        )
        args_schema.syslog.Element = AAZStrArg()

        args_schema.windows_event_logs = AAZCustomListArg(
            options=["--windows-event-logs"],
            arg_group="Data Sources",
            help="The list of Windows Event Log data source configurations." + '''
            Usage: --windows-event-logs streams=XX1 streams=XX2 x-path-queries=XX1 x-path-queries=XX2 name=XX
            streams: Required. List of streams that this data source will be sent to. A stream indicates what schema will be used for this data and usually what table in Log Analytics the data will be sent to.
            x-path-queries: Required. A list of Windows Event Log queries in XPATH format.
            name: Required. A friendly name for the data source.  This name should be unique across all data sources (regardless of type) within the data collection rule.
            Multiple actions can be specified by using more than one --windows-event-logs argument.
            '''
        )
        args_schema.windows_event_logs.Element = AAZStrArg()

        args_schema.log_analytics = AAZCustomListArg(
            options=["--log-analytics"],
            arg_group="Destinations",
            help="List of Log Analytics destinations." + '''
            Usage: --log-analytics resource-id=XX name=XX
            resource-id: Required. The resource ID of the Log Analytics workspace.
            name: Required. A friendly name for the destination.  This name should be unique across all destinations (regardless of type) within the data collection rule.
            Multiple actions can be specified by using more than one --log-analytics argument.
            '''
        )
        args_schema.log_analytics.Element = AAZStrArg()

        args_schema.monitor_metrics = AAZCustomListArg(
            options=["--monitor-metrics"],
            arg_group="Destinations",
            help="Azure Monitor Metrics destination." + '''
            Usage: --monitor-metrics name=XX
            name: Required. A friendly name for the destination.  This name should be unique across all destinations (regardless of type) within the data collection rule.
            '''
        )
        args_schema.monitor_metrics.Element = AAZStrArg()

        return args_schema

    def pre_instance_update(self, instance):
        args = self.ctx.args
        process_data_flows_remain(args)
        process_data_source_extension(args)
        process_data_source_performance_counters(args)
        process_data_source_syslog(args)
        process_data_source_windows_event_logs(args)
        process_destination_log_analytics(args)
        process_destination_monitor_metrics(args)


def data_collection_rules_data_flows_list(cmd, resource_group_name, data_collection_rule_name):
    rule_instance = RuleShow(cli_ctx=cmd.cli_ctx)(command_args={
        "resource_group": resource_group_name,
        "data_collection_rule_name": data_collection_rule_name})
    return rule_instance["dataFlows"]


def data_collection_rules_log_analytics_list(cmd, resource_group_name, data_collection_rule_name):
    rule_instance = RuleShow(cli_ctx=cmd.cli_ctx)(command_args={
        "resource_group": resource_group_name,
        "data_collection_rule_name": data_collection_rule_name
    })
    return rule_instance["destinations"].get("logAnalytics", [])


def data_collection_rules_log_analytics_show(cmd, resource_group_name, data_collection_rule_name, name):
    rule_instance = RuleShow(cli_ctx=cmd.cli_ctx)(command_args={
        "resource_group": resource_group_name,
        "data_collection_rule_name": data_collection_rule_name
    })
    item_list = rule_instance["destinations"].get("logAnalytics", [])
    for item in item_list:
        if item["name"] == name:
            return item
    return {}


def data_collection_rules_performance_counters_list(cmd, resource_group_name, data_collection_rule_name):
    rule_instance = RuleShow(cli_ctx=cmd.cli_ctx)(command_args={
        "resource_group": resource_group_name,
        "data_collection_rule_name": data_collection_rule_name
    })
    return rule_instance["dataSources"].get("performanceCounters", [])


def data_collection_rules_performance_counters_show(cmd, resource_group_name, data_collection_rule_name, name):
    rule_instance = RuleShow(cli_ctx=cmd.cli_ctx)(command_args={
        "resource_group": resource_group_name,
        "data_collection_rule_name": data_collection_rule_name
    })
    item_list = rule_instance["dataSources"].get("performanceCounters", [])
    for item in item_list:
        if item['name'] == name:
            return item
    return {}


def data_collection_rules_windows_event_logs_list(cmd, resource_group_name, data_collection_rule_name):
    rule_instance = RuleShow(cli_ctx=cmd.cli_ctx)(command_args={
        "resource_group": resource_group_name,
        "data_collection_rule_name": data_collection_rule_name
    })
    return rule_instance["dataSources"].get("windowsEventLogs", [])


def data_collection_rules_windows_event_logs_show(cmd, resource_group_name, data_collection_rule_name, name):
    rule_instance = RuleShow(cli_ctx=cmd.cli_ctx)(command_args={
        "resource_group": resource_group_name,
        "data_collection_rule_name": data_collection_rule_name
    })
    item_list = rule_instance["dataSources"].get("windowsEventLogs", [])
    for item in item_list:
        if item['name'] == name:
            return item
    return {}


def data_collection_rules_syslog_list(cmd, resource_group_name, data_collection_rule_name):
    rule_instance = RuleShow(cli_ctx=cmd.cli_ctx)(command_args={
        "resource_group": resource_group_name,
        "data_collection_rule_name": data_collection_rule_name
    })
    return rule_instance["dataSources"].get("syslog", [])


def data_collection_rules_syslog_show(cmd, resource_group_name, data_collection_rule_name, name):
    rule_instance = RuleShow(cli_ctx=cmd.cli_ctx)(command_args={
        "resource_group": resource_group_name,
        "data_collection_rule_name": data_collection_rule_name
    })
    item_list = rule_instance["dataSources"].get("syslog", [])
    for item in item_list:
        if item['name'] == name:
            return item
    return {}
