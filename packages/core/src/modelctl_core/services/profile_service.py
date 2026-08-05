from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Mapping

from modelctl_core.config.manager import ConfigManager
from modelctl_core.services.config_service import COMPATIBILITY_POLICIES

DEFAULT_LAUNCHER = "claude"
DEFAULT_COMPATIBILITY_POLICY = "warn"
PROFILE_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")
PROFILE_FIELDS = frozenset(
    {
        "provider",
        "default_model",
        "launcher",
        "compatibility_policy",
    }
)


@dataclass(frozen=True)
class Profile:
    name: str
    provider: str
    model: str
    launcher: str
    compatibility_policy: str

    def to_config(self) -> dict[str, str]:
        return {
            "provider": self.provider,
            "default_model": self.model,
            "launcher": self.launcher,
            "compatibility_policy": self.compatibility_policy,
        }


class ProfileService:
    def __init__(
        self,
        manager: ConfigManager | None = None,
        selection_service=None,
        launcher_registry=None,
    ) -> None:
        self.manager = manager or ConfigManager()
        self.selection_service = selection_service
        self.launcher_registry = launcher_registry

    def save(self, name: str) -> Profile:
        normalized = self.normalize_name(name)
        config = self.manager.load()
        profile = self._profile_from_current_config(normalized, config)
        self._validate_runtime(profile)

        profiles = self._profiles_from_config(config)
        profiles[normalized] = profile

        updated = dict(config)
        updated["profiles"] = {
            profile_name: stored.to_config()
            for profile_name, stored in sorted(profiles.items())
        }
        self.manager.save(updated)
        return profile

    def list(self) -> list[Profile]:
        profiles = self._profiles_from_config(self.manager.load())
        return [profiles[name] for name in sorted(profiles)]

    def get(self, name: str) -> Profile:
        normalized = self.normalize_name(name)
        profiles = self._profiles_from_config(self.manager.load())
        try:
            return profiles[normalized]
        except KeyError as error:
            raise ValueError(f"Unknown profile: {normalized}") from error

    def use(self, name: str) -> Profile:
        normalized = self.normalize_name(name)
        config = self.manager.load()
        profiles = self._profiles_from_config(config)
        try:
            profile = profiles[normalized]
        except KeyError as error:
            raise ValueError(f"Unknown profile: {normalized}") from error

        self._validate_runtime(profile)

        updated = dict(config)
        updated.update(profile.to_config())
        self.manager.save(updated)
        return profile

    def delete(self, name: str) -> Profile:
        normalized = self.normalize_name(name)
        config = self.manager.load()
        profiles = self._profiles_from_config(config)
        try:
            deleted = profiles.pop(normalized)
        except KeyError as error:
            raise ValueError(f"Unknown profile: {normalized}") from error

        updated = dict(config)
        if profiles:
            updated["profiles"] = {
                profile_name: stored.to_config()
                for profile_name, stored in sorted(profiles.items())
            }
        else:
            updated.pop("profiles", None)
        self.manager.save(updated)
        return deleted

    @staticmethod
    def normalize_name(name: str) -> str:
        normalized = name.strip().lower()
        if PROFILE_NAME_PATTERN.fullmatch(normalized) is None:
            raise ValueError(
                "Invalid profile name. Use 1-64 lowercase letters, numbers, dots, "
                "underscores, or hyphens, beginning with a letter or number."
            )
        return normalized

    def _profile_from_current_config(
        self,
        name: str,
        config: Mapping[str, object],
    ) -> Profile:
        provider = self._required_string(
            config,
            "provider",
            "Cannot save a profile before selecting a provider.",
        )
        model = self._required_string(
            config,
            "default_model",
            "Cannot save a profile before selecting a model.",
        )
        launcher = self._optional_string(
            config,
            "launcher",
            DEFAULT_LAUNCHER,
        )
        policy = self._optional_string(
            config,
            "compatibility_policy",
            DEFAULT_COMPATIBILITY_POLICY,
        ).lower()
        self._validate_policy(policy)
        return Profile(name, provider, model, launcher, policy)

    def _profiles_from_config(
        self,
        config: Mapping[str, object],
    ) -> dict[str, Profile]:
        raw_profiles = config.get("profiles", {})
        if not isinstance(raw_profiles, dict):
            raise ValueError("Invalid profiles configuration: expected an object.")

        profiles: dict[str, Profile] = {}
        for raw_name, raw_profile in raw_profiles.items():
            if not isinstance(raw_name, str):
                raise ValueError(
                    "Invalid profiles configuration: names must be strings."
                )
            normalized = self.normalize_name(raw_name)
            if normalized != raw_name:
                raise ValueError(
                    "Invalid stored profile name "
                    f"'{raw_name}'; expected '{normalized}'."
                )
            profiles[normalized] = self._profile_from_mapping(
                normalized,
                raw_profile,
            )
        return profiles

    def _profile_from_mapping(self, name: str, raw_profile: object) -> Profile:
        if not isinstance(raw_profile, dict):
            raise ValueError(f"Invalid profile '{name}': expected an object.")
        fields = set(raw_profile)
        if fields != PROFILE_FIELDS:
            missing = sorted(PROFILE_FIELDS - fields)
            extra = sorted(fields - PROFILE_FIELDS)
            details: list[str] = []
            if missing:
                details.append(f"missing {', '.join(missing)}")
            if extra:
                details.append(f"unexpected {', '.join(extra)}")
            raise ValueError(f"Invalid profile '{name}': {'; '.join(details)}.")

        provider = self._required_string(
            raw_profile,
            "provider",
            f"Invalid profile '{name}': provider must be a non-empty string.",
        )
        model = self._required_string(
            raw_profile,
            "default_model",
            f"Invalid profile '{name}': default_model must be a non-empty string.",
        )
        launcher = self._required_string(
            raw_profile,
            "launcher",
            f"Invalid profile '{name}': launcher must be a non-empty string.",
        )
        policy = self._required_string(
            raw_profile,
            "compatibility_policy",
            f"Invalid profile '{name}': compatibility_policy must be "
            "a non-empty string.",
        )
        if policy != policy.lower():
            raise ValueError(
                f"Invalid profile '{name}': compatibility_policy must be normalized."
            )
        self._validate_policy(policy)
        return Profile(name, provider, model, launcher, policy)

    def _validate_runtime(self, profile: Profile) -> None:
        if self.selection_service is not None:
            self.selection_service.validate(profile.provider, profile.model)

        if (
            self.launcher_registry is not None
            and self.launcher_registry.get(profile.launcher) is None
        ):
            supported = ", ".join(
                launcher.name for launcher in self.launcher_registry.list()
            )
            raise ValueError(
                f"Unknown launcher in profile '{profile.name}': {profile.launcher}. "
                f"Expected one of: {supported}"
            )

    @staticmethod
    def _validate_policy(policy: str) -> None:
        if policy not in COMPATIBILITY_POLICIES:
            expected = ", ".join(sorted(COMPATIBILITY_POLICIES))
            raise ValueError(
                f"Unknown compatibility policy '{policy}'. Expected one of: {expected}"
            )

    @staticmethod
    def _required_string(
        mapping: Mapping[str, object],
        key: str,
        message: str,
    ) -> str:
        value = mapping.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(message)
        return value.strip()

    @classmethod
    def _optional_string(
        cls,
        mapping: Mapping[str, object],
        key: str,
        default: str,
    ) -> str:
        value = mapping.get(key, default)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Invalid configuration value for {key}.")
        return value.strip()
