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

__all__ = ['ListingIamMemberArgs', 'ListingIamMember']

@pulumi.input_type
class ListingIamMemberArgs:
    def __init__(__self__, *,
                 data_exchange_id: pulumi.Input[str],
                 listing_id: pulumi.Input[str],
                 member: pulumi.Input[str],
                 role: pulumi.Input[str],
                 condition: Optional[pulumi.Input['ListingIamMemberConditionArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ListingIamMember resource.
        :param pulumi.Input[str] data_exchange_id: The ID of the data exchange. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] listing_id: The ID of the listing. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `bigqueryanalyticshub.ListingIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        :param pulumi.Input[str] location: The name of the location this data exchange listing.
               Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        """
        pulumi.set(__self__, "data_exchange_id", data_exchange_id)
        pulumi.set(__self__, "listing_id", listing_id)
        pulumi.set(__self__, "member", member)
        pulumi.set(__self__, "role", role)
        if condition is not None:
            pulumi.set(__self__, "condition", condition)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter(name="dataExchangeId")
    def data_exchange_id(self) -> pulumi.Input[str]:
        """
        The ID of the data exchange. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "data_exchange_id")

    @data_exchange_id.setter
    def data_exchange_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "data_exchange_id", value)

    @property
    @pulumi.getter(name="listingId")
    def listing_id(self) -> pulumi.Input[str]:
        """
        The ID of the listing. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "listing_id")

    @listing_id.setter
    def listing_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "listing_id", value)

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
        `bigqueryanalyticshub.ListingIamBinding` can be used per role. Note that custom roles must be of the format
        `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: pulumi.Input[str]):
        pulumi.set(self, "role", value)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input['ListingIamMemberConditionArgs']]:
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input['ListingIamMemberConditionArgs']]):
        pulumi.set(self, "condition", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the location this data exchange listing.
        Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

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
class _ListingIamMemberState:
    def __init__(__self__, *,
                 condition: Optional[pulumi.Input['ListingIamMemberConditionArgs']] = None,
                 data_exchange_id: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 listing_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 member: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ListingIamMember resources.
        :param pulumi.Input[str] data_exchange_id: The ID of the data exchange. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] etag: (Computed) The etag of the IAM policy.
        :param pulumi.Input[str] listing_id: The ID of the listing. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] location: The name of the location this data exchange listing.
               Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `bigqueryanalyticshub.ListingIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        if condition is not None:
            pulumi.set(__self__, "condition", condition)
        if data_exchange_id is not None:
            pulumi.set(__self__, "data_exchange_id", data_exchange_id)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if listing_id is not None:
            pulumi.set(__self__, "listing_id", listing_id)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if member is not None:
            pulumi.set(__self__, "member", member)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if role is not None:
            pulumi.set(__self__, "role", role)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input['ListingIamMemberConditionArgs']]:
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input['ListingIamMemberConditionArgs']]):
        pulumi.set(self, "condition", value)

    @property
    @pulumi.getter(name="dataExchangeId")
    def data_exchange_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the data exchange. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "data_exchange_id")

    @data_exchange_id.setter
    def data_exchange_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data_exchange_id", value)

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
    @pulumi.getter(name="listingId")
    def listing_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the listing. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "listing_id")

    @listing_id.setter
    def listing_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "listing_id", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the location this data exchange listing.
        Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def member(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "member")

    @member.setter
    def member(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "member", value)

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
        `bigqueryanalyticshub.ListingIamBinding` can be used per role. Note that custom roles must be of the format
        `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role", value)


class ListingIamMember(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 condition: Optional[pulumi.Input[pulumi.InputType['ListingIamMemberConditionArgs']]] = None,
                 data_exchange_id: Optional[pulumi.Input[str]] = None,
                 listing_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 member: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Three different resources help you manage your IAM policy for Bigquery Analytics Hub Listing. Each of these resources serves a different use case:

        * `bigqueryanalyticshub.ListingIamPolicy`: Authoritative. Sets the IAM policy for the listing and replaces any existing policy already attached.
        * `bigqueryanalyticshub.ListingIamBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the listing are preserved.
        * `bigqueryanalyticshub.ListingIamMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the listing are preserved.

        > **Note:** `bigqueryanalyticshub.ListingIamPolicy` **cannot** be used in conjunction with `bigqueryanalyticshub.ListingIamBinding` and `bigqueryanalyticshub.ListingIamMember` or they will fight over what your policy should be.

        > **Note:** `bigqueryanalyticshub.ListingIamBinding` resources **can be** used in conjunction with `bigqueryanalyticshub.ListingIamMember` resources **only if** they do not grant privilege to the same role.

        ## google\\_bigquery\\_analytics\\_hub\\_listing\\_iam\\_policy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/viewer",
            members=["user:jane@example.com"],
        )])
        policy = gcp.bigqueryanalyticshub.ListingIamPolicy("policy",
            project=google_bigquery_analytics_hub_listing["listing"]["project"],
            location=google_bigquery_analytics_hub_listing["listing"]["location"],
            data_exchange_id=google_bigquery_analytics_hub_listing["listing"]["data_exchange_id"],
            listing_id=google_bigquery_analytics_hub_listing["listing"]["listing_id"],
            policy_data=admin.policy_data)
        ```

        ## google\\_bigquery\\_analytics\\_hub\\_listing\\_iam\\_binding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.bigqueryanalyticshub.ListingIamBinding("binding",
            project=google_bigquery_analytics_hub_listing["listing"]["project"],
            location=google_bigquery_analytics_hub_listing["listing"]["location"],
            data_exchange_id=google_bigquery_analytics_hub_listing["listing"]["data_exchange_id"],
            listing_id=google_bigquery_analytics_hub_listing["listing"]["listing_id"],
            role="roles/viewer",
            members=["user:jane@example.com"])
        ```

        ## google\\_bigquery\\_analytics\\_hub\\_listing\\_iam\\_member

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.bigqueryanalyticshub.ListingIamMember("member",
            project=google_bigquery_analytics_hub_listing["listing"]["project"],
            location=google_bigquery_analytics_hub_listing["listing"]["location"],
            data_exchange_id=google_bigquery_analytics_hub_listing["listing"]["data_exchange_id"],
            listing_id=google_bigquery_analytics_hub_listing["listing"]["listing_id"],
            role="roles/viewer",
            member="user:jane@example.com")
        ```

        ## Import

        For all import syntaxes, the "resource in question" can take any of the following forms* projects/{{project}}/locations/{{location}}/dataExchanges/{{data_exchange_id}}/listings/{{listing_id}} * {{project}}/{{location}}/{{data_exchange_id}}/{{listing_id}} * {{location}}/{{data_exchange_id}}/{{listing_id}} * {{listing_id}} Any variables not passed in the import command will be taken from the provider configuration. Bigquery Analytics Hub listing IAM resources can be imported using the resource identifiers, role, and member. IAM member imports use space-delimited identifiersthe resource in question, the role, and the member identity, e.g.

        ```sh
         $ pulumi import gcp:bigqueryanalyticshub/listingIamMember:ListingIamMember editor "projects/{{project}}/locations/{{location}}/dataExchanges/{{data_exchange_id}}/listings/{{listing_id}} roles/viewer user:jane@example.com"
        ```

         IAM binding imports use space-delimited identifiersthe resource in question and the role, e.g.

        ```sh
         $ pulumi import gcp:bigqueryanalyticshub/listingIamMember:ListingIamMember editor "projects/{{project}}/locations/{{location}}/dataExchanges/{{data_exchange_id}}/listings/{{listing_id}} roles/viewer"
        ```

         IAM policy imports use the identifier of the resource in question, e.g.

        ```sh
         $ pulumi import gcp:bigqueryanalyticshub/listingIamMember:ListingIamMember editor projects/{{project}}/locations/{{location}}/dataExchanges/{{data_exchange_id}}/listings/{{listing_id}}
        ```

         -> **Custom Roles**If you're importing a IAM resource with a custom role, make sure to use the

        full name of the custom role, e.g. `[projects/my-project|organizations/my-org]/roles/my-custom-role`.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] data_exchange_id: The ID of the data exchange. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] listing_id: The ID of the listing. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] location: The name of the location this data exchange listing.
               Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `bigqueryanalyticshub.ListingIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ListingIamMemberArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Three different resources help you manage your IAM policy for Bigquery Analytics Hub Listing. Each of these resources serves a different use case:

        * `bigqueryanalyticshub.ListingIamPolicy`: Authoritative. Sets the IAM policy for the listing and replaces any existing policy already attached.
        * `bigqueryanalyticshub.ListingIamBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the listing are preserved.
        * `bigqueryanalyticshub.ListingIamMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the listing are preserved.

        > **Note:** `bigqueryanalyticshub.ListingIamPolicy` **cannot** be used in conjunction with `bigqueryanalyticshub.ListingIamBinding` and `bigqueryanalyticshub.ListingIamMember` or they will fight over what your policy should be.

        > **Note:** `bigqueryanalyticshub.ListingIamBinding` resources **can be** used in conjunction with `bigqueryanalyticshub.ListingIamMember` resources **only if** they do not grant privilege to the same role.

        ## google\\_bigquery\\_analytics\\_hub\\_listing\\_iam\\_policy

        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/viewer",
            members=["user:jane@example.com"],
        )])
        policy = gcp.bigqueryanalyticshub.ListingIamPolicy("policy",
            project=google_bigquery_analytics_hub_listing["listing"]["project"],
            location=google_bigquery_analytics_hub_listing["listing"]["location"],
            data_exchange_id=google_bigquery_analytics_hub_listing["listing"]["data_exchange_id"],
            listing_id=google_bigquery_analytics_hub_listing["listing"]["listing_id"],
            policy_data=admin.policy_data)
        ```

        ## google\\_bigquery\\_analytics\\_hub\\_listing\\_iam\\_binding

        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.bigqueryanalyticshub.ListingIamBinding("binding",
            project=google_bigquery_analytics_hub_listing["listing"]["project"],
            location=google_bigquery_analytics_hub_listing["listing"]["location"],
            data_exchange_id=google_bigquery_analytics_hub_listing["listing"]["data_exchange_id"],
            listing_id=google_bigquery_analytics_hub_listing["listing"]["listing_id"],
            role="roles/viewer",
            members=["user:jane@example.com"])
        ```

        ## google\\_bigquery\\_analytics\\_hub\\_listing\\_iam\\_member

        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.bigqueryanalyticshub.ListingIamMember("member",
            project=google_bigquery_analytics_hub_listing["listing"]["project"],
            location=google_bigquery_analytics_hub_listing["listing"]["location"],
            data_exchange_id=google_bigquery_analytics_hub_listing["listing"]["data_exchange_id"],
            listing_id=google_bigquery_analytics_hub_listing["listing"]["listing_id"],
            role="roles/viewer",
            member="user:jane@example.com")
        ```

        ## Import

        For all import syntaxes, the "resource in question" can take any of the following forms* projects/{{project}}/locations/{{location}}/dataExchanges/{{data_exchange_id}}/listings/{{listing_id}} * {{project}}/{{location}}/{{data_exchange_id}}/{{listing_id}} * {{location}}/{{data_exchange_id}}/{{listing_id}} * {{listing_id}} Any variables not passed in the import command will be taken from the provider configuration. Bigquery Analytics Hub listing IAM resources can be imported using the resource identifiers, role, and member. IAM member imports use space-delimited identifiersthe resource in question, the role, and the member identity, e.g.

        ```sh
         $ pulumi import gcp:bigqueryanalyticshub/listingIamMember:ListingIamMember editor "projects/{{project}}/locations/{{location}}/dataExchanges/{{data_exchange_id}}/listings/{{listing_id}} roles/viewer user:jane@example.com"
        ```

         IAM binding imports use space-delimited identifiersthe resource in question and the role, e.g.

        ```sh
         $ pulumi import gcp:bigqueryanalyticshub/listingIamMember:ListingIamMember editor "projects/{{project}}/locations/{{location}}/dataExchanges/{{data_exchange_id}}/listings/{{listing_id}} roles/viewer"
        ```

         IAM policy imports use the identifier of the resource in question, e.g.

        ```sh
         $ pulumi import gcp:bigqueryanalyticshub/listingIamMember:ListingIamMember editor projects/{{project}}/locations/{{location}}/dataExchanges/{{data_exchange_id}}/listings/{{listing_id}}
        ```

         -> **Custom Roles**If you're importing a IAM resource with a custom role, make sure to use the

        full name of the custom role, e.g. `[projects/my-project|organizations/my-org]/roles/my-custom-role`.

        :param str resource_name: The name of the resource.
        :param ListingIamMemberArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ListingIamMemberArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 condition: Optional[pulumi.Input[pulumi.InputType['ListingIamMemberConditionArgs']]] = None,
                 data_exchange_id: Optional[pulumi.Input[str]] = None,
                 listing_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 member: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ListingIamMemberArgs.__new__(ListingIamMemberArgs)

            __props__.__dict__["condition"] = condition
            if data_exchange_id is None and not opts.urn:
                raise TypeError("Missing required property 'data_exchange_id'")
            __props__.__dict__["data_exchange_id"] = data_exchange_id
            if listing_id is None and not opts.urn:
                raise TypeError("Missing required property 'listing_id'")
            __props__.__dict__["listing_id"] = listing_id
            __props__.__dict__["location"] = location
            if member is None and not opts.urn:
                raise TypeError("Missing required property 'member'")
            __props__.__dict__["member"] = member
            __props__.__dict__["project"] = project
            if role is None and not opts.urn:
                raise TypeError("Missing required property 'role'")
            __props__.__dict__["role"] = role
            __props__.__dict__["etag"] = None
        super(ListingIamMember, __self__).__init__(
            'gcp:bigqueryanalyticshub/listingIamMember:ListingIamMember',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            condition: Optional[pulumi.Input[pulumi.InputType['ListingIamMemberConditionArgs']]] = None,
            data_exchange_id: Optional[pulumi.Input[str]] = None,
            etag: Optional[pulumi.Input[str]] = None,
            listing_id: Optional[pulumi.Input[str]] = None,
            location: Optional[pulumi.Input[str]] = None,
            member: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            role: Optional[pulumi.Input[str]] = None) -> 'ListingIamMember':
        """
        Get an existing ListingIamMember resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] data_exchange_id: The ID of the data exchange. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] etag: (Computed) The etag of the IAM policy.
        :param pulumi.Input[str] listing_id: The ID of the listing. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] location: The name of the location this data exchange listing.
               Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `bigqueryanalyticshub.ListingIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ListingIamMemberState.__new__(_ListingIamMemberState)

        __props__.__dict__["condition"] = condition
        __props__.__dict__["data_exchange_id"] = data_exchange_id
        __props__.__dict__["etag"] = etag
        __props__.__dict__["listing_id"] = listing_id
        __props__.__dict__["location"] = location
        __props__.__dict__["member"] = member
        __props__.__dict__["project"] = project
        __props__.__dict__["role"] = role
        return ListingIamMember(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def condition(self) -> pulumi.Output[Optional['outputs.ListingIamMemberCondition']]:
        return pulumi.get(self, "condition")

    @property
    @pulumi.getter(name="dataExchangeId")
    def data_exchange_id(self) -> pulumi.Output[str]:
        """
        The ID of the data exchange. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "data_exchange_id")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        (Computed) The etag of the IAM policy.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="listingId")
    def listing_id(self) -> pulumi.Output[str]:
        """
        The ID of the listing. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "listing_id")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The name of the location this data exchange listing.
        Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def member(self) -> pulumi.Output[str]:
        return pulumi.get(self, "member")

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
        `bigqueryanalyticshub.ListingIamBinding` can be used per role. Note that custom roles must be of the format
        `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        return pulumi.get(self, "role")

