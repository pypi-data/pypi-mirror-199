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
    'AccessApprovalSettingsEnrolledServiceArgs',
    'IAMBindingConditionArgs',
    'IAMMemberConditionArgs',
    'IamAuditConfigAuditLogConfigArgs',
    'PolicyBooleanPolicyArgs',
    'PolicyListPolicyArgs',
    'PolicyListPolicyAllowArgs',
    'PolicyListPolicyDenyArgs',
    'PolicyRestorePolicyArgs',
    'GetIAMPolicyAuditConfigArgs',
    'GetIAMPolicyAuditConfigAuditLogConfigArgs',
    'GetIAMPolicyBindingArgs',
    'GetIAMPolicyBindingConditionArgs',
]

@pulumi.input_type
class AccessApprovalSettingsEnrolledServiceArgs:
    def __init__(__self__, *,
                 cloud_product: pulumi.Input[str],
                 enrollment_level: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] cloud_product: The product for which Access Approval will be enrolled. Allowed values are listed (case-sensitive):
               all
               appengine.googleapis.com
               bigquery.googleapis.com
               bigtable.googleapis.com
               cloudkms.googleapis.com
               compute.googleapis.com
               dataflow.googleapis.com
               iam.googleapis.com
               pubsub.googleapis.com
               storage.googleapis.com
        :param pulumi.Input[str] enrollment_level: The enrollment level of the service.
               Default value is `BLOCK_ALL`.
               Possible values are `BLOCK_ALL`.
        """
        pulumi.set(__self__, "cloud_product", cloud_product)
        if enrollment_level is not None:
            pulumi.set(__self__, "enrollment_level", enrollment_level)

    @property
    @pulumi.getter(name="cloudProduct")
    def cloud_product(self) -> pulumi.Input[str]:
        """
        The product for which Access Approval will be enrolled. Allowed values are listed (case-sensitive):
        all
        appengine.googleapis.com
        bigquery.googleapis.com
        bigtable.googleapis.com
        cloudkms.googleapis.com
        compute.googleapis.com
        dataflow.googleapis.com
        iam.googleapis.com
        pubsub.googleapis.com
        storage.googleapis.com
        """
        return pulumi.get(self, "cloud_product")

    @cloud_product.setter
    def cloud_product(self, value: pulumi.Input[str]):
        pulumi.set(self, "cloud_product", value)

    @property
    @pulumi.getter(name="enrollmentLevel")
    def enrollment_level(self) -> Optional[pulumi.Input[str]]:
        """
        The enrollment level of the service.
        Default value is `BLOCK_ALL`.
        Possible values are `BLOCK_ALL`.
        """
        return pulumi.get(self, "enrollment_level")

    @enrollment_level.setter
    def enrollment_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "enrollment_level", value)


@pulumi.input_type
class IAMBindingConditionArgs:
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
class IAMMemberConditionArgs:
    def __init__(__self__, *,
                 expression: pulumi.Input[str],
                 title: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] expression: Textual representation of an expression in Common Expression Language syntax.
        :param pulumi.Input[str] title: A title for the expression, i.e. a short string describing its purpose.
        :param pulumi.Input[str] description: An optional description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        """
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> pulumi.Input[str]:
        """
        Textual representation of an expression in Common Expression Language syntax.
        """
        return pulumi.get(self, "expression")

    @expression.setter
    def expression(self, value: pulumi.Input[str]):
        pulumi.set(self, "expression", value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        """
        A title for the expression, i.e. a short string describing its purpose.
        """
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, "title", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        An optional description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class IamAuditConfigAuditLogConfigArgs:
    def __init__(__self__, *,
                 log_type: pulumi.Input[str],
                 exempted_members: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[str] log_type: Permission type for which logging is to be configured.  Must be one of `DATA_READ`, `DATA_WRITE`, or `ADMIN_READ`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] exempted_members: Identities that do not cause logging for this type of permission.
               Each entry can have one of the following values:
               * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
               * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
               * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
               * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
        """
        pulumi.set(__self__, "log_type", log_type)
        if exempted_members is not None:
            pulumi.set(__self__, "exempted_members", exempted_members)

    @property
    @pulumi.getter(name="logType")
    def log_type(self) -> pulumi.Input[str]:
        """
        Permission type for which logging is to be configured.  Must be one of `DATA_READ`, `DATA_WRITE`, or `ADMIN_READ`.
        """
        return pulumi.get(self, "log_type")

    @log_type.setter
    def log_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "log_type", value)

    @property
    @pulumi.getter(name="exemptedMembers")
    def exempted_members(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Identities that do not cause logging for this type of permission.
        Each entry can have one of the following values:
        * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
        * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
        * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
        * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
        """
        return pulumi.get(self, "exempted_members")

    @exempted_members.setter
    def exempted_members(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "exempted_members", value)


@pulumi.input_type
class PolicyBooleanPolicyArgs:
    def __init__(__self__, *,
                 enforced: pulumi.Input[bool]):
        """
        :param pulumi.Input[bool] enforced: If true, then the Policy is enforced. If false, then any configuration is acceptable.
        """
        pulumi.set(__self__, "enforced", enforced)

    @property
    @pulumi.getter
    def enforced(self) -> pulumi.Input[bool]:
        """
        If true, then the Policy is enforced. If false, then any configuration is acceptable.
        """
        return pulumi.get(self, "enforced")

    @enforced.setter
    def enforced(self, value: pulumi.Input[bool]):
        pulumi.set(self, "enforced", value)


@pulumi.input_type
class PolicyListPolicyArgs:
    def __init__(__self__, *,
                 allow: Optional[pulumi.Input['PolicyListPolicyAllowArgs']] = None,
                 deny: Optional[pulumi.Input['PolicyListPolicyDenyArgs']] = None,
                 inherit_from_parent: Optional[pulumi.Input[bool]] = None,
                 suggested_value: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input['PolicyListPolicyAllowArgs'] allow: or `deny` - (Optional) One or the other must be set.
        :param pulumi.Input[bool] inherit_from_parent: If set to true, the values from the effective Policy of the parent resource
               are inherited, meaning the values set in this Policy are added to the values inherited up the hierarchy.
        :param pulumi.Input[str] suggested_value: The Google Cloud Console will try to default to a configuration that matches the value specified in this field.
        """
        if allow is not None:
            pulumi.set(__self__, "allow", allow)
        if deny is not None:
            pulumi.set(__self__, "deny", deny)
        if inherit_from_parent is not None:
            pulumi.set(__self__, "inherit_from_parent", inherit_from_parent)
        if suggested_value is not None:
            pulumi.set(__self__, "suggested_value", suggested_value)

    @property
    @pulumi.getter
    def allow(self) -> Optional[pulumi.Input['PolicyListPolicyAllowArgs']]:
        """
        or `deny` - (Optional) One or the other must be set.
        """
        return pulumi.get(self, "allow")

    @allow.setter
    def allow(self, value: Optional[pulumi.Input['PolicyListPolicyAllowArgs']]):
        pulumi.set(self, "allow", value)

    @property
    @pulumi.getter
    def deny(self) -> Optional[pulumi.Input['PolicyListPolicyDenyArgs']]:
        return pulumi.get(self, "deny")

    @deny.setter
    def deny(self, value: Optional[pulumi.Input['PolicyListPolicyDenyArgs']]):
        pulumi.set(self, "deny", value)

    @property
    @pulumi.getter(name="inheritFromParent")
    def inherit_from_parent(self) -> Optional[pulumi.Input[bool]]:
        """
        If set to true, the values from the effective Policy of the parent resource
        are inherited, meaning the values set in this Policy are added to the values inherited up the hierarchy.
        """
        return pulumi.get(self, "inherit_from_parent")

    @inherit_from_parent.setter
    def inherit_from_parent(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "inherit_from_parent", value)

    @property
    @pulumi.getter(name="suggestedValue")
    def suggested_value(self) -> Optional[pulumi.Input[str]]:
        """
        The Google Cloud Console will try to default to a configuration that matches the value specified in this field.
        """
        return pulumi.get(self, "suggested_value")

    @suggested_value.setter
    def suggested_value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "suggested_value", value)


@pulumi.input_type
class PolicyListPolicyAllowArgs:
    def __init__(__self__, *,
                 all: Optional[pulumi.Input[bool]] = None,
                 values: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[bool] all: The policy allows or denies all values.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] values: The policy can define specific values that are allowed or denied.
        """
        if all is not None:
            pulumi.set(__self__, "all", all)
        if values is not None:
            pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def all(self) -> Optional[pulumi.Input[bool]]:
        """
        The policy allows or denies all values.
        """
        return pulumi.get(self, "all")

    @all.setter
    def all(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "all", value)

    @property
    @pulumi.getter
    def values(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The policy can define specific values that are allowed or denied.
        """
        return pulumi.get(self, "values")

    @values.setter
    def values(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "values", value)


@pulumi.input_type
class PolicyListPolicyDenyArgs:
    def __init__(__self__, *,
                 all: Optional[pulumi.Input[bool]] = None,
                 values: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[bool] all: The policy allows or denies all values.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] values: The policy can define specific values that are allowed or denied.
        """
        if all is not None:
            pulumi.set(__self__, "all", all)
        if values is not None:
            pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def all(self) -> Optional[pulumi.Input[bool]]:
        """
        The policy allows or denies all values.
        """
        return pulumi.get(self, "all")

    @all.setter
    def all(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "all", value)

    @property
    @pulumi.getter
    def values(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The policy can define specific values that are allowed or denied.
        """
        return pulumi.get(self, "values")

    @values.setter
    def values(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "values", value)


@pulumi.input_type
class PolicyRestorePolicyArgs:
    def __init__(__self__, *,
                 default: pulumi.Input[bool]):
        """
        :param pulumi.Input[bool] default: May only be set to true. If set, then the default Policy is restored.
        """
        pulumi.set(__self__, "default", default)

    @property
    @pulumi.getter
    def default(self) -> pulumi.Input[bool]:
        """
        May only be set to true. If set, then the default Policy is restored.
        """
        return pulumi.get(self, "default")

    @default.setter
    def default(self, value: pulumi.Input[bool]):
        pulumi.set(self, "default", value)


@pulumi.input_type
class GetIAMPolicyAuditConfigArgs:
    def __init__(__self__, *,
                 audit_log_configs: Sequence['GetIAMPolicyAuditConfigAuditLogConfigArgs'],
                 service: str):
        """
        :param Sequence['GetIAMPolicyAuditConfigAuditLogConfigArgs'] audit_log_configs: A nested block that defines the operations you'd like to log.
        :param str service: Defines a service that will be enabled for audit logging. For example, `storage.googleapis.com`, `cloudsql.googleapis.com`. `allServices` is a special value that covers all services.
        """
        pulumi.set(__self__, "audit_log_configs", audit_log_configs)
        pulumi.set(__self__, "service", service)

    @property
    @pulumi.getter(name="auditLogConfigs")
    def audit_log_configs(self) -> Sequence['GetIAMPolicyAuditConfigAuditLogConfigArgs']:
        """
        A nested block that defines the operations you'd like to log.
        """
        return pulumi.get(self, "audit_log_configs")

    @audit_log_configs.setter
    def audit_log_configs(self, value: Sequence['GetIAMPolicyAuditConfigAuditLogConfigArgs']):
        pulumi.set(self, "audit_log_configs", value)

    @property
    @pulumi.getter
    def service(self) -> str:
        """
        Defines a service that will be enabled for audit logging. For example, `storage.googleapis.com`, `cloudsql.googleapis.com`. `allServices` is a special value that covers all services.
        """
        return pulumi.get(self, "service")

    @service.setter
    def service(self, value: str):
        pulumi.set(self, "service", value)


@pulumi.input_type
class GetIAMPolicyAuditConfigAuditLogConfigArgs:
    def __init__(__self__, *,
                 log_type: str,
                 exempted_members: Optional[Sequence[str]] = None):
        """
        :param str log_type: Defines the logging level. `DATA_READ`, `DATA_WRITE` and `ADMIN_READ` capture different types of events. See [the audit configuration documentation](https://cloud.google.com/resource-manager/reference/rest/Shared.Types/AuditConfig) for more details.
        :param Sequence[str] exempted_members: Specifies the identities that are exempt from these types of logging operations. Follows the same format of the `members` array for `binding`.
        """
        pulumi.set(__self__, "log_type", log_type)
        if exempted_members is not None:
            pulumi.set(__self__, "exempted_members", exempted_members)

    @property
    @pulumi.getter(name="logType")
    def log_type(self) -> str:
        """
        Defines the logging level. `DATA_READ`, `DATA_WRITE` and `ADMIN_READ` capture different types of events. See [the audit configuration documentation](https://cloud.google.com/resource-manager/reference/rest/Shared.Types/AuditConfig) for more details.
        """
        return pulumi.get(self, "log_type")

    @log_type.setter
    def log_type(self, value: str):
        pulumi.set(self, "log_type", value)

    @property
    @pulumi.getter(name="exemptedMembers")
    def exempted_members(self) -> Optional[Sequence[str]]:
        """
        Specifies the identities that are exempt from these types of logging operations. Follows the same format of the `members` array for `binding`.
        """
        return pulumi.get(self, "exempted_members")

    @exempted_members.setter
    def exempted_members(self, value: Optional[Sequence[str]]):
        pulumi.set(self, "exempted_members", value)


@pulumi.input_type
class GetIAMPolicyBindingArgs:
    def __init__(__self__, *,
                 members: Sequence[str],
                 role: str,
                 condition: Optional['GetIAMPolicyBindingConditionArgs'] = None):
        """
        :param Sequence[str] members: An array of identities that will be granted the privilege in the `role`. For more details on format and restrictions see https://cloud.google.com/billing/reference/rest/v1/Policy#Binding
               Each entry can have one of the following values:
               * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account. Some resources **don't** support this identity.
               * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account. Some resources **don't** support this identity.
               * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com.
               * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
               * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
               * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
        :param str role: The role/permission that will be granted to the members.
               See the [IAM Roles](https://cloud.google.com/compute/docs/access/iam) documentation for a complete list of roles.
               Note that custom roles must be of the format `[projects|organizations]/{parent-name}/roles/{role-name}`.
        :param 'GetIAMPolicyBindingConditionArgs' condition: An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding. Structure is documented below.
        """
        pulumi.set(__self__, "members", members)
        pulumi.set(__self__, "role", role)
        if condition is not None:
            pulumi.set(__self__, "condition", condition)

    @property
    @pulumi.getter
    def members(self) -> Sequence[str]:
        """
        An array of identities that will be granted the privilege in the `role`. For more details on format and restrictions see https://cloud.google.com/billing/reference/rest/v1/Policy#Binding
        Each entry can have one of the following values:
        * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account. Some resources **don't** support this identity.
        * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account. Some resources **don't** support this identity.
        * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com.
        * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
        * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
        * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
        """
        return pulumi.get(self, "members")

    @members.setter
    def members(self, value: Sequence[str]):
        pulumi.set(self, "members", value)

    @property
    @pulumi.getter
    def role(self) -> str:
        """
        The role/permission that will be granted to the members.
        See the [IAM Roles](https://cloud.google.com/compute/docs/access/iam) documentation for a complete list of roles.
        Note that custom roles must be of the format `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: str):
        pulumi.set(self, "role", value)

    @property
    @pulumi.getter
    def condition(self) -> Optional['GetIAMPolicyBindingConditionArgs']:
        """
        An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding. Structure is documented below.
        """
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional['GetIAMPolicyBindingConditionArgs']):
        pulumi.set(self, "condition", value)


@pulumi.input_type
class GetIAMPolicyBindingConditionArgs:
    def __init__(__self__, *,
                 expression: str,
                 title: str,
                 description: Optional[str] = None):
        """
        :param str expression: Textual representation of an expression in Common Expression Language syntax.
        :param str title: A title for the expression, i.e. a short string describing its purpose.
        :param str description: An optional description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        """
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> str:
        """
        Textual representation of an expression in Common Expression Language syntax.
        """
        return pulumi.get(self, "expression")

    @expression.setter
    def expression(self, value: str):
        pulumi.set(self, "expression", value)

    @property
    @pulumi.getter
    def title(self) -> str:
        """
        A title for the expression, i.e. a short string describing its purpose.
        """
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: str):
        pulumi.set(self, "title", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        An optional description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[str]):
        pulumi.set(self, "description", value)


