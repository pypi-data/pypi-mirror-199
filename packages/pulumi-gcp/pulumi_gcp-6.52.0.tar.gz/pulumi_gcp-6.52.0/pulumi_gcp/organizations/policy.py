# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['PolicyArgs', 'Policy']

@pulumi.input_type
class PolicyArgs:
    def __init__(__self__, *,
                 constraint: pulumi.Input[str],
                 org_id: pulumi.Input[str],
                 boolean_policy: Optional[pulumi.Input['PolicyBooleanPolicyArgs']] = None,
                 list_policy: Optional[pulumi.Input['PolicyListPolicyArgs']] = None,
                 restore_policy: Optional[pulumi.Input['PolicyRestorePolicyArgs']] = None,
                 version: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a Policy resource.
        :param pulumi.Input[str] constraint: The name of the Constraint the Policy is configuring, for example, `serviceuser.services`. Check out the [complete list of available constraints](https://cloud.google.com/resource-manager/docs/organization-policy/understanding-constraints#available_constraints).
        :param pulumi.Input[str] org_id: The numeric ID of the organization to set the policy for.
        :param pulumi.Input['PolicyBooleanPolicyArgs'] boolean_policy: A boolean policy is a constraint that is either enforced or not. Structure is documented
               below.
        :param pulumi.Input['PolicyListPolicyArgs'] list_policy: A policy that can define specific values that are allowed or denied for the given constraint. It can also be used to allow or deny all values. Structure is documented below.
        :param pulumi.Input['PolicyRestorePolicyArgs'] restore_policy: A restore policy is a constraint to restore the default policy. Structure is documented below.
        :param pulumi.Input[int] version: Version of the Policy. Default version is 0.
        """
        pulumi.set(__self__, "constraint", constraint)
        pulumi.set(__self__, "org_id", org_id)
        if boolean_policy is not None:
            pulumi.set(__self__, "boolean_policy", boolean_policy)
        if list_policy is not None:
            pulumi.set(__self__, "list_policy", list_policy)
        if restore_policy is not None:
            pulumi.set(__self__, "restore_policy", restore_policy)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def constraint(self) -> pulumi.Input[str]:
        """
        The name of the Constraint the Policy is configuring, for example, `serviceuser.services`. Check out the [complete list of available constraints](https://cloud.google.com/resource-manager/docs/organization-policy/understanding-constraints#available_constraints).
        """
        return pulumi.get(self, "constraint")

    @constraint.setter
    def constraint(self, value: pulumi.Input[str]):
        pulumi.set(self, "constraint", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Input[str]:
        """
        The numeric ID of the organization to set the policy for.
        """
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter(name="booleanPolicy")
    def boolean_policy(self) -> Optional[pulumi.Input['PolicyBooleanPolicyArgs']]:
        """
        A boolean policy is a constraint that is either enforced or not. Structure is documented
        below.
        """
        return pulumi.get(self, "boolean_policy")

    @boolean_policy.setter
    def boolean_policy(self, value: Optional[pulumi.Input['PolicyBooleanPolicyArgs']]):
        pulumi.set(self, "boolean_policy", value)

    @property
    @pulumi.getter(name="listPolicy")
    def list_policy(self) -> Optional[pulumi.Input['PolicyListPolicyArgs']]:
        """
        A policy that can define specific values that are allowed or denied for the given constraint. It can also be used to allow or deny all values. Structure is documented below.
        """
        return pulumi.get(self, "list_policy")

    @list_policy.setter
    def list_policy(self, value: Optional[pulumi.Input['PolicyListPolicyArgs']]):
        pulumi.set(self, "list_policy", value)

    @property
    @pulumi.getter(name="restorePolicy")
    def restore_policy(self) -> Optional[pulumi.Input['PolicyRestorePolicyArgs']]:
        """
        A restore policy is a constraint to restore the default policy. Structure is documented below.
        """
        return pulumi.get(self, "restore_policy")

    @restore_policy.setter
    def restore_policy(self, value: Optional[pulumi.Input['PolicyRestorePolicyArgs']]):
        pulumi.set(self, "restore_policy", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[int]]:
        """
        Version of the Policy. Default version is 0.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "version", value)


@pulumi.input_type
class _PolicyState:
    def __init__(__self__, *,
                 boolean_policy: Optional[pulumi.Input['PolicyBooleanPolicyArgs']] = None,
                 constraint: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 list_policy: Optional[pulumi.Input['PolicyListPolicyArgs']] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 restore_policy: Optional[pulumi.Input['PolicyRestorePolicyArgs']] = None,
                 update_time: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering Policy resources.
        :param pulumi.Input['PolicyBooleanPolicyArgs'] boolean_policy: A boolean policy is a constraint that is either enforced or not. Structure is documented
               below.
        :param pulumi.Input[str] constraint: The name of the Constraint the Policy is configuring, for example, `serviceuser.services`. Check out the [complete list of available constraints](https://cloud.google.com/resource-manager/docs/organization-policy/understanding-constraints#available_constraints).
        :param pulumi.Input[str] etag: (Computed) The etag of the organization policy. `etag` is used for optimistic concurrency control as a way to help prevent simultaneous updates of a policy from overwriting each other.
        :param pulumi.Input['PolicyListPolicyArgs'] list_policy: A policy that can define specific values that are allowed or denied for the given constraint. It can also be used to allow or deny all values. Structure is documented below.
        :param pulumi.Input[str] org_id: The numeric ID of the organization to set the policy for.
        :param pulumi.Input['PolicyRestorePolicyArgs'] restore_policy: A restore policy is a constraint to restore the default policy. Structure is documented below.
        :param pulumi.Input[str] update_time: (Computed) The timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds, representing when the variable was last updated. Example: "2016-10-09T12:33:37.578138407Z".
        :param pulumi.Input[int] version: Version of the Policy. Default version is 0.
        """
        if boolean_policy is not None:
            pulumi.set(__self__, "boolean_policy", boolean_policy)
        if constraint is not None:
            pulumi.set(__self__, "constraint", constraint)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if list_policy is not None:
            pulumi.set(__self__, "list_policy", list_policy)
        if org_id is not None:
            pulumi.set(__self__, "org_id", org_id)
        if restore_policy is not None:
            pulumi.set(__self__, "restore_policy", restore_policy)
        if update_time is not None:
            pulumi.set(__self__, "update_time", update_time)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="booleanPolicy")
    def boolean_policy(self) -> Optional[pulumi.Input['PolicyBooleanPolicyArgs']]:
        """
        A boolean policy is a constraint that is either enforced or not. Structure is documented
        below.
        """
        return pulumi.get(self, "boolean_policy")

    @boolean_policy.setter
    def boolean_policy(self, value: Optional[pulumi.Input['PolicyBooleanPolicyArgs']]):
        pulumi.set(self, "boolean_policy", value)

    @property
    @pulumi.getter
    def constraint(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Constraint the Policy is configuring, for example, `serviceuser.services`. Check out the [complete list of available constraints](https://cloud.google.com/resource-manager/docs/organization-policy/understanding-constraints#available_constraints).
        """
        return pulumi.get(self, "constraint")

    @constraint.setter
    def constraint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "constraint", value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        """
        (Computed) The etag of the organization policy. `etag` is used for optimistic concurrency control as a way to help prevent simultaneous updates of a policy from overwriting each other.
        """
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter(name="listPolicy")
    def list_policy(self) -> Optional[pulumi.Input['PolicyListPolicyArgs']]:
        """
        A policy that can define specific values that are allowed or denied for the given constraint. It can also be used to allow or deny all values. Structure is documented below.
        """
        return pulumi.get(self, "list_policy")

    @list_policy.setter
    def list_policy(self, value: Optional[pulumi.Input['PolicyListPolicyArgs']]):
        pulumi.set(self, "list_policy", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> Optional[pulumi.Input[str]]:
        """
        The numeric ID of the organization to set the policy for.
        """
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter(name="restorePolicy")
    def restore_policy(self) -> Optional[pulumi.Input['PolicyRestorePolicyArgs']]:
        """
        A restore policy is a constraint to restore the default policy. Structure is documented below.
        """
        return pulumi.get(self, "restore_policy")

    @restore_policy.setter
    def restore_policy(self, value: Optional[pulumi.Input['PolicyRestorePolicyArgs']]):
        pulumi.set(self, "restore_policy", value)

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> Optional[pulumi.Input[str]]:
        """
        (Computed) The timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds, representing when the variable was last updated. Example: "2016-10-09T12:33:37.578138407Z".
        """
        return pulumi.get(self, "update_time")

    @update_time.setter
    def update_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "update_time", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[int]]:
        """
        Version of the Policy. Default version is 0.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "version", value)


class Policy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 boolean_policy: Optional[pulumi.Input[pulumi.InputType['PolicyBooleanPolicyArgs']]] = None,
                 constraint: Optional[pulumi.Input[str]] = None,
                 list_policy: Optional[pulumi.Input[pulumi.InputType['PolicyListPolicyArgs']]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 restore_policy: Optional[pulumi.Input[pulumi.InputType['PolicyRestorePolicyArgs']]] = None,
                 version: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        Allows management of Organization Policies for a Google Cloud Organization.

        > **Warning:** This resource has been superseded by `orgpolicy.Policy`. `orgpolicy.Policy` uses Organization Policy API V2 instead of Cloud Resource Manager API V1 and it supports additional features such as tags and conditions.

        To get more information about Organization Policies, see:

        * [API documentation](https://cloud.google.com/resource-manager/reference/rest/v1/organizations/setOrgPolicy)
        * How-to Guides
            * [Introduction to the Organization Policy Service](https://cloud.google.com/resource-manager/docs/organization-policy/overview)

        ## Example Usage

        To set policy with a [boolean constraint](https://cloud.google.com/resource-manager/docs/organization-policy/quickstart-boolean-constraints):

        ```python
        import pulumi
        import pulumi_gcp as gcp

        serial_port_policy = gcp.organizations.Policy("serialPortPolicy",
            boolean_policy=gcp.organizations.PolicyBooleanPolicyArgs(
                enforced=True,
            ),
            constraint="compute.disableSerialPortAccess",
            org_id="123456789")
        ```

        To set a policy with a [list constraint](https://cloud.google.com/resource-manager/docs/organization-policy/quickstart-list-constraints):

        ```python
        import pulumi
        import pulumi_gcp as gcp

        services_policy = gcp.organizations.Policy("servicesPolicy",
            constraint="serviceuser.services",
            list_policy=gcp.organizations.PolicyListPolicyArgs(
                allow=gcp.organizations.PolicyListPolicyAllowArgs(
                    all=True,
                ),
            ),
            org_id="123456789")
        ```

        Or to deny some services, use the following instead:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        services_policy = gcp.organizations.Policy("servicesPolicy",
            constraint="serviceuser.services",
            list_policy=gcp.organizations.PolicyListPolicyArgs(
                deny=gcp.organizations.PolicyListPolicyDenyArgs(
                    values=["cloudresourcemanager.googleapis.com"],
                ),
                suggested_value="compute.googleapis.com",
            ),
            org_id="123456789")
        ```

        To restore the default organization policy, use the following instead:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        services_policy = gcp.organizations.Policy("servicesPolicy",
            constraint="serviceuser.services",
            org_id="123456789",
            restore_policy=gcp.organizations.PolicyRestorePolicyArgs(
                default=True,
            ))
        ```

        ## Import

        Organization Policies can be imported using the `org_id` and the `constraint`, e.g.

        ```sh
         $ pulumi import gcp:organizations/policy:Policy services_policy 123456789/constraints/serviceuser.services
        ```

         It is all right if the constraint contains a slash, as in the example above.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['PolicyBooleanPolicyArgs']] boolean_policy: A boolean policy is a constraint that is either enforced or not. Structure is documented
               below.
        :param pulumi.Input[str] constraint: The name of the Constraint the Policy is configuring, for example, `serviceuser.services`. Check out the [complete list of available constraints](https://cloud.google.com/resource-manager/docs/organization-policy/understanding-constraints#available_constraints).
        :param pulumi.Input[pulumi.InputType['PolicyListPolicyArgs']] list_policy: A policy that can define specific values that are allowed or denied for the given constraint. It can also be used to allow or deny all values. Structure is documented below.
        :param pulumi.Input[str] org_id: The numeric ID of the organization to set the policy for.
        :param pulumi.Input[pulumi.InputType['PolicyRestorePolicyArgs']] restore_policy: A restore policy is a constraint to restore the default policy. Structure is documented below.
        :param pulumi.Input[int] version: Version of the Policy. Default version is 0.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Allows management of Organization Policies for a Google Cloud Organization.

        > **Warning:** This resource has been superseded by `orgpolicy.Policy`. `orgpolicy.Policy` uses Organization Policy API V2 instead of Cloud Resource Manager API V1 and it supports additional features such as tags and conditions.

        To get more information about Organization Policies, see:

        * [API documentation](https://cloud.google.com/resource-manager/reference/rest/v1/organizations/setOrgPolicy)
        * How-to Guides
            * [Introduction to the Organization Policy Service](https://cloud.google.com/resource-manager/docs/organization-policy/overview)

        ## Example Usage

        To set policy with a [boolean constraint](https://cloud.google.com/resource-manager/docs/organization-policy/quickstart-boolean-constraints):

        ```python
        import pulumi
        import pulumi_gcp as gcp

        serial_port_policy = gcp.organizations.Policy("serialPortPolicy",
            boolean_policy=gcp.organizations.PolicyBooleanPolicyArgs(
                enforced=True,
            ),
            constraint="compute.disableSerialPortAccess",
            org_id="123456789")
        ```

        To set a policy with a [list constraint](https://cloud.google.com/resource-manager/docs/organization-policy/quickstart-list-constraints):

        ```python
        import pulumi
        import pulumi_gcp as gcp

        services_policy = gcp.organizations.Policy("servicesPolicy",
            constraint="serviceuser.services",
            list_policy=gcp.organizations.PolicyListPolicyArgs(
                allow=gcp.organizations.PolicyListPolicyAllowArgs(
                    all=True,
                ),
            ),
            org_id="123456789")
        ```

        Or to deny some services, use the following instead:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        services_policy = gcp.organizations.Policy("servicesPolicy",
            constraint="serviceuser.services",
            list_policy=gcp.organizations.PolicyListPolicyArgs(
                deny=gcp.organizations.PolicyListPolicyDenyArgs(
                    values=["cloudresourcemanager.googleapis.com"],
                ),
                suggested_value="compute.googleapis.com",
            ),
            org_id="123456789")
        ```

        To restore the default organization policy, use the following instead:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        services_policy = gcp.organizations.Policy("servicesPolicy",
            constraint="serviceuser.services",
            org_id="123456789",
            restore_policy=gcp.organizations.PolicyRestorePolicyArgs(
                default=True,
            ))
        ```

        ## Import

        Organization Policies can be imported using the `org_id` and the `constraint`, e.g.

        ```sh
         $ pulumi import gcp:organizations/policy:Policy services_policy 123456789/constraints/serviceuser.services
        ```

         It is all right if the constraint contains a slash, as in the example above.

        :param str resource_name: The name of the resource.
        :param PolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 boolean_policy: Optional[pulumi.Input[pulumi.InputType['PolicyBooleanPolicyArgs']]] = None,
                 constraint: Optional[pulumi.Input[str]] = None,
                 list_policy: Optional[pulumi.Input[pulumi.InputType['PolicyListPolicyArgs']]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 restore_policy: Optional[pulumi.Input[pulumi.InputType['PolicyRestorePolicyArgs']]] = None,
                 version: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PolicyArgs.__new__(PolicyArgs)

            __props__.__dict__["boolean_policy"] = boolean_policy
            if constraint is None and not opts.urn:
                raise TypeError("Missing required property 'constraint'")
            __props__.__dict__["constraint"] = constraint
            __props__.__dict__["list_policy"] = list_policy
            if org_id is None and not opts.urn:
                raise TypeError("Missing required property 'org_id'")
            __props__.__dict__["org_id"] = org_id
            __props__.__dict__["restore_policy"] = restore_policy
            __props__.__dict__["version"] = version
            __props__.__dict__["etag"] = None
            __props__.__dict__["update_time"] = None
        super(Policy, __self__).__init__(
            'gcp:organizations/policy:Policy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            boolean_policy: Optional[pulumi.Input[pulumi.InputType['PolicyBooleanPolicyArgs']]] = None,
            constraint: Optional[pulumi.Input[str]] = None,
            etag: Optional[pulumi.Input[str]] = None,
            list_policy: Optional[pulumi.Input[pulumi.InputType['PolicyListPolicyArgs']]] = None,
            org_id: Optional[pulumi.Input[str]] = None,
            restore_policy: Optional[pulumi.Input[pulumi.InputType['PolicyRestorePolicyArgs']]] = None,
            update_time: Optional[pulumi.Input[str]] = None,
            version: Optional[pulumi.Input[int]] = None) -> 'Policy':
        """
        Get an existing Policy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['PolicyBooleanPolicyArgs']] boolean_policy: A boolean policy is a constraint that is either enforced or not. Structure is documented
               below.
        :param pulumi.Input[str] constraint: The name of the Constraint the Policy is configuring, for example, `serviceuser.services`. Check out the [complete list of available constraints](https://cloud.google.com/resource-manager/docs/organization-policy/understanding-constraints#available_constraints).
        :param pulumi.Input[str] etag: (Computed) The etag of the organization policy. `etag` is used for optimistic concurrency control as a way to help prevent simultaneous updates of a policy from overwriting each other.
        :param pulumi.Input[pulumi.InputType['PolicyListPolicyArgs']] list_policy: A policy that can define specific values that are allowed or denied for the given constraint. It can also be used to allow or deny all values. Structure is documented below.
        :param pulumi.Input[str] org_id: The numeric ID of the organization to set the policy for.
        :param pulumi.Input[pulumi.InputType['PolicyRestorePolicyArgs']] restore_policy: A restore policy is a constraint to restore the default policy. Structure is documented below.
        :param pulumi.Input[str] update_time: (Computed) The timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds, representing when the variable was last updated. Example: "2016-10-09T12:33:37.578138407Z".
        :param pulumi.Input[int] version: Version of the Policy. Default version is 0.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PolicyState.__new__(_PolicyState)

        __props__.__dict__["boolean_policy"] = boolean_policy
        __props__.__dict__["constraint"] = constraint
        __props__.__dict__["etag"] = etag
        __props__.__dict__["list_policy"] = list_policy
        __props__.__dict__["org_id"] = org_id
        __props__.__dict__["restore_policy"] = restore_policy
        __props__.__dict__["update_time"] = update_time
        __props__.__dict__["version"] = version
        return Policy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="booleanPolicy")
    def boolean_policy(self) -> pulumi.Output[Optional['outputs.PolicyBooleanPolicy']]:
        """
        A boolean policy is a constraint that is either enforced or not. Structure is documented
        below.
        """
        return pulumi.get(self, "boolean_policy")

    @property
    @pulumi.getter
    def constraint(self) -> pulumi.Output[str]:
        """
        The name of the Constraint the Policy is configuring, for example, `serviceuser.services`. Check out the [complete list of available constraints](https://cloud.google.com/resource-manager/docs/organization-policy/understanding-constraints#available_constraints).
        """
        return pulumi.get(self, "constraint")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        (Computed) The etag of the organization policy. `etag` is used for optimistic concurrency control as a way to help prevent simultaneous updates of a policy from overwriting each other.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="listPolicy")
    def list_policy(self) -> pulumi.Output[Optional['outputs.PolicyListPolicy']]:
        """
        A policy that can define specific values that are allowed or denied for the given constraint. It can also be used to allow or deny all values. Structure is documented below.
        """
        return pulumi.get(self, "list_policy")

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Output[str]:
        """
        The numeric ID of the organization to set the policy for.
        """
        return pulumi.get(self, "org_id")

    @property
    @pulumi.getter(name="restorePolicy")
    def restore_policy(self) -> pulumi.Output[Optional['outputs.PolicyRestorePolicy']]:
        """
        A restore policy is a constraint to restore the default policy. Structure is documented below.
        """
        return pulumi.get(self, "restore_policy")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        (Computed) The timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds, representing when the variable was last updated. Example: "2016-10-09T12:33:37.578138407Z".
        """
        return pulumi.get(self, "update_time")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[int]:
        """
        Version of the Policy. Default version is 0.
        """
        return pulumi.get(self, "version")

