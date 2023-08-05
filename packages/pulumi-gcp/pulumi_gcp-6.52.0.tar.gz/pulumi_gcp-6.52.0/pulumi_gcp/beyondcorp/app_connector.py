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

__all__ = ['AppConnectorArgs', 'AppConnector']

@pulumi.input_type
class AppConnectorArgs:
    def __init__(__self__, *,
                 principal_info: pulumi.Input['AppConnectorPrincipalInfoArgs'],
                 display_name: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AppConnector resource.
        :param pulumi.Input['AppConnectorPrincipalInfoArgs'] principal_info: Principal information about the Identity of the AppConnector.
               Structure is documented below.
        :param pulumi.Input[str] display_name: An arbitrary user-provided name for the AppConnector.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Resource labels to represent user provided metadata.
        :param pulumi.Input[str] name: ID of the AppConnector.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The region of the AppConnector.
        """
        pulumi.set(__self__, "principal_info", principal_info)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if region is not None:
            pulumi.set(__self__, "region", region)

    @property
    @pulumi.getter(name="principalInfo")
    def principal_info(self) -> pulumi.Input['AppConnectorPrincipalInfoArgs']:
        """
        Principal information about the Identity of the AppConnector.
        Structure is documented below.
        """
        return pulumi.get(self, "principal_info")

    @principal_info.setter
    def principal_info(self, value: pulumi.Input['AppConnectorPrincipalInfoArgs']):
        pulumi.set(self, "principal_info", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        An arbitrary user-provided name for the AppConnector.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource labels to represent user provided metadata.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        ID of the AppConnector.
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
        The region of the AppConnector.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)


@pulumi.input_type
class _AppConnectorState:
    def __init__(__self__, *,
                 display_name: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 principal_info: Optional[pulumi.Input['AppConnectorPrincipalInfoArgs']] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AppConnector resources.
        :param pulumi.Input[str] display_name: An arbitrary user-provided name for the AppConnector.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Resource labels to represent user provided metadata.
        :param pulumi.Input[str] name: ID of the AppConnector.
        :param pulumi.Input['AppConnectorPrincipalInfoArgs'] principal_info: Principal information about the Identity of the AppConnector.
               Structure is documented below.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The region of the AppConnector.
        :param pulumi.Input[str] state: Represents the different states of a AppConnector.
        """
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if principal_info is not None:
            pulumi.set(__self__, "principal_info", principal_info)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if state is not None:
            pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        An arbitrary user-provided name for the AppConnector.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource labels to represent user provided metadata.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        ID of the AppConnector.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="principalInfo")
    def principal_info(self) -> Optional[pulumi.Input['AppConnectorPrincipalInfoArgs']]:
        """
        Principal information about the Identity of the AppConnector.
        Structure is documented below.
        """
        return pulumi.get(self, "principal_info")

    @principal_info.setter
    def principal_info(self, value: Optional[pulumi.Input['AppConnectorPrincipalInfoArgs']]):
        pulumi.set(self, "principal_info", value)

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
        The region of the AppConnector.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        """
        Represents the different states of a AppConnector.
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state", value)


class AppConnector(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 principal_info: Optional[pulumi.Input[pulumi.InputType['AppConnectorPrincipalInfoArgs']]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A BeyondCorp AppConnector resource represents an application facing component deployed proximal to
        and with direct access to the application instances. It is used to establish connectivity between the
        remote enterprise environment and GCP. It initiates connections to the applications and can proxy the
        data from users over the connection.

        To get more information about AppConnector, see:

        * [API documentation](https://cloud.google.com/beyondcorp/docs/reference/rest#rest-resource:-v1.projects.locations.appconnectors)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/beyondcorp-enterprise/docs/enable-app-connector)

        ## Example Usage
        ### Beyondcorp App Connector Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        service_account = gcp.service_account.Account("serviceAccount",
            account_id="my-account",
            display_name="Test Service Account")
        app_connector = gcp.beyondcorp.AppConnector("appConnector", principal_info=gcp.beyondcorp.AppConnectorPrincipalInfoArgs(
            service_account=gcp.beyondcorp.AppConnectorPrincipalInfoServiceAccountArgs(
                email=service_account.email,
            ),
        ))
        ```
        ### Beyondcorp App Connector Full

        ```python
        import pulumi
        import pulumi_gcp as gcp

        service_account = gcp.service_account.Account("serviceAccount",
            account_id="my-account",
            display_name="Test Service Account")
        app_connector = gcp.beyondcorp.AppConnector("appConnector",
            region="us-central1",
            display_name="some display name",
            principal_info=gcp.beyondcorp.AppConnectorPrincipalInfoArgs(
                service_account=gcp.beyondcorp.AppConnectorPrincipalInfoServiceAccountArgs(
                    email=service_account.email,
                ),
            ),
            labels={
                "foo": "bar",
                "bar": "baz",
            })
        ```

        ## Import

        AppConnector can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:beyondcorp/appConnector:AppConnector default projects/{{project}}/locations/{{region}}/appConnectors/{{name}}
        ```

        ```sh
         $ pulumi import gcp:beyondcorp/appConnector:AppConnector default {{project}}/{{region}}/{{name}}
        ```

        ```sh
         $ pulumi import gcp:beyondcorp/appConnector:AppConnector default {{region}}/{{name}}
        ```

        ```sh
         $ pulumi import gcp:beyondcorp/appConnector:AppConnector default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] display_name: An arbitrary user-provided name for the AppConnector.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Resource labels to represent user provided metadata.
        :param pulumi.Input[str] name: ID of the AppConnector.
        :param pulumi.Input[pulumi.InputType['AppConnectorPrincipalInfoArgs']] principal_info: Principal information about the Identity of the AppConnector.
               Structure is documented below.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The region of the AppConnector.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AppConnectorArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A BeyondCorp AppConnector resource represents an application facing component deployed proximal to
        and with direct access to the application instances. It is used to establish connectivity between the
        remote enterprise environment and GCP. It initiates connections to the applications and can proxy the
        data from users over the connection.

        To get more information about AppConnector, see:

        * [API documentation](https://cloud.google.com/beyondcorp/docs/reference/rest#rest-resource:-v1.projects.locations.appconnectors)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/beyondcorp-enterprise/docs/enable-app-connector)

        ## Example Usage
        ### Beyondcorp App Connector Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        service_account = gcp.service_account.Account("serviceAccount",
            account_id="my-account",
            display_name="Test Service Account")
        app_connector = gcp.beyondcorp.AppConnector("appConnector", principal_info=gcp.beyondcorp.AppConnectorPrincipalInfoArgs(
            service_account=gcp.beyondcorp.AppConnectorPrincipalInfoServiceAccountArgs(
                email=service_account.email,
            ),
        ))
        ```
        ### Beyondcorp App Connector Full

        ```python
        import pulumi
        import pulumi_gcp as gcp

        service_account = gcp.service_account.Account("serviceAccount",
            account_id="my-account",
            display_name="Test Service Account")
        app_connector = gcp.beyondcorp.AppConnector("appConnector",
            region="us-central1",
            display_name="some display name",
            principal_info=gcp.beyondcorp.AppConnectorPrincipalInfoArgs(
                service_account=gcp.beyondcorp.AppConnectorPrincipalInfoServiceAccountArgs(
                    email=service_account.email,
                ),
            ),
            labels={
                "foo": "bar",
                "bar": "baz",
            })
        ```

        ## Import

        AppConnector can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:beyondcorp/appConnector:AppConnector default projects/{{project}}/locations/{{region}}/appConnectors/{{name}}
        ```

        ```sh
         $ pulumi import gcp:beyondcorp/appConnector:AppConnector default {{project}}/{{region}}/{{name}}
        ```

        ```sh
         $ pulumi import gcp:beyondcorp/appConnector:AppConnector default {{region}}/{{name}}
        ```

        ```sh
         $ pulumi import gcp:beyondcorp/appConnector:AppConnector default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param AppConnectorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AppConnectorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 principal_info: Optional[pulumi.Input[pulumi.InputType['AppConnectorPrincipalInfoArgs']]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AppConnectorArgs.__new__(AppConnectorArgs)

            __props__.__dict__["display_name"] = display_name
            __props__.__dict__["labels"] = labels
            __props__.__dict__["name"] = name
            if principal_info is None and not opts.urn:
                raise TypeError("Missing required property 'principal_info'")
            __props__.__dict__["principal_info"] = principal_info
            __props__.__dict__["project"] = project
            __props__.__dict__["region"] = region
            __props__.__dict__["state"] = None
        super(AppConnector, __self__).__init__(
            'gcp:beyondcorp/appConnector:AppConnector',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            display_name: Optional[pulumi.Input[str]] = None,
            labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            principal_info: Optional[pulumi.Input[pulumi.InputType['AppConnectorPrincipalInfoArgs']]] = None,
            project: Optional[pulumi.Input[str]] = None,
            region: Optional[pulumi.Input[str]] = None,
            state: Optional[pulumi.Input[str]] = None) -> 'AppConnector':
        """
        Get an existing AppConnector resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] display_name: An arbitrary user-provided name for the AppConnector.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Resource labels to represent user provided metadata.
        :param pulumi.Input[str] name: ID of the AppConnector.
        :param pulumi.Input[pulumi.InputType['AppConnectorPrincipalInfoArgs']] principal_info: Principal information about the Identity of the AppConnector.
               Structure is documented below.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The region of the AppConnector.
        :param pulumi.Input[str] state: Represents the different states of a AppConnector.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AppConnectorState.__new__(_AppConnectorState)

        __props__.__dict__["display_name"] = display_name
        __props__.__dict__["labels"] = labels
        __props__.__dict__["name"] = name
        __props__.__dict__["principal_info"] = principal_info
        __props__.__dict__["project"] = project
        __props__.__dict__["region"] = region
        __props__.__dict__["state"] = state
        return AppConnector(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[Optional[str]]:
        """
        An arbitrary user-provided name for the AppConnector.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource labels to represent user provided metadata.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        ID of the AppConnector.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="principalInfo")
    def principal_info(self) -> pulumi.Output['outputs.AppConnectorPrincipalInfo']:
        """
        Principal information about the Identity of the AppConnector.
        Structure is documented below.
        """
        return pulumi.get(self, "principal_info")

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
    def region(self) -> pulumi.Output[Optional[str]]:
        """
        The region of the AppConnector.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        Represents the different states of a AppConnector.
        """
        return pulumi.get(self, "state")

