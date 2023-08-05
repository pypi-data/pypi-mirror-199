# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['NetworkPeeringArgs', 'NetworkPeering']

@pulumi.input_type
class NetworkPeeringArgs:
    def __init__(__self__, *,
                 network: pulumi.Input[str],
                 peer_network: pulumi.Input[str],
                 export_custom_routes: Optional[pulumi.Input[bool]] = None,
                 export_subnet_routes_with_public_ip: Optional[pulumi.Input[bool]] = None,
                 import_custom_routes: Optional[pulumi.Input[bool]] = None,
                 import_subnet_routes_with_public_ip: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a NetworkPeering resource.
        :param pulumi.Input[str] network: The primary network of the peering.
        :param pulumi.Input[str] peer_network: The peer network in the peering. The peer network
               may belong to a different project.
        :param pulumi.Input[bool] export_custom_routes: Whether to export the custom routes to the peer network. Defaults to `false`.
        :param pulumi.Input[bool] export_subnet_routes_with_public_ip: Whether subnet routes with public IP range are exported. The default value is true, all subnet routes are exported. The IPv4 special-use ranges (https://en.wikipedia.org/wiki/IPv4#Special_addresses) are always exported to peers and are not controlled by this field.
        :param pulumi.Input[bool] import_custom_routes: Whether to import the custom routes from the peer network. Defaults to `false`.
        :param pulumi.Input[bool] import_subnet_routes_with_public_ip: Whether subnet routes with public IP range are imported. The default value is false. The IPv4 special-use ranges (https://en.wikipedia.org/wiki/IPv4#Special_addresses) are always imported from peers and are not controlled by this field.
        :param pulumi.Input[str] name: Name of the peering.
        """
        pulumi.set(__self__, "network", network)
        pulumi.set(__self__, "peer_network", peer_network)
        if export_custom_routes is not None:
            pulumi.set(__self__, "export_custom_routes", export_custom_routes)
        if export_subnet_routes_with_public_ip is not None:
            pulumi.set(__self__, "export_subnet_routes_with_public_ip", export_subnet_routes_with_public_ip)
        if import_custom_routes is not None:
            pulumi.set(__self__, "import_custom_routes", import_custom_routes)
        if import_subnet_routes_with_public_ip is not None:
            pulumi.set(__self__, "import_subnet_routes_with_public_ip", import_subnet_routes_with_public_ip)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def network(self) -> pulumi.Input[str]:
        """
        The primary network of the peering.
        """
        return pulumi.get(self, "network")

    @network.setter
    def network(self, value: pulumi.Input[str]):
        pulumi.set(self, "network", value)

    @property
    @pulumi.getter(name="peerNetwork")
    def peer_network(self) -> pulumi.Input[str]:
        """
        The peer network in the peering. The peer network
        may belong to a different project.
        """
        return pulumi.get(self, "peer_network")

    @peer_network.setter
    def peer_network(self, value: pulumi.Input[str]):
        pulumi.set(self, "peer_network", value)

    @property
    @pulumi.getter(name="exportCustomRoutes")
    def export_custom_routes(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to export the custom routes to the peer network. Defaults to `false`.
        """
        return pulumi.get(self, "export_custom_routes")

    @export_custom_routes.setter
    def export_custom_routes(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "export_custom_routes", value)

    @property
    @pulumi.getter(name="exportSubnetRoutesWithPublicIp")
    def export_subnet_routes_with_public_ip(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether subnet routes with public IP range are exported. The default value is true, all subnet routes are exported. The IPv4 special-use ranges (https://en.wikipedia.org/wiki/IPv4#Special_addresses) are always exported to peers and are not controlled by this field.
        """
        return pulumi.get(self, "export_subnet_routes_with_public_ip")

    @export_subnet_routes_with_public_ip.setter
    def export_subnet_routes_with_public_ip(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "export_subnet_routes_with_public_ip", value)

    @property
    @pulumi.getter(name="importCustomRoutes")
    def import_custom_routes(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to import the custom routes from the peer network. Defaults to `false`.
        """
        return pulumi.get(self, "import_custom_routes")

    @import_custom_routes.setter
    def import_custom_routes(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "import_custom_routes", value)

    @property
    @pulumi.getter(name="importSubnetRoutesWithPublicIp")
    def import_subnet_routes_with_public_ip(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether subnet routes with public IP range are imported. The default value is false. The IPv4 special-use ranges (https://en.wikipedia.org/wiki/IPv4#Special_addresses) are always imported from peers and are not controlled by this field.
        """
        return pulumi.get(self, "import_subnet_routes_with_public_ip")

    @import_subnet_routes_with_public_ip.setter
    def import_subnet_routes_with_public_ip(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "import_subnet_routes_with_public_ip", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the peering.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _NetworkPeeringState:
    def __init__(__self__, *,
                 export_custom_routes: Optional[pulumi.Input[bool]] = None,
                 export_subnet_routes_with_public_ip: Optional[pulumi.Input[bool]] = None,
                 import_custom_routes: Optional[pulumi.Input[bool]] = None,
                 import_subnet_routes_with_public_ip: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 peer_network: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None,
                 state_details: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering NetworkPeering resources.
        :param pulumi.Input[bool] export_custom_routes: Whether to export the custom routes to the peer network. Defaults to `false`.
        :param pulumi.Input[bool] export_subnet_routes_with_public_ip: Whether subnet routes with public IP range are exported. The default value is true, all subnet routes are exported. The IPv4 special-use ranges (https://en.wikipedia.org/wiki/IPv4#Special_addresses) are always exported to peers and are not controlled by this field.
        :param pulumi.Input[bool] import_custom_routes: Whether to import the custom routes from the peer network. Defaults to `false`.
        :param pulumi.Input[bool] import_subnet_routes_with_public_ip: Whether subnet routes with public IP range are imported. The default value is false. The IPv4 special-use ranges (https://en.wikipedia.org/wiki/IPv4#Special_addresses) are always imported from peers and are not controlled by this field.
        :param pulumi.Input[str] name: Name of the peering.
        :param pulumi.Input[str] network: The primary network of the peering.
        :param pulumi.Input[str] peer_network: The peer network in the peering. The peer network
               may belong to a different project.
        :param pulumi.Input[str] state: State for the peering, either `ACTIVE` or `INACTIVE`. The peering is
               `ACTIVE` when there's a matching configuration in the peer network.
        :param pulumi.Input[str] state_details: Details about the current state of the peering.
        """
        if export_custom_routes is not None:
            pulumi.set(__self__, "export_custom_routes", export_custom_routes)
        if export_subnet_routes_with_public_ip is not None:
            pulumi.set(__self__, "export_subnet_routes_with_public_ip", export_subnet_routes_with_public_ip)
        if import_custom_routes is not None:
            pulumi.set(__self__, "import_custom_routes", import_custom_routes)
        if import_subnet_routes_with_public_ip is not None:
            pulumi.set(__self__, "import_subnet_routes_with_public_ip", import_subnet_routes_with_public_ip)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if network is not None:
            pulumi.set(__self__, "network", network)
        if peer_network is not None:
            pulumi.set(__self__, "peer_network", peer_network)
        if state is not None:
            pulumi.set(__self__, "state", state)
        if state_details is not None:
            pulumi.set(__self__, "state_details", state_details)

    @property
    @pulumi.getter(name="exportCustomRoutes")
    def export_custom_routes(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to export the custom routes to the peer network. Defaults to `false`.
        """
        return pulumi.get(self, "export_custom_routes")

    @export_custom_routes.setter
    def export_custom_routes(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "export_custom_routes", value)

    @property
    @pulumi.getter(name="exportSubnetRoutesWithPublicIp")
    def export_subnet_routes_with_public_ip(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether subnet routes with public IP range are exported. The default value is true, all subnet routes are exported. The IPv4 special-use ranges (https://en.wikipedia.org/wiki/IPv4#Special_addresses) are always exported to peers and are not controlled by this field.
        """
        return pulumi.get(self, "export_subnet_routes_with_public_ip")

    @export_subnet_routes_with_public_ip.setter
    def export_subnet_routes_with_public_ip(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "export_subnet_routes_with_public_ip", value)

    @property
    @pulumi.getter(name="importCustomRoutes")
    def import_custom_routes(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to import the custom routes from the peer network. Defaults to `false`.
        """
        return pulumi.get(self, "import_custom_routes")

    @import_custom_routes.setter
    def import_custom_routes(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "import_custom_routes", value)

    @property
    @pulumi.getter(name="importSubnetRoutesWithPublicIp")
    def import_subnet_routes_with_public_ip(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether subnet routes with public IP range are imported. The default value is false. The IPv4 special-use ranges (https://en.wikipedia.org/wiki/IPv4#Special_addresses) are always imported from peers and are not controlled by this field.
        """
        return pulumi.get(self, "import_subnet_routes_with_public_ip")

    @import_subnet_routes_with_public_ip.setter
    def import_subnet_routes_with_public_ip(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "import_subnet_routes_with_public_ip", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the peering.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def network(self) -> Optional[pulumi.Input[str]]:
        """
        The primary network of the peering.
        """
        return pulumi.get(self, "network")

    @network.setter
    def network(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network", value)

    @property
    @pulumi.getter(name="peerNetwork")
    def peer_network(self) -> Optional[pulumi.Input[str]]:
        """
        The peer network in the peering. The peer network
        may belong to a different project.
        """
        return pulumi.get(self, "peer_network")

    @peer_network.setter
    def peer_network(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "peer_network", value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        """
        State for the peering, either `ACTIVE` or `INACTIVE`. The peering is
        `ACTIVE` when there's a matching configuration in the peer network.
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state", value)

    @property
    @pulumi.getter(name="stateDetails")
    def state_details(self) -> Optional[pulumi.Input[str]]:
        """
        Details about the current state of the peering.
        """
        return pulumi.get(self, "state_details")

    @state_details.setter
    def state_details(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state_details", value)


class NetworkPeering(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 export_custom_routes: Optional[pulumi.Input[bool]] = None,
                 export_subnet_routes_with_public_ip: Optional[pulumi.Input[bool]] = None,
                 import_custom_routes: Optional[pulumi.Input[bool]] = None,
                 import_subnet_routes_with_public_ip: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 peer_network: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a network peering within GCE. For more information see
        [the official documentation](https://cloud.google.com/compute/docs/vpc/vpc-peering)
        and
        [API](https://cloud.google.com/compute/docs/reference/latest/networks).

        > Both networks must create a peering with each other for the peering
        to be functional.

        > Subnets IP ranges across peered VPC networks cannot overlap.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_gcp as gcp

        default = gcp.compute.Network("default", auto_create_subnetworks=False)
        other = gcp.compute.Network("other", auto_create_subnetworks=False)
        peering1 = gcp.compute.NetworkPeering("peering1",
            network=default.self_link,
            peer_network=other.self_link)
        peering2 = gcp.compute.NetworkPeering("peering2",
            network=other.self_link,
            peer_network=default.self_link)
        ```

        ## Import

        VPC network peerings can be imported using the name and project of the primary network the peering exists in and the name of the network peering

        ```sh
         $ pulumi import gcp:compute/networkPeering:NetworkPeering peering_network project-name/network-name/peering-name
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] export_custom_routes: Whether to export the custom routes to the peer network. Defaults to `false`.
        :param pulumi.Input[bool] export_subnet_routes_with_public_ip: Whether subnet routes with public IP range are exported. The default value is true, all subnet routes are exported. The IPv4 special-use ranges (https://en.wikipedia.org/wiki/IPv4#Special_addresses) are always exported to peers and are not controlled by this field.
        :param pulumi.Input[bool] import_custom_routes: Whether to import the custom routes from the peer network. Defaults to `false`.
        :param pulumi.Input[bool] import_subnet_routes_with_public_ip: Whether subnet routes with public IP range are imported. The default value is false. The IPv4 special-use ranges (https://en.wikipedia.org/wiki/IPv4#Special_addresses) are always imported from peers and are not controlled by this field.
        :param pulumi.Input[str] name: Name of the peering.
        :param pulumi.Input[str] network: The primary network of the peering.
        :param pulumi.Input[str] peer_network: The peer network in the peering. The peer network
               may belong to a different project.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NetworkPeeringArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a network peering within GCE. For more information see
        [the official documentation](https://cloud.google.com/compute/docs/vpc/vpc-peering)
        and
        [API](https://cloud.google.com/compute/docs/reference/latest/networks).

        > Both networks must create a peering with each other for the peering
        to be functional.

        > Subnets IP ranges across peered VPC networks cannot overlap.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_gcp as gcp

        default = gcp.compute.Network("default", auto_create_subnetworks=False)
        other = gcp.compute.Network("other", auto_create_subnetworks=False)
        peering1 = gcp.compute.NetworkPeering("peering1",
            network=default.self_link,
            peer_network=other.self_link)
        peering2 = gcp.compute.NetworkPeering("peering2",
            network=other.self_link,
            peer_network=default.self_link)
        ```

        ## Import

        VPC network peerings can be imported using the name and project of the primary network the peering exists in and the name of the network peering

        ```sh
         $ pulumi import gcp:compute/networkPeering:NetworkPeering peering_network project-name/network-name/peering-name
        ```

        :param str resource_name: The name of the resource.
        :param NetworkPeeringArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NetworkPeeringArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 export_custom_routes: Optional[pulumi.Input[bool]] = None,
                 export_subnet_routes_with_public_ip: Optional[pulumi.Input[bool]] = None,
                 import_custom_routes: Optional[pulumi.Input[bool]] = None,
                 import_subnet_routes_with_public_ip: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 peer_network: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NetworkPeeringArgs.__new__(NetworkPeeringArgs)

            __props__.__dict__["export_custom_routes"] = export_custom_routes
            __props__.__dict__["export_subnet_routes_with_public_ip"] = export_subnet_routes_with_public_ip
            __props__.__dict__["import_custom_routes"] = import_custom_routes
            __props__.__dict__["import_subnet_routes_with_public_ip"] = import_subnet_routes_with_public_ip
            __props__.__dict__["name"] = name
            if network is None and not opts.urn:
                raise TypeError("Missing required property 'network'")
            __props__.__dict__["network"] = network
            if peer_network is None and not opts.urn:
                raise TypeError("Missing required property 'peer_network'")
            __props__.__dict__["peer_network"] = peer_network
            __props__.__dict__["state"] = None
            __props__.__dict__["state_details"] = None
        super(NetworkPeering, __self__).__init__(
            'gcp:compute/networkPeering:NetworkPeering',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            export_custom_routes: Optional[pulumi.Input[bool]] = None,
            export_subnet_routes_with_public_ip: Optional[pulumi.Input[bool]] = None,
            import_custom_routes: Optional[pulumi.Input[bool]] = None,
            import_subnet_routes_with_public_ip: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            network: Optional[pulumi.Input[str]] = None,
            peer_network: Optional[pulumi.Input[str]] = None,
            state: Optional[pulumi.Input[str]] = None,
            state_details: Optional[pulumi.Input[str]] = None) -> 'NetworkPeering':
        """
        Get an existing NetworkPeering resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] export_custom_routes: Whether to export the custom routes to the peer network. Defaults to `false`.
        :param pulumi.Input[bool] export_subnet_routes_with_public_ip: Whether subnet routes with public IP range are exported. The default value is true, all subnet routes are exported. The IPv4 special-use ranges (https://en.wikipedia.org/wiki/IPv4#Special_addresses) are always exported to peers and are not controlled by this field.
        :param pulumi.Input[bool] import_custom_routes: Whether to import the custom routes from the peer network. Defaults to `false`.
        :param pulumi.Input[bool] import_subnet_routes_with_public_ip: Whether subnet routes with public IP range are imported. The default value is false. The IPv4 special-use ranges (https://en.wikipedia.org/wiki/IPv4#Special_addresses) are always imported from peers and are not controlled by this field.
        :param pulumi.Input[str] name: Name of the peering.
        :param pulumi.Input[str] network: The primary network of the peering.
        :param pulumi.Input[str] peer_network: The peer network in the peering. The peer network
               may belong to a different project.
        :param pulumi.Input[str] state: State for the peering, either `ACTIVE` or `INACTIVE`. The peering is
               `ACTIVE` when there's a matching configuration in the peer network.
        :param pulumi.Input[str] state_details: Details about the current state of the peering.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _NetworkPeeringState.__new__(_NetworkPeeringState)

        __props__.__dict__["export_custom_routes"] = export_custom_routes
        __props__.__dict__["export_subnet_routes_with_public_ip"] = export_subnet_routes_with_public_ip
        __props__.__dict__["import_custom_routes"] = import_custom_routes
        __props__.__dict__["import_subnet_routes_with_public_ip"] = import_subnet_routes_with_public_ip
        __props__.__dict__["name"] = name
        __props__.__dict__["network"] = network
        __props__.__dict__["peer_network"] = peer_network
        __props__.__dict__["state"] = state
        __props__.__dict__["state_details"] = state_details
        return NetworkPeering(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="exportCustomRoutes")
    def export_custom_routes(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether to export the custom routes to the peer network. Defaults to `false`.
        """
        return pulumi.get(self, "export_custom_routes")

    @property
    @pulumi.getter(name="exportSubnetRoutesWithPublicIp")
    def export_subnet_routes_with_public_ip(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether subnet routes with public IP range are exported. The default value is true, all subnet routes are exported. The IPv4 special-use ranges (https://en.wikipedia.org/wiki/IPv4#Special_addresses) are always exported to peers and are not controlled by this field.
        """
        return pulumi.get(self, "export_subnet_routes_with_public_ip")

    @property
    @pulumi.getter(name="importCustomRoutes")
    def import_custom_routes(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether to import the custom routes from the peer network. Defaults to `false`.
        """
        return pulumi.get(self, "import_custom_routes")

    @property
    @pulumi.getter(name="importSubnetRoutesWithPublicIp")
    def import_subnet_routes_with_public_ip(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether subnet routes with public IP range are imported. The default value is false. The IPv4 special-use ranges (https://en.wikipedia.org/wiki/IPv4#Special_addresses) are always imported from peers and are not controlled by this field.
        """
        return pulumi.get(self, "import_subnet_routes_with_public_ip")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the peering.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def network(self) -> pulumi.Output[str]:
        """
        The primary network of the peering.
        """
        return pulumi.get(self, "network")

    @property
    @pulumi.getter(name="peerNetwork")
    def peer_network(self) -> pulumi.Output[str]:
        """
        The peer network in the peering. The peer network
        may belong to a different project.
        """
        return pulumi.get(self, "peer_network")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        State for the peering, either `ACTIVE` or `INACTIVE`. The peering is
        `ACTIVE` when there's a matching configuration in the peer network.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="stateDetails")
    def state_details(self) -> pulumi.Output[str]:
        """
        Details about the current state of the peering.
        """
        return pulumi.get(self, "state_details")

