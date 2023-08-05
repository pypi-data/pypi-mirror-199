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
    'GetBackendServiceResult',
    'AwaitableGetBackendServiceResult',
    'get_backend_service',
    'get_backend_service_output',
]

@pulumi.output_type
class GetBackendServiceResult:
    """
    A collection of values returned by getBackendService.
    """
    def __init__(__self__, affinity_cookie_ttl_sec=None, backends=None, cdn_policies=None, circuit_breakers=None, compression_mode=None, connection_draining_timeout_sec=None, consistent_hash=None, creation_timestamp=None, custom_request_headers=None, custom_response_headers=None, description=None, edge_security_policy=None, enable_cdn=None, fingerprint=None, generated_id=None, health_checks=None, iaps=None, id=None, load_balancing_scheme=None, locality_lb_policies=None, locality_lb_policy=None, log_configs=None, name=None, outlier_detections=None, port_name=None, project=None, protocol=None, security_policy=None, security_settings=None, self_link=None, session_affinity=None, timeout_sec=None):
        if affinity_cookie_ttl_sec and not isinstance(affinity_cookie_ttl_sec, int):
            raise TypeError("Expected argument 'affinity_cookie_ttl_sec' to be a int")
        pulumi.set(__self__, "affinity_cookie_ttl_sec", affinity_cookie_ttl_sec)
        if backends and not isinstance(backends, list):
            raise TypeError("Expected argument 'backends' to be a list")
        pulumi.set(__self__, "backends", backends)
        if cdn_policies and not isinstance(cdn_policies, list):
            raise TypeError("Expected argument 'cdn_policies' to be a list")
        pulumi.set(__self__, "cdn_policies", cdn_policies)
        if circuit_breakers and not isinstance(circuit_breakers, list):
            raise TypeError("Expected argument 'circuit_breakers' to be a list")
        pulumi.set(__self__, "circuit_breakers", circuit_breakers)
        if compression_mode and not isinstance(compression_mode, str):
            raise TypeError("Expected argument 'compression_mode' to be a str")
        pulumi.set(__self__, "compression_mode", compression_mode)
        if connection_draining_timeout_sec and not isinstance(connection_draining_timeout_sec, int):
            raise TypeError("Expected argument 'connection_draining_timeout_sec' to be a int")
        pulumi.set(__self__, "connection_draining_timeout_sec", connection_draining_timeout_sec)
        if consistent_hash and not isinstance(consistent_hash, list):
            raise TypeError("Expected argument 'consistent_hash' to be a list")
        pulumi.set(__self__, "consistent_hash", consistent_hash)
        if creation_timestamp and not isinstance(creation_timestamp, str):
            raise TypeError("Expected argument 'creation_timestamp' to be a str")
        pulumi.set(__self__, "creation_timestamp", creation_timestamp)
        if custom_request_headers and not isinstance(custom_request_headers, list):
            raise TypeError("Expected argument 'custom_request_headers' to be a list")
        pulumi.set(__self__, "custom_request_headers", custom_request_headers)
        if custom_response_headers and not isinstance(custom_response_headers, list):
            raise TypeError("Expected argument 'custom_response_headers' to be a list")
        pulumi.set(__self__, "custom_response_headers", custom_response_headers)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if edge_security_policy and not isinstance(edge_security_policy, str):
            raise TypeError("Expected argument 'edge_security_policy' to be a str")
        pulumi.set(__self__, "edge_security_policy", edge_security_policy)
        if enable_cdn and not isinstance(enable_cdn, bool):
            raise TypeError("Expected argument 'enable_cdn' to be a bool")
        pulumi.set(__self__, "enable_cdn", enable_cdn)
        if fingerprint and not isinstance(fingerprint, str):
            raise TypeError("Expected argument 'fingerprint' to be a str")
        pulumi.set(__self__, "fingerprint", fingerprint)
        if generated_id and not isinstance(generated_id, int):
            raise TypeError("Expected argument 'generated_id' to be a int")
        pulumi.set(__self__, "generated_id", generated_id)
        if health_checks and not isinstance(health_checks, list):
            raise TypeError("Expected argument 'health_checks' to be a list")
        pulumi.set(__self__, "health_checks", health_checks)
        if iaps and not isinstance(iaps, list):
            raise TypeError("Expected argument 'iaps' to be a list")
        pulumi.set(__self__, "iaps", iaps)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if load_balancing_scheme and not isinstance(load_balancing_scheme, str):
            raise TypeError("Expected argument 'load_balancing_scheme' to be a str")
        pulumi.set(__self__, "load_balancing_scheme", load_balancing_scheme)
        if locality_lb_policies and not isinstance(locality_lb_policies, list):
            raise TypeError("Expected argument 'locality_lb_policies' to be a list")
        pulumi.set(__self__, "locality_lb_policies", locality_lb_policies)
        if locality_lb_policy and not isinstance(locality_lb_policy, str):
            raise TypeError("Expected argument 'locality_lb_policy' to be a str")
        pulumi.set(__self__, "locality_lb_policy", locality_lb_policy)
        if log_configs and not isinstance(log_configs, list):
            raise TypeError("Expected argument 'log_configs' to be a list")
        pulumi.set(__self__, "log_configs", log_configs)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if outlier_detections and not isinstance(outlier_detections, list):
            raise TypeError("Expected argument 'outlier_detections' to be a list")
        pulumi.set(__self__, "outlier_detections", outlier_detections)
        if port_name and not isinstance(port_name, str):
            raise TypeError("Expected argument 'port_name' to be a str")
        pulumi.set(__self__, "port_name", port_name)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)
        if protocol and not isinstance(protocol, str):
            raise TypeError("Expected argument 'protocol' to be a str")
        pulumi.set(__self__, "protocol", protocol)
        if security_policy and not isinstance(security_policy, str):
            raise TypeError("Expected argument 'security_policy' to be a str")
        pulumi.set(__self__, "security_policy", security_policy)
        if security_settings and not isinstance(security_settings, list):
            raise TypeError("Expected argument 'security_settings' to be a list")
        pulumi.set(__self__, "security_settings", security_settings)
        if self_link and not isinstance(self_link, str):
            raise TypeError("Expected argument 'self_link' to be a str")
        pulumi.set(__self__, "self_link", self_link)
        if session_affinity and not isinstance(session_affinity, str):
            raise TypeError("Expected argument 'session_affinity' to be a str")
        pulumi.set(__self__, "session_affinity", session_affinity)
        if timeout_sec and not isinstance(timeout_sec, int):
            raise TypeError("Expected argument 'timeout_sec' to be a int")
        pulumi.set(__self__, "timeout_sec", timeout_sec)

    @property
    @pulumi.getter(name="affinityCookieTtlSec")
    def affinity_cookie_ttl_sec(self) -> int:
        return pulumi.get(self, "affinity_cookie_ttl_sec")

    @property
    @pulumi.getter
    def backends(self) -> Sequence['outputs.GetBackendServiceBackendResult']:
        """
        The set of backends that serve this Backend Service.
        """
        return pulumi.get(self, "backends")

    @property
    @pulumi.getter(name="cdnPolicies")
    def cdn_policies(self) -> Sequence['outputs.GetBackendServiceCdnPolicyResult']:
        return pulumi.get(self, "cdn_policies")

    @property
    @pulumi.getter(name="circuitBreakers")
    def circuit_breakers(self) -> Sequence['outputs.GetBackendServiceCircuitBreakerResult']:
        return pulumi.get(self, "circuit_breakers")

    @property
    @pulumi.getter(name="compressionMode")
    def compression_mode(self) -> str:
        return pulumi.get(self, "compression_mode")

    @property
    @pulumi.getter(name="connectionDrainingTimeoutSec")
    def connection_draining_timeout_sec(self) -> int:
        """
        Time for which instance will be drained (not accept new connections, but still work to finish started ones).
        """
        return pulumi.get(self, "connection_draining_timeout_sec")

    @property
    @pulumi.getter(name="consistentHash")
    def consistent_hash(self) -> Sequence['outputs.GetBackendServiceConsistentHashResult']:
        return pulumi.get(self, "consistent_hash")

    @property
    @pulumi.getter(name="creationTimestamp")
    def creation_timestamp(self) -> str:
        return pulumi.get(self, "creation_timestamp")

    @property
    @pulumi.getter(name="customRequestHeaders")
    def custom_request_headers(self) -> Sequence[str]:
        return pulumi.get(self, "custom_request_headers")

    @property
    @pulumi.getter(name="customResponseHeaders")
    def custom_response_headers(self) -> Sequence[str]:
        return pulumi.get(self, "custom_response_headers")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Textual description for the Backend Service.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="edgeSecurityPolicy")
    def edge_security_policy(self) -> str:
        return pulumi.get(self, "edge_security_policy")

    @property
    @pulumi.getter(name="enableCdn")
    def enable_cdn(self) -> bool:
        """
        Whether or not Cloud CDN is enabled on the Backend Service.
        """
        return pulumi.get(self, "enable_cdn")

    @property
    @pulumi.getter
    def fingerprint(self) -> str:
        """
        The fingerprint of the Backend Service.
        """
        return pulumi.get(self, "fingerprint")

    @property
    @pulumi.getter(name="generatedId")
    def generated_id(self) -> int:
        """
        The unique identifier for the resource. This identifier is defined by the server.
        """
        return pulumi.get(self, "generated_id")

    @property
    @pulumi.getter(name="healthChecks")
    def health_checks(self) -> Sequence[str]:
        """
        The set of HTTP/HTTPS health checks used by the Backend Service.
        """
        return pulumi.get(self, "health_checks")

    @property
    @pulumi.getter
    def iaps(self) -> Sequence['outputs.GetBackendServiceIapResult']:
        return pulumi.get(self, "iaps")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="loadBalancingScheme")
    def load_balancing_scheme(self) -> str:
        return pulumi.get(self, "load_balancing_scheme")

    @property
    @pulumi.getter(name="localityLbPolicies")
    def locality_lb_policies(self) -> Sequence['outputs.GetBackendServiceLocalityLbPolicyResult']:
        return pulumi.get(self, "locality_lb_policies")

    @property
    @pulumi.getter(name="localityLbPolicy")
    def locality_lb_policy(self) -> str:
        return pulumi.get(self, "locality_lb_policy")

    @property
    @pulumi.getter(name="logConfigs")
    def log_configs(self) -> Sequence['outputs.GetBackendServiceLogConfigResult']:
        return pulumi.get(self, "log_configs")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="outlierDetections")
    def outlier_detections(self) -> Sequence['outputs.GetBackendServiceOutlierDetectionResult']:
        return pulumi.get(self, "outlier_detections")

    @property
    @pulumi.getter(name="portName")
    def port_name(self) -> str:
        """
        The name of a service that has been added to an instance group in this backend.
        """
        return pulumi.get(self, "port_name")

    @property
    @pulumi.getter
    def project(self) -> Optional[str]:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def protocol(self) -> str:
        """
        The protocol for incoming requests.
        """
        return pulumi.get(self, "protocol")

    @property
    @pulumi.getter(name="securityPolicy")
    def security_policy(self) -> str:
        return pulumi.get(self, "security_policy")

    @property
    @pulumi.getter(name="securitySettings")
    def security_settings(self) -> Sequence['outputs.GetBackendServiceSecuritySettingResult']:
        return pulumi.get(self, "security_settings")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> str:
        """
        The URI of the Backend Service.
        """
        return pulumi.get(self, "self_link")

    @property
    @pulumi.getter(name="sessionAffinity")
    def session_affinity(self) -> str:
        """
        The Backend Service session stickiness configuration.
        """
        return pulumi.get(self, "session_affinity")

    @property
    @pulumi.getter(name="timeoutSec")
    def timeout_sec(self) -> int:
        """
        The number of seconds to wait for a backend to respond to a request before considering the request failed.
        """
        return pulumi.get(self, "timeout_sec")


class AwaitableGetBackendServiceResult(GetBackendServiceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBackendServiceResult(
            affinity_cookie_ttl_sec=self.affinity_cookie_ttl_sec,
            backends=self.backends,
            cdn_policies=self.cdn_policies,
            circuit_breakers=self.circuit_breakers,
            compression_mode=self.compression_mode,
            connection_draining_timeout_sec=self.connection_draining_timeout_sec,
            consistent_hash=self.consistent_hash,
            creation_timestamp=self.creation_timestamp,
            custom_request_headers=self.custom_request_headers,
            custom_response_headers=self.custom_response_headers,
            description=self.description,
            edge_security_policy=self.edge_security_policy,
            enable_cdn=self.enable_cdn,
            fingerprint=self.fingerprint,
            generated_id=self.generated_id,
            health_checks=self.health_checks,
            iaps=self.iaps,
            id=self.id,
            load_balancing_scheme=self.load_balancing_scheme,
            locality_lb_policies=self.locality_lb_policies,
            locality_lb_policy=self.locality_lb_policy,
            log_configs=self.log_configs,
            name=self.name,
            outlier_detections=self.outlier_detections,
            port_name=self.port_name,
            project=self.project,
            protocol=self.protocol,
            security_policy=self.security_policy,
            security_settings=self.security_settings,
            self_link=self.self_link,
            session_affinity=self.session_affinity,
            timeout_sec=self.timeout_sec)


def get_backend_service(name: Optional[str] = None,
                        project: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetBackendServiceResult:
    """
    Provide access to a Backend Service's attribute. For more information
    see [the official documentation](https://cloud.google.com/compute/docs/load-balancing/http/backend-service)
    and the [API](https://cloud.google.com/compute/docs/reference/latest/backendServices).


    :param str name: The name of the Backend Service.
    :param str project: The project in which the resource belongs. If it is not provided, the provider project is used.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['project'] = project
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:compute/getBackendService:getBackendService', __args__, opts=opts, typ=GetBackendServiceResult).value

    return AwaitableGetBackendServiceResult(
        affinity_cookie_ttl_sec=__ret__.affinity_cookie_ttl_sec,
        backends=__ret__.backends,
        cdn_policies=__ret__.cdn_policies,
        circuit_breakers=__ret__.circuit_breakers,
        compression_mode=__ret__.compression_mode,
        connection_draining_timeout_sec=__ret__.connection_draining_timeout_sec,
        consistent_hash=__ret__.consistent_hash,
        creation_timestamp=__ret__.creation_timestamp,
        custom_request_headers=__ret__.custom_request_headers,
        custom_response_headers=__ret__.custom_response_headers,
        description=__ret__.description,
        edge_security_policy=__ret__.edge_security_policy,
        enable_cdn=__ret__.enable_cdn,
        fingerprint=__ret__.fingerprint,
        generated_id=__ret__.generated_id,
        health_checks=__ret__.health_checks,
        iaps=__ret__.iaps,
        id=__ret__.id,
        load_balancing_scheme=__ret__.load_balancing_scheme,
        locality_lb_policies=__ret__.locality_lb_policies,
        locality_lb_policy=__ret__.locality_lb_policy,
        log_configs=__ret__.log_configs,
        name=__ret__.name,
        outlier_detections=__ret__.outlier_detections,
        port_name=__ret__.port_name,
        project=__ret__.project,
        protocol=__ret__.protocol,
        security_policy=__ret__.security_policy,
        security_settings=__ret__.security_settings,
        self_link=__ret__.self_link,
        session_affinity=__ret__.session_affinity,
        timeout_sec=__ret__.timeout_sec)


@_utilities.lift_output_func(get_backend_service)
def get_backend_service_output(name: Optional[pulumi.Input[str]] = None,
                               project: Optional[pulumi.Input[Optional[str]]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetBackendServiceResult]:
    """
    Provide access to a Backend Service's attribute. For more information
    see [the official documentation](https://cloud.google.com/compute/docs/load-balancing/http/backend-service)
    and the [API](https://cloud.google.com/compute/docs/reference/latest/backendServices).


    :param str name: The name of the Backend Service.
    :param str project: The project in which the resource belongs. If it is not provided, the provider project is used.
    """
    ...
