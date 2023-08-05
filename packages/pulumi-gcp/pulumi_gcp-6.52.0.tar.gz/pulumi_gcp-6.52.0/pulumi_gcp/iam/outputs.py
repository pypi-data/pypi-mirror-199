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
    'AccessBoundaryPolicyRule',
    'AccessBoundaryPolicyRuleAccessBoundaryRule',
    'AccessBoundaryPolicyRuleAccessBoundaryRuleAvailabilityCondition',
    'DenyPolicyRule',
    'DenyPolicyRuleDenyRule',
    'DenyPolicyRuleDenyRuleDenialCondition',
    'WorkforcePoolProviderOidc',
    'WorkforcePoolProviderSaml',
    'WorkloadIdentityPoolProviderAws',
    'WorkloadIdentityPoolProviderOidc',
    'GetTestablePermissionsPermissionResult',
    'GetWorkloadIdentityPoolProviderAwResult',
    'GetWorkloadIdentityPoolProviderOidcResult',
]

@pulumi.output_type
class AccessBoundaryPolicyRule(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "accessBoundaryRule":
            suggest = "access_boundary_rule"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AccessBoundaryPolicyRule. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AccessBoundaryPolicyRule.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AccessBoundaryPolicyRule.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 access_boundary_rule: Optional['outputs.AccessBoundaryPolicyRuleAccessBoundaryRule'] = None,
                 description: Optional[str] = None):
        """
        :param 'AccessBoundaryPolicyRuleAccessBoundaryRuleArgs' access_boundary_rule: An access boundary rule in an IAM policy.
               Structure is documented below.
        :param str description: The description of the rule.
        """
        if access_boundary_rule is not None:
            pulumi.set(__self__, "access_boundary_rule", access_boundary_rule)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter(name="accessBoundaryRule")
    def access_boundary_rule(self) -> Optional['outputs.AccessBoundaryPolicyRuleAccessBoundaryRule']:
        """
        An access boundary rule in an IAM policy.
        Structure is documented below.
        """
        return pulumi.get(self, "access_boundary_rule")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the rule.
        """
        return pulumi.get(self, "description")


@pulumi.output_type
class AccessBoundaryPolicyRuleAccessBoundaryRule(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "availabilityCondition":
            suggest = "availability_condition"
        elif key == "availablePermissions":
            suggest = "available_permissions"
        elif key == "availableResource":
            suggest = "available_resource"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AccessBoundaryPolicyRuleAccessBoundaryRule. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AccessBoundaryPolicyRuleAccessBoundaryRule.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AccessBoundaryPolicyRuleAccessBoundaryRule.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 availability_condition: Optional['outputs.AccessBoundaryPolicyRuleAccessBoundaryRuleAvailabilityCondition'] = None,
                 available_permissions: Optional[Sequence[str]] = None,
                 available_resource: Optional[str] = None):
        """
        :param 'AccessBoundaryPolicyRuleAccessBoundaryRuleAvailabilityConditionArgs' availability_condition: The availability condition further constrains the access allowed by the access boundary rule.
               Structure is documented below.
        :param Sequence[str] available_permissions: A list of permissions that may be allowed for use on the specified resource.
        :param str available_resource: The full resource name of a Google Cloud resource entity.
        """
        if availability_condition is not None:
            pulumi.set(__self__, "availability_condition", availability_condition)
        if available_permissions is not None:
            pulumi.set(__self__, "available_permissions", available_permissions)
        if available_resource is not None:
            pulumi.set(__self__, "available_resource", available_resource)

    @property
    @pulumi.getter(name="availabilityCondition")
    def availability_condition(self) -> Optional['outputs.AccessBoundaryPolicyRuleAccessBoundaryRuleAvailabilityCondition']:
        """
        The availability condition further constrains the access allowed by the access boundary rule.
        Structure is documented below.
        """
        return pulumi.get(self, "availability_condition")

    @property
    @pulumi.getter(name="availablePermissions")
    def available_permissions(self) -> Optional[Sequence[str]]:
        """
        A list of permissions that may be allowed for use on the specified resource.
        """
        return pulumi.get(self, "available_permissions")

    @property
    @pulumi.getter(name="availableResource")
    def available_resource(self) -> Optional[str]:
        """
        The full resource name of a Google Cloud resource entity.
        """
        return pulumi.get(self, "available_resource")


@pulumi.output_type
class AccessBoundaryPolicyRuleAccessBoundaryRuleAvailabilityCondition(dict):
    def __init__(__self__, *,
                 expression: str,
                 description: Optional[str] = None,
                 location: Optional[str] = None,
                 title: Optional[str] = None):
        """
        :param str expression: Textual representation of an expression in Common Expression Language syntax.
        :param str description: Description of the expression. This is a longer text which describes the expression,
               e.g. when hovered over it in a UI.
        :param str location: String indicating the location of the expression for error reporting,
               e.g. a file name and a position in the file.
        :param str title: Title for the expression, i.e. a short string describing its purpose.
               This can be used e.g. in UIs which allow to enter the expression.
        """
        pulumi.set(__self__, "expression", expression)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if title is not None:
            pulumi.set(__self__, "title", title)

    @property
    @pulumi.getter
    def expression(self) -> str:
        """
        Textual representation of an expression in Common Expression Language syntax.
        """
        return pulumi.get(self, "expression")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Description of the expression. This is a longer text which describes the expression,
        e.g. when hovered over it in a UI.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        String indicating the location of the expression for error reporting,
        e.g. a file name and a position in the file.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def title(self) -> Optional[str]:
        """
        Title for the expression, i.e. a short string describing its purpose.
        This can be used e.g. in UIs which allow to enter the expression.
        """
        return pulumi.get(self, "title")


@pulumi.output_type
class DenyPolicyRule(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "denyRule":
            suggest = "deny_rule"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DenyPolicyRule. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DenyPolicyRule.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DenyPolicyRule.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 deny_rule: Optional['outputs.DenyPolicyRuleDenyRule'] = None,
                 description: Optional[str] = None):
        """
        :param 'DenyPolicyRuleDenyRuleArgs' deny_rule: A deny rule in an IAM deny policy.
               Structure is documented below.
        :param str description: The description of the rule.
        """
        if deny_rule is not None:
            pulumi.set(__self__, "deny_rule", deny_rule)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter(name="denyRule")
    def deny_rule(self) -> Optional['outputs.DenyPolicyRuleDenyRule']:
        """
        A deny rule in an IAM deny policy.
        Structure is documented below.
        """
        return pulumi.get(self, "deny_rule")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the rule.
        """
        return pulumi.get(self, "description")


@pulumi.output_type
class DenyPolicyRuleDenyRule(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "denialCondition":
            suggest = "denial_condition"
        elif key == "deniedPermissions":
            suggest = "denied_permissions"
        elif key == "deniedPrincipals":
            suggest = "denied_principals"
        elif key == "exceptionPermissions":
            suggest = "exception_permissions"
        elif key == "exceptionPrincipals":
            suggest = "exception_principals"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DenyPolicyRuleDenyRule. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DenyPolicyRuleDenyRule.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DenyPolicyRuleDenyRule.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 denial_condition: Optional['outputs.DenyPolicyRuleDenyRuleDenialCondition'] = None,
                 denied_permissions: Optional[Sequence[str]] = None,
                 denied_principals: Optional[Sequence[str]] = None,
                 exception_permissions: Optional[Sequence[str]] = None,
                 exception_principals: Optional[Sequence[str]] = None):
        """
        :param 'DenyPolicyRuleDenyRuleDenialConditionArgs' denial_condition: User defined CEVAL expression. A CEVAL expression is used to specify match criteria such as origin.ip, source.region_code and contents in the request header.
               Structure is documented below.
        :param Sequence[str] denied_permissions: The permissions that are explicitly denied by this rule. Each permission uses the format `{service-fqdn}/{resource}.{verb}`,
               where `{service-fqdn}` is the fully qualified domain name for the service. For example, `iam.googleapis.com/roles.list`.
        :param Sequence[str] denied_principals: The identities that are prevented from using one or more permissions on Google Cloud resources.
        :param Sequence[str] exception_permissions: Specifies the permissions that this rule excludes from the set of denied permissions given by deniedPermissions.
               If a permission appears in deniedPermissions and in exceptionPermissions then it will not be denied.
               The excluded permissions can be specified using the same syntax as deniedPermissions.
        :param Sequence[str] exception_principals: The identities that are excluded from the deny rule, even if they are listed in the deniedPrincipals.
               For example, you could add a Google group to the deniedPrincipals, then exclude specific users who belong to that group.
        """
        if denial_condition is not None:
            pulumi.set(__self__, "denial_condition", denial_condition)
        if denied_permissions is not None:
            pulumi.set(__self__, "denied_permissions", denied_permissions)
        if denied_principals is not None:
            pulumi.set(__self__, "denied_principals", denied_principals)
        if exception_permissions is not None:
            pulumi.set(__self__, "exception_permissions", exception_permissions)
        if exception_principals is not None:
            pulumi.set(__self__, "exception_principals", exception_principals)

    @property
    @pulumi.getter(name="denialCondition")
    def denial_condition(self) -> Optional['outputs.DenyPolicyRuleDenyRuleDenialCondition']:
        """
        User defined CEVAL expression. A CEVAL expression is used to specify match criteria such as origin.ip, source.region_code and contents in the request header.
        Structure is documented below.
        """
        return pulumi.get(self, "denial_condition")

    @property
    @pulumi.getter(name="deniedPermissions")
    def denied_permissions(self) -> Optional[Sequence[str]]:
        """
        The permissions that are explicitly denied by this rule. Each permission uses the format `{service-fqdn}/{resource}.{verb}`,
        where `{service-fqdn}` is the fully qualified domain name for the service. For example, `iam.googleapis.com/roles.list`.
        """
        return pulumi.get(self, "denied_permissions")

    @property
    @pulumi.getter(name="deniedPrincipals")
    def denied_principals(self) -> Optional[Sequence[str]]:
        """
        The identities that are prevented from using one or more permissions on Google Cloud resources.
        """
        return pulumi.get(self, "denied_principals")

    @property
    @pulumi.getter(name="exceptionPermissions")
    def exception_permissions(self) -> Optional[Sequence[str]]:
        """
        Specifies the permissions that this rule excludes from the set of denied permissions given by deniedPermissions.
        If a permission appears in deniedPermissions and in exceptionPermissions then it will not be denied.
        The excluded permissions can be specified using the same syntax as deniedPermissions.
        """
        return pulumi.get(self, "exception_permissions")

    @property
    @pulumi.getter(name="exceptionPrincipals")
    def exception_principals(self) -> Optional[Sequence[str]]:
        """
        The identities that are excluded from the deny rule, even if they are listed in the deniedPrincipals.
        For example, you could add a Google group to the deniedPrincipals, then exclude specific users who belong to that group.
        """
        return pulumi.get(self, "exception_principals")


@pulumi.output_type
class DenyPolicyRuleDenyRuleDenialCondition(dict):
    def __init__(__self__, *,
                 expression: str,
                 description: Optional[str] = None,
                 location: Optional[str] = None,
                 title: Optional[str] = None):
        """
        :param str expression: Textual representation of an expression in Common Expression Language syntax.
        :param str description: Description of the expression. This is a longer text which describes the expression,
               e.g. when hovered over it in a UI.
        :param str location: String indicating the location of the expression for error reporting,
               e.g. a file name and a position in the file.
        :param str title: Title for the expression, i.e. a short string describing its purpose.
               This can be used e.g. in UIs which allow to enter the expression.
        """
        pulumi.set(__self__, "expression", expression)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if title is not None:
            pulumi.set(__self__, "title", title)

    @property
    @pulumi.getter
    def expression(self) -> str:
        """
        Textual representation of an expression in Common Expression Language syntax.
        """
        return pulumi.get(self, "expression")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Description of the expression. This is a longer text which describes the expression,
        e.g. when hovered over it in a UI.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        String indicating the location of the expression for error reporting,
        e.g. a file name and a position in the file.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def title(self) -> Optional[str]:
        """
        Title for the expression, i.e. a short string describing its purpose.
        This can be used e.g. in UIs which allow to enter the expression.
        """
        return pulumi.get(self, "title")


@pulumi.output_type
class WorkforcePoolProviderOidc(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "clientId":
            suggest = "client_id"
        elif key == "issuerUri":
            suggest = "issuer_uri"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkforcePoolProviderOidc. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkforcePoolProviderOidc.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkforcePoolProviderOidc.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 client_id: str,
                 issuer_uri: str):
        """
        :param str client_id: The client ID. Must match the audience claim of the JWT issued by the identity provider.
        :param str issuer_uri: The OIDC issuer URI. Must be a valid URI using the 'https' scheme.
        """
        pulumi.set(__self__, "client_id", client_id)
        pulumi.set(__self__, "issuer_uri", issuer_uri)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> str:
        """
        The client ID. Must match the audience claim of the JWT issued by the identity provider.
        """
        return pulumi.get(self, "client_id")

    @property
    @pulumi.getter(name="issuerUri")
    def issuer_uri(self) -> str:
        """
        The OIDC issuer URI. Must be a valid URI using the 'https' scheme.
        """
        return pulumi.get(self, "issuer_uri")


@pulumi.output_type
class WorkforcePoolProviderSaml(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "idpMetadataXml":
            suggest = "idp_metadata_xml"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkforcePoolProviderSaml. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkforcePoolProviderSaml.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkforcePoolProviderSaml.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 idp_metadata_xml: str):
        """
        :param str idp_metadata_xml: SAML Identity provider configuration metadata xml doc.
               The xml document should comply with [SAML 2.0 specification](https://docs.oasis-open.org/security/saml/v2.0/saml-metadata-2.0-os.pdf).
               The max size of the acceptable xml document will be bounded to 128k characters.
               The metadata xml document should satisfy the following constraints:
               1) Must contain an Identity Provider Entity ID.
               2) Must contain at least one non-expired signing key certificate.
               3) For each signing key:
               a) Valid from should be no more than 7 days from now.
               b) Valid to should be no more than 10 years in the future.
               4) Up to 3 IdP signing keys are allowed in the metadata xml.
               When updating the provider's metadata xml, at least one non-expired signing key
               must overlap with the existing metadata. This requirement is skipped if there are
               no non-expired signing keys present in the existing metadata.
        """
        pulumi.set(__self__, "idp_metadata_xml", idp_metadata_xml)

    @property
    @pulumi.getter(name="idpMetadataXml")
    def idp_metadata_xml(self) -> str:
        """
        SAML Identity provider configuration metadata xml doc.
        The xml document should comply with [SAML 2.0 specification](https://docs.oasis-open.org/security/saml/v2.0/saml-metadata-2.0-os.pdf).
        The max size of the acceptable xml document will be bounded to 128k characters.
        The metadata xml document should satisfy the following constraints:
        1) Must contain an Identity Provider Entity ID.
        2) Must contain at least one non-expired signing key certificate.
        3) For each signing key:
        a) Valid from should be no more than 7 days from now.
        b) Valid to should be no more than 10 years in the future.
        4) Up to 3 IdP signing keys are allowed in the metadata xml.
        When updating the provider's metadata xml, at least one non-expired signing key
        must overlap with the existing metadata. This requirement is skipped if there are
        no non-expired signing keys present in the existing metadata.
        """
        return pulumi.get(self, "idp_metadata_xml")


@pulumi.output_type
class WorkloadIdentityPoolProviderAws(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "accountId":
            suggest = "account_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkloadIdentityPoolProviderAws. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkloadIdentityPoolProviderAws.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkloadIdentityPoolProviderAws.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 account_id: str):
        """
        :param str account_id: The AWS account ID.
        """
        pulumi.set(__self__, "account_id", account_id)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> str:
        """
        The AWS account ID.
        """
        return pulumi.get(self, "account_id")


@pulumi.output_type
class WorkloadIdentityPoolProviderOidc(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "issuerUri":
            suggest = "issuer_uri"
        elif key == "allowedAudiences":
            suggest = "allowed_audiences"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkloadIdentityPoolProviderOidc. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkloadIdentityPoolProviderOidc.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkloadIdentityPoolProviderOidc.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 issuer_uri: str,
                 allowed_audiences: Optional[Sequence[str]] = None):
        """
        :param str issuer_uri: The OIDC issuer URL.
        :param Sequence[str] allowed_audiences: Acceptable values for the `aud` field (audience) in the OIDC token. Token exchange
               requests are rejected if the token audience does not match one of the configured
               values. Each audience may be at most 256 characters. A maximum of 10 audiences may
               be configured.
               If this list is empty, the OIDC token audience must be equal to the full canonical
               resource name of the WorkloadIdentityPoolProvider, with or without the HTTPS prefix.
               For example:
               ```python
               import pulumi
               ```
        """
        pulumi.set(__self__, "issuer_uri", issuer_uri)
        if allowed_audiences is not None:
            pulumi.set(__self__, "allowed_audiences", allowed_audiences)

    @property
    @pulumi.getter(name="issuerUri")
    def issuer_uri(self) -> str:
        """
        The OIDC issuer URL.
        """
        return pulumi.get(self, "issuer_uri")

    @property
    @pulumi.getter(name="allowedAudiences")
    def allowed_audiences(self) -> Optional[Sequence[str]]:
        """
        Acceptable values for the `aud` field (audience) in the OIDC token. Token exchange
        requests are rejected if the token audience does not match one of the configured
        values. Each audience may be at most 256 characters. A maximum of 10 audiences may
        be configured.
        If this list is empty, the OIDC token audience must be equal to the full canonical
        resource name of the WorkloadIdentityPoolProvider, with or without the HTTPS prefix.
        For example:
        ```python
        import pulumi
        ```
        """
        return pulumi.get(self, "allowed_audiences")


@pulumi.output_type
class GetTestablePermissionsPermissionResult(dict):
    def __init__(__self__, *,
                 api_disabled: bool,
                 custom_support_level: str,
                 name: str,
                 stage: str,
                 title: str):
        """
        :param bool api_disabled: Whether the corresponding API has been enabled for the resource.
        :param str custom_support_level: The level of support for custom roles. Can be one of `"NOT_SUPPORTED"`, `"SUPPORTED"`, `"TESTING"`. Default is `"SUPPORTED"`
        :param str name: Name of the permission.
        :param str stage: Release stage of the permission.
        :param str title: Human readable title of the permission.
        """
        pulumi.set(__self__, "api_disabled", api_disabled)
        pulumi.set(__self__, "custom_support_level", custom_support_level)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "stage", stage)
        pulumi.set(__self__, "title", title)

    @property
    @pulumi.getter(name="apiDisabled")
    def api_disabled(self) -> bool:
        """
        Whether the corresponding API has been enabled for the resource.
        """
        return pulumi.get(self, "api_disabled")

    @property
    @pulumi.getter(name="customSupportLevel")
    def custom_support_level(self) -> str:
        """
        The level of support for custom roles. Can be one of `"NOT_SUPPORTED"`, `"SUPPORTED"`, `"TESTING"`. Default is `"SUPPORTED"`
        """
        return pulumi.get(self, "custom_support_level")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the permission.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def stage(self) -> str:
        """
        Release stage of the permission.
        """
        return pulumi.get(self, "stage")

    @property
    @pulumi.getter
    def title(self) -> str:
        """
        Human readable title of the permission.
        """
        return pulumi.get(self, "title")


@pulumi.output_type
class GetWorkloadIdentityPoolProviderAwResult(dict):
    def __init__(__self__, *,
                 account_id: str):
        pulumi.set(__self__, "account_id", account_id)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> str:
        return pulumi.get(self, "account_id")


@pulumi.output_type
class GetWorkloadIdentityPoolProviderOidcResult(dict):
    def __init__(__self__, *,
                 allowed_audiences: Sequence[str],
                 issuer_uri: str):
        pulumi.set(__self__, "allowed_audiences", allowed_audiences)
        pulumi.set(__self__, "issuer_uri", issuer_uri)

    @property
    @pulumi.getter(name="allowedAudiences")
    def allowed_audiences(self) -> Sequence[str]:
        return pulumi.get(self, "allowed_audiences")

    @property
    @pulumi.getter(name="issuerUri")
    def issuer_uri(self) -> str:
        return pulumi.get(self, "issuer_uri")


