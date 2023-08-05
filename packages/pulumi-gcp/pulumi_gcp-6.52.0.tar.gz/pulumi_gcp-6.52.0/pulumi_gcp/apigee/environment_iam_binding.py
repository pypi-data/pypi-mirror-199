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

__all__ = ['EnvironmentIamBindingArgs', 'EnvironmentIamBinding']

@pulumi.input_type
class EnvironmentIamBindingArgs:
    def __init__(__self__, *,
                 env_id: pulumi.Input[str],
                 members: pulumi.Input[Sequence[pulumi.Input[str]]],
                 org_id: pulumi.Input[str],
                 role: pulumi.Input[str],
                 condition: Optional[pulumi.Input['EnvironmentIamBindingConditionArgs']] = None):
        """
        The set of arguments for constructing a EnvironmentIamBinding resource.
        :param pulumi.Input[str] env_id: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `apigee.EnvironmentIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        pulumi.set(__self__, "env_id", env_id)
        pulumi.set(__self__, "members", members)
        pulumi.set(__self__, "org_id", org_id)
        pulumi.set(__self__, "role", role)
        if condition is not None:
            pulumi.set(__self__, "condition", condition)

    @property
    @pulumi.getter(name="envId")
    def env_id(self) -> pulumi.Input[str]:
        """
        Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "env_id")

    @env_id.setter
    def env_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "env_id", value)

    @property
    @pulumi.getter
    def members(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        return pulumi.get(self, "members")

    @members.setter
    def members(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "members", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter
    def role(self) -> pulumi.Input[str]:
        """
        The role that should be applied. Only one
        `apigee.EnvironmentIamBinding` can be used per role. Note that custom roles must be of the format
        `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: pulumi.Input[str]):
        pulumi.set(self, "role", value)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input['EnvironmentIamBindingConditionArgs']]:
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input['EnvironmentIamBindingConditionArgs']]):
        pulumi.set(self, "condition", value)


@pulumi.input_type
class _EnvironmentIamBindingState:
    def __init__(__self__, *,
                 condition: Optional[pulumi.Input['EnvironmentIamBindingConditionArgs']] = None,
                 env_id: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 members: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering EnvironmentIamBinding resources.
        :param pulumi.Input[str] env_id: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] etag: (Computed) The etag of the IAM policy.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `apigee.EnvironmentIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        if condition is not None:
            pulumi.set(__self__, "condition", condition)
        if env_id is not None:
            pulumi.set(__self__, "env_id", env_id)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if members is not None:
            pulumi.set(__self__, "members", members)
        if org_id is not None:
            pulumi.set(__self__, "org_id", org_id)
        if role is not None:
            pulumi.set(__self__, "role", role)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input['EnvironmentIamBindingConditionArgs']]:
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input['EnvironmentIamBindingConditionArgs']]):
        pulumi.set(self, "condition", value)

    @property
    @pulumi.getter(name="envId")
    def env_id(self) -> Optional[pulumi.Input[str]]:
        """
        Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "env_id")

    @env_id.setter
    def env_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "env_id", value)

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
    def members(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "members")

    @members.setter
    def members(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "members", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter
    def role(self) -> Optional[pulumi.Input[str]]:
        """
        The role that should be applied. Only one
        `apigee.EnvironmentIamBinding` can be used per role. Note that custom roles must be of the format
        `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role", value)


class EnvironmentIamBinding(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 condition: Optional[pulumi.Input[pulumi.InputType['EnvironmentIamBindingConditionArgs']]] = None,
                 env_id: Optional[pulumi.Input[str]] = None,
                 members: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Three different resources help you manage your IAM policy for Apigee Environment. Each of these resources serves a different use case:

        * `apigee.EnvironmentIamPolicy`: Authoritative. Sets the IAM policy for the environment and replaces any existing policy already attached.
        * `apigee.EnvironmentIamBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the environment are preserved.
        * `apigee.EnvironmentIamMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the environment are preserved.

        > **Note:** `apigee.EnvironmentIamPolicy` **cannot** be used in conjunction with `apigee.EnvironmentIamBinding` and `apigee.EnvironmentIamMember` or they will fight over what your policy should be.

        > **Note:** `apigee.EnvironmentIamBinding` resources **can be** used in conjunction with `apigee.EnvironmentIamMember` resources **only if** they do not grant privilege to the same role.

        ## google\\_apigee\\_environment\\_iam\\_policy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/viewer",
            members=["user:jane@example.com"],
        )])
        policy = gcp.apigee.EnvironmentIamPolicy("policy",
            org_id=google_apigee_environment["apigee_environment"]["org_id"],
            env_id=google_apigee_environment["apigee_environment"]["name"],
            policy_data=admin.policy_data)
        ```

        ## google\\_apigee\\_environment\\_iam\\_binding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.apigee.EnvironmentIamBinding("binding",
            org_id=google_apigee_environment["apigee_environment"]["org_id"],
            env_id=google_apigee_environment["apigee_environment"]["name"],
            role="roles/viewer",
            members=["user:jane@example.com"])
        ```

        ## google\\_apigee\\_environment\\_iam\\_member

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.apigee.EnvironmentIamMember("member",
            org_id=google_apigee_environment["apigee_environment"]["org_id"],
            env_id=google_apigee_environment["apigee_environment"]["name"],
            role="roles/viewer",
            member="user:jane@example.com")
        ```

        ## Import

        For all import syntaxes, the "resource in question" can take any of the following forms* {{org_id}}/environments/{{name}} * {{name}} Any variables not passed in the import command will be taken from the provider configuration. Apigee environment IAM resources can be imported using the resource identifiers, role, and member. IAM member imports use space-delimited identifiersthe resource in question, the role, and the member identity, e.g.

        ```sh
         $ pulumi import gcp:apigee/environmentIamBinding:EnvironmentIamBinding editor "{{org_id}}/environments/{{environment}} roles/viewer user:jane@example.com"
        ```

         IAM binding imports use space-delimited identifiersthe resource in question and the role, e.g.

        ```sh
         $ pulumi import gcp:apigee/environmentIamBinding:EnvironmentIamBinding editor "{{org_id}}/environments/{{environment}} roles/viewer"
        ```

         IAM policy imports use the identifier of the resource in question, e.g.

        ```sh
         $ pulumi import gcp:apigee/environmentIamBinding:EnvironmentIamBinding editor {{org_id}}/environments/{{environment}}
        ```

         -> **Custom Roles**If you're importing a IAM resource with a custom role, make sure to use the

        full name of the custom role, e.g. `[projects/my-project|organizations/my-org]/roles/my-custom-role`.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] env_id: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `apigee.EnvironmentIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EnvironmentIamBindingArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Three different resources help you manage your IAM policy for Apigee Environment. Each of these resources serves a different use case:

        * `apigee.EnvironmentIamPolicy`: Authoritative. Sets the IAM policy for the environment and replaces any existing policy already attached.
        * `apigee.EnvironmentIamBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the environment are preserved.
        * `apigee.EnvironmentIamMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the environment are preserved.

        > **Note:** `apigee.EnvironmentIamPolicy` **cannot** be used in conjunction with `apigee.EnvironmentIamBinding` and `apigee.EnvironmentIamMember` or they will fight over what your policy should be.

        > **Note:** `apigee.EnvironmentIamBinding` resources **can be** used in conjunction with `apigee.EnvironmentIamMember` resources **only if** they do not grant privilege to the same role.

        ## google\\_apigee\\_environment\\_iam\\_policy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/viewer",
            members=["user:jane@example.com"],
        )])
        policy = gcp.apigee.EnvironmentIamPolicy("policy",
            org_id=google_apigee_environment["apigee_environment"]["org_id"],
            env_id=google_apigee_environment["apigee_environment"]["name"],
            policy_data=admin.policy_data)
        ```

        ## google\\_apigee\\_environment\\_iam\\_binding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.apigee.EnvironmentIamBinding("binding",
            org_id=google_apigee_environment["apigee_environment"]["org_id"],
            env_id=google_apigee_environment["apigee_environment"]["name"],
            role="roles/viewer",
            members=["user:jane@example.com"])
        ```

        ## google\\_apigee\\_environment\\_iam\\_member

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.apigee.EnvironmentIamMember("member",
            org_id=google_apigee_environment["apigee_environment"]["org_id"],
            env_id=google_apigee_environment["apigee_environment"]["name"],
            role="roles/viewer",
            member="user:jane@example.com")
        ```

        ## Import

        For all import syntaxes, the "resource in question" can take any of the following forms* {{org_id}}/environments/{{name}} * {{name}} Any variables not passed in the import command will be taken from the provider configuration. Apigee environment IAM resources can be imported using the resource identifiers, role, and member. IAM member imports use space-delimited identifiersthe resource in question, the role, and the member identity, e.g.

        ```sh
         $ pulumi import gcp:apigee/environmentIamBinding:EnvironmentIamBinding editor "{{org_id}}/environments/{{environment}} roles/viewer user:jane@example.com"
        ```

         IAM binding imports use space-delimited identifiersthe resource in question and the role, e.g.

        ```sh
         $ pulumi import gcp:apigee/environmentIamBinding:EnvironmentIamBinding editor "{{org_id}}/environments/{{environment}} roles/viewer"
        ```

         IAM policy imports use the identifier of the resource in question, e.g.

        ```sh
         $ pulumi import gcp:apigee/environmentIamBinding:EnvironmentIamBinding editor {{org_id}}/environments/{{environment}}
        ```

         -> **Custom Roles**If you're importing a IAM resource with a custom role, make sure to use the

        full name of the custom role, e.g. `[projects/my-project|organizations/my-org]/roles/my-custom-role`.

        :param str resource_name: The name of the resource.
        :param EnvironmentIamBindingArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EnvironmentIamBindingArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 condition: Optional[pulumi.Input[pulumi.InputType['EnvironmentIamBindingConditionArgs']]] = None,
                 env_id: Optional[pulumi.Input[str]] = None,
                 members: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EnvironmentIamBindingArgs.__new__(EnvironmentIamBindingArgs)

            __props__.__dict__["condition"] = condition
            if env_id is None and not opts.urn:
                raise TypeError("Missing required property 'env_id'")
            __props__.__dict__["env_id"] = env_id
            if members is None and not opts.urn:
                raise TypeError("Missing required property 'members'")
            __props__.__dict__["members"] = members
            if org_id is None and not opts.urn:
                raise TypeError("Missing required property 'org_id'")
            __props__.__dict__["org_id"] = org_id
            if role is None and not opts.urn:
                raise TypeError("Missing required property 'role'")
            __props__.__dict__["role"] = role
            __props__.__dict__["etag"] = None
        super(EnvironmentIamBinding, __self__).__init__(
            'gcp:apigee/environmentIamBinding:EnvironmentIamBinding',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            condition: Optional[pulumi.Input[pulumi.InputType['EnvironmentIamBindingConditionArgs']]] = None,
            env_id: Optional[pulumi.Input[str]] = None,
            etag: Optional[pulumi.Input[str]] = None,
            members: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            org_id: Optional[pulumi.Input[str]] = None,
            role: Optional[pulumi.Input[str]] = None) -> 'EnvironmentIamBinding':
        """
        Get an existing EnvironmentIamBinding resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] env_id: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] etag: (Computed) The etag of the IAM policy.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `apigee.EnvironmentIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EnvironmentIamBindingState.__new__(_EnvironmentIamBindingState)

        __props__.__dict__["condition"] = condition
        __props__.__dict__["env_id"] = env_id
        __props__.__dict__["etag"] = etag
        __props__.__dict__["members"] = members
        __props__.__dict__["org_id"] = org_id
        __props__.__dict__["role"] = role
        return EnvironmentIamBinding(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def condition(self) -> pulumi.Output[Optional['outputs.EnvironmentIamBindingCondition']]:
        return pulumi.get(self, "condition")

    @property
    @pulumi.getter(name="envId")
    def env_id(self) -> pulumi.Output[str]:
        """
        Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "env_id")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        (Computed) The etag of the IAM policy.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def members(self) -> pulumi.Output[Sequence[str]]:
        return pulumi.get(self, "members")

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "org_id")

    @property
    @pulumi.getter
    def role(self) -> pulumi.Output[str]:
        """
        The role that should be applied. Only one
        `apigee.EnvironmentIamBinding` can be used per role. Note that custom roles must be of the format
        `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        return pulumi.get(self, "role")

