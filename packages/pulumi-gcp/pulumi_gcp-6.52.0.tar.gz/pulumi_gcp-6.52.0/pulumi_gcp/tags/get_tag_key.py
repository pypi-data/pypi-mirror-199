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
    'GetTagKeyResult',
    'AwaitableGetTagKeyResult',
    'get_tag_key',
    'get_tag_key_output',
]

@pulumi.output_type
class GetTagKeyResult:
    """
    A collection of values returned by getTagKey.
    """
    def __init__(__self__, create_time=None, description=None, id=None, name=None, namespaced_name=None, parent=None, short_name=None, update_time=None):
        if create_time and not isinstance(create_time, str):
            raise TypeError("Expected argument 'create_time' to be a str")
        pulumi.set(__self__, "create_time", create_time)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if namespaced_name and not isinstance(namespaced_name, str):
            raise TypeError("Expected argument 'namespaced_name' to be a str")
        pulumi.set(__self__, "namespaced_name", namespaced_name)
        if parent and not isinstance(parent, str):
            raise TypeError("Expected argument 'parent' to be a str")
        pulumi.set(__self__, "parent", parent)
        if short_name and not isinstance(short_name, str):
            raise TypeError("Expected argument 'short_name' to be a str")
        pulumi.set(__self__, "short_name", short_name)
        if update_time and not isinstance(update_time, str):
            raise TypeError("Expected argument 'update_time' to be a str")
        pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> str:
        """
        Creation time.
        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def description(self) -> str:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        an identifier for the resource with format `tagKeys/{{name}}`
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The generated numeric id for the TagKey.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="namespacedName")
    def namespaced_name(self) -> str:
        """
        Namespaced name of the TagKey.
        """
        return pulumi.get(self, "namespaced_name")

    @property
    @pulumi.getter
    def parent(self) -> str:
        return pulumi.get(self, "parent")

    @property
    @pulumi.getter(name="shortName")
    def short_name(self) -> str:
        return pulumi.get(self, "short_name")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> str:
        """
        Update time.
        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        """
        return pulumi.get(self, "update_time")


class AwaitableGetTagKeyResult(GetTagKeyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTagKeyResult(
            create_time=self.create_time,
            description=self.description,
            id=self.id,
            name=self.name,
            namespaced_name=self.namespaced_name,
            parent=self.parent,
            short_name=self.short_name,
            update_time=self.update_time)


def get_tag_key(parent: Optional[str] = None,
                short_name: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTagKeyResult:
    """
    Get a tag key within a GCP org by `parent` and `short_name`.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    environment_tag_key = gcp.tags.get_tag_key(parent="organizations/12345",
        short_name="environment")
    ```


    :param str parent: The resource name of the parent organization in format `organizations/{org_id}`.
    :param str short_name: The tag key's short_name.
    """
    __args__ = dict()
    __args__['parent'] = parent
    __args__['shortName'] = short_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:tags/getTagKey:getTagKey', __args__, opts=opts, typ=GetTagKeyResult).value

    return AwaitableGetTagKeyResult(
        create_time=__ret__.create_time,
        description=__ret__.description,
        id=__ret__.id,
        name=__ret__.name,
        namespaced_name=__ret__.namespaced_name,
        parent=__ret__.parent,
        short_name=__ret__.short_name,
        update_time=__ret__.update_time)


@_utilities.lift_output_func(get_tag_key)
def get_tag_key_output(parent: Optional[pulumi.Input[str]] = None,
                       short_name: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTagKeyResult]:
    """
    Get a tag key within a GCP org by `parent` and `short_name`.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    environment_tag_key = gcp.tags.get_tag_key(parent="organizations/12345",
        short_name="environment")
    ```


    :param str parent: The resource name of the parent organization in format `organizations/{org_id}`.
    :param str short_name: The tag key's short_name.
    """
    ...
