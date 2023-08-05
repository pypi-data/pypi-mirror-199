# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['SubnetworkIAMPolicyArgs', 'SubnetworkIAMPolicy']

@pulumi.input_type
class SubnetworkIAMPolicyArgs:
    def __init__(__self__, *,
                 policy_data: pulumi.Input[str],
                 subnetwork: pulumi.Input[str],
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SubnetworkIAMPolicy resource.
        :param pulumi.Input[str] policy_data: The policy data generated by
               a _organizations_get_iam_policy_ data source.
        :param pulumi.Input[str] subnetwork: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        :param pulumi.Input[str] region: The GCP region for this subnetwork.
               Used to find the parent resource to bind the IAM policy to. If not specified,
               the value will be parsed from the identifier of the parent resource. If no region is provided in the parent identifier and no
               region is specified, it is taken from the provider configuration.
        """
        pulumi.set(__self__, "policy_data", policy_data)
        pulumi.set(__self__, "subnetwork", subnetwork)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if region is not None:
            pulumi.set(__self__, "region", region)

    @property
    @pulumi.getter(name="policyData")
    def policy_data(self) -> pulumi.Input[str]:
        """
        The policy data generated by
        a _organizations_get_iam_policy_ data source.
        """
        return pulumi.get(self, "policy_data")

    @policy_data.setter
    def policy_data(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_data", value)

    @property
    @pulumi.getter
    def subnetwork(self) -> pulumi.Input[str]:
        """
        Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "subnetwork")

    @subnetwork.setter
    def subnetwork(self, value: pulumi.Input[str]):
        pulumi.set(self, "subnetwork", value)

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
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The GCP region for this subnetwork.
        Used to find the parent resource to bind the IAM policy to. If not specified,
        the value will be parsed from the identifier of the parent resource. If no region is provided in the parent identifier and no
        region is specified, it is taken from the provider configuration.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)


@pulumi.input_type
class _SubnetworkIAMPolicyState:
    def __init__(__self__, *,
                 etag: Optional[pulumi.Input[str]] = None,
                 policy_data: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 subnetwork: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering SubnetworkIAMPolicy resources.
        :param pulumi.Input[str] etag: (Computed) The etag of the IAM policy.
        :param pulumi.Input[str] policy_data: The policy data generated by
               a _organizations_get_iam_policy_ data source.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        :param pulumi.Input[str] region: The GCP region for this subnetwork.
               Used to find the parent resource to bind the IAM policy to. If not specified,
               the value will be parsed from the identifier of the parent resource. If no region is provided in the parent identifier and no
               region is specified, it is taken from the provider configuration.
        :param pulumi.Input[str] subnetwork: Used to find the parent resource to bind the IAM policy to
        """
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if policy_data is not None:
            pulumi.set(__self__, "policy_data", policy_data)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if subnetwork is not None:
            pulumi.set(__self__, "subnetwork", subnetwork)

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
    @pulumi.getter(name="policyData")
    def policy_data(self) -> Optional[pulumi.Input[str]]:
        """
        The policy data generated by
        a _organizations_get_iam_policy_ data source.
        """
        return pulumi.get(self, "policy_data")

    @policy_data.setter
    def policy_data(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_data", value)

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
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The GCP region for this subnetwork.
        Used to find the parent resource to bind the IAM policy to. If not specified,
        the value will be parsed from the identifier of the parent resource. If no region is provided in the parent identifier and no
        region is specified, it is taken from the provider configuration.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter
    def subnetwork(self) -> Optional[pulumi.Input[str]]:
        """
        Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "subnetwork")

    @subnetwork.setter
    def subnetwork(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subnetwork", value)


class SubnetworkIAMPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 policy_data: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 subnetwork: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Three different resources help you manage your IAM policy for Compute Engine Subnetwork. Each of these resources serves a different use case:

        * `compute.SubnetworkIAMPolicy`: Authoritative. Sets the IAM policy for the subnetwork and replaces any existing policy already attached.
        * `compute.SubnetworkIAMBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the subnetwork are preserved.
        * `compute.SubnetworkIAMMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the subnetwork are preserved.

        > **Note:** `compute.SubnetworkIAMPolicy` **cannot** be used in conjunction with `compute.SubnetworkIAMBinding` and `compute.SubnetworkIAMMember` or they will fight over what your policy should be.

        > **Note:** `compute.SubnetworkIAMBinding` resources **can be** used in conjunction with `compute.SubnetworkIAMMember` resources **only if** they do not grant privilege to the same role.

        > **Note:**  This resource supports IAM Conditions but they have some known limitations which can be found [here](https://cloud.google.com/iam/docs/conditions-overview#limitations). Please review this article if you are having issues with IAM Conditions.

        ## google\\_compute\\_subnetwork\\_iam\\_policy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/compute.networkUser",
            members=["user:jane@example.com"],
        )])
        policy = gcp.compute.SubnetworkIAMPolicy("policy",
            project=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["project"],
            region=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["region"],
            subnetwork=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["name"],
            policy_data=admin.policy_data)
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/compute.networkUser",
            members=["user:jane@example.com"],
            condition=gcp.organizations.GetIAMPolicyBindingConditionArgs(
                title="expires_after_2019_12_31",
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\\"2020-01-01T00:00:00Z\\")",
            ),
        )])
        policy = gcp.compute.SubnetworkIAMPolicy("policy",
            project=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["project"],
            region=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["region"],
            subnetwork=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["name"],
            policy_data=admin.policy_data)
        ```
        ## google\\_compute\\_subnetwork\\_iam\\_binding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.compute.SubnetworkIAMBinding("binding",
            project=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["project"],
            region=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["region"],
            subnetwork=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["name"],
            role="roles/compute.networkUser",
            members=["user:jane@example.com"])
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.compute.SubnetworkIAMBinding("binding",
            project=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["project"],
            region=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["region"],
            subnetwork=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["name"],
            role="roles/compute.networkUser",
            members=["user:jane@example.com"],
            condition=gcp.compute.SubnetworkIAMBindingConditionArgs(
                title="expires_after_2019_12_31",
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\\"2020-01-01T00:00:00Z\\")",
            ))
        ```
        ## google\\_compute\\_subnetwork\\_iam\\_member

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.compute.SubnetworkIAMMember("member",
            project=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["project"],
            region=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["region"],
            subnetwork=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["name"],
            role="roles/compute.networkUser",
            member="user:jane@example.com")
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.compute.SubnetworkIAMMember("member",
            project=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["project"],
            region=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["region"],
            subnetwork=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["name"],
            role="roles/compute.networkUser",
            member="user:jane@example.com",
            condition=gcp.compute.SubnetworkIAMMemberConditionArgs(
                title="expires_after_2019_12_31",
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\\"2020-01-01T00:00:00Z\\")",
            ))
        ```

        ## Import

        For all import syntaxes, the "resource in question" can take any of the following forms* projects/{{project}}/regions/{{region}}/subnetworks/{{name}} * {{project}}/{{region}}/{{name}} * {{region}}/{{name}} * {{name}} Any variables not passed in the import command will be taken from the provider configuration. Compute Engine subnetwork IAM resources can be imported using the resource identifiers, role, and member. IAM member imports use space-delimited identifiersthe resource in question, the role, and the member identity, e.g.

        ```sh
         $ pulumi import gcp:compute/subnetworkIAMPolicy:SubnetworkIAMPolicy editor "projects/{{project}}/regions/{{region}}/subnetworks/{{subnetwork}} roles/compute.networkUser user:jane@example.com"
        ```

         IAM binding imports use space-delimited identifiersthe resource in question and the role, e.g.

        ```sh
         $ pulumi import gcp:compute/subnetworkIAMPolicy:SubnetworkIAMPolicy editor "projects/{{project}}/regions/{{region}}/subnetworks/{{subnetwork}} roles/compute.networkUser"
        ```

         IAM policy imports use the identifier of the resource in question, e.g.

        ```sh
         $ pulumi import gcp:compute/subnetworkIAMPolicy:SubnetworkIAMPolicy editor projects/{{project}}/regions/{{region}}/subnetworks/{{subnetwork}}
        ```

         -> **Custom Roles**If you're importing a IAM resource with a custom role, make sure to use the

        full name of the custom role, e.g. `[projects/my-project|organizations/my-org]/roles/my-custom-role`.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] policy_data: The policy data generated by
               a _organizations_get_iam_policy_ data source.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        :param pulumi.Input[str] region: The GCP region for this subnetwork.
               Used to find the parent resource to bind the IAM policy to. If not specified,
               the value will be parsed from the identifier of the parent resource. If no region is provided in the parent identifier and no
               region is specified, it is taken from the provider configuration.
        :param pulumi.Input[str] subnetwork: Used to find the parent resource to bind the IAM policy to
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SubnetworkIAMPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Three different resources help you manage your IAM policy for Compute Engine Subnetwork. Each of these resources serves a different use case:

        * `compute.SubnetworkIAMPolicy`: Authoritative. Sets the IAM policy for the subnetwork and replaces any existing policy already attached.
        * `compute.SubnetworkIAMBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the subnetwork are preserved.
        * `compute.SubnetworkIAMMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the subnetwork are preserved.

        > **Note:** `compute.SubnetworkIAMPolicy` **cannot** be used in conjunction with `compute.SubnetworkIAMBinding` and `compute.SubnetworkIAMMember` or they will fight over what your policy should be.

        > **Note:** `compute.SubnetworkIAMBinding` resources **can be** used in conjunction with `compute.SubnetworkIAMMember` resources **only if** they do not grant privilege to the same role.

        > **Note:**  This resource supports IAM Conditions but they have some known limitations which can be found [here](https://cloud.google.com/iam/docs/conditions-overview#limitations). Please review this article if you are having issues with IAM Conditions.

        ## google\\_compute\\_subnetwork\\_iam\\_policy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/compute.networkUser",
            members=["user:jane@example.com"],
        )])
        policy = gcp.compute.SubnetworkIAMPolicy("policy",
            project=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["project"],
            region=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["region"],
            subnetwork=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["name"],
            policy_data=admin.policy_data)
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/compute.networkUser",
            members=["user:jane@example.com"],
            condition=gcp.organizations.GetIAMPolicyBindingConditionArgs(
                title="expires_after_2019_12_31",
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\\"2020-01-01T00:00:00Z\\")",
            ),
        )])
        policy = gcp.compute.SubnetworkIAMPolicy("policy",
            project=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["project"],
            region=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["region"],
            subnetwork=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["name"],
            policy_data=admin.policy_data)
        ```
        ## google\\_compute\\_subnetwork\\_iam\\_binding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.compute.SubnetworkIAMBinding("binding",
            project=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["project"],
            region=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["region"],
            subnetwork=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["name"],
            role="roles/compute.networkUser",
            members=["user:jane@example.com"])
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.compute.SubnetworkIAMBinding("binding",
            project=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["project"],
            region=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["region"],
            subnetwork=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["name"],
            role="roles/compute.networkUser",
            members=["user:jane@example.com"],
            condition=gcp.compute.SubnetworkIAMBindingConditionArgs(
                title="expires_after_2019_12_31",
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\\"2020-01-01T00:00:00Z\\")",
            ))
        ```
        ## google\\_compute\\_subnetwork\\_iam\\_member

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.compute.SubnetworkIAMMember("member",
            project=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["project"],
            region=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["region"],
            subnetwork=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["name"],
            role="roles/compute.networkUser",
            member="user:jane@example.com")
        ```

        With IAM Conditions:

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.compute.SubnetworkIAMMember("member",
            project=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["project"],
            region=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["region"],
            subnetwork=google_compute_subnetwork["network-with-private-secondary-ip-ranges"]["name"],
            role="roles/compute.networkUser",
            member="user:jane@example.com",
            condition=gcp.compute.SubnetworkIAMMemberConditionArgs(
                title="expires_after_2019_12_31",
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\\"2020-01-01T00:00:00Z\\")",
            ))
        ```

        ## Import

        For all import syntaxes, the "resource in question" can take any of the following forms* projects/{{project}}/regions/{{region}}/subnetworks/{{name}} * {{project}}/{{region}}/{{name}} * {{region}}/{{name}} * {{name}} Any variables not passed in the import command will be taken from the provider configuration. Compute Engine subnetwork IAM resources can be imported using the resource identifiers, role, and member. IAM member imports use space-delimited identifiersthe resource in question, the role, and the member identity, e.g.

        ```sh
         $ pulumi import gcp:compute/subnetworkIAMPolicy:SubnetworkIAMPolicy editor "projects/{{project}}/regions/{{region}}/subnetworks/{{subnetwork}} roles/compute.networkUser user:jane@example.com"
        ```

         IAM binding imports use space-delimited identifiersthe resource in question and the role, e.g.

        ```sh
         $ pulumi import gcp:compute/subnetworkIAMPolicy:SubnetworkIAMPolicy editor "projects/{{project}}/regions/{{region}}/subnetworks/{{subnetwork}} roles/compute.networkUser"
        ```

         IAM policy imports use the identifier of the resource in question, e.g.

        ```sh
         $ pulumi import gcp:compute/subnetworkIAMPolicy:SubnetworkIAMPolicy editor projects/{{project}}/regions/{{region}}/subnetworks/{{subnetwork}}
        ```

         -> **Custom Roles**If you're importing a IAM resource with a custom role, make sure to use the

        full name of the custom role, e.g. `[projects/my-project|organizations/my-org]/roles/my-custom-role`.

        :param str resource_name: The name of the resource.
        :param SubnetworkIAMPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SubnetworkIAMPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 policy_data: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 subnetwork: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SubnetworkIAMPolicyArgs.__new__(SubnetworkIAMPolicyArgs)

            if policy_data is None and not opts.urn:
                raise TypeError("Missing required property 'policy_data'")
            __props__.__dict__["policy_data"] = policy_data
            __props__.__dict__["project"] = project
            __props__.__dict__["region"] = region
            if subnetwork is None and not opts.urn:
                raise TypeError("Missing required property 'subnetwork'")
            __props__.__dict__["subnetwork"] = subnetwork
            __props__.__dict__["etag"] = None
        super(SubnetworkIAMPolicy, __self__).__init__(
            'gcp:compute/subnetworkIAMPolicy:SubnetworkIAMPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            etag: Optional[pulumi.Input[str]] = None,
            policy_data: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            region: Optional[pulumi.Input[str]] = None,
            subnetwork: Optional[pulumi.Input[str]] = None) -> 'SubnetworkIAMPolicy':
        """
        Get an existing SubnetworkIAMPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] etag: (Computed) The etag of the IAM policy.
        :param pulumi.Input[str] policy_data: The policy data generated by
               a _organizations_get_iam_policy_ data source.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        :param pulumi.Input[str] region: The GCP region for this subnetwork.
               Used to find the parent resource to bind the IAM policy to. If not specified,
               the value will be parsed from the identifier of the parent resource. If no region is provided in the parent identifier and no
               region is specified, it is taken from the provider configuration.
        :param pulumi.Input[str] subnetwork: Used to find the parent resource to bind the IAM policy to
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SubnetworkIAMPolicyState.__new__(_SubnetworkIAMPolicyState)

        __props__.__dict__["etag"] = etag
        __props__.__dict__["policy_data"] = policy_data
        __props__.__dict__["project"] = project
        __props__.__dict__["region"] = region
        __props__.__dict__["subnetwork"] = subnetwork
        return SubnetworkIAMPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        (Computed) The etag of the IAM policy.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="policyData")
    def policy_data(self) -> pulumi.Output[str]:
        """
        The policy data generated by
        a _organizations_get_iam_policy_ data source.
        """
        return pulumi.get(self, "policy_data")

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
    def region(self) -> pulumi.Output[str]:
        """
        The GCP region for this subnetwork.
        Used to find the parent resource to bind the IAM policy to. If not specified,
        the value will be parsed from the identifier of the parent resource. If no region is provided in the parent identifier and no
        region is specified, it is taken from the provider configuration.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter
    def subnetwork(self) -> pulumi.Output[str]:
        """
        Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "subnetwork")

