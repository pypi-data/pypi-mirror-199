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
    'AddonsConfigAddonsConfig',
    'AddonsConfigAddonsConfigAdvancedApiOpsConfig',
    'AddonsConfigAddonsConfigApiSecurityConfig',
    'AddonsConfigAddonsConfigConnectorsPlatformConfig',
    'AddonsConfigAddonsConfigIntegrationConfig',
    'AddonsConfigAddonsConfigMonetizationConfig',
    'EnvironmentIamBindingCondition',
    'EnvironmentIamMemberCondition',
    'EnvironmentNodeConfig',
    'OrganizationProperties',
    'OrganizationPropertiesProperty',
    'SharedflowMetaData',
]

@pulumi.output_type
class AddonsConfigAddonsConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "advancedApiOpsConfig":
            suggest = "advanced_api_ops_config"
        elif key == "apiSecurityConfig":
            suggest = "api_security_config"
        elif key == "connectorsPlatformConfig":
            suggest = "connectors_platform_config"
        elif key == "integrationConfig":
            suggest = "integration_config"
        elif key == "monetizationConfig":
            suggest = "monetization_config"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AddonsConfigAddonsConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AddonsConfigAddonsConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AddonsConfigAddonsConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 advanced_api_ops_config: Optional['outputs.AddonsConfigAddonsConfigAdvancedApiOpsConfig'] = None,
                 api_security_config: Optional['outputs.AddonsConfigAddonsConfigApiSecurityConfig'] = None,
                 connectors_platform_config: Optional['outputs.AddonsConfigAddonsConfigConnectorsPlatformConfig'] = None,
                 integration_config: Optional['outputs.AddonsConfigAddonsConfigIntegrationConfig'] = None,
                 monetization_config: Optional['outputs.AddonsConfigAddonsConfigMonetizationConfig'] = None):
        """
        :param 'AddonsConfigAddonsConfigAdvancedApiOpsConfigArgs' advanced_api_ops_config: Configuration for the Monetization add-on.
               Structure is documented below.
        :param 'AddonsConfigAddonsConfigApiSecurityConfigArgs' api_security_config: Configuration for the Monetization add-on.
               Structure is documented below.
        :param 'AddonsConfigAddonsConfigConnectorsPlatformConfigArgs' connectors_platform_config: Configuration for the Monetization add-on.
               Structure is documented below.
        :param 'AddonsConfigAddonsConfigIntegrationConfigArgs' integration_config: Configuration for the Monetization add-on.
               Structure is documented below.
        :param 'AddonsConfigAddonsConfigMonetizationConfigArgs' monetization_config: Configuration for the Monetization add-on.
               Structure is documented below.
        """
        if advanced_api_ops_config is not None:
            pulumi.set(__self__, "advanced_api_ops_config", advanced_api_ops_config)
        if api_security_config is not None:
            pulumi.set(__self__, "api_security_config", api_security_config)
        if connectors_platform_config is not None:
            pulumi.set(__self__, "connectors_platform_config", connectors_platform_config)
        if integration_config is not None:
            pulumi.set(__self__, "integration_config", integration_config)
        if monetization_config is not None:
            pulumi.set(__self__, "monetization_config", monetization_config)

    @property
    @pulumi.getter(name="advancedApiOpsConfig")
    def advanced_api_ops_config(self) -> Optional['outputs.AddonsConfigAddonsConfigAdvancedApiOpsConfig']:
        """
        Configuration for the Monetization add-on.
        Structure is documented below.
        """
        return pulumi.get(self, "advanced_api_ops_config")

    @property
    @pulumi.getter(name="apiSecurityConfig")
    def api_security_config(self) -> Optional['outputs.AddonsConfigAddonsConfigApiSecurityConfig']:
        """
        Configuration for the Monetization add-on.
        Structure is documented below.
        """
        return pulumi.get(self, "api_security_config")

    @property
    @pulumi.getter(name="connectorsPlatformConfig")
    def connectors_platform_config(self) -> Optional['outputs.AddonsConfigAddonsConfigConnectorsPlatformConfig']:
        """
        Configuration for the Monetization add-on.
        Structure is documented below.
        """
        return pulumi.get(self, "connectors_platform_config")

    @property
    @pulumi.getter(name="integrationConfig")
    def integration_config(self) -> Optional['outputs.AddonsConfigAddonsConfigIntegrationConfig']:
        """
        Configuration for the Monetization add-on.
        Structure is documented below.
        """
        return pulumi.get(self, "integration_config")

    @property
    @pulumi.getter(name="monetizationConfig")
    def monetization_config(self) -> Optional['outputs.AddonsConfigAddonsConfigMonetizationConfig']:
        """
        Configuration for the Monetization add-on.
        Structure is documented below.
        """
        return pulumi.get(self, "monetization_config")


@pulumi.output_type
class AddonsConfigAddonsConfigAdvancedApiOpsConfig(dict):
    def __init__(__self__, *,
                 enabled: Optional[bool] = None):
        """
        :param bool enabled: Flag that specifies whether the Advanced API Ops add-on is enabled.
        """
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[bool]:
        """
        Flag that specifies whether the Advanced API Ops add-on is enabled.
        """
        return pulumi.get(self, "enabled")


@pulumi.output_type
class AddonsConfigAddonsConfigApiSecurityConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "expiresAt":
            suggest = "expires_at"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AddonsConfigAddonsConfigApiSecurityConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AddonsConfigAddonsConfigApiSecurityConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AddonsConfigAddonsConfigApiSecurityConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 enabled: Optional[bool] = None,
                 expires_at: Optional[str] = None):
        """
        :param bool enabled: Flag that specifies whether the Advanced API Ops add-on is enabled.
        :param str expires_at: (Output)
               Flag that specifies whether the Advanced API Ops add-on is enabled.
        """
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if expires_at is not None:
            pulumi.set(__self__, "expires_at", expires_at)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[bool]:
        """
        Flag that specifies whether the Advanced API Ops add-on is enabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="expiresAt")
    def expires_at(self) -> Optional[str]:
        """
        (Output)
        Flag that specifies whether the Advanced API Ops add-on is enabled.
        """
        return pulumi.get(self, "expires_at")


@pulumi.output_type
class AddonsConfigAddonsConfigConnectorsPlatformConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "expiresAt":
            suggest = "expires_at"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AddonsConfigAddonsConfigConnectorsPlatformConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AddonsConfigAddonsConfigConnectorsPlatformConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AddonsConfigAddonsConfigConnectorsPlatformConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 enabled: Optional[bool] = None,
                 expires_at: Optional[str] = None):
        """
        :param bool enabled: Flag that specifies whether the Advanced API Ops add-on is enabled.
        :param str expires_at: (Output)
               Flag that specifies whether the Advanced API Ops add-on is enabled.
        """
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if expires_at is not None:
            pulumi.set(__self__, "expires_at", expires_at)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[bool]:
        """
        Flag that specifies whether the Advanced API Ops add-on is enabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="expiresAt")
    def expires_at(self) -> Optional[str]:
        """
        (Output)
        Flag that specifies whether the Advanced API Ops add-on is enabled.
        """
        return pulumi.get(self, "expires_at")


@pulumi.output_type
class AddonsConfigAddonsConfigIntegrationConfig(dict):
    def __init__(__self__, *,
                 enabled: Optional[bool] = None):
        """
        :param bool enabled: Flag that specifies whether the Advanced API Ops add-on is enabled.
        """
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[bool]:
        """
        Flag that specifies whether the Advanced API Ops add-on is enabled.
        """
        return pulumi.get(self, "enabled")


@pulumi.output_type
class AddonsConfigAddonsConfigMonetizationConfig(dict):
    def __init__(__self__, *,
                 enabled: Optional[bool] = None):
        """
        :param bool enabled: Flag that specifies whether the Advanced API Ops add-on is enabled.
        """
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[bool]:
        """
        Flag that specifies whether the Advanced API Ops add-on is enabled.
        """
        return pulumi.get(self, "enabled")


@pulumi.output_type
class EnvironmentIamBindingCondition(dict):
    def __init__(__self__, *,
                 expression: str,
                 title: str,
                 description: Optional[str] = None):
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> str:
        return pulumi.get(self, "expression")

    @property
    @pulumi.getter
    def title(self) -> str:
        return pulumi.get(self, "title")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")


@pulumi.output_type
class EnvironmentIamMemberCondition(dict):
    def __init__(__self__, *,
                 expression: str,
                 title: str,
                 description: Optional[str] = None):
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> str:
        return pulumi.get(self, "expression")

    @property
    @pulumi.getter
    def title(self) -> str:
        return pulumi.get(self, "title")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")


@pulumi.output_type
class EnvironmentNodeConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "currentAggregateNodeCount":
            suggest = "current_aggregate_node_count"
        elif key == "maxNodeCount":
            suggest = "max_node_count"
        elif key == "minNodeCount":
            suggest = "min_node_count"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EnvironmentNodeConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EnvironmentNodeConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EnvironmentNodeConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 current_aggregate_node_count: Optional[str] = None,
                 max_node_count: Optional[str] = None,
                 min_node_count: Optional[str] = None):
        """
        :param str current_aggregate_node_count: (Output)
               The current total number of gateway nodes that each environment currently has across
               all instances.
        :param str max_node_count: The maximum total number of gateway nodes that the is reserved for all instances that
               has the specified environment. If not specified, the default is determined by the
               recommended maximum number of nodes for that gateway.
        :param str min_node_count: The minimum total number of gateway nodes that the is reserved for all instances that
               has the specified environment. If not specified, the default is determined by the
               recommended minimum number of nodes for that gateway.
        """
        if current_aggregate_node_count is not None:
            pulumi.set(__self__, "current_aggregate_node_count", current_aggregate_node_count)
        if max_node_count is not None:
            pulumi.set(__self__, "max_node_count", max_node_count)
        if min_node_count is not None:
            pulumi.set(__self__, "min_node_count", min_node_count)

    @property
    @pulumi.getter(name="currentAggregateNodeCount")
    def current_aggregate_node_count(self) -> Optional[str]:
        """
        (Output)
        The current total number of gateway nodes that each environment currently has across
        all instances.
        """
        return pulumi.get(self, "current_aggregate_node_count")

    @property
    @pulumi.getter(name="maxNodeCount")
    def max_node_count(self) -> Optional[str]:
        """
        The maximum total number of gateway nodes that the is reserved for all instances that
        has the specified environment. If not specified, the default is determined by the
        recommended maximum number of nodes for that gateway.
        """
        return pulumi.get(self, "max_node_count")

    @property
    @pulumi.getter(name="minNodeCount")
    def min_node_count(self) -> Optional[str]:
        """
        The minimum total number of gateway nodes that the is reserved for all instances that
        has the specified environment. If not specified, the default is determined by the
        recommended minimum number of nodes for that gateway.
        """
        return pulumi.get(self, "min_node_count")


@pulumi.output_type
class OrganizationProperties(dict):
    def __init__(__self__, *,
                 properties: Optional[Sequence['outputs.OrganizationPropertiesProperty']] = None):
        """
        :param Sequence['OrganizationPropertiesPropertyArgs'] properties: List of all properties in the object.
               Structure is documented below.
        """
        if properties is not None:
            pulumi.set(__self__, "properties", properties)

    @property
    @pulumi.getter
    def properties(self) -> Optional[Sequence['outputs.OrganizationPropertiesProperty']]:
        """
        List of all properties in the object.
        Structure is documented below.
        """
        return pulumi.get(self, "properties")


@pulumi.output_type
class OrganizationPropertiesProperty(dict):
    def __init__(__self__, *,
                 name: Optional[str] = None,
                 value: Optional[str] = None):
        """
        :param str name: Name of the property.
        :param str value: Value of the property.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Name of the property.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> Optional[str]:
        """
        Value of the property.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class SharedflowMetaData(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "createdAt":
            suggest = "created_at"
        elif key == "lastModifiedAt":
            suggest = "last_modified_at"
        elif key == "subType":
            suggest = "sub_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SharedflowMetaData. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SharedflowMetaData.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SharedflowMetaData.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 created_at: Optional[str] = None,
                 last_modified_at: Optional[str] = None,
                 sub_type: Optional[str] = None):
        """
        :param str created_at: Time at which the API proxy was created, in milliseconds since epoch.
        :param str last_modified_at: Time at which the API proxy was most recently modified, in milliseconds since epoch.
        :param str sub_type: The type of entity described
        """
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if last_modified_at is not None:
            pulumi.set(__self__, "last_modified_at", last_modified_at)
        if sub_type is not None:
            pulumi.set(__self__, "sub_type", sub_type)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        Time at which the API proxy was created, in milliseconds since epoch.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="lastModifiedAt")
    def last_modified_at(self) -> Optional[str]:
        """
        Time at which the API proxy was most recently modified, in milliseconds since epoch.
        """
        return pulumi.get(self, "last_modified_at")

    @property
    @pulumi.getter(name="subType")
    def sub_type(self) -> Optional[str]:
        """
        The type of entity described
        """
        return pulumi.get(self, "sub_type")


