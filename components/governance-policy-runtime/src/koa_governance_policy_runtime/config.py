"""Strict, side-effect-free Governance Policy Runtime configuration."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import ClassVar, Mapping
import re


class ConfigurationError(ValueError):
    """Raised when startup configuration violates the component contract."""


class ActivationMode(StrEnum):
    ALWAYS_AVAILABLE = "always_available"
    SOCKET_ACTIVATED = "socket_activated"
    TASK_ACTIVATED = "task_activated"
    EMBEDDED = "embedded_behind_registered_interface"


class AuditEvidencePolicy(StrEnum):
    NOT_REQUIRED = "not_required"
    LOCAL_BUFFER_PERMITTED = "local_buffer_permitted"
    REQUIRED_DELIVERY = "required_delivery"


_REFERENCE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@+-]{0,254}$")


@dataclass(frozen=True, slots=True)
class GovernancePolicyRuntimeConfig:
    """Validated startup references and operational policy.

    The configuration never contains policy source, evaluation context, raw
    assertions, credentials, signatures, or secrets. Profile and release logic
    provide those values through registered interfaces rather than configuration fields.
    """

    COMPONENT_ID: ClassVar[str] = "governance_policy_runtime"
    CONTRACT_VERSION: ClassVar[str] = "1.0.0"
    INTERFACE_VERSION: ClassVar[str] = "1.0.0"
    RUNTIME_VERSION: ClassVar[str] = "0.1.0"
    ENV_PREFIX: ClassVar[str] = "KOA_GOVERNANCE_POLICY_RUNTIME_"
    SUPPORTED_ENV_KEYS: ClassVar[frozenset[str]] = frozenset(
        {
            "ACTIVATION_MODE",
            "AUDIT_EVIDENCE_POLICY",
            "COMPONENT_ID",
            "CONTRACT_VERSION",
            "INTERFACE_VERSION",
            "OFFLINE_GOVERNED_OPERATION",
            "POLICY_BUNDLE_DIRECTORY",
            "PROFILE_REF",
            "RECEIPT_DIRECTORY",
            "RUNTIME_DIRECTORY",
            "RUNTIME_VERSION",
            "SERVICE_IDENTITY",
            "STATE_DIRECTORY",
            "UNIX_SOCKET_PATH",
        }
    )

    component_id: str = COMPONENT_ID
    contract_version: str = CONTRACT_VERSION
    interface_version: str = INTERFACE_VERSION
    runtime_version: str = RUNTIME_VERSION
    service_identity: str = COMPONENT_ID
    profile_ref: str = "profile:unresolved"
    activation_mode: ActivationMode = ActivationMode.SOCKET_ACTIVATED
    audit_evidence_policy: AuditEvidencePolicy = AuditEvidencePolicy.NOT_REQUIRED
    offline_governed_operation: bool = False
    unix_socket_path: Path = Path(
        "/run/koa/governance-policy-runtime/governance-policy-runtime.sock"
    )
    state_directory: Path = Path("/var/lib/koa/governance-policy-runtime")
    runtime_directory: Path = Path("/run/koa/governance-policy-runtime")
    policy_bundle_directory: Path = Path(
        "/var/lib/koa/governance-policy-runtime/policy-bundles"
    )
    receipt_directory: Path = Path("/var/lib/koa/governance-policy-runtime/receipts")

    def __post_init__(self) -> None:
        errors: list[str] = []
        if self.component_id != self.COMPONENT_ID:
            errors.append(f"component_id must be {self.COMPONENT_ID!r}")
        if self.contract_version != self.CONTRACT_VERSION:
            errors.append(f"unsupported contract_version {self.contract_version!r}")
        if self.interface_version != self.INTERFACE_VERSION:
            errors.append(f"unsupported interface_version {self.interface_version!r}")
        if self.runtime_version != self.RUNTIME_VERSION:
            errors.append(f"unsupported runtime_version {self.runtime_version!r}")
        for name, value in (
            ("service_identity", self.service_identity),
            ("profile_ref", self.profile_ref),
        ):
            if not _REFERENCE.fullmatch(value):
                errors.append(f"{name} must be a bounded reference")

        paths = {
            "unix_socket_path": self.unix_socket_path,
            "state_directory": self.state_directory,
            "runtime_directory": self.runtime_directory,
            "policy_bundle_directory": self.policy_bundle_directory,
            "receipt_directory": self.receipt_directory,
        }
        for name, value in paths.items():
            if not value.is_absolute():
                errors.append(f"{name} must be absolute")
            if ".." in value.parts:
                errors.append(f"{name} must not contain parent traversal")

        if self.unix_socket_path.parent != self.runtime_directory:
            errors.append("unix_socket_path must be directly inside runtime_directory")
        if self.state_directory == self.runtime_directory:
            errors.append("state_directory and runtime_directory must remain distinct")
        if not self.policy_bundle_directory.is_relative_to(self.state_directory):
            errors.append("policy_bundle_directory must be inside state_directory")
        if not self.receipt_directory.is_relative_to(self.state_directory):
            errors.append("receipt_directory must be inside state_directory")
        if self.policy_bundle_directory == self.receipt_directory:
            errors.append("policy_bundle_directory and receipt_directory must remain distinct")
        if self.offline_governed_operation and self.profile_ref == "profile:unresolved":
            errors.append("offline governed operation requires an explicit profile_ref")

        if errors:
            raise ConfigurationError("; ".join(errors))

    @classmethod
    def from_environment(
        cls, environment: Mapping[str, str] | None = None
    ) -> GovernancePolicyRuntimeConfig:
        """Load only registered environment keys and reject implicit extensions."""

        env = MappingProxyType(dict(environment or {}))
        prefix = cls.ENV_PREFIX
        supplied = {key[len(prefix) :] for key in env if key.startswith(prefix)}
        unknown = sorted(supplied - cls.SUPPORTED_ENV_KEYS)
        if unknown:
            raise ConfigurationError(
                "unsupported environment keys: "
                + ", ".join(prefix + key for key in unknown)
            )

        def value(name: str, default: str) -> str:
            return env.get(prefix + name, default).strip()

        def enum_value(name: str, enum_type: type[StrEnum], default: StrEnum) -> StrEnum:
            raw = value(name, str(default))
            try:
                return enum_type(raw)
            except ValueError as exc:
                choices = ", ".join(member.value for member in enum_type)
                raise ConfigurationError(
                    f"{prefix}{name} must be one of: {choices}"
                ) from exc

        def bool_value(name: str, default: bool) -> bool:
            raw = value(name, "true" if default else "false").lower()
            if raw == "true":
                return True
            if raw == "false":
                return False
            raise ConfigurationError(f"{prefix}{name} must be true or false")

        return cls(
            component_id=value("COMPONENT_ID", cls.COMPONENT_ID),
            contract_version=value("CONTRACT_VERSION", cls.CONTRACT_VERSION),
            interface_version=value("INTERFACE_VERSION", cls.INTERFACE_VERSION),
            runtime_version=value("RUNTIME_VERSION", cls.RUNTIME_VERSION),
            service_identity=value("SERVICE_IDENTITY", cls.COMPONENT_ID),
            profile_ref=value("PROFILE_REF", "profile:unresolved"),
            activation_mode=enum_value(
                "ACTIVATION_MODE", ActivationMode, ActivationMode.SOCKET_ACTIVATED
            ),
            audit_evidence_policy=enum_value(
                "AUDIT_EVIDENCE_POLICY",
                AuditEvidencePolicy,
                AuditEvidencePolicy.NOT_REQUIRED,
            ),
            offline_governed_operation=bool_value("OFFLINE_GOVERNED_OPERATION", False),
            unix_socket_path=Path(
                value(
                    "UNIX_SOCKET_PATH",
                    "/run/koa/governance-policy-runtime/governance-policy-runtime.sock",
                )
            ),
            state_directory=Path(
                value("STATE_DIRECTORY", "/var/lib/koa/governance-policy-runtime")
            ),
            runtime_directory=Path(
                value("RUNTIME_DIRECTORY", "/run/koa/governance-policy-runtime")
            ),
            policy_bundle_directory=Path(
                value(
                    "POLICY_BUNDLE_DIRECTORY",
                    "/var/lib/koa/governance-policy-runtime/policy-bundles",
                )
            ),
            receipt_directory=Path(
                value(
                    "RECEIPT_DIRECTORY",
                    "/var/lib/koa/governance-policy-runtime/receipts",
                )
            ),
        )

    def as_public_dict(self) -> dict[str, object]:
        """Return a deterministic non-sensitive configuration projection."""

        return {
            "activation_mode": self.activation_mode.value,
            "audit_evidence_policy": self.audit_evidence_policy.value,
            "component_id": self.component_id,
            "contract_version": self.contract_version,
            "interface_version": self.interface_version,
            "offline_governed_operation": self.offline_governed_operation,
            "policy_bundle_directory": str(self.policy_bundle_directory),
            "profile_ref": self.profile_ref,
            "receipt_directory": str(self.receipt_directory),
            "runtime_directory": str(self.runtime_directory),
            "runtime_version": self.runtime_version,
            "service_identity": self.service_identity,
            "state_directory": str(self.state_directory),
            "unix_socket_path": str(self.unix_socket_path),
        }
