# Development Release Criteria / 개발 버전 완료 기준

## Version / 버전

- Version: `0.2.0`
- Status: **Ready**
- Channel: development release / 개발 버전
- Release branch: `main`
- Development branch: `refac`
- PyPI publication: disabled / 비활성화

## English

Version 0.2.0 is ready for promotion to `main`. Completion is final only on the exact `main` commit that receives tag `v0.2.0` after the independent release workflow succeeds.

### Functional criteria — satisfied

- OpenRouter credential storage, synchronization, selection, diagnostics, and Aider execution are implemented.
- Anthropic, Google Gemini, and OpenAI native catalogs synchronize through their provider APIs.
- Native provider selections route to Claude Code, Gemini CLI, and Codex CLI through declared launcher capabilities.
- Interactive and non-interactive provider/model selection are covered by regression tests.
- Claude Code, Gemini CLI, Codex CLI, and Aider use one immutable launch-request contract.
- Aider translates OpenRouter identifiers without changing native-provider identifiers.
- `modelctl launchers recommend` is provider-aware and read-only by default.
- `modelctl launchers remediate` previews known compatibility changes and applies only with explicit `--apply`.
- Recommendation and remediation refuse unavailable launchers before configuration mutation.
- Persisted `warn` and `strict` compatibility policies and per-run overrides are implemented.
- Native launcher arguments are forwarded without shell execution.

### Quality criteria — satisfied

- All three package versions and the release manifest are `0.2.0`.
- `uv audit --locked` passes with `cryptography 50.0.0` and no advisory exclusion.
- Ruff passes.
- The complete 137-test suite passes on Ubuntu, macOS, and Windows with Python 3.13.
- Focused Anthropic, Google, and OpenAI provider-contract tests run in primary CI.
- Wheels and source distributions build without workspace source overrides.
- Built wheels install together in an isolated Python 3.13 environment.
- Installed imports, `modelctl version`, and `modelctl --help` succeed.

### Security criteria — satisfied

- Credentials use the operating-system keyring by default.
- Plaintext fallback requires explicit approval and private local permissions.
- Protected files use atomic writes and reject symbolic-link paths.
- Provider catalog credentials are not injected into launcher subprocess environments.
- External GitHub Actions are pinned to immutable commit SHAs.
- Release inputs are validated before shell use.
- Locked dependencies are audited without a retained exception for `GHSA-g6cj-pr64-35w5`.
- PyPI publication code and OIDC write permission remain absent.

### Release criteria

- `CHANGELOG.md` contains `0.2.0` with release date 2026-08-04.
- The readiness pull request targets `main` from the exact validated `refac` lineage.
- The release workflow independently reruns dependency audit, Ruff, all tests, builds, installed-wheel smoke checks, and checksum generation.
- Publication requires `status = "ready"` and a trusted `main` push or merged pull request targeting `main`.
- Closed but unmerged pull requests cannot publish.
- The workflow creates immutable tag `v0.2.0` and one GitHub Release with all six distributions and `SHA256SUMS`.
- Existing tags and release assets are never overwritten.

## 한국어

버전 0.2.0은 `main` 승격 준비가 완료됐습니다. 정확한 `main` commit에서 독립 release workflow가 성공하고 `v0.2.0` tag가 생성되어야 최종 완료로 판정합니다.

### 기능 기준 — 충족

- OpenRouter credential 저장, 동기화, 선택, 진단, Aider 실행 흐름을 구현했습니다.
- Anthropic, Google Gemini, OpenAI native catalog를 각 provider API로 동기화합니다.
- Native provider 선택은 launcher capability를 통해 Claude Code, Gemini CLI, Codex CLI로 연결됩니다.
- 대화형·비대화형 provider/model 선택을 회귀 테스트로 검증합니다.
- Claude Code, Gemini CLI, Codex CLI, Aider가 하나의 불변 launch-request 계약을 사용합니다.
- Aider는 OpenRouter identifier만 변환하고 native provider identifier는 변경하지 않습니다.
- `modelctl launchers recommend`는 provider-aware이며 기본적으로 읽기 전용입니다.
- `modelctl launchers remediate`는 알려진 호환성 변경을 미리 보여주며 명시적 `--apply`에서만 적용합니다.
- 추천·remediation은 설치되지 않은 launcher에 대해 설정을 변경하기 전에 거부합니다.
- 저장된 `warn`·`strict` 정책과 실행 1회 override를 지원합니다.
- Native launcher 인자를 shell 없이 전달합니다.

### 품질 기준 — 충족

- 세 package와 release manifest의 버전이 모두 `0.2.0`입니다.
- `cryptography 50.0.0`이 잠긴 상태에서 별도 advisory 예외 없이 `uv audit --locked`가 통과합니다.
- Ruff가 통과합니다.
- Python 3.13 기반 Ubuntu·macOS·Windows에서 전체 137개 테스트가 통과합니다.
- Primary CI에서 Anthropic, Google, OpenAI provider contract 테스트를 실행합니다.
- Workspace source override 없이 wheel과 source distribution을 빌드합니다.
- 격리된 Python 3.13 환경에 생성한 wheel을 함께 설치합니다.
- 설치된 package import, `modelctl version`, `modelctl --help`가 성공합니다.

### 보안 기준 — 충족

- Credential은 운영체제 keyring을 기본 저장소로 사용합니다.
- 평문 fallback은 명시적 승인과 private local 권한을 요구합니다.
- 보호 파일은 원자적 저장을 사용하고 symbolic-link 경로를 거부합니다.
- Provider catalog credential을 launcher subprocess 환경에 주입하지 않습니다.
- 외부 GitHub Actions는 변경 불가능한 commit SHA로 고정합니다.
- Release 입력은 shell 사용 전에 검증합니다.
- `GHSA-g6cj-pr64-35w5` 예외를 유지하지 않고 잠긴 dependency를 audit합니다.
- PyPI 게시 코드와 OIDC write 권한은 존재하지 않습니다.

### 릴리스 기준

- `CHANGELOG.md`에 2026-08-04 날짜의 `0.2.0` 항목이 존재합니다.
- Readiness Pull Request는 정확히 검증된 `refac` 계보에서 `main`을 대상으로 합니다.
- Release workflow가 dependency audit, Ruff, 전체 테스트, build, 설치 wheel smoke test, checksum 생성을 독립적으로 다시 실행합니다.
- `status = "ready"`와 신뢰된 `main` push 또는 `main` 대상 PR 병합을 모두 요구합니다.
- 닫혔지만 병합되지 않은 Pull Request는 게시할 수 없습니다.
- Workflow가 불변 tag `v0.2.0`과 여섯 개 배포 파일 및 `SHA256SUMS`를 포함한 하나의 GitHub Release를 생성합니다.
- 기존 tag와 release asset은 덮어쓰지 않습니다.
