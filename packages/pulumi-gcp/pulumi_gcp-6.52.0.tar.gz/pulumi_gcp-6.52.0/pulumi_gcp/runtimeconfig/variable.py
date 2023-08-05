# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['VariableArgs', 'Variable']

@pulumi.input_type
class VariableArgs:
    def __init__(__self__, *,
                 parent: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 text: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Variable resource.
        :param pulumi.Input[str] parent: The name of the RuntimeConfig resource containing this
               variable.
        :param pulumi.Input[str] name: The name of the variable to manage. Note that variable
               names can be hierarchical using slashes (e.g. "prod-variables/hostname").
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs. If it
               is not provided, the provider project is used.
        :param pulumi.Input[str] text: or `value` - (Required) The content to associate with the variable.
               Exactly one of `text` or `variable` must be specified. If `text` is specified,
               it must be a valid UTF-8 string and less than 4096 bytes in length. If `value`
               is specified, it must be base64 encoded and less than 4096 bytes in length.
        """
        pulumi.set(__self__, "parent", parent)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if text is not None:
            pulumi.set(__self__, "text", text)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def parent(self) -> pulumi.Input[str]:
        """
        The name of the RuntimeConfig resource containing this
        variable.
        """
        return pulumi.get(self, "parent")

    @parent.setter
    def parent(self, value: pulumi.Input[str]):
        pulumi.set(self, "parent", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the variable to manage. Note that variable
        names can be hierarchical using slashes (e.g. "prod-variables/hostname").
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs. If it
        is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter
    def text(self) -> Optional[pulumi.Input[str]]:
        """
        or `value` - (Required) The content to associate with the variable.
        Exactly one of `text` or `variable` must be specified. If `text` is specified,
        it must be a valid UTF-8 string and less than 4096 bytes in length. If `value`
        is specified, it must be base64 encoded and less than 4096 bytes in length.
        """
        return pulumi.get(self, "text")

    @text.setter
    def text(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "text", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class _VariableState:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 parent: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 text: Optional[pulumi.Input[str]] = None,
                 update_time: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Variable resources.
        :param pulumi.Input[str] name: The name of the variable to manage. Note that variable
               names can be hierarchical using slashes (e.g. "prod-variables/hostname").
        :param pulumi.Input[str] parent: The name of the RuntimeConfig resource containing this
               variable.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs. If it
               is not provided, the provider project is used.
        :param pulumi.Input[str] text: or `value` - (Required) The content to associate with the variable.
               Exactly one of `text` or `variable` must be specified. If `text` is specified,
               it must be a valid UTF-8 string and less than 4096 bytes in length. If `value`
               is specified, it must be base64 encoded and less than 4096 bytes in length.
        :param pulumi.Input[str] update_time: (Computed) The timestamp in RFC3339 UTC "Zulu" format,
               accurate to nanoseconds, representing when the variable was last updated.
               Example: "2016-10-09T12:33:37.578138407Z".
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if parent is not None:
            pulumi.set(__self__, "parent", parent)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if text is not None:
            pulumi.set(__self__, "text", text)
        if update_time is not None:
            pulumi.set(__self__, "update_time", update_time)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the variable to manage. Note that variable
        names can be hierarchical using slashes (e.g. "prod-variables/hostname").
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def parent(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the RuntimeConfig resource containing this
        variable.
        """
        return pulumi.get(self, "parent")

    @parent.setter
    def parent(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parent", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs. If it
        is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter
    def text(self) -> Optional[pulumi.Input[str]]:
        """
        or `value` - (Required) The content to associate with the variable.
        Exactly one of `text` or `variable` must be specified. If `text` is specified,
        it must be a valid UTF-8 string and less than 4096 bytes in length. If `value`
        is specified, it must be base64 encoded and less than 4096 bytes in length.
        """
        return pulumi.get(self, "text")

    @text.setter
    def text(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "text", value)

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> Optional[pulumi.Input[str]]:
        """
        (Computed) The timestamp in RFC3339 UTC "Zulu" format,
        accurate to nanoseconds, representing when the variable was last updated.
        Example: "2016-10-09T12:33:37.578138407Z".
        """
        return pulumi.get(self, "update_time")

    @update_time.setter
    def update_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "update_time", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


class Variable(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parent: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 text: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Example Usage

        Example creating a RuntimeConfig variable.

        ```python
        import pulumi
        import pulumi_gcp as gcp

        my_runtime_config = gcp.runtimeconfig.Config("my-runtime-config", description="Runtime configuration values for my service")
        environment = gcp.runtimeconfig.Variable("environment",
            parent=my_runtime_config.name,
            text="example.com")
        ```

        You can also encode binary content using the `value` argument instead. The
        value must be base64 encoded.

        Example of using the `value` argument.

        ```python
        import pulumi
        import base64
        import pulumi_gcp as gcp

        my_runtime_config = gcp.runtimeconfig.Config("my-runtime-config", description="Runtime configuration values for my service")
        my_secret = gcp.runtimeconfig.Variable("my-secret",
            parent=my_runtime_config.name,
            value=(lambda path: base64.b64encode(open(path).read().encode()).decode())("my-encrypted-secret.dat"))
        ```

        ## Import

        Runtime Config Variables can be imported using the `name` or full variable name, e.g.

        ```sh
         $ pulumi import gcp:runtimeconfig/variable:Variable myvariable myconfig/myvariable
        ```

        ```sh
         $ pulumi import gcp:runtimeconfig/variable:Variable myvariable projects/my-gcp-project/configs/myconfig/variables/myvariable
        ```

         When importing using only the name, the provider project must be set.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name of the variable to manage. Note that variable
               names can be hierarchical using slashes (e.g. "prod-variables/hostname").
        :param pulumi.Input[str] parent: The name of the RuntimeConfig resource containing this
               variable.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs. If it
               is not provided, the provider project is used.
        :param pulumi.Input[str] text: or `value` - (Required) The content to associate with the variable.
               Exactly one of `text` or `variable` must be specified. If `text` is specified,
               it must be a valid UTF-8 string and less than 4096 bytes in length. If `value`
               is specified, it must be base64 encoded and less than 4096 bytes in length.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VariableArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        Example creating a RuntimeConfig variable.

        ```python
        import pulumi
        import pulumi_gcp as gcp

        my_runtime_config = gcp.runtimeconfig.Config("my-runtime-config", description="Runtime configuration values for my service")
        environment = gcp.runtimeconfig.Variable("environment",
            parent=my_runtime_config.name,
            text="example.com")
        ```

        You can also encode binary content using the `value` argument instead. The
        value must be base64 encoded.

        Example of using the `value` argument.

        ```python
        import pulumi
        import base64
        import pulumi_gcp as gcp

        my_runtime_config = gcp.runtimeconfig.Config("my-runtime-config", description="Runtime configuration values for my service")
        my_secret = gcp.runtimeconfig.Variable("my-secret",
            parent=my_runtime_config.name,
            value=(lambda path: base64.b64encode(open(path).read().encode()).decode())("my-encrypted-secret.dat"))
        ```

        ## Import

        Runtime Config Variables can be imported using the `name` or full variable name, e.g.

        ```sh
         $ pulumi import gcp:runtimeconfig/variable:Variable myvariable myconfig/myvariable
        ```

        ```sh
         $ pulumi import gcp:runtimeconfig/variable:Variable myvariable projects/my-gcp-project/configs/myconfig/variables/myvariable
        ```

         When importing using only the name, the provider project must be set.

        :param str resource_name: The name of the resource.
        :param VariableArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VariableArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parent: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 text: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = VariableArgs.__new__(VariableArgs)

            __props__.__dict__["name"] = name
            if parent is None and not opts.urn:
                raise TypeError("Missing required property 'parent'")
            __props__.__dict__["parent"] = parent
            __props__.__dict__["project"] = project
            __props__.__dict__["text"] = None if text is None else pulumi.Output.secret(text)
            __props__.__dict__["value"] = None if value is None else pulumi.Output.secret(value)
            __props__.__dict__["update_time"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["text", "value"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(Variable, __self__).__init__(
            'gcp:runtimeconfig/variable:Variable',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            name: Optional[pulumi.Input[str]] = None,
            parent: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            text: Optional[pulumi.Input[str]] = None,
            update_time: Optional[pulumi.Input[str]] = None,
            value: Optional[pulumi.Input[str]] = None) -> 'Variable':
        """
        Get an existing Variable resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name of the variable to manage. Note that variable
               names can be hierarchical using slashes (e.g. "prod-variables/hostname").
        :param pulumi.Input[str] parent: The name of the RuntimeConfig resource containing this
               variable.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs. If it
               is not provided, the provider project is used.
        :param pulumi.Input[str] text: or `value` - (Required) The content to associate with the variable.
               Exactly one of `text` or `variable` must be specified. If `text` is specified,
               it must be a valid UTF-8 string and less than 4096 bytes in length. If `value`
               is specified, it must be base64 encoded and less than 4096 bytes in length.
        :param pulumi.Input[str] update_time: (Computed) The timestamp in RFC3339 UTC "Zulu" format,
               accurate to nanoseconds, representing when the variable was last updated.
               Example: "2016-10-09T12:33:37.578138407Z".
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _VariableState.__new__(_VariableState)

        __props__.__dict__["name"] = name
        __props__.__dict__["parent"] = parent
        __props__.__dict__["project"] = project
        __props__.__dict__["text"] = text
        __props__.__dict__["update_time"] = update_time
        __props__.__dict__["value"] = value
        return Variable(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the variable to manage. Note that variable
        names can be hierarchical using slashes (e.g. "prod-variables/hostname").
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def parent(self) -> pulumi.Output[str]:
        """
        The name of the RuntimeConfig resource containing this
        variable.
        """
        return pulumi.get(self, "parent")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs. If it
        is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def text(self) -> pulumi.Output[Optional[str]]:
        """
        or `value` - (Required) The content to associate with the variable.
        Exactly one of `text` or `variable` must be specified. If `text` is specified,
        it must be a valid UTF-8 string and less than 4096 bytes in length. If `value`
        is specified, it must be base64 encoded and less than 4096 bytes in length.
        """
        return pulumi.get(self, "text")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        (Computed) The timestamp in RFC3339 UTC "Zulu" format,
        accurate to nanoseconds, representing when the variable was last updated.
        Example: "2016-10-09T12:33:37.578138407Z".
        """
        return pulumi.get(self, "update_time")

    @property
    @pulumi.getter
    def value(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "value")

