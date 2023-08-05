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
    'CryptoKeyIAMBindingCondition',
    'CryptoKeyIAMMemberCondition',
    'CryptoKeyVersionAttestation',
    'CryptoKeyVersionAttestationCertChains',
    'CryptoKeyVersionAttestationExternalProtectionLevelOptions',
    'CryptoKeyVersionTemplate',
    'KeyRingIAMBindingCondition',
    'KeyRingIAMMemberCondition',
    'KeyRingImportJobAttestation',
    'KeyRingImportJobPublicKey',
    'RegistryCredential',
    'RegistryEventNotificationConfigItem',
    'GetKMSCryptoKeyVersionPublicKeyResult',
    'GetKMSCryptoKeyVersionTemplateResult',
]

@pulumi.output_type
class CryptoKeyIAMBindingCondition(dict):
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

    @property
    @pulumi.getter
    def title(self) -> str:
        """
        A title for the expression, i.e. a short string describing its purpose.
        """
        return pulumi.get(self, "title")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        An optional description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        """
        return pulumi.get(self, "description")


@pulumi.output_type
class CryptoKeyIAMMemberCondition(dict):
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

    @property
    @pulumi.getter
    def title(self) -> str:
        """
        A title for the expression, i.e. a short string describing its purpose.
        """
        return pulumi.get(self, "title")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        An optional description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        """
        return pulumi.get(self, "description")


@pulumi.output_type
class CryptoKeyVersionAttestation(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "certChains":
            suggest = "cert_chains"
        elif key == "externalProtectionLevelOptions":
            suggest = "external_protection_level_options"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CryptoKeyVersionAttestation. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CryptoKeyVersionAttestation.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CryptoKeyVersionAttestation.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cert_chains: Optional['outputs.CryptoKeyVersionAttestationCertChains'] = None,
                 content: Optional[str] = None,
                 external_protection_level_options: Optional['outputs.CryptoKeyVersionAttestationExternalProtectionLevelOptions'] = None,
                 format: Optional[str] = None):
        """
        :param 'CryptoKeyVersionAttestationCertChainsArgs' cert_chains: The certificate chains needed to validate the attestation
               Structure is documented below.
        :param str content: (Output)
               The attestation data provided by the HSM when the key operation was performed.
        :param 'CryptoKeyVersionAttestationExternalProtectionLevelOptionsArgs' external_protection_level_options: ExternalProtectionLevelOptions stores a group of additional fields for configuring a CryptoKeyVersion that are specific to the EXTERNAL protection level and EXTERNAL_VPC protection levels.
               Structure is documented below.
        :param str format: (Output)
               The format of the attestation data.
        """
        if cert_chains is not None:
            pulumi.set(__self__, "cert_chains", cert_chains)
        if content is not None:
            pulumi.set(__self__, "content", content)
        if external_protection_level_options is not None:
            pulumi.set(__self__, "external_protection_level_options", external_protection_level_options)
        if format is not None:
            pulumi.set(__self__, "format", format)

    @property
    @pulumi.getter(name="certChains")
    def cert_chains(self) -> Optional['outputs.CryptoKeyVersionAttestationCertChains']:
        """
        The certificate chains needed to validate the attestation
        Structure is documented below.
        """
        return pulumi.get(self, "cert_chains")

    @property
    @pulumi.getter
    def content(self) -> Optional[str]:
        """
        (Output)
        The attestation data provided by the HSM when the key operation was performed.
        """
        return pulumi.get(self, "content")

    @property
    @pulumi.getter(name="externalProtectionLevelOptions")
    def external_protection_level_options(self) -> Optional['outputs.CryptoKeyVersionAttestationExternalProtectionLevelOptions']:
        """
        ExternalProtectionLevelOptions stores a group of additional fields for configuring a CryptoKeyVersion that are specific to the EXTERNAL protection level and EXTERNAL_VPC protection levels.
        Structure is documented below.
        """
        return pulumi.get(self, "external_protection_level_options")

    @property
    @pulumi.getter
    def format(self) -> Optional[str]:
        """
        (Output)
        The format of the attestation data.
        """
        return pulumi.get(self, "format")


@pulumi.output_type
class CryptoKeyVersionAttestationCertChains(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "caviumCerts":
            suggest = "cavium_certs"
        elif key == "googleCardCerts":
            suggest = "google_card_certs"
        elif key == "googlePartitionCerts":
            suggest = "google_partition_certs"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CryptoKeyVersionAttestationCertChains. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CryptoKeyVersionAttestationCertChains.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CryptoKeyVersionAttestationCertChains.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cavium_certs: Optional[str] = None,
                 google_card_certs: Optional[str] = None,
                 google_partition_certs: Optional[str] = None):
        """
        :param str cavium_certs: Cavium certificate chain corresponding to the attestation.
        :param str google_card_certs: Google card certificate chain corresponding to the attestation.
        :param str google_partition_certs: Google partition certificate chain corresponding to the attestation.
        """
        if cavium_certs is not None:
            pulumi.set(__self__, "cavium_certs", cavium_certs)
        if google_card_certs is not None:
            pulumi.set(__self__, "google_card_certs", google_card_certs)
        if google_partition_certs is not None:
            pulumi.set(__self__, "google_partition_certs", google_partition_certs)

    @property
    @pulumi.getter(name="caviumCerts")
    def cavium_certs(self) -> Optional[str]:
        """
        Cavium certificate chain corresponding to the attestation.
        """
        return pulumi.get(self, "cavium_certs")

    @property
    @pulumi.getter(name="googleCardCerts")
    def google_card_certs(self) -> Optional[str]:
        """
        Google card certificate chain corresponding to the attestation.
        """
        return pulumi.get(self, "google_card_certs")

    @property
    @pulumi.getter(name="googlePartitionCerts")
    def google_partition_certs(self) -> Optional[str]:
        """
        Google partition certificate chain corresponding to the attestation.
        """
        return pulumi.get(self, "google_partition_certs")


@pulumi.output_type
class CryptoKeyVersionAttestationExternalProtectionLevelOptions(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "ekmConnectionKeyPath":
            suggest = "ekm_connection_key_path"
        elif key == "externalKeyUri":
            suggest = "external_key_uri"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CryptoKeyVersionAttestationExternalProtectionLevelOptions. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CryptoKeyVersionAttestationExternalProtectionLevelOptions.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CryptoKeyVersionAttestationExternalProtectionLevelOptions.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 ekm_connection_key_path: Optional[str] = None,
                 external_key_uri: Optional[str] = None):
        """
        :param str ekm_connection_key_path: The path to the external key material on the EKM when using EkmConnection e.g., "v0/my/key". Set this field instead of externalKeyUri when using an EkmConnection.
        :param str external_key_uri: The URI for an external resource that this CryptoKeyVersion represents.
        """
        if ekm_connection_key_path is not None:
            pulumi.set(__self__, "ekm_connection_key_path", ekm_connection_key_path)
        if external_key_uri is not None:
            pulumi.set(__self__, "external_key_uri", external_key_uri)

    @property
    @pulumi.getter(name="ekmConnectionKeyPath")
    def ekm_connection_key_path(self) -> Optional[str]:
        """
        The path to the external key material on the EKM when using EkmConnection e.g., "v0/my/key". Set this field instead of externalKeyUri when using an EkmConnection.
        """
        return pulumi.get(self, "ekm_connection_key_path")

    @property
    @pulumi.getter(name="externalKeyUri")
    def external_key_uri(self) -> Optional[str]:
        """
        The URI for an external resource that this CryptoKeyVersion represents.
        """
        return pulumi.get(self, "external_key_uri")


@pulumi.output_type
class CryptoKeyVersionTemplate(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "protectionLevel":
            suggest = "protection_level"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CryptoKeyVersionTemplate. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CryptoKeyVersionTemplate.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CryptoKeyVersionTemplate.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 algorithm: str,
                 protection_level: Optional[str] = None):
        """
        :param str algorithm: The algorithm to use when creating a version based on this template.
               See the [algorithm reference](https://cloud.google.com/kms/docs/reference/rest/v1/CryptoKeyVersionAlgorithm) for possible inputs.
        :param str protection_level: The protection level to use when creating a version based on this template. Possible values include "SOFTWARE", "HSM", "EXTERNAL", "EXTERNAL_VPC". Defaults to "SOFTWARE".
        """
        pulumi.set(__self__, "algorithm", algorithm)
        if protection_level is not None:
            pulumi.set(__self__, "protection_level", protection_level)

    @property
    @pulumi.getter
    def algorithm(self) -> str:
        """
        The algorithm to use when creating a version based on this template.
        See the [algorithm reference](https://cloud.google.com/kms/docs/reference/rest/v1/CryptoKeyVersionAlgorithm) for possible inputs.
        """
        return pulumi.get(self, "algorithm")

    @property
    @pulumi.getter(name="protectionLevel")
    def protection_level(self) -> Optional[str]:
        """
        The protection level to use when creating a version based on this template. Possible values include "SOFTWARE", "HSM", "EXTERNAL", "EXTERNAL_VPC". Defaults to "SOFTWARE".
        """
        return pulumi.get(self, "protection_level")


@pulumi.output_type
class KeyRingIAMBindingCondition(dict):
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

    @property
    @pulumi.getter
    def title(self) -> str:
        """
        A title for the expression, i.e. a short string describing its purpose.
        """
        return pulumi.get(self, "title")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        An optional description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        """
        return pulumi.get(self, "description")


@pulumi.output_type
class KeyRingIAMMemberCondition(dict):
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

    @property
    @pulumi.getter
    def title(self) -> str:
        """
        A title for the expression, i.e. a short string describing its purpose.
        """
        return pulumi.get(self, "title")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        An optional description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        """
        return pulumi.get(self, "description")


@pulumi.output_type
class KeyRingImportJobAttestation(dict):
    def __init__(__self__, *,
                 content: Optional[str] = None,
                 format: Optional[str] = None):
        """
        :param str content: (Output)
               The attestation data provided by the HSM when the key operation was performed.
               A base64-encoded string.
        :param str format: (Output)
               The format of the attestation data.
        """
        if content is not None:
            pulumi.set(__self__, "content", content)
        if format is not None:
            pulumi.set(__self__, "format", format)

    @property
    @pulumi.getter
    def content(self) -> Optional[str]:
        """
        (Output)
        The attestation data provided by the HSM when the key operation was performed.
        A base64-encoded string.
        """
        return pulumi.get(self, "content")

    @property
    @pulumi.getter
    def format(self) -> Optional[str]:
        """
        (Output)
        The format of the attestation data.
        """
        return pulumi.get(self, "format")


@pulumi.output_type
class KeyRingImportJobPublicKey(dict):
    def __init__(__self__, *,
                 pem: Optional[str] = None):
        """
        :param str pem: (Output)
               The public key, encoded in PEM format. For more information, see the RFC 7468 sections
               for General Considerations and Textual Encoding of Subject Public Key Info.
        """
        if pem is not None:
            pulumi.set(__self__, "pem", pem)

    @property
    @pulumi.getter
    def pem(self) -> Optional[str]:
        """
        (Output)
        The public key, encoded in PEM format. For more information, see the RFC 7468 sections
        for General Considerations and Textual Encoding of Subject Public Key Info.
        """
        return pulumi.get(self, "pem")


@pulumi.output_type
class RegistryCredential(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "publicKeyCertificate":
            suggest = "public_key_certificate"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RegistryCredential. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RegistryCredential.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RegistryCredential.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 public_key_certificate: Mapping[str, Any]):
        """
        :param Mapping[str, Any] public_key_certificate: A public key certificate format and data.
        """
        pulumi.set(__self__, "public_key_certificate", public_key_certificate)

    @property
    @pulumi.getter(name="publicKeyCertificate")
    def public_key_certificate(self) -> Mapping[str, Any]:
        """
        A public key certificate format and data.
        """
        return pulumi.get(self, "public_key_certificate")


@pulumi.output_type
class RegistryEventNotificationConfigItem(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "pubsubTopicName":
            suggest = "pubsub_topic_name"
        elif key == "subfolderMatches":
            suggest = "subfolder_matches"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RegistryEventNotificationConfigItem. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RegistryEventNotificationConfigItem.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RegistryEventNotificationConfigItem.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 pubsub_topic_name: str,
                 subfolder_matches: Optional[str] = None):
        """
        :param str pubsub_topic_name: PubSub topic name to publish device events.
        :param str subfolder_matches: If the subfolder name matches this string exactly, this
               configuration will be used. The string must not include the
               leading '/' character. If empty, all strings are matched. Empty
               value can only be used for the last `event_notification_configs`
               item.
        """
        pulumi.set(__self__, "pubsub_topic_name", pubsub_topic_name)
        if subfolder_matches is not None:
            pulumi.set(__self__, "subfolder_matches", subfolder_matches)

    @property
    @pulumi.getter(name="pubsubTopicName")
    def pubsub_topic_name(self) -> str:
        """
        PubSub topic name to publish device events.
        """
        return pulumi.get(self, "pubsub_topic_name")

    @property
    @pulumi.getter(name="subfolderMatches")
    def subfolder_matches(self) -> Optional[str]:
        """
        If the subfolder name matches this string exactly, this
        configuration will be used. The string must not include the
        leading '/' character. If empty, all strings are matched. Empty
        value can only be used for the last `event_notification_configs`
        item.
        """
        return pulumi.get(self, "subfolder_matches")


@pulumi.output_type
class GetKMSCryptoKeyVersionPublicKeyResult(dict):
    def __init__(__self__, *,
                 algorithm: str,
                 pem: str):
        """
        :param str algorithm: The CryptoKeyVersionAlgorithm that this CryptoKeyVersion supports.
        :param str pem: The public key, encoded in PEM format. For more information, see the RFC 7468 sections for General Considerations and Textual Encoding of Subject Public Key Info.
        """
        pulumi.set(__self__, "algorithm", algorithm)
        pulumi.set(__self__, "pem", pem)

    @property
    @pulumi.getter
    def algorithm(self) -> str:
        """
        The CryptoKeyVersionAlgorithm that this CryptoKeyVersion supports.
        """
        return pulumi.get(self, "algorithm")

    @property
    @pulumi.getter
    def pem(self) -> str:
        """
        The public key, encoded in PEM format. For more information, see the RFC 7468 sections for General Considerations and Textual Encoding of Subject Public Key Info.
        """
        return pulumi.get(self, "pem")


@pulumi.output_type
class GetKMSCryptoKeyVersionTemplateResult(dict):
    def __init__(__self__, *,
                 algorithm: str,
                 protection_level: str):
        pulumi.set(__self__, "algorithm", algorithm)
        pulumi.set(__self__, "protection_level", protection_level)

    @property
    @pulumi.getter
    def algorithm(self) -> str:
        return pulumi.get(self, "algorithm")

    @property
    @pulumi.getter(name="protectionLevel")
    def protection_level(self) -> str:
        return pulumi.get(self, "protection_level")


