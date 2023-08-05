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
    'GetSinkResult',
    'AwaitableGetSinkResult',
    'get_sink',
    'get_sink_output',
]

@pulumi.output_type
class GetSinkResult:
    """
    A collection of values returned by getSink.
    """
    def __init__(__self__, bigquery_options=None, description=None, destination=None, disabled=None, exclusions=None, filter=None, id=None, name=None, writer_identity=None):
        if bigquery_options and not isinstance(bigquery_options, list):
            raise TypeError("Expected argument 'bigquery_options' to be a list")
        pulumi.set(__self__, "bigquery_options", bigquery_options)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if destination and not isinstance(destination, str):
            raise TypeError("Expected argument 'destination' to be a str")
        pulumi.set(__self__, "destination", destination)
        if disabled and not isinstance(disabled, bool):
            raise TypeError("Expected argument 'disabled' to be a bool")
        pulumi.set(__self__, "disabled", disabled)
        if exclusions and not isinstance(exclusions, list):
            raise TypeError("Expected argument 'exclusions' to be a list")
        pulumi.set(__self__, "exclusions", exclusions)
        if filter and not isinstance(filter, str):
            raise TypeError("Expected argument 'filter' to be a str")
        pulumi.set(__self__, "filter", filter)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if writer_identity and not isinstance(writer_identity, str):
            raise TypeError("Expected argument 'writer_identity' to be a str")
        pulumi.set(__self__, "writer_identity", writer_identity)

    @property
    @pulumi.getter(name="bigqueryOptions")
    def bigquery_options(self) -> Sequence['outputs.GetSinkBigqueryOptionResult']:
        """
        Options that affect sinks exporting data to BigQuery. Structure is documented below.
        """
        return pulumi.get(self, "bigquery_options")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        A description of this exclusion.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def destination(self) -> str:
        """
        The destination of the sink (or, in other words, where logs are written to).
        """
        return pulumi.get(self, "destination")

    @property
    @pulumi.getter
    def disabled(self) -> bool:
        """
        Whether this exclusion is disabled and it does not exclude any log entries.
        """
        return pulumi.get(self, "disabled")

    @property
    @pulumi.getter
    def exclusions(self) -> Sequence['outputs.GetSinkExclusionResult']:
        """
        Log entries that match any of the exclusion filters are not exported. Structure is documented below.
        """
        return pulumi.get(self, "exclusions")

    @property
    @pulumi.getter
    def filter(self) -> str:
        """
        An advanced logs filter that matches the log entries to be excluded.
        """
        return pulumi.get(self, "filter")

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        A client-assigned identifier, such as `load-balancer-exclusion`.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="writerIdentity")
    def writer_identity(self) -> str:
        """
        The identity associated with this sink. This identity must be granted write access to the configured `destination`.
        """
        return pulumi.get(self, "writer_identity")


class AwaitableGetSinkResult(GetSinkResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSinkResult(
            bigquery_options=self.bigquery_options,
            description=self.description,
            destination=self.destination,
            disabled=self.disabled,
            exclusions=self.exclusions,
            filter=self.filter,
            id=self.id,
            name=self.name,
            writer_identity=self.writer_identity)


def get_sink(id: Optional[str] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSinkResult:
    """
    Use this data source to get a project, folder, organization or billing account logging sink details.
    To get more information about Service, see:

    [API documentation](https://cloud.google.com/logging/docs/reference/v2/rest/v2/sinks)

    ## Example Usage
    ### Retrieve Project Logging Sink Basic

    ```python
    import pulumi
    import pulumi_gcp as gcp

    project_sink = gcp.logging.get_sink(id="projects/0123456789/sinks/my-sink-name")
    ```


    :param str id: The identifier for the resource. 
           Examples:
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:logging/getSink:getSink', __args__, opts=opts, typ=GetSinkResult).value

    return AwaitableGetSinkResult(
        bigquery_options=__ret__.bigquery_options,
        description=__ret__.description,
        destination=__ret__.destination,
        disabled=__ret__.disabled,
        exclusions=__ret__.exclusions,
        filter=__ret__.filter,
        id=__ret__.id,
        name=__ret__.name,
        writer_identity=__ret__.writer_identity)


@_utilities.lift_output_func(get_sink)
def get_sink_output(id: Optional[pulumi.Input[str]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSinkResult]:
    """
    Use this data source to get a project, folder, organization or billing account logging sink details.
    To get more information about Service, see:

    [API documentation](https://cloud.google.com/logging/docs/reference/v2/rest/v2/sinks)

    ## Example Usage
    ### Retrieve Project Logging Sink Basic

    ```python
    import pulumi
    import pulumi_gcp as gcp

    project_sink = gcp.logging.get_sink(id="projects/0123456789/sinks/my-sink-name")
    ```


    :param str id: The identifier for the resource. 
           Examples:
    """
    ...
