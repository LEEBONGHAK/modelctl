# Launcher Plugins / Launcher 플러그인

`modelctl` v0.3.0 discovers launcher extensions only from installed Python package metadata. It does not scan arbitrary directories, download plugin code, or install packages automatically.

`modelctl` v0.3.0은 설치된 Python 패키지 metadata에서만 launcher 확장을 탐색합니다. 임의 디렉터리를 스캔하거나 plugin 코드를 다운로드하거나 패키지를 자동 설치하지 않습니다.

## Entry point / Entry point 등록

Launcher packages register exactly one dedicated entry-point group:

Launcher 패키지는 전용 entry-point group 하나에 등록합니다.

```toml
[project.entry-points."modelctl.launchers"]
my-launcher = "my_package:MyLauncher"
```

The entry-point name is the launcher ID and **must match** `LauncherMetadata.launcher_id`.

Entry-point 이름은 launcher ID이며 `LauncherMetadata.launcher_id`와 **반드시 동일해야 합니다**.

## Public SDK contract / 공개 SDK 계약

A launcher uses the public `modelctl_sdk` types:

Launcher는 공개 `modelctl_sdk` 타입을 사용합니다.

```python
from modelctl_sdk import (
    LaunchRequest,
    LauncherCapabilities,
    LauncherMetadata,
)


class MyLauncher:
    metadata = LauncherMetadata(
        plugin_id="example.my-plugin",
        launcher_id="my-launcher",
        display_name="My Launcher",
    )
    capabilities = LauncherCapabilities(native_provider="example")

    def available(self) -> bool:
        return True

    def run(self, request: LaunchRequest) -> None:
        ...
```

An entry point may expose a plugin instance, a zero-argument class, or a zero-argument factory returning a `LauncherPlugin`. Loaded objects must provide valid `LauncherMetadata`, `LauncherCapabilities`, `available()`, and `run()` behavior.

Entry point는 plugin instance, 인자 없는 class, 또는 `LauncherPlugin`을 반환하는 인자 없는 factory를 노출할 수 있습니다. 로드된 객체는 유효한 `LauncherMetadata`, `LauncherCapabilities`, `available()`, `run()` 동작을 제공해야 합니다.

The current launcher contract version is `1.0`. Contract compatibility follows the contract major version rather than the modelctl package minor version.

현재 launcher contract version은 `1.0`입니다. Contract 호환성은 modelctl package minor version이 아니라 contract major version을 기준으로 판단합니다.

## Discovery behavior / 탐색 동작

At startup, the launcher registry:

Launcher registry는 시작 시 다음 순서로 동작합니다.

1. registers the built-in Claude Code, Gemini CLI, Codex CLI, and Aider launchers;
2. reads only the `modelctl.launchers` installed entry-point group;
3. sorts candidates deterministically;
4. refuses entry points whose ID collides with a built-in launcher **without loading them**;
5. refuses all external candidates when multiple installed entry points claim the same launcher ID;
6. loads each remaining candidate independently;
7. validates its SDK metadata and launcher ID;
8. adapts successful plugins to the same core launcher runtime used by built-ins.

1. built-in Claude Code, Gemini CLI, Codex CLI, Aider launcher를 먼저 등록합니다.
2. 설치된 `modelctl.launchers` entry-point group만 읽습니다.
3. 후보를 결정적인 순서로 정렬합니다.
4. built-in ID와 충돌하는 entry point는 **로드하지 않고** 거부합니다.
5. 동일 launcher ID를 여러 외부 entry point가 주장하면 해당 후보를 모두 거부합니다.
6. 나머지 후보는 서로 독립적으로 로드합니다.
7. SDK metadata와 launcher ID를 검증합니다.
8. 성공한 plugin은 built-in과 동일한 core launcher runtime으로 연결합니다.

A broken plugin therefore does not prevent unrelated built-ins or other valid plugins from loading.

따라서 하나의 손상된 plugin이 unrelated built-in 또는 다른 정상 plugin의 로드를 막지 않습니다.

## Diagnostics / 진단

Run:

```bash
modelctl launchers list
```

The table includes the launcher source and load status. Installed plugin sources are reported using their distribution name and version when available, for example `modelctl-example-plugin==1.2.0`. Import failures, initialization failures, incompatible contract versions, metadata mismatches, and duplicate IDs remain visible as failed diagnostic rows.

표에는 launcher source와 load status가 표시됩니다. 설치 plugin source는 가능한 경우 `modelctl-example-plugin==1.2.0`처럼 distribution 이름과 버전으로 표시됩니다. Import 실패, 초기화 실패, 비호환 contract version, metadata 불일치, 중복 ID는 실패한 진단 행으로 남습니다.

## Trust boundary / 신뢰 경계

Python entry points are executable extension points. Installing a third-party launcher package grants that package code execution when modelctl loads its registered entry point. modelctl limits *discovery* to already-installed package metadata, but it does not sandbox trusted installed Python packages.

Python entry point는 실행 가능한 확장 지점입니다. 제3자 launcher 패키지를 설치하면 modelctl이 해당 entry point를 로드할 때 그 패키지 코드가 실행될 수 있습니다. modelctl은 *탐색 범위*를 이미 설치된 package metadata로 제한하지만, 신뢰하여 설치한 Python package 자체를 sandbox하지는 않습니다.

v0.3.0 does not provide provider plugins, remote plugin registries, arbitrary filesystem plugin paths, automatic installation, or automatic updates.

v0.3.0에서는 provider plugin, remote plugin registry, 임의 filesystem plugin path, 자동 설치, 자동 업데이트를 제공하지 않습니다.
