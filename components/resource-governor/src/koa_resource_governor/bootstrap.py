"""Resource Governor bootstrap and bounded runtime observation wiring."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import os
from pathlib import Path
from typing import Mapping

from .config import (
    EnforcementAdapterMode,
    ObservationSourceMode,
    QueueBackendMode,
    ReceiptMode,
    ResourceGovernorConfig,
)
from .health import (
    Capability,
    CheckResult,
    CheckState,
    ComponentStatus,
    PressureState,
    evaluate_status,
)


@dataclass(frozen=True, slots=True)
class RuntimeObservation:
    """Bounded observations supplied by runtime adapters and orchestration layers."""

    runtime_ready: CheckState = CheckState.UNKNOWN
    profile_resolved: CheckState = CheckState.UNKNOWN
    envelopes_resolved: CheckState = CheckState.UNKNOWN
    enforcement_adapter_ready: CheckState = CheckState.UNKNOWN
    observation_source_ready: CheckState = CheckState.UNKNOWN
    queue_backend_ready: CheckState = CheckState.UNKNOWN
    allocation_state_reconciled: CheckState = CheckState.UNKNOWN
    schema_and_contract_versions_supported: CheckState = CheckState.PASS
    state_root_accessible: CheckState = CheckState.UNKNOWN
    runtime_root_accessible: CheckState = CheckState.UNKNOWN
    pressure_state: PressureState = PressureState.UNKNOWN
    active_envelope_refs: tuple[str, ...] = ()
    active_workloads: int = 0
    queued_workloads: int = 0
    orphaned_execution_count: int = 0
    component_implementation_ready: bool = False
    restoring: bool = False

    def __post_init__(self) -> None:
        for name in (
            "runtime_ready",
            "profile_resolved",
            "envelopes_resolved",
            "enforcement_adapter_ready",
            "observation_source_ready",
            "queue_backend_ready",
            "allocation_state_reconciled",
            "schema_and_contract_versions_supported",
            "state_root_accessible",
            "runtime_root_accessible",
        ):
            object.__setattr__(self, name, CheckState(getattr(self, name)))
        object.__setattr__(self, "pressure_state", PressureState(self.pressure_state))
        for value, name in (
            (self.active_workloads, "active_workloads"),
            (self.queued_workloads, "queued_workloads"),
            (self.orphaned_execution_count, "orphaned_execution_count"),
        ):
            if value < 0:
                raise ValueError(f"{name} cannot be negative")

    @classmethod
    def probe_local_paths(cls, config: ResourceGovernorConfig) -> RuntimeObservation:
        """Probe local path accessibility without creating or mutating state."""
        return cls(
            runtime_ready=CheckState.PASS,
            state_root_accessible=_directory_check(config.state_root),
            runtime_root_accessible=_directory_check(config.runtime_root),
        )


@dataclass(frozen=True, slots=True)
class BootstrapResult:
    config: ResourceGovernorConfig
    status: ComponentStatus
    started_at: datetime
    process_id: int

    def to_dict(self, *, view: str = "operational") -> dict[str, object]:
        return {
            "config": self.config.public_dict(),
            "status": self.status.to_dict(view=view),
            "started_at": self.started_at.astimezone(UTC).isoformat().replace("+00:00", "Z"),
            "process_id": self.process_id,
        }


def _directory_check(path: Path) -> CheckState:
    if not path.exists() or not path.is_dir():
        return CheckState.UNKNOWN
    if os.access(path, os.R_OK | os.X_OK):
        return CheckState.PASS
    return CheckState.FAIL


def _check(check_id: str, state: CheckState, reason: str) -> CheckResult:
    state = CheckState(state)
    return CheckResult(check_id, state, None if state is CheckState.PASS else reason)


def _adapter_check(config: ResourceGovernorConfig, observed: CheckState) -> CheckResult:
    check_id = "enforcement_adapter_ready"
    if config.enforcement_adapter_mode is EnforcementAdapterMode.UNAVAILABLE:
        return CheckResult(check_id, CheckState.FAIL, "ENFORCEMENT_ADAPTER_UNAVAILABLE")
    if config.enforcement_adapter_mode is EnforcementAdapterMode.DEGRADED:
        return CheckResult(check_id, CheckState.DEGRADED, "ENFORCEMENT_ADAPTER_DEGRADED")
    return _check(check_id, observed, "ENFORCEMENT_ADAPTER_NOT_VERIFIED")


def _observation_check(config: ResourceGovernorConfig, observed: CheckState) -> CheckResult:
    check_id = "observation_source_ready"
    if config.observation_source_mode is ObservationSourceMode.UNAVAILABLE:
        return CheckResult(check_id, CheckState.FAIL, "OBSERVATION_SOURCE_UNAVAILABLE")
    if config.observation_source_mode is ObservationSourceMode.STALE:
        return CheckResult(check_id, CheckState.DEGRADED, "OBSERVATION_SOURCE_STALE")
    return _check(check_id, observed, "OBSERVATION_SOURCE_NOT_VERIFIED")


def _queue_check(config: ResourceGovernorConfig, observed: CheckState) -> CheckResult:
    check_id = "queue_backend_ready"
    if config.queue_backend_mode is QueueBackendMode.UNAVAILABLE:
        return CheckResult(check_id, CheckState.DEGRADED, "QUEUE_BACKEND_UNAVAILABLE")
    if config.queue_backend_mode is QueueBackendMode.VOLATILE:
        return CheckResult(check_id, CheckState.DEGRADED, "QUEUE_BACKEND_NOT_DURABLE")
    return _check(check_id, observed, "QUEUE_BACKEND_NOT_VERIFIED")


def _receipt_check(config: ResourceGovernorConfig) -> CheckResult:
    check_id = "receipt_sink_available"
    if config.receipt_mode is ReceiptMode.DURABLE:
        return CheckResult(check_id, CheckState.PASS)
    if config.receipt_mode is ReceiptMode.BUFFERED:
        return CheckResult(check_id, CheckState.DEGRADED, "RECEIPT_DELIVERY_BUFFERED")
    return CheckResult(check_id, CheckState.DEGRADED, "RECEIPT_SINK_UNAVAILABLE")


def _pressure_check(pressure_state: PressureState) -> CheckResult:
    check_id = "resource_pressure_state"
    if pressure_state is PressureState.NORMAL:
        return CheckResult(check_id, CheckState.PASS)
    if pressure_state is PressureState.UNKNOWN:
        return CheckResult(check_id, CheckState.UNKNOWN, "RESOURCE_PRESSURE_UNKNOWN")
    return CheckResult(check_id, CheckState.DEGRADED, pressure_state.value.upper())


def bootstrap(
    config: ResourceGovernorConfig,
    *,
    observation: RuntimeObservation | None = None,
    started_at: datetime | None = None,
) -> BootstrapResult:
    """Evaluate startup without activating envelopes or admitting workloads."""
    observed = observation or RuntimeObservation.probe_local_paths(config)
    start = started_at or datetime.now(UTC)
    if start.tzinfo is None:
        raise ValueError("started_at must be timezone-aware")

    health_checks: Mapping[str, CheckResult] = {
        "runtime_ready": _check("runtime_ready", observed.runtime_ready, "RUNTIME_NOT_READY"),
        "state_root_accessible": _check(
            "state_root_accessible", observed.state_root_accessible, "STATE_ROOT_NOT_ACCESSIBLE"
        ),
        "runtime_root_accessible": _check(
            "runtime_root_accessible", observed.runtime_root_accessible, "RUNTIME_ROOT_NOT_ACCESSIBLE"
        ),
        "queue_backend_ready": _queue_check(config, observed.queue_backend_ready),
        "resource_pressure_state": _pressure_check(observed.pressure_state),
        "receipt_sink_available": _receipt_check(config),
    }
    readiness_checks: Mapping[str, CheckResult] = {
        "profile_resolved": _check(
            "profile_resolved", observed.profile_resolved, "ACTIVE_PROFILE_NOT_RESOLVED"
        ),
        "envelopes_resolved": _check(
            "envelopes_resolved", observed.envelopes_resolved, "ACTIVE_ENVELOPE_NOT_RESOLVED"
        ),
        "enforcement_adapter_ready": _adapter_check(config, observed.enforcement_adapter_ready),
        "observation_source_ready": _observation_check(config, observed.observation_source_ready),
        "allocation_state_reconciled": _check(
            "allocation_state_reconciled",
            observed.allocation_state_reconciled,
            "ALLOCATION_STATE_NOT_RECONCILED",
        ),
        "schema_and_contract_versions_supported": _check(
            "schema_and_contract_versions_supported",
            observed.schema_and_contract_versions_supported,
            "CONTRACT_OR_SCHEMA_VERSION_UNSUPPORTED",
        ),
    }

    available: set[Capability] = set()
    degraded: set[Capability] = set()
    blocked: set[Capability] = set()

    implementation_ready = observed.component_implementation_ready
    profile_ready = observed.profile_resolved is CheckState.PASS
    envelopes_ready = observed.envelopes_resolved is CheckState.PASS
    adapter_ready = (
        config.enforcement_adapter_mode is EnforcementAdapterMode.AVAILABLE
        and observed.enforcement_adapter_ready is CheckState.PASS
    )
    observation_ready = (
        config.observation_source_mode is ObservationSourceMode.AVAILABLE
        and observed.observation_source_ready is CheckState.PASS
    )
    reconciled = (
        observed.allocation_state_reconciled is CheckState.PASS
        or not config.reconciliation_required
    )
    contracts_ready = observed.schema_and_contract_versions_supported is CheckState.PASS

    if implementation_ready and profile_ready and envelopes_ready and contracts_ready:
        available.add(Capability.ENVELOPE_RESOLUTION)
    else:
        blocked.add(Capability.ENVELOPE_RESOLUTION)

    core_ready = implementation_ready and profile_ready and envelopes_ready and adapter_ready and reconciled
    if core_ready and observation_ready and contracts_ready:
        available.update(
            {
                Capability.WORKLOAD_ADMISSION,
                Capability.RUNTIME_ENFORCEMENT,
                Capability.PRIORITY_SCHEDULING,
                Capability.CONCURRENCY_CONTROL,
            }
        )
    elif core_ready and config.allow_low_risk_without_observation and contracts_ready:
        degraded.add(Capability.WORKLOAD_ADMISSION)
        available.update(
            {
                Capability.RUNTIME_ENFORCEMENT,
                Capability.PRIORITY_SCHEDULING,
                Capability.CONCURRENCY_CONTROL,
            }
        )
    else:
        blocked.update(
            {
                Capability.WORKLOAD_ADMISSION,
                Capability.RUNTIME_ENFORCEMENT,
                Capability.PRIORITY_SCHEDULING,
                Capability.CONCURRENCY_CONTROL,
            }
        )

    if implementation_ready and observation_ready:
        available.add(Capability.RESOURCE_OBSERVABILITY)
    elif implementation_ready and config.allow_low_risk_without_observation:
        degraded.add(Capability.RESOURCE_OBSERVABILITY)
    else:
        blocked.add(Capability.RESOURCE_OBSERVABILITY)

    if implementation_ready and observed.pressure_state is not PressureState.UNKNOWN:
        if observed.pressure_state is PressureState.NORMAL:
            available.add(Capability.PRESSURE_DEGRADATION)
        else:
            degraded.add(Capability.PRESSURE_DEGRADATION)
    else:
        blocked.add(Capability.PRESSURE_DEGRADATION)

    if (
        implementation_ready
        and config.queue_backend_mode is QueueBackendMode.DURABLE
        and observed.queue_backend_ready is CheckState.PASS
    ):
        available.add(Capability.QUEUE_MANAGEMENT)
    elif implementation_ready and config.queue_backend_mode is QueueBackendMode.VOLATILE:
        degraded.add(Capability.QUEUE_MANAGEMENT)
    else:
        blocked.add(Capability.QUEUE_MANAGEMENT)

    critical_transitions_ready = config.receipt_mode is ReceiptMode.DURABLE
    checks_observed = not any(
        result.state is CheckState.UNKNOWN
        for result in (*health_checks.values(), *readiness_checks.values())
    )
    startup_complete = implementation_ready and checks_observed and not observed.restoring
    if not implementation_ready:
        startup_stage = "waiting_for_component_implementation"
    elif observed.restoring:
        startup_stage = "reconciling_verified_state"
    elif not checks_observed:
        startup_stage = "waiting_for_runtime_dependencies"
    else:
        startup_stage = "ready_evaluated"

    status = evaluate_status(
        instance_id=config.instance_id,
        health_checks=health_checks,
        readiness_checks=readiness_checks,
        startup_stage=startup_stage,
        startup_complete=startup_complete,
        restoring=observed.restoring,
        pressure_state=observed.pressure_state,
        available_capabilities=available,
        degraded_capabilities=degraded,
        blocked_capabilities=blocked,
        critical_transitions_ready=critical_transitions_ready,
        active_envelope_refs=observed.active_envelope_refs,
        active_workloads=observed.active_workloads,
        queued_workloads=observed.queued_workloads,
        orphaned_execution_count=observed.orphaned_execution_count,
    )
    return BootstrapResult(config=config, status=status, started_at=start, process_id=os.getpid())
