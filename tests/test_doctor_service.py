from pathlib import Path
from types import SimpleNamespace

from modelctl_core.launcher.base import LaunchRequest
from modelctl_core.services.doctor_service import DoctorService


class FakeConfig:
    path = Path("/tmp/modelctl-config.json")

    def __init__(self, data):
        self.data = data

    def load(self):
        return self.data


class FakeCredentials:
    def __init__(self, token=None):
        self.token = token

    def load(self, provider):
        return self.token


class FakeProvider:
    id = "openrouter"


class FakeProviders:
    def list(self):
        return [FakeProvider()]


class FakeLauncher:
    display_name = "Claude Code"

    def __init__(self, available=True, warning=None, metadata=None):
        self._available = available
        self.warning = warning
        self.request = None
        self.metadata = metadata

    def available(self):
        if isinstance(self._available, BaseException):
            raise self._available
        return self._available

    def compatibility_warning(self, request):
        self.request = request
        return self.warning


class FakeLaunchers:
    def __init__(self, launcher=None, *, extra=None, records=None):
        self.launcher = launcher
        self.extra = extra or {}
        self.records = records or []

    def get(self, launcher_id):
        if launcher_id == "claude":
            return self.launcher
        return self.extra.get(launcher_id)

    def diagnostics(self):
        return list(self.records)


class FakeConnection:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return None

    def execute(self, statement):
        return statement


class FakeEngine:
    def connect(self):
        return FakeConnection()


def plugin_record(
    launcher_id: str,
    *,
    status: str = "loaded",
    source: str = "modelctl-custom==1.0.0",
    plugin_id: str | None = "example.plugin",
    error: str | None = None,
):
    return SimpleNamespace(
        launcher_id=launcher_id,
        source=source,
        status=status,
        display_name=None,
        plugin_id=plugin_id,
        error=error,
    )


def service_for(config, launchers, token="token"):
    return DoctorService(
        FakeConfig(config),
        FakeCredentials(token),
        FakeProviders(),
        launchers,
        FakeEngine(),
    )


def test_doctor_reports_working_configuration(monkeypatch):
    monkeypatch.setattr(Path, "exists", lambda self: True)
    launcher = FakeLauncher()
    service = service_for(
        {
            "provider": "openrouter",
            "default_model": "anthropic/claude-sonnet-4",
            "launcher": "claude",
        },
        FakeLaunchers(launcher),
    )

    checks = service.run()

    assert all(check.status == "ok" for check in checks)
    assert launcher.request == LaunchRequest(
        model="anthropic/claude-sonnet-4",
        provider="openrouter",
    )


def test_doctor_reports_missing_runtime_selection(monkeypatch):
    monkeypatch.setattr(Path, "exists", lambda self: False)
    service = service_for(
        {},
        FakeLaunchers(FakeLauncher(available=False)),
        token=None,
    )

    checks = {check.name: check for check in service.run()}

    assert checks["Configuration"].status == "warning"
    assert checks["Provider"].status == "error"
    assert checks["Model"].status == "error"
    assert checks["Credential"].status == "warning"
    assert checks["Compatibility"].status == "warning"


def test_doctor_reports_launcher_compatibility_warning(monkeypatch):
    monkeypatch.setattr(Path, "exists", lambda self: True)
    service = service_for(
        {
            "provider": "openrouter",
            "default_model": "anthropic/claude-sonnet-4",
            "launcher": "claude",
        },
        FakeLaunchers(FakeLauncher(warning="Potential mismatch")),
    )

    checks = {check.name: check for check in service.run()}

    assert checks["Compatibility"].status == "warning"
    assert checks["Compatibility"].detail == "Potential mismatch"


def test_doctor_reports_loaded_plugin_origin_contract_and_availability(monkeypatch):
    monkeypatch.setattr(Path, "exists", lambda self: True)
    plugin = FakeLauncher(
        available=True,
        metadata=SimpleNamespace(
            plugin_id="example.plugin",
            launcher_id="custom",
            contract_version="1.0",
        ),
    )
    service = service_for(
        {
            "provider": "openrouter",
            "default_model": "custom-model",
            "launcher": "custom",
        },
        FakeLaunchers(
            FakeLauncher(),
            extra={"custom": plugin},
            records=[plugin_record("custom")],
        ),
    )

    checks = {check.name: check for check in service.run()}
    check = checks["Launcher plugin custom"]

    assert check.status == "ok"
    assert "modelctl-custom==1.0.0" in check.detail
    assert "plugin=example.plugin" in check.detail
    assert "contract=1.0 compatible" in check.detail
    assert "executable=available" in check.detail


def test_doctor_reports_unselected_broken_and_duplicate_plugins_as_warnings(monkeypatch):
    monkeypatch.setattr(Path, "exists", lambda self: True)
    service = service_for(
        {
            "provider": "openrouter",
            "default_model": "anthropic/claude-sonnet-4",
            "launcher": "claude",
        },
        FakeLaunchers(
            FakeLauncher(),
            records=[
                plugin_record(
                    "broken",
                    status="error",
                    source="broken-plugin==1.0.0",
                    plugin_id=None,
                    error="ImportError: boom",
                ),
                plugin_record(
                    "custom",
                    status="duplicate",
                    source="duplicate-plugin==1.0.0",
                    plugin_id=None,
                    error="Multiple installed entry points claim the same launcher ID.",
                ),
            ],
        ),
    )

    checks = {check.name: check for check in service.run()}

    assert checks["Launcher plugin broken"].status == "warning"
    assert "ImportError: boom" in checks["Launcher plugin broken"].detail
    assert checks["Launcher plugin custom"].status == "warning"
    assert "duplicate" in checks["Launcher plugin custom"].detail


def test_doctor_escalates_selected_plugin_load_failure_to_error(monkeypatch):
    monkeypatch.setattr(Path, "exists", lambda self: True)
    service = service_for(
        {
            "provider": "openrouter",
            "default_model": "custom-model",
            "launcher": "broken",
        },
        FakeLaunchers(
            FakeLauncher(),
            records=[
                plugin_record(
                    "broken",
                    status="error",
                    source="broken-plugin==1.0.0",
                    plugin_id=None,
                    error="ImportError: boom",
                )
            ],
        ),
    )

    checks = {check.name: check for check in service.run()}

    assert checks["Launcher"].status == "error"
    assert checks["Launcher plugin broken"].status == "error"
    assert "ImportError: boom" in checks["Launcher plugin broken"].detail


def test_doctor_reports_plugin_availability_check_failure(monkeypatch):
    monkeypatch.setattr(Path, "exists", lambda self: True)
    plugin = FakeLauncher(
        available=RuntimeError("probe failed"),
        metadata=SimpleNamespace(
            plugin_id="example.plugin",
            launcher_id="custom",
            contract_version="1.0",
        ),
    )
    service = service_for(
        {
            "provider": "openrouter",
            "default_model": "custom-model",
            "launcher": "claude",
        },
        FakeLaunchers(
            FakeLauncher(),
            extra={"custom": plugin},
            records=[plugin_record("custom")],
        ),
    )

    checks = {check.name: check for check in service.run()}
    check = checks["Launcher plugin custom"]

    assert check.status == "warning"
    assert "availability check failed" in check.detail
    assert "RuntimeError: probe failed" in check.detail
