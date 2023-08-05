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
    'NoteAttestationAuthorityArgs',
    'NoteAttestationAuthorityHintArgs',
    'NoteRelatedUrlArgs',
    'OccurenceAttestationArgs',
    'OccurenceAttestationSignatureArgs',
]

@pulumi.input_type
class NoteAttestationAuthorityArgs:
    def __init__(__self__, *,
                 hint: pulumi.Input['NoteAttestationAuthorityHintArgs']):
        """
        :param pulumi.Input['NoteAttestationAuthorityHintArgs'] hint: This submessage provides human-readable hints about the purpose of
               the AttestationAuthority. Because the name of a Note acts as its
               resource reference, it is important to disambiguate the canonical
               name of the Note (which might be a UUID for security purposes)
               from "readable" names more suitable for debug output. Note that
               these hints should NOT be used to look up AttestationAuthorities
               in security sensitive contexts, such as when looking up
               Attestations to verify.
               Structure is documented below.
        """
        pulumi.set(__self__, "hint", hint)

    @property
    @pulumi.getter
    def hint(self) -> pulumi.Input['NoteAttestationAuthorityHintArgs']:
        """
        This submessage provides human-readable hints about the purpose of
        the AttestationAuthority. Because the name of a Note acts as its
        resource reference, it is important to disambiguate the canonical
        name of the Note (which might be a UUID for security purposes)
        from "readable" names more suitable for debug output. Note that
        these hints should NOT be used to look up AttestationAuthorities
        in security sensitive contexts, such as when looking up
        Attestations to verify.
        Structure is documented below.
        """
        return pulumi.get(self, "hint")

    @hint.setter
    def hint(self, value: pulumi.Input['NoteAttestationAuthorityHintArgs']):
        pulumi.set(self, "hint", value)


@pulumi.input_type
class NoteAttestationAuthorityHintArgs:
    def __init__(__self__, *,
                 human_readable_name: pulumi.Input[str]):
        """
        :param pulumi.Input[str] human_readable_name: The human readable name of this Attestation Authority, for
               example "qa".
        """
        pulumi.set(__self__, "human_readable_name", human_readable_name)

    @property
    @pulumi.getter(name="humanReadableName")
    def human_readable_name(self) -> pulumi.Input[str]:
        """
        The human readable name of this Attestation Authority, for
        example "qa".
        """
        return pulumi.get(self, "human_readable_name")

    @human_readable_name.setter
    def human_readable_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "human_readable_name", value)


@pulumi.input_type
class NoteRelatedUrlArgs:
    def __init__(__self__, *,
                 url: pulumi.Input[str],
                 label: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] url: Specific URL associated with the resource.
        :param pulumi.Input[str] label: Label to describe usage of the URL
        """
        pulumi.set(__self__, "url", url)
        if label is not None:
            pulumi.set(__self__, "label", label)

    @property
    @pulumi.getter
    def url(self) -> pulumi.Input[str]:
        """
        Specific URL associated with the resource.
        """
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: pulumi.Input[str]):
        pulumi.set(self, "url", value)

    @property
    @pulumi.getter
    def label(self) -> Optional[pulumi.Input[str]]:
        """
        Label to describe usage of the URL
        """
        return pulumi.get(self, "label")

    @label.setter
    def label(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "label", value)


@pulumi.input_type
class OccurenceAttestationArgs:
    def __init__(__self__, *,
                 serialized_payload: pulumi.Input[str],
                 signatures: pulumi.Input[Sequence[pulumi.Input['OccurenceAttestationSignatureArgs']]]):
        """
        :param pulumi.Input[str] serialized_payload: The serialized payload that is verified by one or
               more signatures. A base64-encoded string.
        :param pulumi.Input[Sequence[pulumi.Input['OccurenceAttestationSignatureArgs']]] signatures: One or more signatures over serializedPayload.
               Verifier implementations should consider this attestation
               message verified if at least one signature verifies
               serializedPayload. See Signature in common.proto for more
               details on signature structure and verification.
               Structure is documented below.
        """
        pulumi.set(__self__, "serialized_payload", serialized_payload)
        pulumi.set(__self__, "signatures", signatures)

    @property
    @pulumi.getter(name="serializedPayload")
    def serialized_payload(self) -> pulumi.Input[str]:
        """
        The serialized payload that is verified by one or
        more signatures. A base64-encoded string.
        """
        return pulumi.get(self, "serialized_payload")

    @serialized_payload.setter
    def serialized_payload(self, value: pulumi.Input[str]):
        pulumi.set(self, "serialized_payload", value)

    @property
    @pulumi.getter
    def signatures(self) -> pulumi.Input[Sequence[pulumi.Input['OccurenceAttestationSignatureArgs']]]:
        """
        One or more signatures over serializedPayload.
        Verifier implementations should consider this attestation
        message verified if at least one signature verifies
        serializedPayload. See Signature in common.proto for more
        details on signature structure and verification.
        Structure is documented below.
        """
        return pulumi.get(self, "signatures")

    @signatures.setter
    def signatures(self, value: pulumi.Input[Sequence[pulumi.Input['OccurenceAttestationSignatureArgs']]]):
        pulumi.set(self, "signatures", value)


@pulumi.input_type
class OccurenceAttestationSignatureArgs:
    def __init__(__self__, *,
                 public_key_id: pulumi.Input[str],
                 signature: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] public_key_id: The identifier for the public key that verifies this
               signature. MUST be an RFC3986 conformant
               URI. * When possible, the key id should be an
               immutable reference, such as a cryptographic digest.
               Examples of valid values:
               * OpenPGP V4 public key fingerprint. See https://www.iana.org/assignments/uri-schemes/prov/openpgp4fpr
               for more details on this scheme.
               * `openpgp4fpr:74FAF3B861BDA0870C7B6DEF607E48D2A663AEEA`
               * RFC6920 digest-named SubjectPublicKeyInfo (digest of the DER serialization):
               * "ni:///sha-256;cD9o9Cq6LG3jD0iKXqEi_vdjJGecm_iXkbqVoScViaU"
        :param pulumi.Input[str] signature: The content of the signature, an opaque bytestring.
               The payload that this signature verifies MUST be
               unambiguously provided with the Signature during
               verification. A wrapper message might provide the
               payload explicitly. Alternatively, a message might
               have a canonical serialization that can always be
               unambiguously computed to derive the payload.
        """
        pulumi.set(__self__, "public_key_id", public_key_id)
        if signature is not None:
            pulumi.set(__self__, "signature", signature)

    @property
    @pulumi.getter(name="publicKeyId")
    def public_key_id(self) -> pulumi.Input[str]:
        """
        The identifier for the public key that verifies this
        signature. MUST be an RFC3986 conformant
        URI. * When possible, the key id should be an
        immutable reference, such as a cryptographic digest.
        Examples of valid values:
        * OpenPGP V4 public key fingerprint. See https://www.iana.org/assignments/uri-schemes/prov/openpgp4fpr
        for more details on this scheme.
        * `openpgp4fpr:74FAF3B861BDA0870C7B6DEF607E48D2A663AEEA`
        * RFC6920 digest-named SubjectPublicKeyInfo (digest of the DER serialization):
        * "ni:///sha-256;cD9o9Cq6LG3jD0iKXqEi_vdjJGecm_iXkbqVoScViaU"
        """
        return pulumi.get(self, "public_key_id")

    @public_key_id.setter
    def public_key_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "public_key_id", value)

    @property
    @pulumi.getter
    def signature(self) -> Optional[pulumi.Input[str]]:
        """
        The content of the signature, an opaque bytestring.
        The payload that this signature verifies MUST be
        unambiguously provided with the Signature during
        verification. A wrapper message might provide the
        payload explicitly. Alternatively, a message might
        have a canonical serialization that can always be
        unambiguously computed to derive the payload.
        """
        return pulumi.get(self, "signature")

    @signature.setter
    def signature(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "signature", value)


