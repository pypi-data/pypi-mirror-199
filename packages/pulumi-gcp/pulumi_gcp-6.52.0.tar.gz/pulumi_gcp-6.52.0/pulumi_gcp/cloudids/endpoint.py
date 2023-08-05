# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['EndpointArgs', 'Endpoint']

@pulumi.input_type
class EndpointArgs:
    def __init__(__self__, *,
                 location: pulumi.Input[str],
                 network: pulumi.Input[str],
                 severity: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 threat_exceptions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Endpoint resource.
        :param pulumi.Input[str] location: The location for the endpoint.
        :param pulumi.Input[str] network: Name of the VPC network that is connected to the IDS endpoint. This can either contain the VPC network name itself (like "src-net") or the full URL to the network (like "projects/{project_id}/global/networks/src-net").
        :param pulumi.Input[str] severity: The minimum alert severity level that is reported by the endpoint.
               Possible values are `INFORMATIONAL`, `LOW`, `MEDIUM`, `HIGH`, and `CRITICAL`.
        :param pulumi.Input[str] description: An optional description of the endpoint.
        :param pulumi.Input[str] name: Name of the endpoint in the format projects/{project_id}/locations/{locationId}/endpoints/{endpointId}.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] threat_exceptions: Configuration for threat IDs excluded from generating alerts. Limit: 99 IDs.
        """
        pulumi.set(__self__, "location", location)
        pulumi.set(__self__, "network", network)
        pulumi.set(__self__, "severity", severity)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if threat_exceptions is not None:
            pulumi.set(__self__, "threat_exceptions", threat_exceptions)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Input[str]:
        """
        The location for the endpoint.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: pulumi.Input[str]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def network(self) -> pulumi.Input[str]:
        """
        Name of the VPC network that is connected to the IDS endpoint. This can either contain the VPC network name itself (like "src-net") or the full URL to the network (like "projects/{project_id}/global/networks/src-net").
        """
        return pulumi.get(self, "network")

    @network.setter
    def network(self, value: pulumi.Input[str]):
        pulumi.set(self, "network", value)

    @property
    @pulumi.getter
    def severity(self) -> pulumi.Input[str]:
        """
        The minimum alert severity level that is reported by the endpoint.
        Possible values are `INFORMATIONAL`, `LOW`, `MEDIUM`, `HIGH`, and `CRITICAL`.
        """
        return pulumi.get(self, "severity")

    @severity.setter
    def severity(self, value: pulumi.Input[str]):
        pulumi.set(self, "severity", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        An optional description of the endpoint.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the endpoint in the format projects/{project_id}/locations/{locationId}/endpoints/{endpointId}.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="threatExceptions")
    def threat_exceptions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Configuration for threat IDs excluded from generating alerts. Limit: 99 IDs.
        """
        return pulumi.get(self, "threat_exceptions")

    @threat_exceptions.setter
    def threat_exceptions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "threat_exceptions", value)


@pulumi.input_type
class _EndpointState:
    def __init__(__self__, *,
                 create_time: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 endpoint_forwarding_rule: Optional[pulumi.Input[str]] = None,
                 endpoint_ip: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 severity: Optional[pulumi.Input[str]] = None,
                 threat_exceptions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 update_time: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Endpoint resources.
        :param pulumi.Input[str] create_time: Creation timestamp in RFC 3339 text format.
        :param pulumi.Input[str] description: An optional description of the endpoint.
        :param pulumi.Input[str] endpoint_forwarding_rule: URL of the endpoint's network address to which traffic is to be sent by Packet Mirroring.
        :param pulumi.Input[str] endpoint_ip: Internal IP address of the endpoint's network entry point.
        :param pulumi.Input[str] location: The location for the endpoint.
        :param pulumi.Input[str] name: Name of the endpoint in the format projects/{project_id}/locations/{locationId}/endpoints/{endpointId}.
        :param pulumi.Input[str] network: Name of the VPC network that is connected to the IDS endpoint. This can either contain the VPC network name itself (like "src-net") or the full URL to the network (like "projects/{project_id}/global/networks/src-net").
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] severity: The minimum alert severity level that is reported by the endpoint.
               Possible values are `INFORMATIONAL`, `LOW`, `MEDIUM`, `HIGH`, and `CRITICAL`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] threat_exceptions: Configuration for threat IDs excluded from generating alerts. Limit: 99 IDs.
        :param pulumi.Input[str] update_time: Last update timestamp in RFC 3339 text format.
        """
        if create_time is not None:
            pulumi.set(__self__, "create_time", create_time)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if endpoint_forwarding_rule is not None:
            pulumi.set(__self__, "endpoint_forwarding_rule", endpoint_forwarding_rule)
        if endpoint_ip is not None:
            pulumi.set(__self__, "endpoint_ip", endpoint_ip)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if network is not None:
            pulumi.set(__self__, "network", network)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if severity is not None:
            pulumi.set(__self__, "severity", severity)
        if threat_exceptions is not None:
            pulumi.set(__self__, "threat_exceptions", threat_exceptions)
        if update_time is not None:
            pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[pulumi.Input[str]]:
        """
        Creation timestamp in RFC 3339 text format.
        """
        return pulumi.get(self, "create_time")

    @create_time.setter
    def create_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_time", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        An optional description of the endpoint.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="endpointForwardingRule")
    def endpoint_forwarding_rule(self) -> Optional[pulumi.Input[str]]:
        """
        URL of the endpoint's network address to which traffic is to be sent by Packet Mirroring.
        """
        return pulumi.get(self, "endpoint_forwarding_rule")

    @endpoint_forwarding_rule.setter
    def endpoint_forwarding_rule(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "endpoint_forwarding_rule", value)

    @property
    @pulumi.getter(name="endpointIp")
    def endpoint_ip(self) -> Optional[pulumi.Input[str]]:
        """
        Internal IP address of the endpoint's network entry point.
        """
        return pulumi.get(self, "endpoint_ip")

    @endpoint_ip.setter
    def endpoint_ip(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "endpoint_ip", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location for the endpoint.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the endpoint in the format projects/{project_id}/locations/{locationId}/endpoints/{endpointId}.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def network(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the VPC network that is connected to the IDS endpoint. This can either contain the VPC network name itself (like "src-net") or the full URL to the network (like "projects/{project_id}/global/networks/src-net").
        """
        return pulumi.get(self, "network")

    @network.setter
    def network(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter
    def severity(self) -> Optional[pulumi.Input[str]]:
        """
        The minimum alert severity level that is reported by the endpoint.
        Possible values are `INFORMATIONAL`, `LOW`, `MEDIUM`, `HIGH`, and `CRITICAL`.
        """
        return pulumi.get(self, "severity")

    @severity.setter
    def severity(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "severity", value)

    @property
    @pulumi.getter(name="threatExceptions")
    def threat_exceptions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Configuration for threat IDs excluded from generating alerts. Limit: 99 IDs.
        """
        return pulumi.get(self, "threat_exceptions")

    @threat_exceptions.setter
    def threat_exceptions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "threat_exceptions", value)

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> Optional[pulumi.Input[str]]:
        """
        Last update timestamp in RFC 3339 text format.
        """
        return pulumi.get(self, "update_time")

    @update_time.setter
    def update_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "update_time", value)


class Endpoint(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 severity: Optional[pulumi.Input[str]] = None,
                 threat_exceptions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Cloud IDS is an intrusion detection service that provides threat detection for intrusions, malware, spyware, and command-and-control attacks on your network.

        To get more information about Endpoint, see:

        * [API documentation](https://cloud.google.com/intrusion-detection-system/docs/configuring-ids)

        ## Example Usage
        ### Cloudids Endpoint

        ```python
        import pulumi
        import pulumi_gcp as gcp

        default = gcp.compute.Network("default")
        service_range = gcp.compute.GlobalAddress("serviceRange",
            purpose="VPC_PEERING",
            address_type="INTERNAL",
            prefix_length=16,
            network=default.id)
        private_service_connection = gcp.servicenetworking.Connection("privateServiceConnection",
            network=default.id,
            service="servicenetworking.googleapis.com",
            reserved_peering_ranges=[service_range.name])
        example_endpoint = gcp.cloudids.Endpoint("example-endpoint",
            location="us-central1-f",
            network=default.id,
            severity="INFORMATIONAL",
            opts=pulumi.ResourceOptions(depends_on=[private_service_connection]))
        ```

        ## Import

        Endpoint can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:cloudids/endpoint:Endpoint default projects/{{project}}/locations/{{location}}/endpoints/{{name}}
        ```

        ```sh
         $ pulumi import gcp:cloudids/endpoint:Endpoint default {{project}}/{{location}}/{{name}}
        ```

        ```sh
         $ pulumi import gcp:cloudids/endpoint:Endpoint default {{location}}/{{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: An optional description of the endpoint.
        :param pulumi.Input[str] location: The location for the endpoint.
        :param pulumi.Input[str] name: Name of the endpoint in the format projects/{project_id}/locations/{locationId}/endpoints/{endpointId}.
        :param pulumi.Input[str] network: Name of the VPC network that is connected to the IDS endpoint. This can either contain the VPC network name itself (like "src-net") or the full URL to the network (like "projects/{project_id}/global/networks/src-net").
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] severity: The minimum alert severity level that is reported by the endpoint.
               Possible values are `INFORMATIONAL`, `LOW`, `MEDIUM`, `HIGH`, and `CRITICAL`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] threat_exceptions: Configuration for threat IDs excluded from generating alerts. Limit: 99 IDs.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EndpointArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Cloud IDS is an intrusion detection service that provides threat detection for intrusions, malware, spyware, and command-and-control attacks on your network.

        To get more information about Endpoint, see:

        * [API documentation](https://cloud.google.com/intrusion-detection-system/docs/configuring-ids)

        ## Example Usage
        ### Cloudids Endpoint

        ```python
        import pulumi
        import pulumi_gcp as gcp

        default = gcp.compute.Network("default")
        service_range = gcp.compute.GlobalAddress("serviceRange",
            purpose="VPC_PEERING",
            address_type="INTERNAL",
            prefix_length=16,
            network=default.id)
        private_service_connection = gcp.servicenetworking.Connection("privateServiceConnection",
            network=default.id,
            service="servicenetworking.googleapis.com",
            reserved_peering_ranges=[service_range.name])
        example_endpoint = gcp.cloudids.Endpoint("example-endpoint",
            location="us-central1-f",
            network=default.id,
            severity="INFORMATIONAL",
            opts=pulumi.ResourceOptions(depends_on=[private_service_connection]))
        ```

        ## Import

        Endpoint can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:cloudids/endpoint:Endpoint default projects/{{project}}/locations/{{location}}/endpoints/{{name}}
        ```

        ```sh
         $ pulumi import gcp:cloudids/endpoint:Endpoint default {{project}}/{{location}}/{{name}}
        ```

        ```sh
         $ pulumi import gcp:cloudids/endpoint:Endpoint default {{location}}/{{name}}
        ```

        :param str resource_name: The name of the resource.
        :param EndpointArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EndpointArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 severity: Optional[pulumi.Input[str]] = None,
                 threat_exceptions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EndpointArgs.__new__(EndpointArgs)

            __props__.__dict__["description"] = description
            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            if network is None and not opts.urn:
                raise TypeError("Missing required property 'network'")
            __props__.__dict__["network"] = network
            __props__.__dict__["project"] = project
            if severity is None and not opts.urn:
                raise TypeError("Missing required property 'severity'")
            __props__.__dict__["severity"] = severity
            __props__.__dict__["threat_exceptions"] = threat_exceptions
            __props__.__dict__["create_time"] = None
            __props__.__dict__["endpoint_forwarding_rule"] = None
            __props__.__dict__["endpoint_ip"] = None
            __props__.__dict__["update_time"] = None
        super(Endpoint, __self__).__init__(
            'gcp:cloudids/endpoint:Endpoint',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            create_time: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            endpoint_forwarding_rule: Optional[pulumi.Input[str]] = None,
            endpoint_ip: Optional[pulumi.Input[str]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            network: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            severity: Optional[pulumi.Input[str]] = None,
            threat_exceptions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            update_time: Optional[pulumi.Input[str]] = None) -> 'Endpoint':
        """
        Get an existing Endpoint resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] create_time: Creation timestamp in RFC 3339 text format.
        :param pulumi.Input[str] description: An optional description of the endpoint.
        :param pulumi.Input[str] endpoint_forwarding_rule: URL of the endpoint's network address to which traffic is to be sent by Packet Mirroring.
        :param pulumi.Input[str] endpoint_ip: Internal IP address of the endpoint's network entry point.
        :param pulumi.Input[str] location: The location for the endpoint.
        :param pulumi.Input[str] name: Name of the endpoint in the format projects/{project_id}/locations/{locationId}/endpoints/{endpointId}.
        :param pulumi.Input[str] network: Name of the VPC network that is connected to the IDS endpoint. This can either contain the VPC network name itself (like "src-net") or the full URL to the network (like "projects/{project_id}/global/networks/src-net").
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] severity: The minimum alert severity level that is reported by the endpoint.
               Possible values are `INFORMATIONAL`, `LOW`, `MEDIUM`, `HIGH`, and `CRITICAL`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] threat_exceptions: Configuration for threat IDs excluded from generating alerts. Limit: 99 IDs.
        :param pulumi.Input[str] update_time: Last update timestamp in RFC 3339 text format.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EndpointState.__new__(_EndpointState)

        __props__.__dict__["create_time"] = create_time
        __props__.__dict__["description"] = description
        __props__.__dict__["endpoint_forwarding_rule"] = endpoint_forwarding_rule
        __props__.__dict__["endpoint_ip"] = endpoint_ip
        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["network"] = network
        __props__.__dict__["project"] = project
        __props__.__dict__["severity"] = severity
        __props__.__dict__["threat_exceptions"] = threat_exceptions
        __props__.__dict__["update_time"] = update_time
        return Endpoint(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        Creation timestamp in RFC 3339 text format.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        An optional description of the endpoint.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="endpointForwardingRule")
    def endpoint_forwarding_rule(self) -> pulumi.Output[str]:
        """
        URL of the endpoint's network address to which traffic is to be sent by Packet Mirroring.
        """
        return pulumi.get(self, "endpoint_forwarding_rule")

    @property
    @pulumi.getter(name="endpointIp")
    def endpoint_ip(self) -> pulumi.Output[str]:
        """
        Internal IP address of the endpoint's network entry point.
        """
        return pulumi.get(self, "endpoint_ip")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The location for the endpoint.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the endpoint in the format projects/{project_id}/locations/{locationId}/endpoints/{endpointId}.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def network(self) -> pulumi.Output[str]:
        """
        Name of the VPC network that is connected to the IDS endpoint. This can either contain the VPC network name itself (like "src-net") or the full URL to the network (like "projects/{project_id}/global/networks/src-net").
        """
        return pulumi.get(self, "network")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def severity(self) -> pulumi.Output[str]:
        """
        The minimum alert severity level that is reported by the endpoint.
        Possible values are `INFORMATIONAL`, `LOW`, `MEDIUM`, `HIGH`, and `CRITICAL`.
        """
        return pulumi.get(self, "severity")

    @property
    @pulumi.getter(name="threatExceptions")
    def threat_exceptions(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Configuration for threat IDs excluded from generating alerts. Limit: 99 IDs.
        """
        return pulumi.get(self, "threat_exceptions")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        Last update timestamp in RFC 3339 text format.
        """
        return pulumi.get(self, "update_time")

