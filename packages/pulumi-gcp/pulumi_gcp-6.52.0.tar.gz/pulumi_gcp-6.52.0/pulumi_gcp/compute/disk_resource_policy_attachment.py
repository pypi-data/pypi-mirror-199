# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['DiskResourcePolicyAttachmentArgs', 'DiskResourcePolicyAttachment']

@pulumi.input_type
class DiskResourcePolicyAttachmentArgs:
    def __init__(__self__, *,
                 disk: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 zone: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a DiskResourcePolicyAttachment resource.
        :param pulumi.Input[str] disk: The name of the disk in which the resource policies are attached to.
        :param pulumi.Input[str] name: The resource policy to be attached to the disk for scheduling snapshot
               creation. Do not specify the self link.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] zone: A reference to the zone where the disk resides.
        """
        pulumi.set(__self__, "disk", disk)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if zone is not None:
            pulumi.set(__self__, "zone", zone)

    @property
    @pulumi.getter
    def disk(self) -> pulumi.Input[str]:
        """
        The name of the disk in which the resource policies are attached to.
        """
        return pulumi.get(self, "disk")

    @disk.setter
    def disk(self, value: pulumi.Input[str]):
        pulumi.set(self, "disk", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The resource policy to be attached to the disk for scheduling snapshot
        creation. Do not specify the self link.
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
    def zone(self) -> Optional[pulumi.Input[str]]:
        """
        A reference to the zone where the disk resides.
        """
        return pulumi.get(self, "zone")

    @zone.setter
    def zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "zone", value)


@pulumi.input_type
class _DiskResourcePolicyAttachmentState:
    def __init__(__self__, *,
                 disk: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 zone: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering DiskResourcePolicyAttachment resources.
        :param pulumi.Input[str] disk: The name of the disk in which the resource policies are attached to.
        :param pulumi.Input[str] name: The resource policy to be attached to the disk for scheduling snapshot
               creation. Do not specify the self link.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] zone: A reference to the zone where the disk resides.
        """
        if disk is not None:
            pulumi.set(__self__, "disk", disk)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if zone is not None:
            pulumi.set(__self__, "zone", zone)

    @property
    @pulumi.getter
    def disk(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the disk in which the resource policies are attached to.
        """
        return pulumi.get(self, "disk")

    @disk.setter
    def disk(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "disk", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The resource policy to be attached to the disk for scheduling snapshot
        creation. Do not specify the self link.
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
    def zone(self) -> Optional[pulumi.Input[str]]:
        """
        A reference to the zone where the disk resides.
        """
        return pulumi.get(self, "zone")

    @zone.setter
    def zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "zone", value)


class DiskResourcePolicyAttachment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 disk: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 zone: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Adds existing resource policies to a disk. You can only add one policy
        which will be applied to this disk for scheduling snapshot creation.

        > **Note:** This resource does not support regional disks (`compute.RegionDisk`). For regional disks, please refer to the `compute.RegionDiskResourcePolicyAttachment` resource.

        ## Example Usage
        ### Disk Resource Policy Attachment Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        my_image = gcp.compute.get_image(family="debian-11",
            project="debian-cloud")
        ssd = gcp.compute.Disk("ssd",
            image=my_image.self_link,
            size=50,
            type="pd-ssd",
            zone="us-central1-a")
        attachment = gcp.compute.DiskResourcePolicyAttachment("attachment",
            disk=ssd.name,
            zone="us-central1-a")
        policy = gcp.compute.ResourcePolicy("policy",
            region="us-central1",
            snapshot_schedule_policy=gcp.compute.ResourcePolicySnapshotSchedulePolicyArgs(
                schedule=gcp.compute.ResourcePolicySnapshotSchedulePolicyScheduleArgs(
                    daily_schedule=gcp.compute.ResourcePolicySnapshotSchedulePolicyScheduleDailyScheduleArgs(
                        days_in_cycle=1,
                        start_time="04:00",
                    ),
                ),
            ))
        ```

        ## Import

        DiskResourcePolicyAttachment can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:compute/diskResourcePolicyAttachment:DiskResourcePolicyAttachment default projects/{{project}}/zones/{{zone}}/disks/{{disk}}/{{name}}
        ```

        ```sh
         $ pulumi import gcp:compute/diskResourcePolicyAttachment:DiskResourcePolicyAttachment default {{project}}/{{zone}}/{{disk}}/{{name}}
        ```

        ```sh
         $ pulumi import gcp:compute/diskResourcePolicyAttachment:DiskResourcePolicyAttachment default {{zone}}/{{disk}}/{{name}}
        ```

        ```sh
         $ pulumi import gcp:compute/diskResourcePolicyAttachment:DiskResourcePolicyAttachment default {{disk}}/{{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] disk: The name of the disk in which the resource policies are attached to.
        :param pulumi.Input[str] name: The resource policy to be attached to the disk for scheduling snapshot
               creation. Do not specify the self link.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] zone: A reference to the zone where the disk resides.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DiskResourcePolicyAttachmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Adds existing resource policies to a disk. You can only add one policy
        which will be applied to this disk for scheduling snapshot creation.

        > **Note:** This resource does not support regional disks (`compute.RegionDisk`). For regional disks, please refer to the `compute.RegionDiskResourcePolicyAttachment` resource.

        ## Example Usage
        ### Disk Resource Policy Attachment Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        my_image = gcp.compute.get_image(family="debian-11",
            project="debian-cloud")
        ssd = gcp.compute.Disk("ssd",
            image=my_image.self_link,
            size=50,
            type="pd-ssd",
            zone="us-central1-a")
        attachment = gcp.compute.DiskResourcePolicyAttachment("attachment",
            disk=ssd.name,
            zone="us-central1-a")
        policy = gcp.compute.ResourcePolicy("policy",
            region="us-central1",
            snapshot_schedule_policy=gcp.compute.ResourcePolicySnapshotSchedulePolicyArgs(
                schedule=gcp.compute.ResourcePolicySnapshotSchedulePolicyScheduleArgs(
                    daily_schedule=gcp.compute.ResourcePolicySnapshotSchedulePolicyScheduleDailyScheduleArgs(
                        days_in_cycle=1,
                        start_time="04:00",
                    ),
                ),
            ))
        ```

        ## Import

        DiskResourcePolicyAttachment can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:compute/diskResourcePolicyAttachment:DiskResourcePolicyAttachment default projects/{{project}}/zones/{{zone}}/disks/{{disk}}/{{name}}
        ```

        ```sh
         $ pulumi import gcp:compute/diskResourcePolicyAttachment:DiskResourcePolicyAttachment default {{project}}/{{zone}}/{{disk}}/{{name}}
        ```

        ```sh
         $ pulumi import gcp:compute/diskResourcePolicyAttachment:DiskResourcePolicyAttachment default {{zone}}/{{disk}}/{{name}}
        ```

        ```sh
         $ pulumi import gcp:compute/diskResourcePolicyAttachment:DiskResourcePolicyAttachment default {{disk}}/{{name}}
        ```

        :param str resource_name: The name of the resource.
        :param DiskResourcePolicyAttachmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DiskResourcePolicyAttachmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 disk: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 zone: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DiskResourcePolicyAttachmentArgs.__new__(DiskResourcePolicyAttachmentArgs)

            if disk is None and not opts.urn:
                raise TypeError("Missing required property 'disk'")
            __props__.__dict__["disk"] = disk
            __props__.__dict__["name"] = name
            __props__.__dict__["project"] = project
            __props__.__dict__["zone"] = zone
        super(DiskResourcePolicyAttachment, __self__).__init__(
            'gcp:compute/diskResourcePolicyAttachment:DiskResourcePolicyAttachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            disk: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            zone: Optional[pulumi.Input[str]] = None) -> 'DiskResourcePolicyAttachment':
        """
        Get an existing DiskResourcePolicyAttachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] disk: The name of the disk in which the resource policies are attached to.
        :param pulumi.Input[str] name: The resource policy to be attached to the disk for scheduling snapshot
               creation. Do not specify the self link.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] zone: A reference to the zone where the disk resides.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DiskResourcePolicyAttachmentState.__new__(_DiskResourcePolicyAttachmentState)

        __props__.__dict__["disk"] = disk
        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        __props__.__dict__["zone"] = zone
        return DiskResourcePolicyAttachment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def disk(self) -> pulumi.Output[str]:
        """
        The name of the disk in which the resource policies are attached to.
        """
        return pulumi.get(self, "disk")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource policy to be attached to the disk for scheduling snapshot
        creation. Do not specify the self link.
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
    def zone(self) -> pulumi.Output[str]:
        """
        A reference to the zone where the disk resides.
        """
        return pulumi.get(self, "zone")

