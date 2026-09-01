from modelctl_sdk import LaunchRequest, LauncherCapabilities, LauncherMetadata


class FixtureLauncher:
    metadata = LauncherMetadata(
        plugin_id="modelctl.test-fixture",
        launcher_id="fixture",
        display_name="Fixture Launcher",
    )
    capabilities = LauncherCapabilities(native_provider="fixture-provider")

    def available(self) -> bool:
        return True

    def run(self, request: LaunchRequest) -> None:
        return None
