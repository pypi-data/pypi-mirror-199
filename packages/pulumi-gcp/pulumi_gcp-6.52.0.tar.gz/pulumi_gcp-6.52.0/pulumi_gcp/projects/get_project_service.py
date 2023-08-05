# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetProjectServiceResult',
    'AwaitableGetProjectServiceResult',
    'get_project_service',
    'get_project_service_output',
]

@pulumi.output_type
class GetProjectServiceResult:
    """
    A collection of values returned by getProjectService.
    """
    def __init__(__self__, disable_dependent_services=None, disable_on_destroy=None, id=None, project=None, service=None):
        if disable_dependent_services and not isinstance(disable_dependent_services, bool):
            raise TypeError("Expected argument 'disable_dependent_services' to be a bool")
        pulumi.set(__self__, "disable_dependent_services", disable_dependent_services)
        if disable_on_destroy and not isinstance(disable_on_destroy, bool):
            raise TypeError("Expected argument 'disable_on_destroy' to be a bool")
        pulumi.set(__self__, "disable_on_destroy", disable_on_destroy)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)
        if service and not isinstance(service, str):
            raise TypeError("Expected argument 'service' to be a str")
        pulumi.set(__self__, "service", service)

    @property
    @pulumi.getter(name="disableDependentServices")
    def disable_dependent_services(self) -> bool:
        return pulumi.get(self, "disable_dependent_services")

    @property
    @pulumi.getter(name="disableOnDestroy")
    def disable_on_destroy(self) -> bool:
        return pulumi.get(self, "disable_on_destroy")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def project(self) -> Optional[str]:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def service(self) -> str:
        return pulumi.get(self, "service")


class AwaitableGetProjectServiceResult(GetProjectServiceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetProjectServiceResult(
            disable_dependent_services=self.disable_dependent_services,
            disable_on_destroy=self.disable_on_destroy,
            id=self.id,
            project=self.project,
            service=self.service)


def get_project_service(project: Optional[str] = None,
                        service: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetProjectServiceResult:
    """
    Verify the API service for the Google Cloud Platform project to see if it is enabled or not.

    For a list of services available, visit the [API library page](https://console.cloud.google.com/apis/library)
    or run `gcloud services list --available`.

    This datasource requires the [Service Usage API](https://console.cloud.google.com/apis/library/serviceusage.googleapis.com)
    to use.

    To get more information about `projects.Service`, see:

    * [API documentation](https://cloud.google.com/service-usage/docs/reference/rest/v1/services)
    * How-to Guides
        * [Enabling and Disabling Services](https://cloud.google.com/service-usage/docs/enable-disable)

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    my_project_service = gcp.projects.get_project_service(service="my-project-service")
    ```


    :param str project: The project in which the resource belongs. If it
           is not provided, the provider project is used.
    :param str service: The name of the Google Platform project service.
    """
    __args__ = dict()
    __args__['project'] = project
    __args__['service'] = service
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:projects/getProjectService:getProjectService', __args__, opts=opts, typ=GetProjectServiceResult).value

    return AwaitableGetProjectServiceResult(
        disable_dependent_services=__ret__.disable_dependent_services,
        disable_on_destroy=__ret__.disable_on_destroy,
        id=__ret__.id,
        project=__ret__.project,
        service=__ret__.service)


@_utilities.lift_output_func(get_project_service)
def get_project_service_output(project: Optional[pulumi.Input[Optional[str]]] = None,
                               service: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetProjectServiceResult]:
    """
    Verify the API service for the Google Cloud Platform project to see if it is enabled or not.

    For a list of services available, visit the [API library page](https://console.cloud.google.com/apis/library)
    or run `gcloud services list --available`.

    This datasource requires the [Service Usage API](https://console.cloud.google.com/apis/library/serviceusage.googleapis.com)
    to use.

    To get more information about `projects.Service`, see:

    * [API documentation](https://cloud.google.com/service-usage/docs/reference/rest/v1/services)
    * How-to Guides
        * [Enabling and Disabling Services](https://cloud.google.com/service-usage/docs/enable-disable)

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    my_project_service = gcp.projects.get_project_service(service="my-project-service")
    ```


    :param str project: The project in which the resource belongs. If it
           is not provided, the provider project is used.
    :param str service: The name of the Google Platform project service.
    """
    ...
