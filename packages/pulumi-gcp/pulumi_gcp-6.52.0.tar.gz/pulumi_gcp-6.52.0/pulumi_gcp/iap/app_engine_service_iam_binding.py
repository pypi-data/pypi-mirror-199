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

__all__ = ['AppEngineServiceIamBindingArgs', 'AppEngineServiceIamBinding']

@pulumi.input_type
class AppEngineServiceIamBindingArgs:
    def __init__(__self__, *,
                 app_id: pulumi.Input[str],
                 members: pulumi.Input[Sequence[pulumi.Input[str]]],
                 role: pulumi.Input[str],
                 service: pulumi.Input[str],
                 condition: Optional[pulumi.Input['AppEngineServiceIamBindingConditionArgs']] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AppEngineServiceIamBinding resource.
        :param pulumi.Input[str] app_id: Id of the App Engine application. Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `iap.AppEngineServiceIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        :param pulumi.Input[str] service: Service id of the App Engine application Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input['AppEngineServiceIamBindingConditionArgs'] condition: An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding.
               Structure is documented below.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        """
        pulumi.set(__self__, "app_id", app_id)
        pulumi.set(__self__, "members", members)
        pulumi.set(__self__, "role", role)
        pulumi.set(__self__, "service", service)
        if condition is not None:
            pulumi.set(__self__, "condition", condition)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter(name="appId")
    def app_id(self) -> pulumi.Input[str]:
        """
        Id of the App Engine application. Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "app_id")

    @app_id.setter
    def app_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "app_id", value)

    @property
    @pulumi.getter
    def members(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        return pulumi.get(self, "members")

    @members.setter
    def members(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "members", value)

    @property
    @pulumi.getter
    def role(self) -> pulumi.Input[str]:
        """
        The role that should be applied. Only one
        `iap.AppEngineServiceIamBinding` can be used per role. Note that custom roles must be of the format
        `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: pulumi.Input[str]):
        pulumi.set(self, "role", value)

    @property
    @pulumi.getter
    def service(self) -> pulumi.Input[str]:
        """
        Service id of the App Engine application Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "service")

    @service.setter
    def service(self, value: pulumi.Input[str]):
        pulumi.set(self, "service", value)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input['AppEngineServiceIamBindingConditionArgs']]:
        """
        An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding.
        Structure is documented below.
        """
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input['AppEngineServiceIamBindingConditionArgs']]):
        pulumi.set(self, "condition", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)


@pulumi.input_type
class _AppEngineServiceIamBindingState:
    def __init__(__self__, *,
                 app_id: Optional[pulumi.Input[str]] = None,
                 condition: Optional[pulumi.Input['AppEngineServiceIamBindingConditionArgs']] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 members: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 service: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AppEngineServiceIamBinding resources.
        :param pulumi.Input[str] app_id: Id of the App Engine application. Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input['AppEngineServiceIamBindingConditionArgs'] condition: An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding.
               Structure is documented below.
        :param pulumi.Input[str] etag: (Computed) The etag of the IAM policy.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `iap.AppEngineServiceIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        :param pulumi.Input[str] service: Service id of the App Engine application Used to find the parent resource to bind the IAM policy to
        """
        if app_id is not None:
            pulumi.set(__self__, "app_id", app_id)
        if condition is not None:
            pulumi.set(__self__, "condition", condition)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if members is not None:
            pulumi.set(__self__, "members", members)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if role is not None:
            pulumi.set(__self__, "role", role)
        if service is not None:
            pulumi.set(__self__, "service", service)

    @property
    @pulumi.getter(name="appId")
    def app_id(self) -> Optional[pulumi.Input[str]]:
        """
        Id of the App Engine application. Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "app_id")

    @app_id.setter
    def app_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "app_id", value)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input['AppEngineServiceIamBindingConditionArgs']]:
        """
        An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding.
        Structure is documented below.
        """
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input['AppEngineServiceIamBindingConditionArgs']]):
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
    def members(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "members")

    @members.setter
    def members(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "members", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter
    def role(self) -> Optional[pulumi.Input[str]]:
        """
        The role that should be applied. Only one
        `iap.AppEngineServiceIamBinding` can be used per role. Note that custom roles must be of the format
        `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role", value)

    @property
    @pulumi.getter
    def service(self) -> Optional[pulumi.Input[str]]:
        """
        Service id of the App Engine application Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "service")

    @service.setter
    def service(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service", value)


class AppEngineServiceIamBinding(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_id: Optional[pulumi.Input[str]] = None,
                 condition: Optional[pulumi.Input[pulumi.InputType['AppEngineServiceIamBindingConditionArgs']]] = None,
                 members: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 service: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Three different resources help you manage your IAM policy for Identity-Aware Proxy AppEngineService. Each of these resources serves a different use case:

        * `iap.AppEngineServiceIamPolicy`: Authoritative. Sets the IAM policy for the appengineservice and replaces any existing policy already attached.
        * `iap.AppEngineServiceIamBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the appengineservice are preserved.
        * `iap.AppEngineServiceIamMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the appengineservice are preserved.

        > **Note:** `iap.AppEngineServiceIamPolicy` **cannot** be used in conjunction with `iap.AppEngineServiceIamBinding` and `iap.AppEngineServiceIamMember` or they will fight over what your policy should be.

        > **Note:** `iap.AppEngineServiceIamBinding` resources **can be** used in conjunction with `iap.AppEngineServiceIamMember` resources **only if** they do not grant privilege to the same role.

        > **Note:**  This resource supports IAM Conditions but they have some known limitations which can be found [here](https://cloud.google.com/iam/docs/conditions-overview#limitations). Please review this article if you are having issues with IAM Conditions.

        ## google\\_iap\\_app\\_engine\\_service\\_iam\\_policy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/iap.httpsResourceAccessor",
            members=["user:jane@example.com"],
        )])
        policy = gcp.iap.AppEngineServiceIamPolicy("policy",
            project=google_app_engine_standard_app_version["version"]["project"],
            app_id=google_app_engine_standard_app_version["version"]["project"],
            service=google_app_engine_standard_app_version["version"]["service"],
            policy_data=admin.policy_data)
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/iap.httpsResourceAccessor",
            members=["user:jane@example.com"],
            condition=gcp.organizations.GetIAMPolicyBindingConditionArgs(
                title="expires_after_2019_12_31",
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\\"2020-01-01T00:00:00Z\\")",
            ),
        )])
        policy = gcp.iap.AppEngineServiceIamPolicy("policy",
            project=google_app_engine_standard_app_version["version"]["project"],
            app_id=google_app_engine_standard_app_version["version"]["project"],
            service=google_app_engine_standard_app_version["version"]["service"],
            policy_data=admin.policy_data)
        ```
        ## google\\_iap\\_app\\_engine\\_service\\_iam\\_binding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.iap.AppEngineServiceIamBinding("binding",
            app_id=google_app_engine_standard_app_version["version"]["project"],
            members=["user:jane@example.com"],
            project=google_app_engine_standard_app_version["version"]["project"],
            role="roles/iap.httpsResourceAccessor",
            service=google_app_engine_standard_app_version["version"]["service"])
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.iap.AppEngineServiceIamBinding("binding",
            app_id=google_app_engine_standard_app_version["version"]["project"],
            condition=gcp.iap.AppEngineServiceIamBindingConditionArgs(
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\\"2020-01-01T00:00:00Z\\")",
                title="expires_after_2019_12_31",
            ),
            members=["user:jane@example.com"],
            project=google_app_engine_standard_app_version["version"]["project"],
            role="roles/iap.httpsResourceAccessor",
            service=google_app_engine_standard_app_version["version"]["service"])
        ```
        ## google\\_iap\\_app\\_engine\\_service\\_iam\\_member

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.iap.AppEngineServiceIamMember("member",
            app_id=google_app_engine_standard_app_version["version"]["project"],
            member="user:jane@example.com",
            project=google_app_engine_standard_app_version["version"]["project"],
            role="roles/iap.httpsResourceAccessor",
            service=google_app_engine_standard_app_version["version"]["service"])
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.iap.AppEngineServiceIamMember("member",
            app_id=google_app_engine_standard_app_version["version"]["project"],
            condition=gcp.iap.AppEngineServiceIamMemberConditionArgs(
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\\"2020-01-01T00:00:00Z\\")",
                title="expires_after_2019_12_31",
            ),
            member="user:jane@example.com",
            project=google_app_engine_standard_app_version["version"]["project"],
            role="roles/iap.httpsResourceAccessor",
            service=google_app_engine_standard_app_version["version"]["service"])
        ```

        ## Import

        For all import syntaxes, the "resource in question" can take any of the following forms* projects/{{project}}/iap_web/appengine-{{appId}}/services/{{service}} * {{project}}/{{appId}}/{{service}} * {{appId}}/{{service}} * {{service}} Any variables not passed in the import command will be taken from the provider configuration. Identity-Aware Proxy appengineservice IAM resources can be imported using the resource identifiers, role, and member. IAM member imports use space-delimited identifiersthe resource in question, the role, and the member identity, e.g.

        ```sh
         $ pulumi import gcp:iap/appEngineServiceIamBinding:AppEngineServiceIamBinding editor "projects/{{project}}/iap_web/appengine-{{appId}}/services/{{service}} roles/iap.httpsResourceAccessor user:jane@example.com"
        ```

         IAM binding imports use space-delimited identifiersthe resource in question and the role, e.g.

        ```sh
         $ pulumi import gcp:iap/appEngineServiceIamBinding:AppEngineServiceIamBinding editor "projects/{{project}}/iap_web/appengine-{{appId}}/services/{{service}} roles/iap.httpsResourceAccessor"
        ```

         IAM policy imports use the identifier of the resource in question, e.g.

        ```sh
         $ pulumi import gcp:iap/appEngineServiceIamBinding:AppEngineServiceIamBinding editor projects/{{project}}/iap_web/appengine-{{appId}}/services/{{service}}
        ```

         -> **Custom Roles**If you're importing a IAM resource with a custom role, make sure to use the

        full name of the custom role, e.g. `[projects/my-project|organizations/my-org]/roles/my-custom-role`.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] app_id: Id of the App Engine application. Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[pulumi.InputType['AppEngineServiceIamBindingConditionArgs']] condition: An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding.
               Structure is documented below.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `iap.AppEngineServiceIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        :param pulumi.Input[str] service: Service id of the App Engine application Used to find the parent resource to bind the IAM policy to
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AppEngineServiceIamBindingArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Three different resources help you manage your IAM policy for Identity-Aware Proxy AppEngineService. Each of these resources serves a different use case:

        * `iap.AppEngineServiceIamPolicy`: Authoritative. Sets the IAM policy for the appengineservice and replaces any existing policy already attached.
        * `iap.AppEngineServiceIamBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the appengineservice are preserved.
        * `iap.AppEngineServiceIamMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the appengineservice are preserved.

        > **Note:** `iap.AppEngineServiceIamPolicy` **cannot** be used in conjunction with `iap.AppEngineServiceIamBinding` and `iap.AppEngineServiceIamMember` or they will fight over what your policy should be.

        > **Note:** `iap.AppEngineServiceIamBinding` resources **can be** used in conjunction with `iap.AppEngineServiceIamMember` resources **only if** they do not grant privilege to the same role.

        > **Note:**  This resource supports IAM Conditions but they have some known limitations which can be found [here](https://cloud.google.com/iam/docs/conditions-overview#limitations). Please review this article if you are having issues with IAM Conditions.

        ## google\\_iap\\_app\\_engine\\_service\\_iam\\_policy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/iap.httpsResourceAccessor",
            members=["user:jane@example.com"],
        )])
        policy = gcp.iap.AppEngineServiceIamPolicy("policy",
            project=google_app_engine_standard_app_version["version"]["project"],
            app_id=google_app_engine_standard_app_version["version"]["project"],
            service=google_app_engine_standard_app_version["version"]["service"],
            policy_data=admin.policy_data)
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/iap.httpsResourceAccessor",
            members=["user:jane@example.com"],
            condition=gcp.organizations.GetIAMPolicyBindingConditionArgs(
                title="expires_after_2019_12_31",
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\\"2020-01-01T00:00:00Z\\")",
            ),
        )])
        policy = gcp.iap.AppEngineServiceIamPolicy("policy",
            project=google_app_engine_standard_app_version["version"]["project"],
            app_id=google_app_engine_standard_app_version["version"]["project"],
            service=google_app_engine_standard_app_version["version"]["service"],
            policy_data=admin.policy_data)
        ```
        ## google\\_iap\\_app\\_engine\\_service\\_iam\\_binding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.iap.AppEngineServiceIamBinding("binding",
            app_id=google_app_engine_standard_app_version["version"]["project"],
            members=["user:jane@example.com"],
            project=google_app_engine_standard_app_version["version"]["project"],
            role="roles/iap.httpsResourceAccessor",
            service=google_app_engine_standard_app_version["version"]["service"])
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.iap.AppEngineServiceIamBinding("binding",
            app_id=google_app_engine_standard_app_version["version"]["project"],
            condition=gcp.iap.AppEngineServiceIamBindingConditionArgs(
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\\"2020-01-01T00:00:00Z\\")",
                title="expires_after_2019_12_31",
            ),
            members=["user:jane@example.com"],
            project=google_app_engine_standard_app_version["version"]["project"],
            role="roles/iap.httpsResourceAccessor",
            service=google_app_engine_standard_app_version["version"]["service"])
        ```
        ## google\\_iap\\_app\\_engine\\_service\\_iam\\_member

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.iap.AppEngineServiceIamMember("member",
            app_id=google_app_engine_standard_app_version["version"]["project"],
            member="user:jane@example.com",
            project=google_app_engine_standard_app_version["version"]["project"],
            role="roles/iap.httpsResourceAccessor",
            service=google_app_engine_standard_app_version["version"]["service"])
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.iap.AppEngineServiceIamMember("member",
            app_id=google_app_engine_standard_app_version["version"]["project"],
            condition=gcp.iap.AppEngineServiceIamMemberConditionArgs(
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\\"2020-01-01T00:00:00Z\\")",
                title="expires_after_2019_12_31",
            ),
            member="user:jane@example.com",
            project=google_app_engine_standard_app_version["version"]["project"],
            role="roles/iap.httpsResourceAccessor",
            service=google_app_engine_standard_app_version["version"]["service"])
        ```

        ## Import

        For all import syntaxes, the "resource in question" can take any of the following forms* projects/{{project}}/iap_web/appengine-{{appId}}/services/{{service}} * {{project}}/{{appId}}/{{service}} * {{appId}}/{{service}} * {{service}} Any variables not passed in the import command will be taken from the provider configuration. Identity-Aware Proxy appengineservice IAM resources can be imported using the resource identifiers, role, and member. IAM member imports use space-delimited identifiersthe resource in question, the role, and the member identity, e.g.

        ```sh
         $ pulumi import gcp:iap/appEngineServiceIamBinding:AppEngineServiceIamBinding editor "projects/{{project}}/iap_web/appengine-{{appId}}/services/{{service}} roles/iap.httpsResourceAccessor user:jane@example.com"
        ```

         IAM binding imports use space-delimited identifiersthe resource in question and the role, e.g.

        ```sh
         $ pulumi import gcp:iap/appEngineServiceIamBinding:AppEngineServiceIamBinding editor "projects/{{project}}/iap_web/appengine-{{appId}}/services/{{service}} roles/iap.httpsResourceAccessor"
        ```

         IAM policy imports use the identifier of the resource in question, e.g.

        ```sh
         $ pulumi import gcp:iap/appEngineServiceIamBinding:AppEngineServiceIamBinding editor projects/{{project}}/iap_web/appengine-{{appId}}/services/{{service}}
        ```

         -> **Custom Roles**If you're importing a IAM resource with a custom role, make sure to use the

        full name of the custom role, e.g. `[projects/my-project|organizations/my-org]/roles/my-custom-role`.

        :param str resource_name: The name of the resource.
        :param AppEngineServiceIamBindingArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AppEngineServiceIamBindingArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_id: Optional[pulumi.Input[str]] = None,
                 condition: Optional[pulumi.Input[pulumi.InputType['AppEngineServiceIamBindingConditionArgs']]] = None,
                 members: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 service: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AppEngineServiceIamBindingArgs.__new__(AppEngineServiceIamBindingArgs)

            if app_id is None and not opts.urn:
                raise TypeError("Missing required property 'app_id'")
            __props__.__dict__["app_id"] = app_id
            __props__.__dict__["condition"] = condition
            if members is None and not opts.urn:
                raise TypeError("Missing required property 'members'")
            __props__.__dict__["members"] = members
            __props__.__dict__["project"] = project
            if role is None and not opts.urn:
                raise TypeError("Missing required property 'role'")
            __props__.__dict__["role"] = role
            if service is None and not opts.urn:
                raise TypeError("Missing required property 'service'")
            __props__.__dict__["service"] = service
            __props__.__dict__["etag"] = None
        super(AppEngineServiceIamBinding, __self__).__init__(
            'gcp:iap/appEngineServiceIamBinding:AppEngineServiceIamBinding',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            app_id: Optional[pulumi.Input[str]] = None,
            condition: Optional[pulumi.Input[pulumi.InputType['AppEngineServiceIamBindingConditionArgs']]] = None,
            etag: Optional[pulumi.Input[str]] = None,
            members: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            project: Optional[pulumi.Input[str]] = None,
            role: Optional[pulumi.Input[str]] = None,
            service: Optional[pulumi.Input[str]] = None) -> 'AppEngineServiceIamBinding':
        """
        Get an existing AppEngineServiceIamBinding resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] app_id: Id of the App Engine application. Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[pulumi.InputType['AppEngineServiceIamBindingConditionArgs']] condition: An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding.
               Structure is documented below.
        :param pulumi.Input[str] etag: (Computed) The etag of the IAM policy.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `iap.AppEngineServiceIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        :param pulumi.Input[str] service: Service id of the App Engine application Used to find the parent resource to bind the IAM policy to
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AppEngineServiceIamBindingState.__new__(_AppEngineServiceIamBindingState)

        __props__.__dict__["app_id"] = app_id
        __props__.__dict__["condition"] = condition
        __props__.__dict__["etag"] = etag
        __props__.__dict__["members"] = members
        __props__.__dict__["project"] = project
        __props__.__dict__["role"] = role
        __props__.__dict__["service"] = service
        return AppEngineServiceIamBinding(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="appId")
    def app_id(self) -> pulumi.Output[str]:
        """
        Id of the App Engine application. Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "app_id")

    @property
    @pulumi.getter
    def condition(self) -> pulumi.Output[Optional['outputs.AppEngineServiceIamBindingCondition']]:
        """
        An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding.
        Structure is documented below.
        """
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
    def members(self) -> pulumi.Output[Sequence[str]]:
        return pulumi.get(self, "members")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def role(self) -> pulumi.Output[str]:
        """
        The role that should be applied. Only one
        `iap.AppEngineServiceIamBinding` can be used per role. Note that custom roles must be of the format
        `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        return pulumi.get(self, "role")

    @property
    @pulumi.getter
    def service(self) -> pulumi.Output[str]:
        """
        Service id of the App Engine application Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "service")

