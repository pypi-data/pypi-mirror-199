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
    'HostingVersionConfigArgs',
    'HostingVersionConfigRedirectArgs',
    'HostingVersionConfigRewriteArgs',
    'HostingVersionConfigRewriteRunArgs',
]

@pulumi.input_type
class HostingVersionConfigArgs:
    def __init__(__self__, *,
                 redirects: Optional[pulumi.Input[Sequence[pulumi.Input['HostingVersionConfigRedirectArgs']]]] = None,
                 rewrites: Optional[pulumi.Input[Sequence[pulumi.Input['HostingVersionConfigRewriteArgs']]]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input['HostingVersionConfigRedirectArgs']]] redirects: An array of objects (called redirect rules), where each rule specifies a URL pattern that, if matched to the request URL path,
               triggers Hosting to respond with a redirect to the specified destination path.
               Structure is documented below.
        :param pulumi.Input[Sequence[pulumi.Input['HostingVersionConfigRewriteArgs']]] rewrites: An array of objects (called rewrite rules), where each rule specifies a URL pattern that, if matched to the
               request URL path, triggers Hosting to respond as if the service were given the specified destination URL.
               Structure is documented below.
        """
        if redirects is not None:
            pulumi.set(__self__, "redirects", redirects)
        if rewrites is not None:
            pulumi.set(__self__, "rewrites", rewrites)

    @property
    @pulumi.getter
    def redirects(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['HostingVersionConfigRedirectArgs']]]]:
        """
        An array of objects (called redirect rules), where each rule specifies a URL pattern that, if matched to the request URL path,
        triggers Hosting to respond with a redirect to the specified destination path.
        Structure is documented below.
        """
        return pulumi.get(self, "redirects")

    @redirects.setter
    def redirects(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['HostingVersionConfigRedirectArgs']]]]):
        pulumi.set(self, "redirects", value)

    @property
    @pulumi.getter
    def rewrites(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['HostingVersionConfigRewriteArgs']]]]:
        """
        An array of objects (called rewrite rules), where each rule specifies a URL pattern that, if matched to the
        request URL path, triggers Hosting to respond as if the service were given the specified destination URL.
        Structure is documented below.
        """
        return pulumi.get(self, "rewrites")

    @rewrites.setter
    def rewrites(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['HostingVersionConfigRewriteArgs']]]]):
        pulumi.set(self, "rewrites", value)


@pulumi.input_type
class HostingVersionConfigRedirectArgs:
    def __init__(__self__, *,
                 location: pulumi.Input[str],
                 status_code: pulumi.Input[int],
                 glob: Optional[pulumi.Input[str]] = None,
                 regex: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] location: The value to put in the HTTP location header of the response.
               The location can contain capture group values from the pattern using a : prefix to identify
               the segment and an optional * to capture the rest of the URL. For example:
               ```python
               import pulumi
               ```
        :param pulumi.Input[int] status_code: The status HTTP code to return in the response. It must be a valid 3xx status code.
        :param pulumi.Input[str] glob: The user-supplied glob to match against the request URL path.
        :param pulumi.Input[str] regex: The user-supplied RE2 regular expression to match against the request URL path.
        """
        pulumi.set(__self__, "location", location)
        pulumi.set(__self__, "status_code", status_code)
        if glob is not None:
            pulumi.set(__self__, "glob", glob)
        if regex is not None:
            pulumi.set(__self__, "regex", regex)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Input[str]:
        """
        The value to put in the HTTP location header of the response.
        The location can contain capture group values from the pattern using a : prefix to identify
        the segment and an optional * to capture the rest of the URL. For example:
        ```python
        import pulumi
        ```
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: pulumi.Input[str]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="statusCode")
    def status_code(self) -> pulumi.Input[int]:
        """
        The status HTTP code to return in the response. It must be a valid 3xx status code.
        """
        return pulumi.get(self, "status_code")

    @status_code.setter
    def status_code(self, value: pulumi.Input[int]):
        pulumi.set(self, "status_code", value)

    @property
    @pulumi.getter
    def glob(self) -> Optional[pulumi.Input[str]]:
        """
        The user-supplied glob to match against the request URL path.
        """
        return pulumi.get(self, "glob")

    @glob.setter
    def glob(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "glob", value)

    @property
    @pulumi.getter
    def regex(self) -> Optional[pulumi.Input[str]]:
        """
        The user-supplied RE2 regular expression to match against the request URL path.
        """
        return pulumi.get(self, "regex")

    @regex.setter
    def regex(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "regex", value)


@pulumi.input_type
class HostingVersionConfigRewriteArgs:
    def __init__(__self__, *,
                 function: Optional[pulumi.Input[str]] = None,
                 glob: Optional[pulumi.Input[str]] = None,
                 regex: Optional[pulumi.Input[str]] = None,
                 run: Optional[pulumi.Input['HostingVersionConfigRewriteRunArgs']] = None):
        """
        :param pulumi.Input[str] function: The function to proxy requests to. Must match the exported function name exactly.
        :param pulumi.Input[str] glob: The user-supplied glob to match against the request URL path.
        :param pulumi.Input[str] regex: The user-supplied RE2 regular expression to match against the request URL path.
        :param pulumi.Input['HostingVersionConfigRewriteRunArgs'] run: The request will be forwarded to Cloud Run.
               Structure is documented below.
        """
        if function is not None:
            pulumi.set(__self__, "function", function)
        if glob is not None:
            pulumi.set(__self__, "glob", glob)
        if regex is not None:
            pulumi.set(__self__, "regex", regex)
        if run is not None:
            pulumi.set(__self__, "run", run)

    @property
    @pulumi.getter
    def function(self) -> Optional[pulumi.Input[str]]:
        """
        The function to proxy requests to. Must match the exported function name exactly.
        """
        return pulumi.get(self, "function")

    @function.setter
    def function(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "function", value)

    @property
    @pulumi.getter
    def glob(self) -> Optional[pulumi.Input[str]]:
        """
        The user-supplied glob to match against the request URL path.
        """
        return pulumi.get(self, "glob")

    @glob.setter
    def glob(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "glob", value)

    @property
    @pulumi.getter
    def regex(self) -> Optional[pulumi.Input[str]]:
        """
        The user-supplied RE2 regular expression to match against the request URL path.
        """
        return pulumi.get(self, "regex")

    @regex.setter
    def regex(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "regex", value)

    @property
    @pulumi.getter
    def run(self) -> Optional[pulumi.Input['HostingVersionConfigRewriteRunArgs']]:
        """
        The request will be forwarded to Cloud Run.
        Structure is documented below.
        """
        return pulumi.get(self, "run")

    @run.setter
    def run(self, value: Optional[pulumi.Input['HostingVersionConfigRewriteRunArgs']]):
        pulumi.set(self, "run", value)


@pulumi.input_type
class HostingVersionConfigRewriteRunArgs:
    def __init__(__self__, *,
                 service_id: pulumi.Input[str],
                 region: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] service_id: User-defined ID of the Cloud Run service.
        :param pulumi.Input[str] region: Optional. User-provided region where the Cloud Run service is hosted. Defaults to `us-central1` if not supplied.
        """
        pulumi.set(__self__, "service_id", service_id)
        if region is not None:
            pulumi.set(__self__, "region", region)

    @property
    @pulumi.getter(name="serviceId")
    def service_id(self) -> pulumi.Input[str]:
        """
        User-defined ID of the Cloud Run service.
        """
        return pulumi.get(self, "service_id")

    @service_id.setter
    def service_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_id", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. User-provided region where the Cloud Run service is hosted. Defaults to `us-central1` if not supplied.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)


