# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['FirewallRuleArgs', 'FirewallRule']

@pulumi.input_type
class FirewallRuleArgs:
    def __init__(__self__, *,
                 action: pulumi.Input[str],
                 source_range: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a FirewallRule resource.
        :param pulumi.Input[str] action: The action to take if this rule matches.
               Possible values are `UNSPECIFIED_ACTION`, `ALLOW`, and `DENY`.
        :param pulumi.Input[str] source_range: IP address or range, defined using CIDR notation, of requests that this rule applies to.
        :param pulumi.Input[str] description: An optional string description of this rule.
        :param pulumi.Input[int] priority: A positive integer that defines the order of rule evaluation.
               Rules with the lowest priority are evaluated first.
               A default rule at priority Int32.MaxValue matches all IPv4 and
               IPv6 traffic when no previous rule matches. Only the action of
               this rule can be modified by the user.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        pulumi.set(__self__, "action", action)
        pulumi.set(__self__, "source_range", source_range)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if priority is not None:
            pulumi.set(__self__, "priority", priority)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Input[str]:
        """
        The action to take if this rule matches.
        Possible values are `UNSPECIFIED_ACTION`, `ALLOW`, and `DENY`.
        """
        return pulumi.get(self, "action")

    @action.setter
    def action(self, value: pulumi.Input[str]):
        pulumi.set(self, "action", value)

    @property
    @pulumi.getter(name="sourceRange")
    def source_range(self) -> pulumi.Input[str]:
        """
        IP address or range, defined using CIDR notation, of requests that this rule applies to.
        """
        return pulumi.get(self, "source_range")

    @source_range.setter
    def source_range(self, value: pulumi.Input[str]):
        pulumi.set(self, "source_range", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        An optional string description of this rule.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def priority(self) -> Optional[pulumi.Input[int]]:
        """
        A positive integer that defines the order of rule evaluation.
        Rules with the lowest priority are evaluated first.
        A default rule at priority Int32.MaxValue matches all IPv4 and
        IPv6 traffic when no previous rule matches. Only the action of
        this rule can be modified by the user.
        """
        return pulumi.get(self, "priority")

    @priority.setter
    def priority(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "priority", value)

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


@pulumi.input_type
class _FirewallRuleState:
    def __init__(__self__, *,
                 action: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 source_range: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering FirewallRule resources.
        :param pulumi.Input[str] action: The action to take if this rule matches.
               Possible values are `UNSPECIFIED_ACTION`, `ALLOW`, and `DENY`.
        :param pulumi.Input[str] description: An optional string description of this rule.
        :param pulumi.Input[int] priority: A positive integer that defines the order of rule evaluation.
               Rules with the lowest priority are evaluated first.
               A default rule at priority Int32.MaxValue matches all IPv4 and
               IPv6 traffic when no previous rule matches. Only the action of
               this rule can be modified by the user.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] source_range: IP address or range, defined using CIDR notation, of requests that this rule applies to.
        """
        if action is not None:
            pulumi.set(__self__, "action", action)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if priority is not None:
            pulumi.set(__self__, "priority", priority)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if source_range is not None:
            pulumi.set(__self__, "source_range", source_range)

    @property
    @pulumi.getter
    def action(self) -> Optional[pulumi.Input[str]]:
        """
        The action to take if this rule matches.
        Possible values are `UNSPECIFIED_ACTION`, `ALLOW`, and `DENY`.
        """
        return pulumi.get(self, "action")

    @action.setter
    def action(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "action", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        An optional string description of this rule.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def priority(self) -> Optional[pulumi.Input[int]]:
        """
        A positive integer that defines the order of rule evaluation.
        Rules with the lowest priority are evaluated first.
        A default rule at priority Int32.MaxValue matches all IPv4 and
        IPv6 traffic when no previous rule matches. Only the action of
        this rule can be modified by the user.
        """
        return pulumi.get(self, "priority")

    @priority.setter
    def priority(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "priority", value)

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
    @pulumi.getter(name="sourceRange")
    def source_range(self) -> Optional[pulumi.Input[str]]:
        """
        IP address or range, defined using CIDR notation, of requests that this rule applies to.
        """
        return pulumi.get(self, "source_range")

    @source_range.setter
    def source_range(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_range", value)


class FirewallRule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 source_range: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A single firewall rule that is evaluated against incoming traffic
        and provides an action to take on matched requests.

        To get more information about FirewallRule, see:

        * [API documentation](https://cloud.google.com/appengine/docs/admin-api/reference/rest/v1/apps.firewall.ingressRules)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/appengine/docs/standard/python/creating-firewalls#creating_firewall_rules)

        ## Example Usage
        ### App Engine Firewall Rule Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        my_project = gcp.organizations.Project("myProject",
            project_id="ae-project",
            org_id="123456789")
        app = gcp.appengine.Application("app",
            project=my_project.project_id,
            location_id="us-central")
        rule = gcp.appengine.FirewallRule("rule",
            project=app.project,
            priority=1000,
            action="ALLOW",
            source_range="*")
        ```

        ## Import

        FirewallRule can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:appengine/firewallRule:FirewallRule default apps/{{project}}/firewall/ingressRules/{{priority}}
        ```

        ```sh
         $ pulumi import gcp:appengine/firewallRule:FirewallRule default {{project}}/{{priority}}
        ```

        ```sh
         $ pulumi import gcp:appengine/firewallRule:FirewallRule default {{priority}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] action: The action to take if this rule matches.
               Possible values are `UNSPECIFIED_ACTION`, `ALLOW`, and `DENY`.
        :param pulumi.Input[str] description: An optional string description of this rule.
        :param pulumi.Input[int] priority: A positive integer that defines the order of rule evaluation.
               Rules with the lowest priority are evaluated first.
               A default rule at priority Int32.MaxValue matches all IPv4 and
               IPv6 traffic when no previous rule matches. Only the action of
               this rule can be modified by the user.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] source_range: IP address or range, defined using CIDR notation, of requests that this rule applies to.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: FirewallRuleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A single firewall rule that is evaluated against incoming traffic
        and provides an action to take on matched requests.

        To get more information about FirewallRule, see:

        * [API documentation](https://cloud.google.com/appengine/docs/admin-api/reference/rest/v1/apps.firewall.ingressRules)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/appengine/docs/standard/python/creating-firewalls#creating_firewall_rules)

        ## Example Usage
        ### App Engine Firewall Rule Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        my_project = gcp.organizations.Project("myProject",
            project_id="ae-project",
            org_id="123456789")
        app = gcp.appengine.Application("app",
            project=my_project.project_id,
            location_id="us-central")
        rule = gcp.appengine.FirewallRule("rule",
            project=app.project,
            priority=1000,
            action="ALLOW",
            source_range="*")
        ```

        ## Import

        FirewallRule can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:appengine/firewallRule:FirewallRule default apps/{{project}}/firewall/ingressRules/{{priority}}
        ```

        ```sh
         $ pulumi import gcp:appengine/firewallRule:FirewallRule default {{project}}/{{priority}}
        ```

        ```sh
         $ pulumi import gcp:appengine/firewallRule:FirewallRule default {{priority}}
        ```

        :param str resource_name: The name of the resource.
        :param FirewallRuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(FirewallRuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 source_range: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = FirewallRuleArgs.__new__(FirewallRuleArgs)

            if action is None and not opts.urn:
                raise TypeError("Missing required property 'action'")
            __props__.__dict__["action"] = action
            __props__.__dict__["description"] = description
            __props__.__dict__["priority"] = priority
            __props__.__dict__["project"] = project
            if source_range is None and not opts.urn:
                raise TypeError("Missing required property 'source_range'")
            __props__.__dict__["source_range"] = source_range
        super(FirewallRule, __self__).__init__(
            'gcp:appengine/firewallRule:FirewallRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            action: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            priority: Optional[pulumi.Input[int]] = None,
            project: Optional[pulumi.Input[str]] = None,
            source_range: Optional[pulumi.Input[str]] = None) -> 'FirewallRule':
        """
        Get an existing FirewallRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] action: The action to take if this rule matches.
               Possible values are `UNSPECIFIED_ACTION`, `ALLOW`, and `DENY`.
        :param pulumi.Input[str] description: An optional string description of this rule.
        :param pulumi.Input[int] priority: A positive integer that defines the order of rule evaluation.
               Rules with the lowest priority are evaluated first.
               A default rule at priority Int32.MaxValue matches all IPv4 and
               IPv6 traffic when no previous rule matches. Only the action of
               this rule can be modified by the user.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] source_range: IP address or range, defined using CIDR notation, of requests that this rule applies to.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _FirewallRuleState.__new__(_FirewallRuleState)

        __props__.__dict__["action"] = action
        __props__.__dict__["description"] = description
        __props__.__dict__["priority"] = priority
        __props__.__dict__["project"] = project
        __props__.__dict__["source_range"] = source_range
        return FirewallRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Output[str]:
        """
        The action to take if this rule matches.
        Possible values are `UNSPECIFIED_ACTION`, `ALLOW`, and `DENY`.
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        An optional string description of this rule.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def priority(self) -> pulumi.Output[Optional[int]]:
        """
        A positive integer that defines the order of rule evaluation.
        Rules with the lowest priority are evaluated first.
        A default rule at priority Int32.MaxValue matches all IPv4 and
        IPv6 traffic when no previous rule matches. Only the action of
        this rule can be modified by the user.
        """
        return pulumi.get(self, "priority")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="sourceRange")
    def source_range(self) -> pulumi.Output[str]:
        """
        IP address or range, defined using CIDR notation, of requests that this rule applies to.
        """
        return pulumi.get(self, "source_range")

