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
    'GetFolderResult',
    'AwaitableGetFolderResult',
    'get_folder',
    'get_folder_output',
]

@pulumi.output_type
class GetFolderResult:
    """
    A collection of values returned by getFolder.
    """
    def __init__(__self__, create_time=None, display_name=None, folder=None, folder_id=None, id=None, lifecycle_state=None, lookup_organization=None, name=None, organization=None, parent=None):
        if create_time and not isinstance(create_time, str):
            raise TypeError("Expected argument 'create_time' to be a str")
        pulumi.set(__self__, "create_time", create_time)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if folder and not isinstance(folder, str):
            raise TypeError("Expected argument 'folder' to be a str")
        pulumi.set(__self__, "folder", folder)
        if folder_id and not isinstance(folder_id, str):
            raise TypeError("Expected argument 'folder_id' to be a str")
        pulumi.set(__self__, "folder_id", folder_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if lifecycle_state and not isinstance(lifecycle_state, str):
            raise TypeError("Expected argument 'lifecycle_state' to be a str")
        pulumi.set(__self__, "lifecycle_state", lifecycle_state)
        if lookup_organization and not isinstance(lookup_organization, bool):
            raise TypeError("Expected argument 'lookup_organization' to be a bool")
        pulumi.set(__self__, "lookup_organization", lookup_organization)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if organization and not isinstance(organization, str):
            raise TypeError("Expected argument 'organization' to be a str")
        pulumi.set(__self__, "organization", organization)
        if parent and not isinstance(parent, str):
            raise TypeError("Expected argument 'parent' to be a str")
        pulumi.set(__self__, "parent", parent)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> str:
        """
        Timestamp when the Organization was created. A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z".
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        The folder's display name.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def folder(self) -> str:
        return pulumi.get(self, "folder")

    @property
    @pulumi.getter(name="folderId")
    def folder_id(self) -> str:
        return pulumi.get(self, "folder_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lifecycleState")
    def lifecycle_state(self) -> str:
        """
        The Folder's current lifecycle state.
        """
        return pulumi.get(self, "lifecycle_state")

    @property
    @pulumi.getter(name="lookupOrganization")
    def lookup_organization(self) -> Optional[bool]:
        return pulumi.get(self, "lookup_organization")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The resource name of the Folder in the form `folders/{folder_id}`.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def organization(self) -> str:
        """
        If `lookup_organization` is enable, the resource name of the Organization that the folder belongs.
        """
        return pulumi.get(self, "organization")

    @property
    @pulumi.getter
    def parent(self) -> str:
        """
        The resource name of the parent Folder or Organization.
        """
        return pulumi.get(self, "parent")


class AwaitableGetFolderResult(GetFolderResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFolderResult(
            create_time=self.create_time,
            display_name=self.display_name,
            folder=self.folder,
            folder_id=self.folder_id,
            id=self.id,
            lifecycle_state=self.lifecycle_state,
            lookup_organization=self.lookup_organization,
            name=self.name,
            organization=self.organization,
            parent=self.parent)


def get_folder(folder: Optional[str] = None,
               lookup_organization: Optional[bool] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFolderResult:
    """
    Use this data source to get information about a Google Cloud Folder.

    ```python
    import pulumi
    import pulumi_gcp as gcp

    my_folder1 = gcp.organizations.get_folder(folder="folders/12345",
        lookup_organization=True)
    my_folder2 = gcp.organizations.get_folder(folder="folders/23456")
    pulumi.export("myFolder1Organization", my_folder1.organization)
    pulumi.export("myFolder2Parent", my_folder2.parent)
    ```


    :param str folder: The name of the Folder in the form `{folder_id}` or `folders/{folder_id}`.
    :param bool lookup_organization: `true` to find the organization that the folder belongs, `false` to avoid the lookup. It searches up the tree. (defaults to `false`)
    """
    __args__ = dict()
    __args__['folder'] = folder
    __args__['lookupOrganization'] = lookup_organization
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:organizations/getFolder:getFolder', __args__, opts=opts, typ=GetFolderResult).value

    return AwaitableGetFolderResult(
        create_time=__ret__.create_time,
        display_name=__ret__.display_name,
        folder=__ret__.folder,
        folder_id=__ret__.folder_id,
        id=__ret__.id,
        lifecycle_state=__ret__.lifecycle_state,
        lookup_organization=__ret__.lookup_organization,
        name=__ret__.name,
        organization=__ret__.organization,
        parent=__ret__.parent)


@_utilities.lift_output_func(get_folder)
def get_folder_output(folder: Optional[pulumi.Input[str]] = None,
                      lookup_organization: Optional[pulumi.Input[Optional[bool]]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetFolderResult]:
    """
    Use this data source to get information about a Google Cloud Folder.

    ```python
    import pulumi
    import pulumi_gcp as gcp

    my_folder1 = gcp.organizations.get_folder(folder="folders/12345",
        lookup_organization=True)
    my_folder2 = gcp.organizations.get_folder(folder="folders/23456")
    pulumi.export("myFolder1Organization", my_folder1.organization)
    pulumi.export("myFolder2Parent", my_folder2.parent)
    ```


    :param str folder: The name of the Folder in the form `{folder_id}` or `folders/{folder_id}`.
    :param bool lookup_organization: `true` to find the organization that the folder belongs, `false` to avoid the lookup. It searches up the tree. (defaults to `false`)
    """
    ...
