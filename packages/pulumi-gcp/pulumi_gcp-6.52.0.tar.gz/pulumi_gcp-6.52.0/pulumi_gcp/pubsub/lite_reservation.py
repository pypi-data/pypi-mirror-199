# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['LiteReservationArgs', 'LiteReservation']

@pulumi.input_type
class LiteReservationArgs:
    def __init__(__self__, *,
                 throughput_capacity: pulumi.Input[int],
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a LiteReservation resource.
        :param pulumi.Input[int] throughput_capacity: The reserved throughput capacity. Every unit of throughput capacity is
               equivalent to 1 MiB/s of published messages or 2 MiB/s of subscribed
               messages.
        :param pulumi.Input[str] name: Name of the reservation.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The region of the pubsub lite reservation.
        """
        pulumi.set(__self__, "throughput_capacity", throughput_capacity)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if region is not None:
            pulumi.set(__self__, "region", region)

    @property
    @pulumi.getter(name="throughputCapacity")
    def throughput_capacity(self) -> pulumi.Input[int]:
        """
        The reserved throughput capacity. Every unit of throughput capacity is
        equivalent to 1 MiB/s of published messages or 2 MiB/s of subscribed
        messages.
        """
        return pulumi.get(self, "throughput_capacity")

    @throughput_capacity.setter
    def throughput_capacity(self, value: pulumi.Input[int]):
        pulumi.set(self, "throughput_capacity", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the reservation.
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
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The region of the pubsub lite reservation.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)


@pulumi.input_type
class _LiteReservationState:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 throughput_capacity: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering LiteReservation resources.
        :param pulumi.Input[str] name: Name of the reservation.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The region of the pubsub lite reservation.
        :param pulumi.Input[int] throughput_capacity: The reserved throughput capacity. Every unit of throughput capacity is
               equivalent to 1 MiB/s of published messages or 2 MiB/s of subscribed
               messages.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if throughput_capacity is not None:
            pulumi.set(__self__, "throughput_capacity", throughput_capacity)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the reservation.
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
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The region of the pubsub lite reservation.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter(name="throughputCapacity")
    def throughput_capacity(self) -> Optional[pulumi.Input[int]]:
        """
        The reserved throughput capacity. Every unit of throughput capacity is
        equivalent to 1 MiB/s of published messages or 2 MiB/s of subscribed
        messages.
        """
        return pulumi.get(self, "throughput_capacity")

    @throughput_capacity.setter
    def throughput_capacity(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "throughput_capacity", value)


class LiteReservation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 throughput_capacity: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        A named resource representing a shared pool of capacity.

        To get more information about Reservation, see:

        * [API documentation](https://cloud.google.com/pubsub/lite/docs/reference/rest/v1/admin.projects.locations.reservations)
        * How-to Guides
            * [Managing Reservations](https://cloud.google.com/pubsub/lite/docs/reservations)

        ## Example Usage
        ### Pubsub Lite Reservation Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        project = gcp.organizations.get_project()
        example = gcp.pubsub.LiteReservation("example",
            project=project.number,
            throughput_capacity=2)
        ```

        ## Import

        Reservation can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:pubsub/liteReservation:LiteReservation default projects/{{project}}/locations/{{region}}/reservations/{{name}}
        ```

        ```sh
         $ pulumi import gcp:pubsub/liteReservation:LiteReservation default {{project}}/{{region}}/{{name}}
        ```

        ```sh
         $ pulumi import gcp:pubsub/liteReservation:LiteReservation default {{region}}/{{name}}
        ```

        ```sh
         $ pulumi import gcp:pubsub/liteReservation:LiteReservation default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: Name of the reservation.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The region of the pubsub lite reservation.
        :param pulumi.Input[int] throughput_capacity: The reserved throughput capacity. Every unit of throughput capacity is
               equivalent to 1 MiB/s of published messages or 2 MiB/s of subscribed
               messages.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: LiteReservationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A named resource representing a shared pool of capacity.

        To get more information about Reservation, see:

        * [API documentation](https://cloud.google.com/pubsub/lite/docs/reference/rest/v1/admin.projects.locations.reservations)
        * How-to Guides
            * [Managing Reservations](https://cloud.google.com/pubsub/lite/docs/reservations)

        ## Example Usage
        ### Pubsub Lite Reservation Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        project = gcp.organizations.get_project()
        example = gcp.pubsub.LiteReservation("example",
            project=project.number,
            throughput_capacity=2)
        ```

        ## Import

        Reservation can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:pubsub/liteReservation:LiteReservation default projects/{{project}}/locations/{{region}}/reservations/{{name}}
        ```

        ```sh
         $ pulumi import gcp:pubsub/liteReservation:LiteReservation default {{project}}/{{region}}/{{name}}
        ```

        ```sh
         $ pulumi import gcp:pubsub/liteReservation:LiteReservation default {{region}}/{{name}}
        ```

        ```sh
         $ pulumi import gcp:pubsub/liteReservation:LiteReservation default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param LiteReservationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LiteReservationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 throughput_capacity: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LiteReservationArgs.__new__(LiteReservationArgs)

            __props__.__dict__["name"] = name
            __props__.__dict__["project"] = project
            __props__.__dict__["region"] = region
            if throughput_capacity is None and not opts.urn:
                raise TypeError("Missing required property 'throughput_capacity'")
            __props__.__dict__["throughput_capacity"] = throughput_capacity
        super(LiteReservation, __self__).__init__(
            'gcp:pubsub/liteReservation:LiteReservation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            region: Optional[pulumi.Input[str]] = None,
            throughput_capacity: Optional[pulumi.Input[int]] = None) -> 'LiteReservation':
        """
        Get an existing LiteReservation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: Name of the reservation.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The region of the pubsub lite reservation.
        :param pulumi.Input[int] throughput_capacity: The reserved throughput capacity. Every unit of throughput capacity is
               equivalent to 1 MiB/s of published messages or 2 MiB/s of subscribed
               messages.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _LiteReservationState.__new__(_LiteReservationState)

        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        __props__.__dict__["region"] = region
        __props__.__dict__["throughput_capacity"] = throughput_capacity
        return LiteReservation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the reservation.
        """
        return pulumi.get(self, "name")

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
    def region(self) -> pulumi.Output[Optional[str]]:
        """
        The region of the pubsub lite reservation.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="throughputCapacity")
    def throughput_capacity(self) -> pulumi.Output[int]:
        """
        The reserved throughput capacity. Every unit of throughput capacity is
        equivalent to 1 MiB/s of published messages or 2 MiB/s of subscribed
        messages.
        """
        return pulumi.get(self, "throughput_capacity")

