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
    'AddonsConfigAddonsConfigArgs',
    'AddonsConfigAddonsConfigAdvancedApiOpsConfigArgs',
    'AddonsConfigAddonsConfigApiSecurityConfigArgs',
    'AddonsConfigAddonsConfigConnectorsPlatformConfigArgs',
    'AddonsConfigAddonsConfigIntegrationConfigArgs',
    'AddonsConfigAddonsConfigMonetizationConfigArgs',
    'EnvironmentIamBindingConditionArgs',
    'EnvironmentIamMemberConditionArgs',
    'EnvironmentNodeConfigArgs',
    'OrganizationPropertiesArgs',
    'OrganizationPropertiesPropertyArgs',
    'SharedflowMetaDataArgs',
]

@pulumi.input_type
class AddonsConfigAddonsConfigArgs:
    def __init__(__self__, *,
                 advanced_api_ops_config: Optional[pulumi.Input['AddonsConfigAddonsConfigAdvancedApiOpsConfigArgs']] = None,
                 api_security_config: Optional[pulumi.Input['AddonsConfigAddonsConfigApiSecurityConfigArgs']] = None,
                 connectors_platform_config: Optional[pulumi.Input['AddonsConfigAddonsConfigConnectorsPlatformConfigArgs']] = None,
                 integration_config: Optional[pulumi.Input['AddonsConfigAddonsConfigIntegrationConfigArgs']] = None,
                 monetization_config: Optional[pulumi.Input['AddonsConfigAddonsConfigMonetizationConfigArgs']] = None):
        """
        :param pulumi.Input['AddonsConfigAddonsConfigAdvancedApiOpsConfigArgs'] advanced_api_ops_config: Configuration for the Monetization add-on.
               Structure is documented below.
        :param pulumi.Input['AddonsConfigAddonsConfigApiSecurityConfigArgs'] api_security_config: Configuration for the Monetization add-on.
               Structure is documented below.
        :param pulumi.Input['AddonsConfigAddonsConfigConnectorsPlatformConfigArgs'] connectors_platform_config: Configuration for the Monetization add-on.
               Structure is documented below.
        :param pulumi.Input['AddonsConfigAddonsConfigIntegrationConfigArgs'] integration_config: Configuration for the Monetization add-on.
               Structure is documented below.
        :param pulumi.Input['AddonsConfigAddonsConfigMonetizationConfigArgs'] monetization_config: Configuration for the Monetization add-on.
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
    def advanced_api_ops_config(self) -> Optional[pulumi.Input['AddonsConfigAddonsConfigAdvancedApiOpsConfigArgs']]:
        """
        Configuration for the Monetization add-on.
        Structure is documented below.
        """
        return pulumi.get(self, "advanced_api_ops_config")

    @advanced_api_ops_config.setter
    def advanced_api_ops_config(self, value: Optional[pulumi.Input['AddonsConfigAddonsConfigAdvancedApiOpsConfigArgs']]):
        pulumi.set(self, "advanced_api_ops_config", value)

    @property
    @pulumi.getter(name="apiSecurityConfig")
    def api_security_config(self) -> Optional[pulumi.Input['AddonsConfigAddonsConfigApiSecurityConfigArgs']]:
        """
        Configuration for the Monetization add-on.
        Structure is documented below.
        """
        return pulumi.get(self, "api_security_config")

    @api_security_config.setter
    def api_security_config(self, value: Optional[pulumi.Input['AddonsConfigAddonsConfigApiSecurityConfigArgs']]):
        pulumi.set(self, "api_security_config", value)

    @property
    @pulumi.getter(name="connectorsPlatformConfig")
    def connectors_platform_config(self) -> Optional[pulumi.Input['AddonsConfigAddonsConfigConnectorsPlatformConfigArgs']]:
        """
        Configuration for the Monetization add-on.
        Structure is documented below.
        """
        return pulumi.get(self, "connectors_platform_config")

    @connectors_platform_config.setter
    def connectors_platform_config(self, value: Optional[pulumi.Input['AddonsConfigAddonsConfigConnectorsPlatformConfigArgs']]):
        pulumi.set(self, "connectors_platform_config", value)

    @property
    @pulumi.getter(name="integrationConfig")
    def integration_config(self) -> Optional[pulumi.Input['AddonsConfigAddonsConfigIntegrationConfigArgs']]:
        """
        Configuration for the Monetization add-on.
        Structure is documented below.
        """
        return pulumi.get(self, "integration_config")

    @integration_config.setter
    def integration_config(self, value: Optional[pulumi.Input['AddonsConfigAddonsConfigIntegrationConfigArgs']]):
        pulumi.set(self, "integration_config", value)

    @property
    @pulumi.getter(name="monetizationConfig")
    def monetization_config(self) -> Optional[pulumi.Input['AddonsConfigAddonsConfigMonetizationConfigArgs']]:
        """
        Configuration for the Monetization add-on.
        Structure is documented below.
        """
        return pulumi.get(self, "monetization_config")

    @monetization_config.setter
    def monetization_config(self, value: Optional[pulumi.Input['AddonsConfigAddonsConfigMonetizationConfigArgs']]):
        pulumi.set(self, "monetization_config", value)


@pulumi.input_type
class AddonsConfigAddonsConfigAdvancedApiOpsConfigArgs:
    def __init__(__self__, *,
                 enabled: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input[bool] enabled: Flag that specifies whether the Advanced API Ops add-on is enabled.
        """
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Flag that specifies whether the Advanced API Ops add-on is enabled.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)


@pulumi.input_type
class AddonsConfigAddonsConfigApiSecurityConfigArgs:
    def __init__(__self__, *,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 expires_at: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[bool] enabled: Flag that specifies whether the Advanced API Ops add-on is enabled.
        :param pulumi.Input[str] expires_at: (Output)
               Flag that specifies whether the Advanced API Ops add-on is enabled.
        """
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if expires_at is not None:
            pulumi.set(__self__, "expires_at", expires_at)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Flag that specifies whether the Advanced API Ops add-on is enabled.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="expiresAt")
    def expires_at(self) -> Optional[pulumi.Input[str]]:
        """
        (Output)
        Flag that specifies whether the Advanced API Ops add-on is enabled.
        """
        return pulumi.get(self, "expires_at")

    @expires_at.setter
    def expires_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "expires_at", value)


@pulumi.input_type
class AddonsConfigAddonsConfigConnectorsPlatformConfigArgs:
    def __init__(__self__, *,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 expires_at: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[bool] enabled: Flag that specifies whether the Advanced API Ops add-on is enabled.
        :param pulumi.Input[str] expires_at: (Output)
               Flag that specifies whether the Advanced API Ops add-on is enabled.
        """
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if expires_at is not None:
            pulumi.set(__self__, "expires_at", expires_at)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Flag that specifies whether the Advanced API Ops add-on is enabled.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="expiresAt")
    def expires_at(self) -> Optional[pulumi.Input[str]]:
        """
        (Output)
        Flag that specifies whether the Advanced API Ops add-on is enabled.
        """
        return pulumi.get(self, "expires_at")

    @expires_at.setter
    def expires_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "expires_at", value)


@pulumi.input_type
class AddonsConfigAddonsConfigIntegrationConfigArgs:
    def __init__(__self__, *,
                 enabled: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input[bool] enabled: Flag that specifies whether the Advanced API Ops add-on is enabled.
        """
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Flag that specifies whether the Advanced API Ops add-on is enabled.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)


@pulumi.input_type
class AddonsConfigAddonsConfigMonetizationConfigArgs:
    def __init__(__self__, *,
                 enabled: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input[bool] enabled: Flag that specifies whether the Advanced API Ops add-on is enabled.
        """
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Flag that specifies whether the Advanced API Ops add-on is enabled.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)


@pulumi.input_type
class EnvironmentIamBindingConditionArgs:
    def __init__(__self__, *,
                 expression: pulumi.Input[str],
                 title: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> pulumi.Input[str]:
        return pulumi.get(self, "expression")

    @expression.setter
    def expression(self, value: pulumi.Input[str]):
        pulumi.set(self, "expression", value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, "title", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class EnvironmentIamMemberConditionArgs:
    def __init__(__self__, *,
                 expression: pulumi.Input[str],
                 title: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> pulumi.Input[str]:
        return pulumi.get(self, "expression")

    @expression.setter
    def expression(self, value: pulumi.Input[str]):
        pulumi.set(self, "expression", value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, "title", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class EnvironmentNodeConfigArgs:
    def __init__(__self__, *,
                 current_aggregate_node_count: Optional[pulumi.Input[str]] = None,
                 max_node_count: Optional[pulumi.Input[str]] = None,
                 min_node_count: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] current_aggregate_node_count: (Output)
               The current total number of gateway nodes that each environment currently has across
               all instances.
        :param pulumi.Input[str] max_node_count: The maximum total number of gateway nodes that the is reserved for all instances that
               has the specified environment. If not specified, the default is determined by the
               recommended maximum number of nodes for that gateway.
        :param pulumi.Input[str] min_node_count: The minimum total number of gateway nodes that the is reserved for all instances that
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
    def current_aggregate_node_count(self) -> Optional[pulumi.Input[str]]:
        """
        (Output)
        The current total number of gateway nodes that each environment currently has across
        all instances.
        """
        return pulumi.get(self, "current_aggregate_node_count")

    @current_aggregate_node_count.setter
    def current_aggregate_node_count(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "current_aggregate_node_count", value)

    @property
    @pulumi.getter(name="maxNodeCount")
    def max_node_count(self) -> Optional[pulumi.Input[str]]:
        """
        The maximum total number of gateway nodes that the is reserved for all instances that
        has the specified environment. If not specified, the default is determined by the
        recommended maximum number of nodes for that gateway.
        """
        return pulumi.get(self, "max_node_count")

    @max_node_count.setter
    def max_node_count(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "max_node_count", value)

    @property
    @pulumi.getter(name="minNodeCount")
    def min_node_count(self) -> Optional[pulumi.Input[str]]:
        """
        The minimum total number of gateway nodes that the is reserved for all instances that
        has the specified environment. If not specified, the default is determined by the
        recommended minimum number of nodes for that gateway.
        """
        return pulumi.get(self, "min_node_count")

    @min_node_count.setter
    def min_node_count(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "min_node_count", value)


@pulumi.input_type
class OrganizationPropertiesArgs:
    def __init__(__self__, *,
                 properties: Optional[pulumi.Input[Sequence[pulumi.Input['OrganizationPropertiesPropertyArgs']]]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input['OrganizationPropertiesPropertyArgs']]] properties: List of all properties in the object.
               Structure is documented below.
        """
        if properties is not None:
            pulumi.set(__self__, "properties", properties)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OrganizationPropertiesPropertyArgs']]]]:
        """
        List of all properties in the object.
        Structure is documented below.
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OrganizationPropertiesPropertyArgs']]]]):
        pulumi.set(self, "properties", value)


@pulumi.input_type
class OrganizationPropertiesPropertyArgs:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] name: Name of the property.
        :param pulumi.Input[str] value: Value of the property.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the property.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        Value of the property.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class SharedflowMetaDataArgs:
    def __init__(__self__, *,
                 created_at: Optional[pulumi.Input[str]] = None,
                 last_modified_at: Optional[pulumi.Input[str]] = None,
                 sub_type: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] created_at: Time at which the API proxy was created, in milliseconds since epoch.
        :param pulumi.Input[str] last_modified_at: Time at which the API proxy was most recently modified, in milliseconds since epoch.
        :param pulumi.Input[str] sub_type: The type of entity described
        """
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if last_modified_at is not None:
            pulumi.set(__self__, "last_modified_at", last_modified_at)
        if sub_type is not None:
            pulumi.set(__self__, "sub_type", sub_type)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[pulumi.Input[str]]:
        """
        Time at which the API proxy was created, in milliseconds since epoch.
        """
        return pulumi.get(self, "created_at")

    @created_at.setter
    def created_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_at", value)

    @property
    @pulumi.getter(name="lastModifiedAt")
    def last_modified_at(self) -> Optional[pulumi.Input[str]]:
        """
        Time at which the API proxy was most recently modified, in milliseconds since epoch.
        """
        return pulumi.get(self, "last_modified_at")

    @last_modified_at.setter
    def last_modified_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_modified_at", value)

    @property
    @pulumi.getter(name="subType")
    def sub_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of entity described
        """
        return pulumi.get(self, "sub_type")

    @sub_type.setter
    def sub_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sub_type", value)


