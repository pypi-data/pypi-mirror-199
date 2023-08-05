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

__all__ = [
    'GetCaCertsResult',
    'AwaitableGetCaCertsResult',
    'get_ca_certs',
    'get_ca_certs_output',
]

@pulumi.output_type
class GetCaCertsResult:
    """
    A collection of values returned by getCaCerts.
    """
    def __init__(__self__, active_version=None, certs=None, id=None, instance=None, project=None):
        if active_version and not isinstance(active_version, str):
            raise TypeError("Expected argument 'active_version' to be a str")
        pulumi.set(__self__, "active_version", active_version)
        if certs and not isinstance(certs, list):
            raise TypeError("Expected argument 'certs' to be a list")
        pulumi.set(__self__, "certs", certs)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if instance and not isinstance(instance, str):
            raise TypeError("Expected argument 'instance' to be a str")
        pulumi.set(__self__, "instance", instance)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter(name="activeVersion")
    def active_version(self) -> str:
        """
        SHA1 fingerprint of the currently active CA certificate.
        """
        return pulumi.get(self, "active_version")

    @property
    @pulumi.getter
    def certs(self) -> Sequence['outputs.GetCaCertsCertResult']:
        """
        A list of server CA certificates for the instance. Each contains:
        """
        return pulumi.get(self, "certs")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def instance(self) -> str:
        return pulumi.get(self, "instance")

    @property
    @pulumi.getter
    def project(self) -> str:
        return pulumi.get(self, "project")


class AwaitableGetCaCertsResult(GetCaCertsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCaCertsResult(
            active_version=self.active_version,
            certs=self.certs,
            id=self.id,
            instance=self.instance,
            project=self.project)


def get_ca_certs(instance: Optional[str] = None,
                 project: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCaCertsResult:
    """
    Get all of the trusted Certificate Authorities (CAs) for the specified SQL database instance. For more information see the
    [official documentation](https://cloud.google.com/sql/)
    and
    [API](https://cloud.google.com/sql/docs/mysql/admin-api/rest/v1beta4/instances/listServerCas).


    :param str instance: The name or self link of the instance.
    :param str project: The ID of the project in which the resource belongs. If `project` is not provided, the provider project is used.
    """
    __args__ = dict()
    __args__['instance'] = instance
    __args__['project'] = project
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:sql/getCaCerts:getCaCerts', __args__, opts=opts, typ=GetCaCertsResult).value

    return AwaitableGetCaCertsResult(
        active_version=__ret__.active_version,
        certs=__ret__.certs,
        id=__ret__.id,
        instance=__ret__.instance,
        project=__ret__.project)


@_utilities.lift_output_func(get_ca_certs)
def get_ca_certs_output(instance: Optional[pulumi.Input[str]] = None,
                        project: Optional[pulumi.Input[Optional[str]]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCaCertsResult]:
    """
    Get all of the trusted Certificate Authorities (CAs) for the specified SQL database instance. For more information see the
    [official documentation](https://cloud.google.com/sql/)
    and
    [API](https://cloud.google.com/sql/docs/mysql/admin-api/rest/v1beta4/instances/listServerCas).


    :param str instance: The name or self link of the instance.
    :param str project: The ID of the project in which the resource belongs. If `project` is not provided, the provider project is used.
    """
    ...
