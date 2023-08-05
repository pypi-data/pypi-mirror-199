# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['FirewallPolicyArgs', 'FirewallPolicy']

@pulumi.input_type
class FirewallPolicyArgs:
    def __init__(__self__, *,
                 parent: pulumi.Input[str],
                 short_name: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a FirewallPolicy resource.
        :param pulumi.Input[str] parent: The parent of the firewall policy.
        :param pulumi.Input[str] short_name: User-provided name of the Organization firewall policy. The name should be unique in the organization in which the firewall policy is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression a-z? which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.
        :param pulumi.Input[str] description: An optional description of this resource. Provide this property when you create the resource.
        """
        pulumi.set(__self__, "parent", parent)
        pulumi.set(__self__, "short_name", short_name)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def parent(self) -> pulumi.Input[str]:
        """
        The parent of the firewall policy.
        """
        return pulumi.get(self, "parent")

    @parent.setter
    def parent(self, value: pulumi.Input[str]):
        pulumi.set(self, "parent", value)

    @property
    @pulumi.getter(name="shortName")
    def short_name(self) -> pulumi.Input[str]:
        """
        User-provided name of the Organization firewall policy. The name should be unique in the organization in which the firewall policy is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression a-z? which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.
        """
        return pulumi.get(self, "short_name")

    @short_name.setter
    def short_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "short_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        An optional description of this resource. Provide this property when you create the resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class _FirewallPolicyState:
    def __init__(__self__, *,
                 creation_timestamp: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 fingerprint: Optional[pulumi.Input[str]] = None,
                 firewall_policy_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parent: Optional[pulumi.Input[str]] = None,
                 rule_tuple_count: Optional[pulumi.Input[int]] = None,
                 self_link: Optional[pulumi.Input[str]] = None,
                 self_link_with_id: Optional[pulumi.Input[str]] = None,
                 short_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering FirewallPolicy resources.
        :param pulumi.Input[str] creation_timestamp: Creation timestamp in RFC3339 text format.
        :param pulumi.Input[str] description: An optional description of this resource. Provide this property when you create the resource.
        :param pulumi.Input[str] fingerprint: Fingerprint of the resource. This field is used internally during updates of this resource.
        :param pulumi.Input[str] firewall_policy_id: The unique identifier for the resource. This identifier is defined by the server.
        :param pulumi.Input[str] name: Name of the resource. It is a numeric ID allocated by GCP which uniquely identifies the Firewall Policy.
        :param pulumi.Input[str] parent: The parent of the firewall policy.
        :param pulumi.Input[int] rule_tuple_count: Total count of all firewall policy rule tuples. A firewall policy can not exceed a set number of tuples.
        :param pulumi.Input[str] self_link: Server-defined URL for the resource.
        :param pulumi.Input[str] self_link_with_id: Server-defined URL for this resource with the resource id.
        :param pulumi.Input[str] short_name: User-provided name of the Organization firewall policy. The name should be unique in the organization in which the firewall policy is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression a-z? which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.
        """
        if creation_timestamp is not None:
            pulumi.set(__self__, "creation_timestamp", creation_timestamp)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if fingerprint is not None:
            pulumi.set(__self__, "fingerprint", fingerprint)
        if firewall_policy_id is not None:
            pulumi.set(__self__, "firewall_policy_id", firewall_policy_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if parent is not None:
            pulumi.set(__self__, "parent", parent)
        if rule_tuple_count is not None:
            pulumi.set(__self__, "rule_tuple_count", rule_tuple_count)
        if self_link is not None:
            pulumi.set(__self__, "self_link", self_link)
        if self_link_with_id is not None:
            pulumi.set(__self__, "self_link_with_id", self_link_with_id)
        if short_name is not None:
            pulumi.set(__self__, "short_name", short_name)

    @property
    @pulumi.getter(name="creationTimestamp")
    def creation_timestamp(self) -> Optional[pulumi.Input[str]]:
        """
        Creation timestamp in RFC3339 text format.
        """
        return pulumi.get(self, "creation_timestamp")

    @creation_timestamp.setter
    def creation_timestamp(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "creation_timestamp", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        An optional description of this resource. Provide this property when you create the resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def fingerprint(self) -> Optional[pulumi.Input[str]]:
        """
        Fingerprint of the resource. This field is used internally during updates of this resource.
        """
        return pulumi.get(self, "fingerprint")

    @fingerprint.setter
    def fingerprint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "fingerprint", value)

    @property
    @pulumi.getter(name="firewallPolicyId")
    def firewall_policy_id(self) -> Optional[pulumi.Input[str]]:
        """
        The unique identifier for the resource. This identifier is defined by the server.
        """
        return pulumi.get(self, "firewall_policy_id")

    @firewall_policy_id.setter
    def firewall_policy_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "firewall_policy_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource. It is a numeric ID allocated by GCP which uniquely identifies the Firewall Policy.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def parent(self) -> Optional[pulumi.Input[str]]:
        """
        The parent of the firewall policy.
        """
        return pulumi.get(self, "parent")

    @parent.setter
    def parent(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parent", value)

    @property
    @pulumi.getter(name="ruleTupleCount")
    def rule_tuple_count(self) -> Optional[pulumi.Input[int]]:
        """
        Total count of all firewall policy rule tuples. A firewall policy can not exceed a set number of tuples.
        """
        return pulumi.get(self, "rule_tuple_count")

    @rule_tuple_count.setter
    def rule_tuple_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "rule_tuple_count", value)

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> Optional[pulumi.Input[str]]:
        """
        Server-defined URL for the resource.
        """
        return pulumi.get(self, "self_link")

    @self_link.setter
    def self_link(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "self_link", value)

    @property
    @pulumi.getter(name="selfLinkWithId")
    def self_link_with_id(self) -> Optional[pulumi.Input[str]]:
        """
        Server-defined URL for this resource with the resource id.
        """
        return pulumi.get(self, "self_link_with_id")

    @self_link_with_id.setter
    def self_link_with_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "self_link_with_id", value)

    @property
    @pulumi.getter(name="shortName")
    def short_name(self) -> Optional[pulumi.Input[str]]:
        """
        User-provided name of the Organization firewall policy. The name should be unique in the organization in which the firewall policy is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression a-z? which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.
        """
        return pulumi.get(self, "short_name")

    @short_name.setter
    def short_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "short_name", value)


class FirewallPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 parent: Optional[pulumi.Input[str]] = None,
                 short_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Hierarchical firewall policy rules let you create and enforce a consistent firewall policy across your organization. Rules can explicitly allow or deny connections or delegate evaluation to lower level policies. Policies can be created within organizations or folders.

        This resource should be generally be used with `compute.FirewallPolicyAssociation` and `compute.FirewallPolicyRule`

        For more information see the [official documentation](https://cloud.google.com/vpc/docs/firewall-policies)

        ## Example Usage

        ```python
        import pulumi
        import pulumi_gcp as gcp

        default = gcp.compute.FirewallPolicy("default",
            description="Example Resource",
            parent="organizations/12345",
            short_name="my-policy")
        ```

        ## Import

        FirewallPolicy can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:compute/firewallPolicy:FirewallPolicy default locations/global/firewallPolicies/{{name}}
        ```

        ```sh
         $ pulumi import gcp:compute/firewallPolicy:FirewallPolicy default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: An optional description of this resource. Provide this property when you create the resource.
        :param pulumi.Input[str] parent: The parent of the firewall policy.
        :param pulumi.Input[str] short_name: User-provided name of the Organization firewall policy. The name should be unique in the organization in which the firewall policy is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression a-z? which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: FirewallPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Hierarchical firewall policy rules let you create and enforce a consistent firewall policy across your organization. Rules can explicitly allow or deny connections or delegate evaluation to lower level policies. Policies can be created within organizations or folders.

        This resource should be generally be used with `compute.FirewallPolicyAssociation` and `compute.FirewallPolicyRule`

        For more information see the [official documentation](https://cloud.google.com/vpc/docs/firewall-policies)

        ## Example Usage

        ```python
        import pulumi
        import pulumi_gcp as gcp

        default = gcp.compute.FirewallPolicy("default",
            description="Example Resource",
            parent="organizations/12345",
            short_name="my-policy")
        ```

        ## Import

        FirewallPolicy can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:compute/firewallPolicy:FirewallPolicy default locations/global/firewallPolicies/{{name}}
        ```

        ```sh
         $ pulumi import gcp:compute/firewallPolicy:FirewallPolicy default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param FirewallPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(FirewallPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 parent: Optional[pulumi.Input[str]] = None,
                 short_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = FirewallPolicyArgs.__new__(FirewallPolicyArgs)

            __props__.__dict__["description"] = description
            if parent is None and not opts.urn:
                raise TypeError("Missing required property 'parent'")
            __props__.__dict__["parent"] = parent
            if short_name is None and not opts.urn:
                raise TypeError("Missing required property 'short_name'")
            __props__.__dict__["short_name"] = short_name
            __props__.__dict__["creation_timestamp"] = None
            __props__.__dict__["fingerprint"] = None
            __props__.__dict__["firewall_policy_id"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["rule_tuple_count"] = None
            __props__.__dict__["self_link"] = None
            __props__.__dict__["self_link_with_id"] = None
        super(FirewallPolicy, __self__).__init__(
            'gcp:compute/firewallPolicy:FirewallPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            creation_timestamp: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            fingerprint: Optional[pulumi.Input[str]] = None,
            firewall_policy_id: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            parent: Optional[pulumi.Input[str]] = None,
            rule_tuple_count: Optional[pulumi.Input[int]] = None,
            self_link: Optional[pulumi.Input[str]] = None,
            self_link_with_id: Optional[pulumi.Input[str]] = None,
            short_name: Optional[pulumi.Input[str]] = None) -> 'FirewallPolicy':
        """
        Get an existing FirewallPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] creation_timestamp: Creation timestamp in RFC3339 text format.
        :param pulumi.Input[str] description: An optional description of this resource. Provide this property when you create the resource.
        :param pulumi.Input[str] fingerprint: Fingerprint of the resource. This field is used internally during updates of this resource.
        :param pulumi.Input[str] firewall_policy_id: The unique identifier for the resource. This identifier is defined by the server.
        :param pulumi.Input[str] name: Name of the resource. It is a numeric ID allocated by GCP which uniquely identifies the Firewall Policy.
        :param pulumi.Input[str] parent: The parent of the firewall policy.
        :param pulumi.Input[int] rule_tuple_count: Total count of all firewall policy rule tuples. A firewall policy can not exceed a set number of tuples.
        :param pulumi.Input[str] self_link: Server-defined URL for the resource.
        :param pulumi.Input[str] self_link_with_id: Server-defined URL for this resource with the resource id.
        :param pulumi.Input[str] short_name: User-provided name of the Organization firewall policy. The name should be unique in the organization in which the firewall policy is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression a-z? which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _FirewallPolicyState.__new__(_FirewallPolicyState)

        __props__.__dict__["creation_timestamp"] = creation_timestamp
        __props__.__dict__["description"] = description
        __props__.__dict__["fingerprint"] = fingerprint
        __props__.__dict__["firewall_policy_id"] = firewall_policy_id
        __props__.__dict__["name"] = name
        __props__.__dict__["parent"] = parent
        __props__.__dict__["rule_tuple_count"] = rule_tuple_count
        __props__.__dict__["self_link"] = self_link
        __props__.__dict__["self_link_with_id"] = self_link_with_id
        __props__.__dict__["short_name"] = short_name
        return FirewallPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="creationTimestamp")
    def creation_timestamp(self) -> pulumi.Output[str]:
        """
        Creation timestamp in RFC3339 text format.
        """
        return pulumi.get(self, "creation_timestamp")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        An optional description of this resource. Provide this property when you create the resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def fingerprint(self) -> pulumi.Output[str]:
        """
        Fingerprint of the resource. This field is used internally during updates of this resource.
        """
        return pulumi.get(self, "fingerprint")

    @property
    @pulumi.getter(name="firewallPolicyId")
    def firewall_policy_id(self) -> pulumi.Output[str]:
        """
        The unique identifier for the resource. This identifier is defined by the server.
        """
        return pulumi.get(self, "firewall_policy_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the resource. It is a numeric ID allocated by GCP which uniquely identifies the Firewall Policy.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def parent(self) -> pulumi.Output[str]:
        """
        The parent of the firewall policy.
        """
        return pulumi.get(self, "parent")

    @property
    @pulumi.getter(name="ruleTupleCount")
    def rule_tuple_count(self) -> pulumi.Output[int]:
        """
        Total count of all firewall policy rule tuples. A firewall policy can not exceed a set number of tuples.
        """
        return pulumi.get(self, "rule_tuple_count")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> pulumi.Output[str]:
        """
        Server-defined URL for the resource.
        """
        return pulumi.get(self, "self_link")

    @property
    @pulumi.getter(name="selfLinkWithId")
    def self_link_with_id(self) -> pulumi.Output[str]:
        """
        Server-defined URL for this resource with the resource id.
        """
        return pulumi.get(self, "self_link_with_id")

    @property
    @pulumi.getter(name="shortName")
    def short_name(self) -> pulumi.Output[str]:
        """
        User-provided name of the Organization firewall policy. The name should be unique in the organization in which the firewall policy is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression a-z? which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.
        """
        return pulumi.get(self, "short_name")

