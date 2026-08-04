import re
from unittest.mock import Mock, patch

from typer.testing import CliRunner

from modelctl_cli.main import app

runner = CliRunner()
ANSI_ESCAPE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def test_config_set_persists_compatibility_policy():
    service = Mock()

    with patch("modelctl_cli.commands.config.ConfigService", return_value=service):
        result = runner.invoke(
            app,
            ["config", "set", "compatibility-policy", "strict"],
        )

    assert result.exit_code == 0
    assert "Set compatibility-policy to strict" in result.stdout
    service.set_compatibility_policy.assert_called_once_with("strict")


def test_config_set_reports_invalid_compatibility_policy():
    service = Mock()
    service.set_compatibility_policy.side_effect = ValueError(
        "Unknown compatibility policy 'automatic'. Expected one of: strict, warn"
    )

    with patch("modelctl_cli.commands.config.ConfigService", return_value=service):
        result = runner.invoke(
            app,
            ["config", "set", "compatibility-policy", "automatic"],
        )

    output = " ".join(ANSI_ESCAPE.sub("", result.output).split())
    assert result.exit_code != 0
    assert "Expected one of: strict, warn" in output
