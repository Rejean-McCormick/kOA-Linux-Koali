"""Public Identity and Trust runtime surface.

The component also contains domain, application, port, adapter, API, migration,
and integration layers. This module intentionally re-exports only the bounded
bootstrap, configuration, health, and receipt surface.
"""

from .bootstrap import BootstrapResult, RuntimeObservation, bootstrap
from .config import ConfigurationError, IdentityTrustConfig, Profile
from .health import (
    Capability,
    CheckResult,
    CheckState,
    ComponentStatus,
    OperationalState,
    evaluate_status,
)
from .receipts import (
    Receipt,
    ReceiptClass,
    ReceiptError,
    ReceiptOutcome,
    ReceiptPathUnavailable,
    create_receipt,
)

__all__ = [
    "BootstrapResult",
    "Capability",
    "CheckResult",
    "CheckState",
    "ComponentStatus",
    "ConfigurationError",
    "IdentityTrustConfig",
    "OperationalState",
    "Profile",
    "Receipt",
    "ReceiptClass",
    "ReceiptError",
    "ReceiptOutcome",
    "ReceiptPathUnavailable",
    "RuntimeObservation",
    "bootstrap",
    "create_receipt",
    "evaluate_status",
]

__version__ = "1.0.0"
COMPONENT_ID = "identity_and_trust"
COMPONENT_CONTRACT_VERSION = "1.0.0"
