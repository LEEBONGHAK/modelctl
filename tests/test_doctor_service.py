from pathlib import Path

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

    def __init__(self, available=True, warning=None):
        self._available = available
        self.warning = warning

    def available(self):
        return self._available

    def compatibility_warning(self, provider, model):
        return self.warning


class FakeLaunchers:
    def __init__(self, launcher=None):
        self.launcher = launcher

    def get(self, launcher_id):
        return self.launcher if launcher_id == "claude" else None


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


def test_doctor_reports_working_configuration(monkeypatch):
    monkeypatch.setattr(Path, "exists", lambda self: True)
    service = DoctorService(
        FakeConfig(
            {
                "provider": "openrouter",
                "default_model": "anthropic/claude-sonnet-4",
                "launcher": "claude",
            }
        ),
        FakeCredentials("token"),
        FakeProviders(),
        FakeLaunchers(FakeLauncher()),
        FakeEngine(),
    )

    checks = service.run()

    assert all(check.status == "ok" for check in checks)


def test_doctor_reports_missing_runtime_selection(monkeypatch):
    monkeypatch.setattr(Path, "exists", lambda self: False)
    service = DoctorService(
        FakeConfig({}),
        FakeCredentials(),
        FakeProviders(),
        FakeLaunchers(FakeLauncher(available=False)),
        FakeEngine(),
    )

    checks = {check.name: check for check in service.run()}

    assert checks["Configuration"].status == "warning"
    assert checks["Provider"].status == "error"
    assert checks["Model"].status == "error"
    assert checks["Credential"].status == "warning"
    assert checks["Compatibility"].status == "warning"


def test_doctor_reports_launcher_compatibility_warning(monkeypatch):
    monkeypatch.setattr(Path, "exists", lambda self: True)
    service = DoctorService(
        FakeConfig(
            {
                "provider": "openrouter",
                "default_model": "anthropic/claude-sonnet-4",
                "launcher": "claude",
            }
        ),
        FakeCredentials("token"),
        FakeProviders(),
        FakeLaunchers(FakeLauncher(warning="Potential mismatch")),
        FakeEngine(),
    )

    checks = {check.name: check for check in service.run()}

    assert checks["Compatibility"].status == "warning"
    assert checks["Compatibility"].detail == "Potential mismatch"
