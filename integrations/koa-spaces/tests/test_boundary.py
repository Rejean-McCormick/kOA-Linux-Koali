from __future__ import annotations

import ast
from copy import deepcopy
from pathlib import Path

import pytest

from koa_spaces_adapter import (
    AdapterConfig,
    HostBridge,
    ManifestValidationError,
    RouteBridge,
    RouteState,
    SpacesClient,
    build_adapter,
    validate_manifest,
)

from ._support import PACKAGE, ROOT


class HostPort:
    def __init__(self):
        self.calls = []

    def invoke(self, operation_id, parameters, *, correlation_id, idempotency_key):
        self.calls.append(
            (operation_id, dict(parameters), correlation_id, idempotency_key)
        )
        return {"state": "completed", "receipt_ref": "receipt:host-1"}


def test_host_bridge_uses_only_injected_registered_operations(transport_factory):
    host = HostPort()
    adapter = build_adapter(
        transport=transport_factory(
            {"health.read": {"state": "healthy", "ready": True, "reason": None}}
        ),
        config=AdapterConfig(
            host_start_operation_id="profile.koa_spaces.start",
            host_stop_operation_id="profile.koa_spaces.stop",
            host_status_operation_id="profile.koa_spaces.status",
        ),
        host_port=host,
    )
    result = adapter.host.start(
        profile_id="user_lightweight",
        correlation_id="corr-host-1",
        idempotency_key="start-host-1",
    )
    assert result["state"] == "completed"
    assert host.calls[0][0] == "profile.koa_spaces.start"
    assert host.calls[0][1] == {
        "subsystem_id": "koa_spaces",
        "profile_id": "user_lightweight",
    }


def test_manifest_cannot_claim_authority(module_manifest):
    altered = deepcopy(module_manifest)
    altered["authority_boundary"]["may_grant_capabilities"] = True
    with pytest.raises(ManifestValidationError, match="presentation-only"):
        validate_manifest(altered)


def test_source_boundary_has_no_private_component_import_or_direct_execution():
    prohibited_import_roots = {
        "koa_identity_and_trust",
        "koa_audit_broker",
        "koa_resource_governor",
        "koa_governance_policy_runtime",
        "koa_mediatheque",
        "koa_publication_gateway",
    }
    prohibited_modules = {"sqlite3", "subprocess", "ctypes", "pty", "resource"}
    for path in PACKAGE.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert "TODO" not in source
        assert "pass\n" not in source
        tree = ast.parse(source, filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = {alias.name.split(".")[0] for alias in node.names}
                assert not names & prohibited_import_roots
                assert not names & prohibited_modules
            elif isinstance(node, ast.ImportFrom) and node.module:
                root = node.module.split(".")[0]
                assert root not in prohibited_import_roots
                assert root not in prohibited_modules
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                assert node.func.id not in {"eval", "exec", "compile"}


def test_only_declared_bundle_files_exist():
    allowed = {
        'integrations/koa-spaces/README.md',
        'integrations/koa-spaces/adapter/pyproject.toml',
        'integrations/koa-spaces/adapter/src/koa_spaces_adapter/__init__.py',
        'integrations/koa-spaces/adapter/src/koa_spaces_adapter/appearance.py',
        'integrations/koa-spaces/adapter/src/koa_spaces_adapter/bootstrap.py',
        'integrations/koa-spaces/adapter/src/koa_spaces_adapter/capabilities.py',
        'integrations/koa-spaces/adapter/src/koa_spaces_adapter/client.py',
        'integrations/koa-spaces/adapter/src/koa_spaces_adapter/health.py',
        'integrations/koa-spaces/adapter/src/koa_spaces_adapter/host_bridge.py',
        'integrations/koa-spaces/adapter/src/koa_spaces_adapter/module_manifest.py',
        'integrations/koa-spaces/adapter/src/koa_spaces_adapter/native_workspace.py',
        'integrations/koa-spaces/adapter/src/koa_spaces_adapter/receipts.py',
        'integrations/koa-spaces/adapter/src/koa_spaces_adapter/route_bridge.py',
        'integrations/koa-spaces/adapter/src/koa_spaces_adapter/space_activation.py',
        'integrations/koa-spaces/adapter/src/koa_spaces_adapter/unix_transport.py',
        'integrations/koa-spaces/backup.toml',
        'integrations/koa-spaces/compatibility.json',
        'integrations/koa-spaces/degradation.toml',
        'integrations/koa-spaces/deployment.toml',
        'integrations/koa-spaces/health.toml',
        'integrations/koa-spaces/integration.toml',
        'integrations/koa-spaces/interface/appearance/accent-palette.json',
        'integrations/koa-spaces/interface/community-space.json',
        'integrations/koa-spaces/interface/default-space.json',
        'integrations/koa-spaces/interface/global-widgets.json',
        'integrations/koa-spaces/interface/school-space.json',
        'integrations/koa-spaces/resource-envelope.toml',
        'integrations/koa-spaces/source.lock.json',
        'integrations/koa-spaces/storage.toml',
        'integrations/koa-spaces/tests/_support.py',
        'integrations/koa-spaces/tests/conftest.py',
        'integrations/koa-spaces/tests/test_boundary.py',
        'integrations/koa-spaces/tests/test_capability_projection.py',
        'integrations/koa-spaces/tests/test_contract.py',
        'integrations/koa-spaces/tests/test_degradation.py',
        'integrations/koa-spaces/tests/test_health.py',
        'integrations/koa-spaces/adapter/src/koa_spaces_adapter/interface_assets.py',
        'integrations/koa-spaces/adapter/src/koa_spaces_adapter/interface_theme.py',
        'integrations/koa-spaces/adapter/src/koa_spaces_adapter/shell_state.py',
        'integrations/koa-spaces/interface/icons/home.svg',
        'integrations/koa-spaces/interface/icons/search.svg',
        'integrations/koa-spaces/interface/icons/network.svg',
        'integrations/koa-spaces/interface/icons/learn.svg',
        'integrations/koa-spaces/interface/icons/library.svg',
        'integrations/koa-spaces/interface/icons/assignments.svg',
        'integrations/koa-spaces/interface/icons/guidance.svg',
        'integrations/koa-spaces/interface/icons/community.svg',
        'integrations/koa-spaces/interface/icons/work.svg',
        'integrations/koa-spaces/interface/themes/default.json',
        'integrations/koa-spaces/interface/themes/school.json',
        'integrations/koa-spaces/interface/themes/community.json',
        'integrations/koa-spaces/interface/localization/koa-spaces.en.json',
        'integrations/koa-spaces/interface/localization/koa-spaces.fr-CA.json',
        'integrations/koa-spaces/tests/test_ks2_contract_convergence.py',
        'integrations/koa-spaces/tests/test_native_workspace_bridge.py',
        'integrations/koa-spaces/tests/test_interface_assets.py',
        'integrations/koa-spaces/tests/test_interface_theme.py',
        'integrations/koa-spaces/tests/test_unix_transport.py',
        'integrations/koa-spaces/tests/test_shell_state.py',
    }
    actual = {
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "integrations/koa-spaces").rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }
    assert actual == allowed
