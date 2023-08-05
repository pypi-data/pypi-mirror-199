# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ProjectArgs', 'Project']

@pulumi.input_type
class ProjectArgs:
    def __init__(__self__, *,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Project resource.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        if project is not None:
            pulumi.set(__self__, "project", project)

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


@pulumi.input_type
class _ProjectState:
    def __init__(__self__, *,
                 display_name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 project_number: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Project resources.
        :param pulumi.Input[str] display_name: The GCP project display name
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] project_number: The number of the google project that firebase is enabled on.
        """
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if project_number is not None:
            pulumi.set(__self__, "project_number", project_number)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        The GCP project display name
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

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
    @pulumi.getter(name="projectNumber")
    def project_number(self) -> Optional[pulumi.Input[str]]:
        """
        The number of the google project that firebase is enabled on.
        """
        return pulumi.get(self, "project_number")

    @project_number.setter
    def project_number(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project_number", value)


class Project(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A Google Cloud Firebase instance. This enables Firebase resources on a given google project.
        Since a FirebaseProject is actually also a GCP Project, a FirebaseProject uses underlying GCP
        identifiers (most importantly, the projectId) as its own for easy interop with GCP APIs.
        Once Firebase has been added to a Google Project it cannot be removed.

        To get more information about Project, see:

        * [API documentation](https://firebase.google.com/docs/reference/firebase-management/rest/v1beta1/projects)
        * How-to Guides
            * [Official Documentation](https://firebase.google.com/)

        ## Example Usage
        ### Firebase Project Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        default_project = gcp.organizations.Project("defaultProject",
            project_id="tf-test",
            org_id="123456789",
            labels={
                "firebase": "enabled",
            },
            opts=pulumi.ResourceOptions(provider=google_beta))
        default_firebase_project_project = gcp.firebase.Project("defaultFirebase/projectProject", project=default_project.project_id,
        opts=pulumi.ResourceOptions(provider=google_beta))
        ```

        ## Import

        Project can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:firebase/project:Project default projects/{{project}}
        ```

        ```sh
         $ pulumi import gcp:firebase/project:Project default {{project}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ProjectArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A Google Cloud Firebase instance. This enables Firebase resources on a given google project.
        Since a FirebaseProject is actually also a GCP Project, a FirebaseProject uses underlying GCP
        identifiers (most importantly, the projectId) as its own for easy interop with GCP APIs.
        Once Firebase has been added to a Google Project it cannot be removed.

        To get more information about Project, see:

        * [API documentation](https://firebase.google.com/docs/reference/firebase-management/rest/v1beta1/projects)
        * How-to Guides
            * [Official Documentation](https://firebase.google.com/)

        ## Example Usage
        ### Firebase Project Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        default_project = gcp.organizations.Project("defaultProject",
            project_id="tf-test",
            org_id="123456789",
            labels={
                "firebase": "enabled",
            },
            opts=pulumi.ResourceOptions(provider=google_beta))
        default_firebase_project_project = gcp.firebase.Project("defaultFirebase/projectProject", project=default_project.project_id,
        opts=pulumi.ResourceOptions(provider=google_beta))
        ```

        ## Import

        Project can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:firebase/project:Project default projects/{{project}}
        ```

        ```sh
         $ pulumi import gcp:firebase/project:Project default {{project}}
        ```

        :param str resource_name: The name of the resource.
        :param ProjectArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ProjectArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ProjectArgs.__new__(ProjectArgs)

            __props__.__dict__["project"] = project
            __props__.__dict__["display_name"] = None
            __props__.__dict__["project_number"] = None
        super(Project, __self__).__init__(
            'gcp:firebase/project:Project',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            display_name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            project_number: Optional[pulumi.Input[str]] = None) -> 'Project':
        """
        Get an existing Project resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] display_name: The GCP project display name
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] project_number: The number of the google project that firebase is enabled on.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ProjectState.__new__(_ProjectState)

        __props__.__dict__["display_name"] = display_name
        __props__.__dict__["project"] = project
        __props__.__dict__["project_number"] = project_number
        return Project(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        The GCP project display name
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="projectNumber")
    def project_number(self) -> pulumi.Output[str]:
        """
        The number of the google project that firebase is enabled on.
        """
        return pulumi.get(self, "project_number")

