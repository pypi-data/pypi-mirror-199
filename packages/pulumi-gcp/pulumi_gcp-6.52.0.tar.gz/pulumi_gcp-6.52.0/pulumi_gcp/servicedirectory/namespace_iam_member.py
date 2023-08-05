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

__all__ = ['NamespaceIamMemberArgs', 'NamespaceIamMember']

@pulumi.input_type
class NamespaceIamMemberArgs:
    def __init__(__self__, *,
                 member: pulumi.Input[str],
                 role: pulumi.Input[str],
                 condition: Optional[pulumi.Input['NamespaceIamMemberConditionArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a NamespaceIamMember resource.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `servicedirectory.NamespaceIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        :param pulumi.Input[str] name: Used to find the parent resource to bind the IAM policy to
        """
        pulumi.set(__self__, "member", member)
        pulumi.set(__self__, "role", role)
        if condition is not None:
            pulumi.set(__self__, "condition", condition)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def member(self) -> pulumi.Input[str]:
        return pulumi.get(self, "member")

    @member.setter
    def member(self, value: pulumi.Input[str]):
        pulumi.set(self, "member", value)

    @property
    @pulumi.getter
    def role(self) -> pulumi.Input[str]:
        """
        The role that should be applied. Only one
        `servicedirectory.NamespaceIamBinding` can be used per role. Note that custom roles must be of the format
        `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: pulumi.Input[str]):
        pulumi.set(self, "role", value)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input['NamespaceIamMemberConditionArgs']]:
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input['NamespaceIamMemberConditionArgs']]):
        pulumi.set(self, "condition", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _NamespaceIamMemberState:
    def __init__(__self__, *,
                 condition: Optional[pulumi.Input['NamespaceIamMemberConditionArgs']] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 member: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering NamespaceIamMember resources.
        :param pulumi.Input[str] etag: (Computed) The etag of the IAM policy.
        :param pulumi.Input[str] name: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `servicedirectory.NamespaceIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        if condition is not None:
            pulumi.set(__self__, "condition", condition)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if member is not None:
            pulumi.set(__self__, "member", member)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if role is not None:
            pulumi.set(__self__, "role", role)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input['NamespaceIamMemberConditionArgs']]:
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input['NamespaceIamMemberConditionArgs']]):
        pulumi.set(self, "condition", value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        """
        (Computed) The etag of the IAM policy.
        """
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter
    def member(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "member")

    @member.setter
    def member(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "member", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def role(self) -> Optional[pulumi.Input[str]]:
        """
        The role that should be applied. Only one
        `servicedirectory.NamespaceIamBinding` can be used per role. Note that custom roles must be of the format
        `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role", value)


class NamespaceIamMember(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 condition: Optional[pulumi.Input[pulumi.InputType['NamespaceIamMemberConditionArgs']]] = None,
                 member: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Three different resources help you manage your IAM policy for Service Directory Namespace. Each of these resources serves a different use case:

        * `servicedirectory.NamespaceIamPolicy`: Authoritative. Sets the IAM policy for the namespace and replaces any existing policy already attached.
        * `servicedirectory.NamespaceIamBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the namespace are preserved.
        * `servicedirectory.NamespaceIamMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the namespace are preserved.

        > **Note:** `servicedirectory.NamespaceIamPolicy` **cannot** be used in conjunction with `servicedirectory.NamespaceIamBinding` and `servicedirectory.NamespaceIamMember` or they will fight over what your policy should be.

        > **Note:** `servicedirectory.NamespaceIamBinding` resources **can be** used in conjunction with `servicedirectory.NamespaceIamMember` resources **only if** they do not grant privilege to the same role.

        ## google\\_service\\_directory\\_namespace\\_iam\\_policy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/viewer",
            members=["user:jane@example.com"],
        )])
        policy = gcp.servicedirectory.NamespaceIamPolicy("policy", policy_data=admin.policy_data,
        opts=pulumi.ResourceOptions(provider=google_beta))
        ```

        ## google\\_service\\_directory\\_namespace\\_iam\\_binding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.servicedirectory.NamespaceIamBinding("binding",
            role="roles/viewer",
            members=["user:jane@example.com"],
            opts=pulumi.ResourceOptions(provider=google_beta))
        ```

        ## google\\_service\\_directory\\_namespace\\_iam\\_member

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.servicedirectory.NamespaceIamMember("member",
            role="roles/viewer",
            member="user:jane@example.com",
            opts=pulumi.ResourceOptions(provider=google_beta))
        ```

        ## Import

        For all import syntaxes, the "resource in question" can take any of the following forms* projects/{{project}}/locations/{{location}}/namespaces/{{namespace_id}} * {{project}}/{{location}}/{{namespace_id}} * {{location}}/{{namespace_id}} Any variables not passed in the import command will be taken from the provider configuration. Service Directory namespace IAM resources can be imported using the resource identifiers, role, and member. IAM member imports use space-delimited identifiersthe resource in question, the role, and the member identity, e.g.

        ```sh
         $ pulumi import gcp:servicedirectory/namespaceIamMember:NamespaceIamMember editor "projects/{{project}}/locations/{{location}}/namespaces/{{namespace_id}} roles/viewer user:jane@example.com"
        ```

         IAM binding imports use space-delimited identifiersthe resource in question and the role, e.g.

        ```sh
         $ pulumi import gcp:servicedirectory/namespaceIamMember:NamespaceIamMember editor "projects/{{project}}/locations/{{location}}/namespaces/{{namespace_id}} roles/viewer"
        ```

         IAM policy imports use the identifier of the resource in question, e.g.

        ```sh
         $ pulumi import gcp:servicedirectory/namespaceIamMember:NamespaceIamMember editor projects/{{project}}/locations/{{location}}/namespaces/{{namespace_id}}
        ```

         -> **Custom Roles**If you're importing a IAM resource with a custom role, make sure to use the

        full name of the custom role, e.g. `[projects/my-project|organizations/my-org]/roles/my-custom-role`.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `servicedirectory.NamespaceIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NamespaceIamMemberArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Three different resources help you manage your IAM policy for Service Directory Namespace. Each of these resources serves a different use case:

        * `servicedirectory.NamespaceIamPolicy`: Authoritative. Sets the IAM policy for the namespace and replaces any existing policy already attached.
        * `servicedirectory.NamespaceIamBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the namespace are preserved.
        * `servicedirectory.NamespaceIamMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the namespace are preserved.

        > **Note:** `servicedirectory.NamespaceIamPolicy` **cannot** be used in conjunction with `servicedirectory.NamespaceIamBinding` and `servicedirectory.NamespaceIamMember` or they will fight over what your policy should be.

        > **Note:** `servicedirectory.NamespaceIamBinding` resources **can be** used in conjunction with `servicedirectory.NamespaceIamMember` resources **only if** they do not grant privilege to the same role.

        ## google\\_service\\_directory\\_namespace\\_iam\\_policy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/viewer",
            members=["user:jane@example.com"],
        )])
        policy = gcp.servicedirectory.NamespaceIamPolicy("policy", policy_data=admin.policy_data,
        opts=pulumi.ResourceOptions(provider=google_beta))
        ```

        ## google\\_service\\_directory\\_namespace\\_iam\\_binding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.servicedirectory.NamespaceIamBinding("binding",
            role="roles/viewer",
            members=["user:jane@example.com"],
            opts=pulumi.ResourceOptions(provider=google_beta))
        ```

        ## google\\_service\\_directory\\_namespace\\_iam\\_member

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.servicedirectory.NamespaceIamMember("member",
            role="roles/viewer",
            member="user:jane@example.com",
            opts=pulumi.ResourceOptions(provider=google_beta))
        ```

        ## Import

        For all import syntaxes, the "resource in question" can take any of the following forms* projects/{{project}}/locations/{{location}}/namespaces/{{namespace_id}} * {{project}}/{{location}}/{{namespace_id}} * {{location}}/{{namespace_id}} Any variables not passed in the import command will be taken from the provider configuration. Service Directory namespace IAM resources can be imported using the resource identifiers, role, and member. IAM member imports use space-delimited identifiersthe resource in question, the role, and the member identity, e.g.

        ```sh
         $ pulumi import gcp:servicedirectory/namespaceIamMember:NamespaceIamMember editor "projects/{{project}}/locations/{{location}}/namespaces/{{namespace_id}} roles/viewer user:jane@example.com"
        ```

         IAM binding imports use space-delimited identifiersthe resource in question and the role, e.g.

        ```sh
         $ pulumi import gcp:servicedirectory/namespaceIamMember:NamespaceIamMember editor "projects/{{project}}/locations/{{location}}/namespaces/{{namespace_id}} roles/viewer"
        ```

         IAM policy imports use the identifier of the resource in question, e.g.

        ```sh
         $ pulumi import gcp:servicedirectory/namespaceIamMember:NamespaceIamMember editor projects/{{project}}/locations/{{location}}/namespaces/{{namespace_id}}
        ```

         -> **Custom Roles**If you're importing a IAM resource with a custom role, make sure to use the

        full name of the custom role, e.g. `[projects/my-project|organizations/my-org]/roles/my-custom-role`.

        :param str resource_name: The name of the resource.
        :param NamespaceIamMemberArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NamespaceIamMemberArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 condition: Optional[pulumi.Input[pulumi.InputType['NamespaceIamMemberConditionArgs']]] = None,
                 member: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NamespaceIamMemberArgs.__new__(NamespaceIamMemberArgs)

            __props__.__dict__["condition"] = condition
            if member is None and not opts.urn:
                raise TypeError("Missing required property 'member'")
            __props__.__dict__["member"] = member
            __props__.__dict__["name"] = name
            if role is None and not opts.urn:
                raise TypeError("Missing required property 'role'")
            __props__.__dict__["role"] = role
            __props__.__dict__["etag"] = None
        super(NamespaceIamMember, __self__).__init__(
            'gcp:servicedirectory/namespaceIamMember:NamespaceIamMember',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            condition: Optional[pulumi.Input[pulumi.InputType['NamespaceIamMemberConditionArgs']]] = None,
            etag: Optional[pulumi.Input[str]] = None,
            member: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            role: Optional[pulumi.Input[str]] = None) -> 'NamespaceIamMember':
        """
        Get an existing NamespaceIamMember resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] etag: (Computed) The etag of the IAM policy.
        :param pulumi.Input[str] name: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `servicedirectory.NamespaceIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _NamespaceIamMemberState.__new__(_NamespaceIamMemberState)

        __props__.__dict__["condition"] = condition
        __props__.__dict__["etag"] = etag
        __props__.__dict__["member"] = member
        __props__.__dict__["name"] = name
        __props__.__dict__["role"] = role
        return NamespaceIamMember(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def condition(self) -> pulumi.Output[Optional['outputs.NamespaceIamMemberCondition']]:
        return pulumi.get(self, "condition")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        (Computed) The etag of the IAM policy.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def member(self) -> pulumi.Output[str]:
        return pulumi.get(self, "member")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def role(self) -> pulumi.Output[str]:
        """
        The role that should be applied. Only one
        `servicedirectory.NamespaceIamBinding` can be used per role. Note that custom roles must be of the format
        `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        return pulumi.get(self, "role")

