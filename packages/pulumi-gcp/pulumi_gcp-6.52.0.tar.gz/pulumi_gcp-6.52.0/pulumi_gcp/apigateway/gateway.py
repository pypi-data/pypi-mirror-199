# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['GatewayArgs', 'Gateway']

@pulumi.input_type
class GatewayArgs:
    def __init__(__self__, *,
                 api_config: pulumi.Input[str],
                 gateway_id: pulumi.Input[str],
                 display_name: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Gateway resource.
        :param pulumi.Input[str] api_config: Resource name of the API Config for this Gateway. Format: projects/{project}/locations/global/apis/{api}/configs/{apiConfig}.
               When changing api configs please ensure the new config is a new resource and the lifecycle rule `create_before_destroy` is set.
        :param pulumi.Input[str] gateway_id: Identifier to assign to the Gateway. Must be unique within scope of the parent resource(project).
        :param pulumi.Input[str] display_name: A user-visible name for the API.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Resource labels to represent user-provided metadata.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The region of the gateway for the API.
        """
        pulumi.set(__self__, "api_config", api_config)
        pulumi.set(__self__, "gateway_id", gateway_id)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if region is not None:
            pulumi.set(__self__, "region", region)

    @property
    @pulumi.getter(name="apiConfig")
    def api_config(self) -> pulumi.Input[str]:
        """
        Resource name of the API Config for this Gateway. Format: projects/{project}/locations/global/apis/{api}/configs/{apiConfig}.
        When changing api configs please ensure the new config is a new resource and the lifecycle rule `create_before_destroy` is set.
        """
        return pulumi.get(self, "api_config")

    @api_config.setter
    def api_config(self, value: pulumi.Input[str]):
        pulumi.set(self, "api_config", value)

    @property
    @pulumi.getter(name="gatewayId")
    def gateway_id(self) -> pulumi.Input[str]:
        """
        Identifier to assign to the Gateway. Must be unique within scope of the parent resource(project).
        """
        return pulumi.get(self, "gateway_id")

    @gateway_id.setter
    def gateway_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "gateway_id", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        A user-visible name for the API.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource labels to represent user-provided metadata.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

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
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The region of the gateway for the API.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)


@pulumi.input_type
class _GatewayState:
    def __init__(__self__, *,
                 api_config: Optional[pulumi.Input[str]] = None,
                 default_hostname: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 gateway_id: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Gateway resources.
        :param pulumi.Input[str] api_config: Resource name of the API Config for this Gateway. Format: projects/{project}/locations/global/apis/{api}/configs/{apiConfig}.
               When changing api configs please ensure the new config is a new resource and the lifecycle rule `create_before_destroy` is set.
        :param pulumi.Input[str] default_hostname: The default API Gateway host name of the form {gatewayId}-{hash}.{region_code}.gateway.dev.
        :param pulumi.Input[str] display_name: A user-visible name for the API.
        :param pulumi.Input[str] gateway_id: Identifier to assign to the Gateway. Must be unique within scope of the parent resource(project).
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Resource labels to represent user-provided metadata.
        :param pulumi.Input[str] name: Resource name of the Gateway. Format: projects/{project}/locations/{region}/gateways/{gateway}
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The region of the gateway for the API.
        """
        if api_config is not None:
            pulumi.set(__self__, "api_config", api_config)
        if default_hostname is not None:
            pulumi.set(__self__, "default_hostname", default_hostname)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if gateway_id is not None:
            pulumi.set(__self__, "gateway_id", gateway_id)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if region is not None:
            pulumi.set(__self__, "region", region)

    @property
    @pulumi.getter(name="apiConfig")
    def api_config(self) -> Optional[pulumi.Input[str]]:
        """
        Resource name of the API Config for this Gateway. Format: projects/{project}/locations/global/apis/{api}/configs/{apiConfig}.
        When changing api configs please ensure the new config is a new resource and the lifecycle rule `create_before_destroy` is set.
        """
        return pulumi.get(self, "api_config")

    @api_config.setter
    def api_config(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "api_config", value)

    @property
    @pulumi.getter(name="defaultHostname")
    def default_hostname(self) -> Optional[pulumi.Input[str]]:
        """
        The default API Gateway host name of the form {gatewayId}-{hash}.{region_code}.gateway.dev.
        """
        return pulumi.get(self, "default_hostname")

    @default_hostname.setter
    def default_hostname(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_hostname", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        A user-visible name for the API.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="gatewayId")
    def gateway_id(self) -> Optional[pulumi.Input[str]]:
        """
        Identifier to assign to the Gateway. Must be unique within scope of the parent resource(project).
        """
        return pulumi.get(self, "gateway_id")

    @gateway_id.setter
    def gateway_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "gateway_id", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource labels to represent user-provided metadata.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Resource name of the Gateway. Format: projects/{project}/locations/{region}/gateways/{gateway}
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

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
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The region of the gateway for the API.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)


class Gateway(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_config: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 gateway_id: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A consumable API that can be used by multiple Gateways.

        To get more information about Gateway, see:

        * [API documentation](https://cloud.google.com/api-gateway/docs/reference/rest/v1beta/projects.locations.apis)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/api-gateway/docs/quickstart)

        ## Example Usage
        ### Apigateway Gateway Basic

        ```python
        import pulumi
        import base64
        import pulumi_gcp as gcp

        api_gw_api = gcp.apigateway.Api("apiGwApi", api_id="api-gw",
        opts=pulumi.ResourceOptions(provider=google_beta))
        api_gw_api_config = gcp.apigateway.ApiConfig("apiGwApiConfig",
            api=api_gw_api.api_id,
            api_config_id="config",
            openapi_documents=[gcp.apigateway.ApiConfigOpenapiDocumentArgs(
                document=gcp.apigateway.ApiConfigOpenapiDocumentDocumentArgs(
                    path="spec.yaml",
                    contents=(lambda path: base64.b64encode(open(path).read().encode()).decode())("test-fixtures/apigateway/openapi.yaml"),
                ),
            )],
            opts=pulumi.ResourceOptions(provider=google_beta))
        api_gw_gateway = gcp.apigateway.Gateway("apiGwGateway",
            api_config=api_gw_api_config.id,
            gateway_id="api-gw",
            opts=pulumi.ResourceOptions(provider=google_beta))
        ```

        ## Import

        Gateway can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:apigateway/gateway:Gateway default projects/{{project}}/locations/{{region}}/gateways/{{gateway_id}}
        ```

        ```sh
         $ pulumi import gcp:apigateway/gateway:Gateway default {{project}}/{{region}}/{{gateway_id}}
        ```

        ```sh
         $ pulumi import gcp:apigateway/gateway:Gateway default {{region}}/{{gateway_id}}
        ```

        ```sh
         $ pulumi import gcp:apigateway/gateway:Gateway default {{gateway_id}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_config: Resource name of the API Config for this Gateway. Format: projects/{project}/locations/global/apis/{api}/configs/{apiConfig}.
               When changing api configs please ensure the new config is a new resource and the lifecycle rule `create_before_destroy` is set.
        :param pulumi.Input[str] display_name: A user-visible name for the API.
        :param pulumi.Input[str] gateway_id: Identifier to assign to the Gateway. Must be unique within scope of the parent resource(project).
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Resource labels to represent user-provided metadata.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The region of the gateway for the API.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: GatewayArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A consumable API that can be used by multiple Gateways.

        To get more information about Gateway, see:

        * [API documentation](https://cloud.google.com/api-gateway/docs/reference/rest/v1beta/projects.locations.apis)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/api-gateway/docs/quickstart)

        ## Example Usage
        ### Apigateway Gateway Basic

        ```python
        import pulumi
        import base64
        import pulumi_gcp as gcp

        api_gw_api = gcp.apigateway.Api("apiGwApi", api_id="api-gw",
        opts=pulumi.ResourceOptions(provider=google_beta))
        api_gw_api_config = gcp.apigateway.ApiConfig("apiGwApiConfig",
            api=api_gw_api.api_id,
            api_config_id="config",
            openapi_documents=[gcp.apigateway.ApiConfigOpenapiDocumentArgs(
                document=gcp.apigateway.ApiConfigOpenapiDocumentDocumentArgs(
                    path="spec.yaml",
                    contents=(lambda path: base64.b64encode(open(path).read().encode()).decode())("test-fixtures/apigateway/openapi.yaml"),
                ),
            )],
            opts=pulumi.ResourceOptions(provider=google_beta))
        api_gw_gateway = gcp.apigateway.Gateway("apiGwGateway",
            api_config=api_gw_api_config.id,
            gateway_id="api-gw",
            opts=pulumi.ResourceOptions(provider=google_beta))
        ```

        ## Import

        Gateway can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:apigateway/gateway:Gateway default projects/{{project}}/locations/{{region}}/gateways/{{gateway_id}}
        ```

        ```sh
         $ pulumi import gcp:apigateway/gateway:Gateway default {{project}}/{{region}}/{{gateway_id}}
        ```

        ```sh
         $ pulumi import gcp:apigateway/gateway:Gateway default {{region}}/{{gateway_id}}
        ```

        ```sh
         $ pulumi import gcp:apigateway/gateway:Gateway default {{gateway_id}}
        ```

        :param str resource_name: The name of the resource.
        :param GatewayArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(GatewayArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_config: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 gateway_id: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = GatewayArgs.__new__(GatewayArgs)

            if api_config is None and not opts.urn:
                raise TypeError("Missing required property 'api_config'")
            __props__.__dict__["api_config"] = api_config
            __props__.__dict__["display_name"] = display_name
            if gateway_id is None and not opts.urn:
                raise TypeError("Missing required property 'gateway_id'")
            __props__.__dict__["gateway_id"] = gateway_id
            __props__.__dict__["labels"] = labels
            __props__.__dict__["project"] = project
            __props__.__dict__["region"] = region
            __props__.__dict__["default_hostname"] = None
            __props__.__dict__["name"] = None
        super(Gateway, __self__).__init__(
            'gcp:apigateway/gateway:Gateway',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            api_config: Optional[pulumi.Input[str]] = None,
            default_hostname: Optional[pulumi.Input[str]] = None,
            display_name: Optional[pulumi.Input[str]] = None,
            gateway_id: Optional[pulumi.Input[str]] = None,
            labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            region: Optional[pulumi.Input[str]] = None) -> 'Gateway':
        """
        Get an existing Gateway resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_config: Resource name of the API Config for this Gateway. Format: projects/{project}/locations/global/apis/{api}/configs/{apiConfig}.
               When changing api configs please ensure the new config is a new resource and the lifecycle rule `create_before_destroy` is set.
        :param pulumi.Input[str] default_hostname: The default API Gateway host name of the form {gatewayId}-{hash}.{region_code}.gateway.dev.
        :param pulumi.Input[str] display_name: A user-visible name for the API.
        :param pulumi.Input[str] gateway_id: Identifier to assign to the Gateway. Must be unique within scope of the parent resource(project).
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Resource labels to represent user-provided metadata.
        :param pulumi.Input[str] name: Resource name of the Gateway. Format: projects/{project}/locations/{region}/gateways/{gateway}
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The region of the gateway for the API.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _GatewayState.__new__(_GatewayState)

        __props__.__dict__["api_config"] = api_config
        __props__.__dict__["default_hostname"] = default_hostname
        __props__.__dict__["display_name"] = display_name
        __props__.__dict__["gateway_id"] = gateway_id
        __props__.__dict__["labels"] = labels
        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        __props__.__dict__["region"] = region
        return Gateway(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="apiConfig")
    def api_config(self) -> pulumi.Output[str]:
        """
        Resource name of the API Config for this Gateway. Format: projects/{project}/locations/global/apis/{api}/configs/{apiConfig}.
        When changing api configs please ensure the new config is a new resource and the lifecycle rule `create_before_destroy` is set.
        """
        return pulumi.get(self, "api_config")

    @property
    @pulumi.getter(name="defaultHostname")
    def default_hostname(self) -> pulumi.Output[str]:
        """
        The default API Gateway host name of the form {gatewayId}-{hash}.{region_code}.gateway.dev.
        """
        return pulumi.get(self, "default_hostname")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        A user-visible name for the API.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="gatewayId")
    def gateway_id(self) -> pulumi.Output[str]:
        """
        Identifier to assign to the Gateway. Must be unique within scope of the parent resource(project).
        """
        return pulumi.get(self, "gateway_id")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource labels to represent user-provided metadata.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name of the Gateway. Format: projects/{project}/locations/{region}/gateways/{gateway}
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output[str]:
        """
        The region of the gateway for the API.
        """
        return pulumi.get(self, "region")

