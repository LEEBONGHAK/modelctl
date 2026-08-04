from dataclasses import dataclass, replace

from modelctl_core.launcher.base import LaunchRequest


COMPATIBILITY_POLICY_WARN = "warn"
COMPATIBILITY_POLICY_STRICT = "strict"
COMPATIBILITY_POLICIES = frozenset(
    {
        COMPATIBILITY_POLICY_WARN,
        COMPATIBILITY_POLICY_STRICT,
    }
)


@dataclass(frozen=True)
class LauncherRecommendation:
    name: str
    display_name: str
    provider: str
    model: str
    reason: str
    installed: bool
    active: bool
    changed: bool = False


class LauncherService:
    def __init__(self, registry, config):
        self.registry = registry
        self.config = config

    def compatibility_warning(self) -> str | None:
        launcher, request = self._execution_request()
        return launcher.compatibility_warning(request)

    def compatibility_policy(self) -> str:
        config = self.config.load()
        policy = config.get("compatibility_policy", COMPATIBILITY_POLICY_WARN)
        return self._validate_compatibility_policy(policy)

    def check_compatibility(self, *, policy: str | None = None) -> str | None:
        resolved_policy = (
            self.compatibility_policy()
            if policy is None
            else self._validate_compatibility_policy(policy)
        )
        warning = self.compatibility_warning()
        if resolved_policy == COMPATIBILITY_POLICY_STRICT and warning:
            raise RuntimeError(f"Strict compatibility check failed: {warning}")
        return warning

    def recommend(self) -> LauncherRecommendation | None:
        provider, model, active_name = self._configured_values()
        launcher = self._recommended_launcher(provider)
        if launcher is None:
            return None

        if launcher.capabilities.translates(provider):
            reason = (
                f"{launcher.display_name} translates {provider} model identifiers "
                "automatically and uses the selected provider context."
            )
        else:
            reason = (
                f"{launcher.display_name} is the native launcher for provider "
                f"'{provider}'."
            )

        return LauncherRecommendation(
            name=launcher.name,
            display_name=launcher.display_name,
            provider=provider,
            model=model,
            reason=reason,
            installed=launcher.available(),
            active=launcher.name == active_name,
        )

    def apply_recommendation(self) -> LauncherRecommendation:
        recommendation = self.recommend()
        if recommendation is None:
            provider, _, _ = self._configured_values()
            raise RuntimeError(
                f"No launcher recommendation is available for provider '{provider}'."
            )

        if not recommendation.installed:
            raise RuntimeError(
                f"Recommended launcher '{recommendation.name}' is not installed or not "
                "available on PATH. Install it first, or select a launcher explicitly with "
                f"`modelctl launchers use {recommendation.name}`."
            )

        if recommendation.active:
            return recommendation

        self.config.update(launcher=recommendation.name)
        return replace(recommendation, active=True, changed=True)

    def run(self, extra_args: list[str] | None = None) -> None:
        launcher, request = self._execution_request(extra_args)
        launcher.run(request)

    def _recommended_launcher(self, provider: str):
        launchers = self.registry.list()
        translated = next(
            (
                item
                for item in launchers
                if item.capabilities.translates(provider)
            ),
            None,
        )
        if translated is not None:
            return translated

        return next(
            (
                item
                for item in launchers
                if item.capabilities.native_provider == provider
            ),
            None,
        )

    def _configured_values(self) -> tuple[str, str, str]:
        config = self.config.load()
        provider = config.get("provider")
        model = config.get("default_model")
        active_name = config.get("launcher", "claude")

        if not isinstance(provider, str) or not provider:
            raise RuntimeError("No provider selected. Run: modelctl use")
        if not isinstance(model, str) or not model:
            raise RuntimeError("No model selected. Run: modelctl use")
        if not isinstance(active_name, str) or not active_name:
            active_name = "claude"

        return provider, model, active_name

    def _execution_request(
        self,
        extra_args: list[str] | None = None,
    ):
        config = self.config.load()
        launcher_name = config.get("launcher", "claude")
        model = config.get("default_model")
        provider = config.get("provider")

        if not isinstance(model, str) or not model:
            raise RuntimeError("No model selected. Run: modelctl use")
        if not isinstance(launcher_name, str) or not launcher_name:
            launcher_name = "claude"

        launcher = self.registry.get(launcher_name)
        if not launcher:
            raise RuntimeError(f"Unknown launcher: {launcher_name}")

        request = LaunchRequest.create(
            model=model,
            provider=provider if isinstance(provider, str) and provider else None,
            extra_args=extra_args,
        )
        return launcher, request

    @staticmethod
    def _validate_compatibility_policy(policy: object) -> str:
        if isinstance(policy, str) and policy in COMPATIBILITY_POLICIES:
            return policy

        expected = ", ".join(sorted(COMPATIBILITY_POLICIES))
        raise RuntimeError(
            f"Invalid compatibility policy '{policy}'. Expected one of: {expected}. "
            "Run: modelctl config set compatibility-policy warn"
        )
