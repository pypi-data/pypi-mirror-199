# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['EnvReferencesArgs', 'EnvReferences']

@pulumi.input_type
class EnvReferencesArgs:
    def __init__(__self__, *,
                 env_id: pulumi.Input[str],
                 refers: pulumi.Input[str],
                 resource_type: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a EnvReferences resource.
        :param pulumi.Input[str] env_id: The Apigee environment group associated with the Apigee environment,
               in the format `organizations/{{org_name}}/environments/{{env_name}}`.
        :param pulumi.Input[str] refers: Required. The id of the resource to which this reference refers. Must be the id of a resource that exists in the parent environment and is of the given resourceType.
        :param pulumi.Input[str] resource_type: The type of resource referred to by this reference. Valid values are 'KeyStore' or 'TrustStore'.
        :param pulumi.Input[str] description: Optional. A human-readable description of this reference.
        :param pulumi.Input[str] name: Required. The resource id of this reference. Values must match the regular expression [\\w\\s-.]+.
        """
        pulumi.set(__self__, "env_id", env_id)
        pulumi.set(__self__, "refers", refers)
        pulumi.set(__self__, "resource_type", resource_type)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="envId")
    def env_id(self) -> pulumi.Input[str]:
        """
        The Apigee environment group associated with the Apigee environment,
        in the format `organizations/{{org_name}}/environments/{{env_name}}`.
        """
        return pulumi.get(self, "env_id")

    @env_id.setter
    def env_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "env_id", value)

    @property
    @pulumi.getter
    def refers(self) -> pulumi.Input[str]:
        """
        Required. The id of the resource to which this reference refers. Must be the id of a resource that exists in the parent environment and is of the given resourceType.
        """
        return pulumi.get(self, "refers")

    @refers.setter
    def refers(self, value: pulumi.Input[str]):
        pulumi.set(self, "refers", value)

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> pulumi.Input[str]:
        """
        The type of resource referred to by this reference. Valid values are 'KeyStore' or 'TrustStore'.
        """
        return pulumi.get(self, "resource_type")

    @resource_type.setter
    def resource_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_type", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. A human-readable description of this reference.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Required. The resource id of this reference. Values must match the regular expression [\\w\\s-.]+.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _EnvReferencesState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 env_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 refers: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering EnvReferences resources.
        :param pulumi.Input[str] description: Optional. A human-readable description of this reference.
        :param pulumi.Input[str] env_id: The Apigee environment group associated with the Apigee environment,
               in the format `organizations/{{org_name}}/environments/{{env_name}}`.
        :param pulumi.Input[str] name: Required. The resource id of this reference. Values must match the regular expression [\\w\\s-.]+.
        :param pulumi.Input[str] refers: Required. The id of the resource to which this reference refers. Must be the id of a resource that exists in the parent environment and is of the given resourceType.
        :param pulumi.Input[str] resource_type: The type of resource referred to by this reference. Valid values are 'KeyStore' or 'TrustStore'.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if env_id is not None:
            pulumi.set(__self__, "env_id", env_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if refers is not None:
            pulumi.set(__self__, "refers", refers)
        if resource_type is not None:
            pulumi.set(__self__, "resource_type", resource_type)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. A human-readable description of this reference.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="envId")
    def env_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Apigee environment group associated with the Apigee environment,
        in the format `organizations/{{org_name}}/environments/{{env_name}}`.
        """
        return pulumi.get(self, "env_id")

    @env_id.setter
    def env_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "env_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Required. The resource id of this reference. Values must match the regular expression [\\w\\s-.]+.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def refers(self) -> Optional[pulumi.Input[str]]:
        """
        Required. The id of the resource to which this reference refers. Must be the id of a resource that exists in the parent environment and is of the given resourceType.
        """
        return pulumi.get(self, "refers")

    @refers.setter
    def refers(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "refers", value)

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of resource referred to by this reference. Valid values are 'KeyStore' or 'TrustStore'.
        """
        return pulumi.get(self, "resource_type")

    @resource_type.setter
    def resource_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_type", value)


class EnvReferences(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 env_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 refers: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        An `Environment Reference` in Apigee.

        To get more information about EnvReferences, see:

        * [API documentation](https://cloud.google.com/apigee/docs/reference/apis/apigee/rest/v1/organizations.environments.references/create)
        * How-to Guides
            * [Creating an environment](https://cloud.google.com/apigee/docs/api-platform/get-started/create-environment)

        ## Import

        EnvReferences can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:apigee/envReferences:EnvReferences default {{env_id}}/references/{{name}}
        ```

        ```sh
         $ pulumi import gcp:apigee/envReferences:EnvReferences default {{env_id}}/{{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Optional. A human-readable description of this reference.
        :param pulumi.Input[str] env_id: The Apigee environment group associated with the Apigee environment,
               in the format `organizations/{{org_name}}/environments/{{env_name}}`.
        :param pulumi.Input[str] name: Required. The resource id of this reference. Values must match the regular expression [\\w\\s-.]+.
        :param pulumi.Input[str] refers: Required. The id of the resource to which this reference refers. Must be the id of a resource that exists in the parent environment and is of the given resourceType.
        :param pulumi.Input[str] resource_type: The type of resource referred to by this reference. Valid values are 'KeyStore' or 'TrustStore'.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EnvReferencesArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An `Environment Reference` in Apigee.

        To get more information about EnvReferences, see:

        * [API documentation](https://cloud.google.com/apigee/docs/reference/apis/apigee/rest/v1/organizations.environments.references/create)
        * How-to Guides
            * [Creating an environment](https://cloud.google.com/apigee/docs/api-platform/get-started/create-environment)

        ## Import

        EnvReferences can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:apigee/envReferences:EnvReferences default {{env_id}}/references/{{name}}
        ```

        ```sh
         $ pulumi import gcp:apigee/envReferences:EnvReferences default {{env_id}}/{{name}}
        ```

        :param str resource_name: The name of the resource.
        :param EnvReferencesArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EnvReferencesArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 env_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 refers: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EnvReferencesArgs.__new__(EnvReferencesArgs)

            __props__.__dict__["description"] = description
            if env_id is None and not opts.urn:
                raise TypeError("Missing required property 'env_id'")
            __props__.__dict__["env_id"] = env_id
            __props__.__dict__["name"] = name
            if refers is None and not opts.urn:
                raise TypeError("Missing required property 'refers'")
            __props__.__dict__["refers"] = refers
            if resource_type is None and not opts.urn:
                raise TypeError("Missing required property 'resource_type'")
            __props__.__dict__["resource_type"] = resource_type
        super(EnvReferences, __self__).__init__(
            'gcp:apigee/envReferences:EnvReferences',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            env_id: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            refers: Optional[pulumi.Input[str]] = None,
            resource_type: Optional[pulumi.Input[str]] = None) -> 'EnvReferences':
        """
        Get an existing EnvReferences resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Optional. A human-readable description of this reference.
        :param pulumi.Input[str] env_id: The Apigee environment group associated with the Apigee environment,
               in the format `organizations/{{org_name}}/environments/{{env_name}}`.
        :param pulumi.Input[str] name: Required. The resource id of this reference. Values must match the regular expression [\\w\\s-.]+.
        :param pulumi.Input[str] refers: Required. The id of the resource to which this reference refers. Must be the id of a resource that exists in the parent environment and is of the given resourceType.
        :param pulumi.Input[str] resource_type: The type of resource referred to by this reference. Valid values are 'KeyStore' or 'TrustStore'.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EnvReferencesState.__new__(_EnvReferencesState)

        __props__.__dict__["description"] = description
        __props__.__dict__["env_id"] = env_id
        __props__.__dict__["name"] = name
        __props__.__dict__["refers"] = refers
        __props__.__dict__["resource_type"] = resource_type
        return EnvReferences(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Optional. A human-readable description of this reference.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="envId")
    def env_id(self) -> pulumi.Output[str]:
        """
        The Apigee environment group associated with the Apigee environment,
        in the format `organizations/{{org_name}}/environments/{{env_name}}`.
        """
        return pulumi.get(self, "env_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Required. The resource id of this reference. Values must match the regular expression [\\w\\s-.]+.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def refers(self) -> pulumi.Output[str]:
        """
        Required. The id of the resource to which this reference refers. Must be the id of a resource that exists in the parent environment and is of the given resourceType.
        """
        return pulumi.get(self, "refers")

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> pulumi.Output[str]:
        """
        The type of resource referred to by this reference. Valid values are 'KeyStore' or 'TrustStore'.
        """
        return pulumi.get(self, "resource_type")

