# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AuthorizedOrgsDescArgs', 'AuthorizedOrgsDesc']

@pulumi.input_type
class AuthorizedOrgsDescArgs:
    def __init__(__self__, *,
                 parent: pulumi.Input[str],
                 asset_type: Optional[pulumi.Input[str]] = None,
                 authorization_direction: Optional[pulumi.Input[str]] = None,
                 authorization_type: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 orgs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a AuthorizedOrgsDesc resource.
        :param pulumi.Input[str] parent: Required. Resource name for the access policy which owns this `AuthorizedOrgsDesc`.
        :param pulumi.Input[str] asset_type: The type of entities that need to use the authorization relationship during
               evaluation, such as a device. Valid values are "ASSET_TYPE_DEVICE" and
               "ASSET_TYPE_CREDENTIAL_STRENGTH".
               Possible values are `ASSET_TYPE_DEVICE` and `ASSET_TYPE_CREDENTIAL_STRENGTH`.
        :param pulumi.Input[str] authorization_direction: The direction of the authorization relationship between this organization
               and the organizations listed in the "orgs" field. The valid values for this
               field include the following:
               AUTHORIZATION_DIRECTION_FROM: Allows this organization to evaluate traffic
               in the organizations listed in the `orgs` field.
               AUTHORIZATION_DIRECTION_TO: Allows the organizations listed in the `orgs`
               field to evaluate the traffic in this organization.
               For the authorization relationship to take effect, all of the organizations
               must authorize and specify the appropriate relationship direction. For
               example, if organization A authorized organization B and C to evaluate its
               traffic, by specifying "AUTHORIZATION_DIRECTION_TO" as the authorization
               direction, organizations B and C must specify
               "AUTHORIZATION_DIRECTION_FROM" as the authorization direction in their
               "AuthorizedOrgsDesc" resource.
               Possible values are `AUTHORIZATION_DIRECTION_TO` and `AUTHORIZATION_DIRECTION_FROM`.
        :param pulumi.Input[str] authorization_type: A granular control type for authorization levels. Valid value is "AUTHORIZATION_TYPE_TRUST".
               Possible values are `AUTHORIZATION_TYPE_TRUST`.
        :param pulumi.Input[str] name: Resource name for the `AuthorizedOrgsDesc`. Format:
               `accessPolicies/{access_policy}/authorizedOrgsDescs/{authorized_orgs_desc}`.
               The `authorized_orgs_desc` component must begin with a letter, followed by
               alphanumeric characters or `_`.
               After you create an `AuthorizedOrgsDesc`, you cannot change its `name`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] orgs: The list of organization ids in this AuthorizedOrgsDesc.
               Format: `organizations/<org_number>`
               Example: `organizations/123456`
        """
        pulumi.set(__self__, "parent", parent)
        if asset_type is not None:
            pulumi.set(__self__, "asset_type", asset_type)
        if authorization_direction is not None:
            pulumi.set(__self__, "authorization_direction", authorization_direction)
        if authorization_type is not None:
            pulumi.set(__self__, "authorization_type", authorization_type)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if orgs is not None:
            pulumi.set(__self__, "orgs", orgs)

    @property
    @pulumi.getter
    def parent(self) -> pulumi.Input[str]:
        """
        Required. Resource name for the access policy which owns this `AuthorizedOrgsDesc`.
        """
        return pulumi.get(self, "parent")

    @parent.setter
    def parent(self, value: pulumi.Input[str]):
        pulumi.set(self, "parent", value)

    @property
    @pulumi.getter(name="assetType")
    def asset_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of entities that need to use the authorization relationship during
        evaluation, such as a device. Valid values are "ASSET_TYPE_DEVICE" and
        "ASSET_TYPE_CREDENTIAL_STRENGTH".
        Possible values are `ASSET_TYPE_DEVICE` and `ASSET_TYPE_CREDENTIAL_STRENGTH`.
        """
        return pulumi.get(self, "asset_type")

    @asset_type.setter
    def asset_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "asset_type", value)

    @property
    @pulumi.getter(name="authorizationDirection")
    def authorization_direction(self) -> Optional[pulumi.Input[str]]:
        """
        The direction of the authorization relationship between this organization
        and the organizations listed in the "orgs" field. The valid values for this
        field include the following:
        AUTHORIZATION_DIRECTION_FROM: Allows this organization to evaluate traffic
        in the organizations listed in the `orgs` field.
        AUTHORIZATION_DIRECTION_TO: Allows the organizations listed in the `orgs`
        field to evaluate the traffic in this organization.
        For the authorization relationship to take effect, all of the organizations
        must authorize and specify the appropriate relationship direction. For
        example, if organization A authorized organization B and C to evaluate its
        traffic, by specifying "AUTHORIZATION_DIRECTION_TO" as the authorization
        direction, organizations B and C must specify
        "AUTHORIZATION_DIRECTION_FROM" as the authorization direction in their
        "AuthorizedOrgsDesc" resource.
        Possible values are `AUTHORIZATION_DIRECTION_TO` and `AUTHORIZATION_DIRECTION_FROM`.
        """
        return pulumi.get(self, "authorization_direction")

    @authorization_direction.setter
    def authorization_direction(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "authorization_direction", value)

    @property
    @pulumi.getter(name="authorizationType")
    def authorization_type(self) -> Optional[pulumi.Input[str]]:
        """
        A granular control type for authorization levels. Valid value is "AUTHORIZATION_TYPE_TRUST".
        Possible values are `AUTHORIZATION_TYPE_TRUST`.
        """
        return pulumi.get(self, "authorization_type")

    @authorization_type.setter
    def authorization_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "authorization_type", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Resource name for the `AuthorizedOrgsDesc`. Format:
        `accessPolicies/{access_policy}/authorizedOrgsDescs/{authorized_orgs_desc}`.
        The `authorized_orgs_desc` component must begin with a letter, followed by
        alphanumeric characters or `_`.
        After you create an `AuthorizedOrgsDesc`, you cannot change its `name`.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def orgs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The list of organization ids in this AuthorizedOrgsDesc.
        Format: `organizations/<org_number>`
        Example: `organizations/123456`
        """
        return pulumi.get(self, "orgs")

    @orgs.setter
    def orgs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "orgs", value)


@pulumi.input_type
class _AuthorizedOrgsDescState:
    def __init__(__self__, *,
                 asset_type: Optional[pulumi.Input[str]] = None,
                 authorization_direction: Optional[pulumi.Input[str]] = None,
                 authorization_type: Optional[pulumi.Input[str]] = None,
                 create_time: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 orgs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 parent: Optional[pulumi.Input[str]] = None,
                 update_time: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AuthorizedOrgsDesc resources.
        :param pulumi.Input[str] asset_type: The type of entities that need to use the authorization relationship during
               evaluation, such as a device. Valid values are "ASSET_TYPE_DEVICE" and
               "ASSET_TYPE_CREDENTIAL_STRENGTH".
               Possible values are `ASSET_TYPE_DEVICE` and `ASSET_TYPE_CREDENTIAL_STRENGTH`.
        :param pulumi.Input[str] authorization_direction: The direction of the authorization relationship between this organization
               and the organizations listed in the "orgs" field. The valid values for this
               field include the following:
               AUTHORIZATION_DIRECTION_FROM: Allows this organization to evaluate traffic
               in the organizations listed in the `orgs` field.
               AUTHORIZATION_DIRECTION_TO: Allows the organizations listed in the `orgs`
               field to evaluate the traffic in this organization.
               For the authorization relationship to take effect, all of the organizations
               must authorize and specify the appropriate relationship direction. For
               example, if organization A authorized organization B and C to evaluate its
               traffic, by specifying "AUTHORIZATION_DIRECTION_TO" as the authorization
               direction, organizations B and C must specify
               "AUTHORIZATION_DIRECTION_FROM" as the authorization direction in their
               "AuthorizedOrgsDesc" resource.
               Possible values are `AUTHORIZATION_DIRECTION_TO` and `AUTHORIZATION_DIRECTION_FROM`.
        :param pulumi.Input[str] authorization_type: A granular control type for authorization levels. Valid value is "AUTHORIZATION_TYPE_TRUST".
               Possible values are `AUTHORIZATION_TYPE_TRUST`.
        :param pulumi.Input[str] create_time: Time the AuthorizedOrgsDesc was created in UTC.
        :param pulumi.Input[str] name: Resource name for the `AuthorizedOrgsDesc`. Format:
               `accessPolicies/{access_policy}/authorizedOrgsDescs/{authorized_orgs_desc}`.
               The `authorized_orgs_desc` component must begin with a letter, followed by
               alphanumeric characters or `_`.
               After you create an `AuthorizedOrgsDesc`, you cannot change its `name`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] orgs: The list of organization ids in this AuthorizedOrgsDesc.
               Format: `organizations/<org_number>`
               Example: `organizations/123456`
        :param pulumi.Input[str] parent: Required. Resource name for the access policy which owns this `AuthorizedOrgsDesc`.
        :param pulumi.Input[str] update_time: Time the AuthorizedOrgsDesc was updated in UTC.
        """
        if asset_type is not None:
            pulumi.set(__self__, "asset_type", asset_type)
        if authorization_direction is not None:
            pulumi.set(__self__, "authorization_direction", authorization_direction)
        if authorization_type is not None:
            pulumi.set(__self__, "authorization_type", authorization_type)
        if create_time is not None:
            pulumi.set(__self__, "create_time", create_time)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if orgs is not None:
            pulumi.set(__self__, "orgs", orgs)
        if parent is not None:
            pulumi.set(__self__, "parent", parent)
        if update_time is not None:
            pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter(name="assetType")
    def asset_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of entities that need to use the authorization relationship during
        evaluation, such as a device. Valid values are "ASSET_TYPE_DEVICE" and
        "ASSET_TYPE_CREDENTIAL_STRENGTH".
        Possible values are `ASSET_TYPE_DEVICE` and `ASSET_TYPE_CREDENTIAL_STRENGTH`.
        """
        return pulumi.get(self, "asset_type")

    @asset_type.setter
    def asset_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "asset_type", value)

    @property
    @pulumi.getter(name="authorizationDirection")
    def authorization_direction(self) -> Optional[pulumi.Input[str]]:
        """
        The direction of the authorization relationship between this organization
        and the organizations listed in the "orgs" field. The valid values for this
        field include the following:
        AUTHORIZATION_DIRECTION_FROM: Allows this organization to evaluate traffic
        in the organizations listed in the `orgs` field.
        AUTHORIZATION_DIRECTION_TO: Allows the organizations listed in the `orgs`
        field to evaluate the traffic in this organization.
        For the authorization relationship to take effect, all of the organizations
        must authorize and specify the appropriate relationship direction. For
        example, if organization A authorized organization B and C to evaluate its
        traffic, by specifying "AUTHORIZATION_DIRECTION_TO" as the authorization
        direction, organizations B and C must specify
        "AUTHORIZATION_DIRECTION_FROM" as the authorization direction in their
        "AuthorizedOrgsDesc" resource.
        Possible values are `AUTHORIZATION_DIRECTION_TO` and `AUTHORIZATION_DIRECTION_FROM`.
        """
        return pulumi.get(self, "authorization_direction")

    @authorization_direction.setter
    def authorization_direction(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "authorization_direction", value)

    @property
    @pulumi.getter(name="authorizationType")
    def authorization_type(self) -> Optional[pulumi.Input[str]]:
        """
        A granular control type for authorization levels. Valid value is "AUTHORIZATION_TYPE_TRUST".
        Possible values are `AUTHORIZATION_TYPE_TRUST`.
        """
        return pulumi.get(self, "authorization_type")

    @authorization_type.setter
    def authorization_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "authorization_type", value)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[pulumi.Input[str]]:
        """
        Time the AuthorizedOrgsDesc was created in UTC.
        """
        return pulumi.get(self, "create_time")

    @create_time.setter
    def create_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_time", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Resource name for the `AuthorizedOrgsDesc`. Format:
        `accessPolicies/{access_policy}/authorizedOrgsDescs/{authorized_orgs_desc}`.
        The `authorized_orgs_desc` component must begin with a letter, followed by
        alphanumeric characters or `_`.
        After you create an `AuthorizedOrgsDesc`, you cannot change its `name`.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def orgs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The list of organization ids in this AuthorizedOrgsDesc.
        Format: `organizations/<org_number>`
        Example: `organizations/123456`
        """
        return pulumi.get(self, "orgs")

    @orgs.setter
    def orgs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "orgs", value)

    @property
    @pulumi.getter
    def parent(self) -> Optional[pulumi.Input[str]]:
        """
        Required. Resource name for the access policy which owns this `AuthorizedOrgsDesc`.
        """
        return pulumi.get(self, "parent")

    @parent.setter
    def parent(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parent", value)

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> Optional[pulumi.Input[str]]:
        """
        Time the AuthorizedOrgsDesc was updated in UTC.
        """
        return pulumi.get(self, "update_time")

    @update_time.setter
    def update_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "update_time", value)


class AuthorizedOrgsDesc(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 asset_type: Optional[pulumi.Input[str]] = None,
                 authorization_direction: Optional[pulumi.Input[str]] = None,
                 authorization_type: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 orgs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 parent: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        An authorized organizations description describes a list of organizations
        (1) that have been authorized to use certain asset (for example, device) data
        owned by different organizations at the enforcement points, or (2) with certain
        asset (for example, device) have been authorized to access the resources in
        another organization at the enforcement points.

        To get more information about AuthorizedOrgsDesc, see:

        * [API documentation](https://cloud.google.com/access-context-manager/docs/reference/rest/v1/accessPolicies.authorizedOrgsDescs)
        * How-to Guides
            * [gcloud docs](https://cloud.google.com/beyondcorp-enterprise/docs/cross-org-authorization)

        > **Warning:** If you are using User ADCs (Application Default Credentials) with this resource,
        you must specify a `billing_project` and set `user_project_override` to true
        in the provider configuration. Otherwise the ACM API will return a 403 error.
        Your account must have the `serviceusage.services.use` permission on the
        `billing_project` you defined.

        ## Example Usage
        ### Access Context Manager Authorized Orgs Desc Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        test_access = gcp.accesscontextmanager.AccessPolicy("test-access",
            parent="organizations/",
            title="my policy")
        authorized_orgs_desc = gcp.accesscontextmanager.AuthorizedOrgsDesc("authorized-orgs-desc",
            asset_type="ASSET_TYPE_CREDENTIAL_STRENGTH",
            authorization_direction="AUTHORIZATION_DIRECTION_TO",
            authorization_type="AUTHORIZATION_TYPE_TRUST",
            orgs=[
                "organizations/12345",
                "organizations/98765",
            ],
            parent=test_access.name.apply(lambda name: f"accessPolicies/{name}"))
        ```

        ## Import

        AuthorizedOrgsDesc can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:accesscontextmanager/authorizedOrgsDesc:AuthorizedOrgsDesc default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] asset_type: The type of entities that need to use the authorization relationship during
               evaluation, such as a device. Valid values are "ASSET_TYPE_DEVICE" and
               "ASSET_TYPE_CREDENTIAL_STRENGTH".
               Possible values are `ASSET_TYPE_DEVICE` and `ASSET_TYPE_CREDENTIAL_STRENGTH`.
        :param pulumi.Input[str] authorization_direction: The direction of the authorization relationship between this organization
               and the organizations listed in the "orgs" field. The valid values for this
               field include the following:
               AUTHORIZATION_DIRECTION_FROM: Allows this organization to evaluate traffic
               in the organizations listed in the `orgs` field.
               AUTHORIZATION_DIRECTION_TO: Allows the organizations listed in the `orgs`
               field to evaluate the traffic in this organization.
               For the authorization relationship to take effect, all of the organizations
               must authorize and specify the appropriate relationship direction. For
               example, if organization A authorized organization B and C to evaluate its
               traffic, by specifying "AUTHORIZATION_DIRECTION_TO" as the authorization
               direction, organizations B and C must specify
               "AUTHORIZATION_DIRECTION_FROM" as the authorization direction in their
               "AuthorizedOrgsDesc" resource.
               Possible values are `AUTHORIZATION_DIRECTION_TO` and `AUTHORIZATION_DIRECTION_FROM`.
        :param pulumi.Input[str] authorization_type: A granular control type for authorization levels. Valid value is "AUTHORIZATION_TYPE_TRUST".
               Possible values are `AUTHORIZATION_TYPE_TRUST`.
        :param pulumi.Input[str] name: Resource name for the `AuthorizedOrgsDesc`. Format:
               `accessPolicies/{access_policy}/authorizedOrgsDescs/{authorized_orgs_desc}`.
               The `authorized_orgs_desc` component must begin with a letter, followed by
               alphanumeric characters or `_`.
               After you create an `AuthorizedOrgsDesc`, you cannot change its `name`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] orgs: The list of organization ids in this AuthorizedOrgsDesc.
               Format: `organizations/<org_number>`
               Example: `organizations/123456`
        :param pulumi.Input[str] parent: Required. Resource name for the access policy which owns this `AuthorizedOrgsDesc`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AuthorizedOrgsDescArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An authorized organizations description describes a list of organizations
        (1) that have been authorized to use certain asset (for example, device) data
        owned by different organizations at the enforcement points, or (2) with certain
        asset (for example, device) have been authorized to access the resources in
        another organization at the enforcement points.

        To get more information about AuthorizedOrgsDesc, see:

        * [API documentation](https://cloud.google.com/access-context-manager/docs/reference/rest/v1/accessPolicies.authorizedOrgsDescs)
        * How-to Guides
            * [gcloud docs](https://cloud.google.com/beyondcorp-enterprise/docs/cross-org-authorization)

        > **Warning:** If you are using User ADCs (Application Default Credentials) with this resource,
        you must specify a `billing_project` and set `user_project_override` to true
        in the provider configuration. Otherwise the ACM API will return a 403 error.
        Your account must have the `serviceusage.services.use` permission on the
        `billing_project` you defined.

        ## Example Usage
        ### Access Context Manager Authorized Orgs Desc Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        test_access = gcp.accesscontextmanager.AccessPolicy("test-access",
            parent="organizations/",
            title="my policy")
        authorized_orgs_desc = gcp.accesscontextmanager.AuthorizedOrgsDesc("authorized-orgs-desc",
            asset_type="ASSET_TYPE_CREDENTIAL_STRENGTH",
            authorization_direction="AUTHORIZATION_DIRECTION_TO",
            authorization_type="AUTHORIZATION_TYPE_TRUST",
            orgs=[
                "organizations/12345",
                "organizations/98765",
            ],
            parent=test_access.name.apply(lambda name: f"accessPolicies/{name}"))
        ```

        ## Import

        AuthorizedOrgsDesc can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:accesscontextmanager/authorizedOrgsDesc:AuthorizedOrgsDesc default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param AuthorizedOrgsDescArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AuthorizedOrgsDescArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 asset_type: Optional[pulumi.Input[str]] = None,
                 authorization_direction: Optional[pulumi.Input[str]] = None,
                 authorization_type: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 orgs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 parent: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AuthorizedOrgsDescArgs.__new__(AuthorizedOrgsDescArgs)

            __props__.__dict__["asset_type"] = asset_type
            __props__.__dict__["authorization_direction"] = authorization_direction
            __props__.__dict__["authorization_type"] = authorization_type
            __props__.__dict__["name"] = name
            __props__.__dict__["orgs"] = orgs
            if parent is None and not opts.urn:
                raise TypeError("Missing required property 'parent'")
            __props__.__dict__["parent"] = parent
            __props__.__dict__["create_time"] = None
            __props__.__dict__["update_time"] = None
        super(AuthorizedOrgsDesc, __self__).__init__(
            'gcp:accesscontextmanager/authorizedOrgsDesc:AuthorizedOrgsDesc',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            asset_type: Optional[pulumi.Input[str]] = None,
            authorization_direction: Optional[pulumi.Input[str]] = None,
            authorization_type: Optional[pulumi.Input[str]] = None,
            create_time: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            orgs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            parent: Optional[pulumi.Input[str]] = None,
            update_time: Optional[pulumi.Input[str]] = None) -> 'AuthorizedOrgsDesc':
        """
        Get an existing AuthorizedOrgsDesc resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] asset_type: The type of entities that need to use the authorization relationship during
               evaluation, such as a device. Valid values are "ASSET_TYPE_DEVICE" and
               "ASSET_TYPE_CREDENTIAL_STRENGTH".
               Possible values are `ASSET_TYPE_DEVICE` and `ASSET_TYPE_CREDENTIAL_STRENGTH`.
        :param pulumi.Input[str] authorization_direction: The direction of the authorization relationship between this organization
               and the organizations listed in the "orgs" field. The valid values for this
               field include the following:
               AUTHORIZATION_DIRECTION_FROM: Allows this organization to evaluate traffic
               in the organizations listed in the `orgs` field.
               AUTHORIZATION_DIRECTION_TO: Allows the organizations listed in the `orgs`
               field to evaluate the traffic in this organization.
               For the authorization relationship to take effect, all of the organizations
               must authorize and specify the appropriate relationship direction. For
               example, if organization A authorized organization B and C to evaluate its
               traffic, by specifying "AUTHORIZATION_DIRECTION_TO" as the authorization
               direction, organizations B and C must specify
               "AUTHORIZATION_DIRECTION_FROM" as the authorization direction in their
               "AuthorizedOrgsDesc" resource.
               Possible values are `AUTHORIZATION_DIRECTION_TO` and `AUTHORIZATION_DIRECTION_FROM`.
        :param pulumi.Input[str] authorization_type: A granular control type for authorization levels. Valid value is "AUTHORIZATION_TYPE_TRUST".
               Possible values are `AUTHORIZATION_TYPE_TRUST`.
        :param pulumi.Input[str] create_time: Time the AuthorizedOrgsDesc was created in UTC.
        :param pulumi.Input[str] name: Resource name for the `AuthorizedOrgsDesc`. Format:
               `accessPolicies/{access_policy}/authorizedOrgsDescs/{authorized_orgs_desc}`.
               The `authorized_orgs_desc` component must begin with a letter, followed by
               alphanumeric characters or `_`.
               After you create an `AuthorizedOrgsDesc`, you cannot change its `name`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] orgs: The list of organization ids in this AuthorizedOrgsDesc.
               Format: `organizations/<org_number>`
               Example: `organizations/123456`
        :param pulumi.Input[str] parent: Required. Resource name for the access policy which owns this `AuthorizedOrgsDesc`.
        :param pulumi.Input[str] update_time: Time the AuthorizedOrgsDesc was updated in UTC.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AuthorizedOrgsDescState.__new__(_AuthorizedOrgsDescState)

        __props__.__dict__["asset_type"] = asset_type
        __props__.__dict__["authorization_direction"] = authorization_direction
        __props__.__dict__["authorization_type"] = authorization_type
        __props__.__dict__["create_time"] = create_time
        __props__.__dict__["name"] = name
        __props__.__dict__["orgs"] = orgs
        __props__.__dict__["parent"] = parent
        __props__.__dict__["update_time"] = update_time
        return AuthorizedOrgsDesc(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="assetType")
    def asset_type(self) -> pulumi.Output[Optional[str]]:
        """
        The type of entities that need to use the authorization relationship during
        evaluation, such as a device. Valid values are "ASSET_TYPE_DEVICE" and
        "ASSET_TYPE_CREDENTIAL_STRENGTH".
        Possible values are `ASSET_TYPE_DEVICE` and `ASSET_TYPE_CREDENTIAL_STRENGTH`.
        """
        return pulumi.get(self, "asset_type")

    @property
    @pulumi.getter(name="authorizationDirection")
    def authorization_direction(self) -> pulumi.Output[Optional[str]]:
        """
        The direction of the authorization relationship between this organization
        and the organizations listed in the "orgs" field. The valid values for this
        field include the following:
        AUTHORIZATION_DIRECTION_FROM: Allows this organization to evaluate traffic
        in the organizations listed in the `orgs` field.
        AUTHORIZATION_DIRECTION_TO: Allows the organizations listed in the `orgs`
        field to evaluate the traffic in this organization.
        For the authorization relationship to take effect, all of the organizations
        must authorize and specify the appropriate relationship direction. For
        example, if organization A authorized organization B and C to evaluate its
        traffic, by specifying "AUTHORIZATION_DIRECTION_TO" as the authorization
        direction, organizations B and C must specify
        "AUTHORIZATION_DIRECTION_FROM" as the authorization direction in their
        "AuthorizedOrgsDesc" resource.
        Possible values are `AUTHORIZATION_DIRECTION_TO` and `AUTHORIZATION_DIRECTION_FROM`.
        """
        return pulumi.get(self, "authorization_direction")

    @property
    @pulumi.getter(name="authorizationType")
    def authorization_type(self) -> pulumi.Output[Optional[str]]:
        """
        A granular control type for authorization levels. Valid value is "AUTHORIZATION_TYPE_TRUST".
        Possible values are `AUTHORIZATION_TYPE_TRUST`.
        """
        return pulumi.get(self, "authorization_type")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        Time the AuthorizedOrgsDesc was created in UTC.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name for the `AuthorizedOrgsDesc`. Format:
        `accessPolicies/{access_policy}/authorizedOrgsDescs/{authorized_orgs_desc}`.
        The `authorized_orgs_desc` component must begin with a letter, followed by
        alphanumeric characters or `_`.
        After you create an `AuthorizedOrgsDesc`, you cannot change its `name`.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def orgs(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The list of organization ids in this AuthorizedOrgsDesc.
        Format: `organizations/<org_number>`
        Example: `organizations/123456`
        """
        return pulumi.get(self, "orgs")

    @property
    @pulumi.getter
    def parent(self) -> pulumi.Output[str]:
        """
        Required. Resource name for the access policy which owns this `AuthorizedOrgsDesc`.
        """
        return pulumi.get(self, "parent")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        Time the AuthorizedOrgsDesc was updated in UTC.
        """
        return pulumi.get(self, "update_time")

