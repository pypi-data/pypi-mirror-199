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
    'GetSecretVersionResult',
    'AwaitableGetSecretVersionResult',
    'get_secret_version',
    'get_secret_version_output',
]

warnings.warn("""gcp.monitoring.getSecretVersion has been deprecated in favor of gcp.secretmanager.getSecretVersion""", DeprecationWarning)

@pulumi.output_type
class GetSecretVersionResult:
    """
    A collection of values returned by getSecretVersion.
    """
    def __init__(__self__, create_time=None, destroy_time=None, enabled=None, id=None, name=None, project=None, secret=None, secret_data=None, version=None):
        if create_time and not isinstance(create_time, str):
            raise TypeError("Expected argument 'create_time' to be a str")
        pulumi.set(__self__, "create_time", create_time)
        if destroy_time and not isinstance(destroy_time, str):
            raise TypeError("Expected argument 'destroy_time' to be a str")
        pulumi.set(__self__, "destroy_time", destroy_time)
        if enabled and not isinstance(enabled, bool):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, "enabled", enabled)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)
        if secret and not isinstance(secret, str):
            raise TypeError("Expected argument 'secret' to be a str")
        pulumi.set(__self__, "secret", secret)
        if secret_data and not isinstance(secret_data, str):
            raise TypeError("Expected argument 'secret_data' to be a str")
        pulumi.set(__self__, "secret_data", secret_data)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> str:
        """
        The time at which the Secret was created.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="destroyTime")
    def destroy_time(self) -> str:
        """
        The time at which the Secret was destroyed. Only present if state is DESTROYED.
        """
        return pulumi.get(self, "destroy_time")

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        """
        True if the current state of the SecretVersion is enabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The resource name of the SecretVersion. Format:
        `projects/{{project}}/secrets/{{secret_id}}/versions/{{version}}`
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def project(self) -> str:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def secret(self) -> str:
        return pulumi.get(self, "secret")

    @property
    @pulumi.getter(name="secretData")
    def secret_data(self) -> str:
        """
        The secret data. No larger than 64KiB.
        """
        return pulumi.get(self, "secret_data")

    @property
    @pulumi.getter
    def version(self) -> str:
        return pulumi.get(self, "version")


class AwaitableGetSecretVersionResult(GetSecretVersionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSecretVersionResult(
            create_time=self.create_time,
            destroy_time=self.destroy_time,
            enabled=self.enabled,
            id=self.id,
            name=self.name,
            project=self.project,
            secret=self.secret,
            secret_data=self.secret_data,
            version=self.version)


def get_secret_version(project: Optional[str] = None,
                       secret: Optional[str] = None,
                       version: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSecretVersionResult:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    basic = gcp.secretmanager.get_secret_version(secret="my-secret")
    ```


    :param str project: The project to get the secret version for. If it
           is not provided, the provider project is used.
    :param str secret: The secret to get the secret version for.
    :param str version: The version of the secret to get. If it
           is not provided, the latest version is retrieved.
    """
    pulumi.log.warn("""get_secret_version is deprecated: gcp.monitoring.getSecretVersion has been deprecated in favor of gcp.secretmanager.getSecretVersion""")
    __args__ = dict()
    __args__['project'] = project
    __args__['secret'] = secret
    __args__['version'] = version
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:monitoring/getSecretVersion:getSecretVersion', __args__, opts=opts, typ=GetSecretVersionResult).value

    return AwaitableGetSecretVersionResult(
        create_time=__ret__.create_time,
        destroy_time=__ret__.destroy_time,
        enabled=__ret__.enabled,
        id=__ret__.id,
        name=__ret__.name,
        project=__ret__.project,
        secret=__ret__.secret,
        secret_data=__ret__.secret_data,
        version=__ret__.version)


@_utilities.lift_output_func(get_secret_version)
def get_secret_version_output(project: Optional[pulumi.Input[Optional[str]]] = None,
                              secret: Optional[pulumi.Input[str]] = None,
                              version: Optional[pulumi.Input[Optional[str]]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSecretVersionResult]:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    basic = gcp.secretmanager.get_secret_version(secret="my-secret")
    ```


    :param str project: The project to get the secret version for. If it
           is not provided, the provider project is used.
    :param str secret: The secret to get the secret version for.
    :param str version: The version of the secret to get. If it
           is not provided, the latest version is retrieved.
    """
    pulumi.log.warn("""get_secret_version is deprecated: gcp.monitoring.getSecretVersion has been deprecated in favor of gcp.secretmanager.getSecretVersion""")
    ...
