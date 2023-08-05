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
    'GetObjectSignedUrlResult',
    'AwaitableGetObjectSignedUrlResult',
    'get_object_signed_url',
    'get_object_signed_url_output',
]

@pulumi.output_type
class GetObjectSignedUrlResult:
    """
    A collection of values returned by getObjectSignedUrl.
    """
    def __init__(__self__, bucket=None, content_md5=None, content_type=None, credentials=None, duration=None, extension_headers=None, http_method=None, id=None, path=None, signed_url=None):
        if bucket and not isinstance(bucket, str):
            raise TypeError("Expected argument 'bucket' to be a str")
        pulumi.set(__self__, "bucket", bucket)
        if content_md5 and not isinstance(content_md5, str):
            raise TypeError("Expected argument 'content_md5' to be a str")
        pulumi.set(__self__, "content_md5", content_md5)
        if content_type and not isinstance(content_type, str):
            raise TypeError("Expected argument 'content_type' to be a str")
        pulumi.set(__self__, "content_type", content_type)
        if credentials and not isinstance(credentials, str):
            raise TypeError("Expected argument 'credentials' to be a str")
        pulumi.set(__self__, "credentials", credentials)
        if duration and not isinstance(duration, str):
            raise TypeError("Expected argument 'duration' to be a str")
        pulumi.set(__self__, "duration", duration)
        if extension_headers and not isinstance(extension_headers, dict):
            raise TypeError("Expected argument 'extension_headers' to be a dict")
        pulumi.set(__self__, "extension_headers", extension_headers)
        if http_method and not isinstance(http_method, str):
            raise TypeError("Expected argument 'http_method' to be a str")
        pulumi.set(__self__, "http_method", http_method)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if path and not isinstance(path, str):
            raise TypeError("Expected argument 'path' to be a str")
        pulumi.set(__self__, "path", path)
        if signed_url and not isinstance(signed_url, str):
            raise TypeError("Expected argument 'signed_url' to be a str")
        pulumi.set(__self__, "signed_url", signed_url)

    @property
    @pulumi.getter
    def bucket(self) -> str:
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter(name="contentMd5")
    def content_md5(self) -> Optional[str]:
        return pulumi.get(self, "content_md5")

    @property
    @pulumi.getter(name="contentType")
    def content_type(self) -> Optional[str]:
        return pulumi.get(self, "content_type")

    @property
    @pulumi.getter
    def credentials(self) -> Optional[str]:
        return pulumi.get(self, "credentials")

    @property
    @pulumi.getter
    def duration(self) -> Optional[str]:
        return pulumi.get(self, "duration")

    @property
    @pulumi.getter(name="extensionHeaders")
    def extension_headers(self) -> Optional[Mapping[str, str]]:
        return pulumi.get(self, "extension_headers")

    @property
    @pulumi.getter(name="httpMethod")
    def http_method(self) -> Optional[str]:
        return pulumi.get(self, "http_method")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def path(self) -> str:
        return pulumi.get(self, "path")

    @property
    @pulumi.getter(name="signedUrl")
    def signed_url(self) -> str:
        """
        The signed URL that can be used to access the storage object without authentication.
        """
        return pulumi.get(self, "signed_url")


class AwaitableGetObjectSignedUrlResult(GetObjectSignedUrlResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetObjectSignedUrlResult(
            bucket=self.bucket,
            content_md5=self.content_md5,
            content_type=self.content_type,
            credentials=self.credentials,
            duration=self.duration,
            extension_headers=self.extension_headers,
            http_method=self.http_method,
            id=self.id,
            path=self.path,
            signed_url=self.signed_url)


def get_object_signed_url(bucket: Optional[str] = None,
                          content_md5: Optional[str] = None,
                          content_type: Optional[str] = None,
                          credentials: Optional[str] = None,
                          duration: Optional[str] = None,
                          extension_headers: Optional[Mapping[str, str]] = None,
                          http_method: Optional[str] = None,
                          path: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetObjectSignedUrlResult:
    """
    The Google Cloud storage signed URL data source generates a signed URL for a given storage object. Signed URLs provide a way to give time-limited read or write access to anyone in possession of the URL, regardless of whether they have a Google account.

    For more info about signed URL's is available [here](https://cloud.google.com/storage/docs/access-control/signed-urls).

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    artifact = gcp.storage.get_object_signed_url(bucket="install_binaries",
        path="path/to/install_file.bin")
    vm = gcp.compute.Instance("vm")
    ```
    ## Full Example

    ```python
    import pulumi
    import pulumi_gcp as gcp

    get_url = gcp.storage.get_object_signed_url(bucket="fried_chicken",
        path="path/to/file",
        content_md5="pRviqwS4c4OTJRTe03FD1w==",
        content_type="text/plain",
        duration="2d",
        credentials=(lambda path: open(path).read())("path/to/credentials.json"),
        extension_headers={
            "x-goog-if-generation-match": "1",
        })
    ```


    :param str bucket: The name of the bucket to read the object from
    :param str content_md5: The [MD5 digest](https://cloud.google.com/storage/docs/hashes-etags#_MD5) value in Base64.
           Typically retrieved from `google_storage_bucket_object.object.md5hash` attribute.
           If you provide this in the datasource, the client (e.g. browser, curl) must provide the `Content-MD5` HTTP header with this same value in its request.
    :param str content_type: If you specify this in the datasource, the client must provide the `Content-Type` HTTP header with the same value in its request.
    :param str credentials: What Google service account credentials json should be used to sign the URL.
           This data source checks the following locations for credentials, in order of preference: data source `credentials` attribute, provider `credentials` attribute and finally the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    :param str duration: For how long shall the signed URL be valid (defaults to 1 hour - i.e. `1h`).
           See [here](https://golang.org/pkg/time/#ParseDuration) for info on valid duration formats.
    :param Mapping[str, str] extension_headers: As needed. The server checks to make sure that the client provides matching values in requests using the signed URL.
           Any header starting with `x-goog-` is accepted but see the [Google Docs](https://cloud.google.com/storage/docs/xml-api/reference-headers) for list of headers that are supported by Google.
    :param str http_method: What HTTP Method will the signed URL allow (defaults to `GET`)
    :param str path: The full path to the object inside the bucket
    """
    __args__ = dict()
    __args__['bucket'] = bucket
    __args__['contentMd5'] = content_md5
    __args__['contentType'] = content_type
    __args__['credentials'] = credentials
    __args__['duration'] = duration
    __args__['extensionHeaders'] = extension_headers
    __args__['httpMethod'] = http_method
    __args__['path'] = path
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:storage/getObjectSignedUrl:getObjectSignedUrl', __args__, opts=opts, typ=GetObjectSignedUrlResult).value

    return AwaitableGetObjectSignedUrlResult(
        bucket=__ret__.bucket,
        content_md5=__ret__.content_md5,
        content_type=__ret__.content_type,
        credentials=__ret__.credentials,
        duration=__ret__.duration,
        extension_headers=__ret__.extension_headers,
        http_method=__ret__.http_method,
        id=__ret__.id,
        path=__ret__.path,
        signed_url=__ret__.signed_url)


@_utilities.lift_output_func(get_object_signed_url)
def get_object_signed_url_output(bucket: Optional[pulumi.Input[str]] = None,
                                 content_md5: Optional[pulumi.Input[Optional[str]]] = None,
                                 content_type: Optional[pulumi.Input[Optional[str]]] = None,
                                 credentials: Optional[pulumi.Input[Optional[str]]] = None,
                                 duration: Optional[pulumi.Input[Optional[str]]] = None,
                                 extension_headers: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                                 http_method: Optional[pulumi.Input[Optional[str]]] = None,
                                 path: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetObjectSignedUrlResult]:
    """
    The Google Cloud storage signed URL data source generates a signed URL for a given storage object. Signed URLs provide a way to give time-limited read or write access to anyone in possession of the URL, regardless of whether they have a Google account.

    For more info about signed URL's is available [here](https://cloud.google.com/storage/docs/access-control/signed-urls).

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gcp as gcp

    artifact = gcp.storage.get_object_signed_url(bucket="install_binaries",
        path="path/to/install_file.bin")
    vm = gcp.compute.Instance("vm")
    ```
    ## Full Example

    ```python
    import pulumi
    import pulumi_gcp as gcp

    get_url = gcp.storage.get_object_signed_url(bucket="fried_chicken",
        path="path/to/file",
        content_md5="pRviqwS4c4OTJRTe03FD1w==",
        content_type="text/plain",
        duration="2d",
        credentials=(lambda path: open(path).read())("path/to/credentials.json"),
        extension_headers={
            "x-goog-if-generation-match": "1",
        })
    ```


    :param str bucket: The name of the bucket to read the object from
    :param str content_md5: The [MD5 digest](https://cloud.google.com/storage/docs/hashes-etags#_MD5) value in Base64.
           Typically retrieved from `google_storage_bucket_object.object.md5hash` attribute.
           If you provide this in the datasource, the client (e.g. browser, curl) must provide the `Content-MD5` HTTP header with this same value in its request.
    :param str content_type: If you specify this in the datasource, the client must provide the `Content-Type` HTTP header with the same value in its request.
    :param str credentials: What Google service account credentials json should be used to sign the URL.
           This data source checks the following locations for credentials, in order of preference: data source `credentials` attribute, provider `credentials` attribute and finally the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    :param str duration: For how long shall the signed URL be valid (defaults to 1 hour - i.e. `1h`).
           See [here](https://golang.org/pkg/time/#ParseDuration) for info on valid duration formats.
    :param Mapping[str, str] extension_headers: As needed. The server checks to make sure that the client provides matching values in requests using the signed URL.
           Any header starting with `x-goog-` is accepted but see the [Google Docs](https://cloud.google.com/storage/docs/xml-api/reference-headers) for list of headers that are supported by Google.
    :param str http_method: What HTTP Method will the signed URL allow (defaults to `GET`)
    :param str path: The full path to the object inside the bucket
    """
    ...
