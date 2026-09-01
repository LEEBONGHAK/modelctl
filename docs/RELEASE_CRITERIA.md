# Development Release Criteria / 개발 버전 완료 기준

## Version / 버전

- Version: `0.3.0`
- Status: **Draft**
- Phase: feature complete; readiness validation pending / 기능 완료; readiness validation 대기
- Channel: development release / 개발 버전
- Release branch: `main`
- Development branch: `refac`
- PyPI publication: disabled / 비활성화

## English

Version 0.3.0 has completed its planned functional increments. This checklist records the final completion boundary before readiness validation and promotion to `main`.

### Functional criteria

- [x] Save the current provider, model, launcher, and compatibility policy as a named profile.
- [x] List and inspect saved profile snapshots.
- [x] Validate and atomically apply a complete profile snapshot.
- [x] Delete a named profile explicitly and reject unknown names.
- [x] Preserve existing `config`, `use`, `doctor`, `launchers`, and `run` behavior.
- [x] Defer profile portability from v0.3.0 because no concrete usage need has been demonstrated; revisit only with evidence.
- [x] Define and validate the minimum versioned launcher plugin contract planned for v0.3.0.
- [x] Discover already-installed launcher plugins only from the dedicated `modelctl.launchers` entry-point group.
- [x] Preserve built-ins and reject duplicate or conflicting launcher IDs deterministically.
- [x] Expose plugin origin and load status without hiding broken plugin packages.
- [x] Extend `modelctl doctor` with plugin contract and executable health diagnostics.
- [x] Verify external launchers use the existing recommendation, remediation, compatibility, and execution paths.

### Quality criteria

- [x] Coordinate the workspace, CLI, core, SDK, release manifest, and lockfile at `0.3.0`.
- [x] Keep the release manifest in `draft` during feature development and final documentation review.
- [x] Pass Ruff and focused provider contract tests in primary CI.
- [x] Pass the complete test suite on Ubuntu, macOS, and Windows with Python 3.13.
- [x] Build all wheel and source distributions.
- [x] Install built wheels together and smoke-test installed imports and CLI startup.
- [x] Install a real launcher-plugin fixture and verify entry-point discovery from an isolated wheel environment.
- [x] Enforce strict basedpyright checks at the SDK, profile, and launcher-plugin boundaries in primary CI.
- [x] Ship PEP 561 `py.typed` markers and verify them from installed SDK/core wheels.
- [x] Complete all planned v0.3.0 functional increments and the final documentation/scope review.
- [ ] Run the final clean dependency audit, strict type check, cross-platform tests, release dry-run, installed-wheel/plugin smoke checks, and checksum validation on the completed tree.

### Profile safety criteria

- [x] Profiles include only provider, model, launcher, and compatibility policy.
- [x] Profiles never include provider credentials or launcher-managed authentication data.
- [x] Invalid names, malformed snapshots, missing fields, and unexpected fields fail explicitly.
- [x] Provider/model and launcher validation completes before configuration mutation.
- [x] Applying a profile performs one atomic configuration write and preserves unrelated settings.

### Launcher plugin safety criteria

- [x] Plugin discovery never scans arbitrary filesystem paths or downloads code.
- [x] Built-in launcher IDs cannot be replaced by installed plugins.
- [x] Multiple external entry points claiming one launcher ID are all rejected instead of choosing nondeterministically.
- [x] Broken, malformed, or incompatible plugins are isolated from unrelated launchers.
- [x] `modelctl doctor` distinguishes unrelated plugin failures from failure of the currently selected launcher.
- [x] Unavailable recommended external launchers cannot be applied to configuration.
- [x] Installed third-party launcher packages are documented as trusted executable extension code, not sandboxed code.

### Release criteria

- [x] `CHANGELOG.md` contains an active `0.3.0` heading.
- [x] `release.toml` declares `0.3.0`, `draft`, development channel, and disabled PyPI publication before readiness promotion.
- [x] The release workflow independently repeats audit, lint, strict type checking, tests, builds, installed-wheel smoke checks, and checksums.
- [ ] The completed `refac` tree passes one final full readiness validation with no unresolved review threads.
- [ ] A dedicated readiness pull request changes `release.toml` to `ready`, finalizes release documentation, and promotes the exact validated lineage to `main`.
- [ ] Only the exact validated `main` commit may receive immutable tag `v0.3.0` and its GitHub Release.

## 한국어

버전 0.3.0은 계획된 기능 increment를 모두 완료했습니다. 이 체크리스트는 readiness validation과 `main` 승격 전 최종 완료 경계를 기록합니다.

### 기능 기준

- [x] 현재 provider, model, launcher, compatibility policy를 이름 있는 profile로 저장합니다.
- [x] 저장한 profile snapshot을 목록으로 확인하고 상세 조회합니다.
- [x] 전체 profile을 먼저 검증한 뒤 원자적으로 적용합니다.
- [x] Profile을 명시적으로 삭제하고 존재하지 않는 이름은 거부합니다.
- [x] 기존 `config`, `use`, `doctor`, `launchers`, `run` 동작을 유지합니다.
- [x] 실제 사용에서 구체적 필요가 확인되지 않았으므로 profile portability를 v0.3.0에서 defer하고, 증거가 생길 때만 재검토합니다.
- [x] v0.3.0에서 계획한 최소 versioned launcher plugin 계약을 정의하고 검증합니다.
- [x] 전용 `modelctl.launchers` entry-point group에서 이미 설치된 launcher plugin만 탐색합니다.
- [x] Built-in을 보존하고 duplicate 또는 충돌 launcher ID를 결정적으로 거부합니다.
- [x] 손상된 plugin package를 숨기지 않고 plugin origin과 load status를 표시합니다.
- [x] `modelctl doctor`에 plugin contract 및 executable health 진단을 추가합니다.
- [x] 외부 launcher가 기존 recommendation, remediation, compatibility, execution 경로를 사용하는지 검증합니다.

### 품질 기준

- [x] Workspace, CLI, core, SDK, release manifest, lockfile 버전을 `0.3.0`으로 맞춥니다.
- [x] 기능 개발 및 최종 문서 검토 중 release manifest를 `draft`로 유지합니다.
- [x] Primary CI에서 Ruff와 provider contract 테스트가 통과합니다.
- [x] Python 3.13 기반 Ubuntu, macOS, Windows에서 전체 테스트가 통과합니다.
- [x] 모든 wheel과 source distribution을 빌드합니다.
- [x] 생성한 wheel을 함께 설치하고 package import와 CLI 실행을 smoke test합니다.
- [x] 실제 launcher-plugin fixture를 설치하고 격리 wheel 환경에서 entry-point discovery를 검증합니다.
- [x] SDK, profile, launcher-plugin 경계에 strict basedpyright 검사를 primary CI gate로 강제합니다.
- [x] PEP 561 `py.typed` marker를 배포하고 설치된 SDK/core wheel에서 실제 포함 여부를 검증합니다.
- [x] 계획된 v0.3.0 기능 increment와 최종 문서/scope 검토를 완료합니다.
- [ ] 완료된 tree에서 최종 clean dependency audit, strict type check, cross-platform test, release dry-run, 설치 wheel/plugin smoke check, checksum 검증을 수행합니다.

### Profile 안전 기준

- [x] Profile에는 provider, model, launcher, compatibility policy만 포함합니다.
- [x] Provider credential과 launcher가 관리하는 인증정보를 profile에 포함하지 않습니다.
- [x] 잘못된 이름, 손상된 snapshot, 누락 필드, 예상하지 않은 필드를 명시적으로 거부합니다.
- [x] Provider/model 및 launcher 검증을 설정 변경 전에 완료합니다.
- [x] Profile 적용은 설정을 한 번만 원자적으로 저장하고 관련 없는 설정을 보존합니다.

### Launcher plugin 안전 기준

- [x] Plugin discovery는 임의 filesystem path를 스캔하거나 코드를 다운로드하지 않습니다.
- [x] 설치 plugin이 built-in launcher ID를 대체할 수 없습니다.
- [x] 여러 외부 entry point가 동일 launcher ID를 주장하면 임의 선택하지 않고 모두 거부합니다.
- [x] 손상되거나 malformed 또는 incompatible plugin은 unrelated launcher와 격리됩니다.
- [x] `modelctl doctor`는 unrelated plugin 실패와 현재 선택된 launcher 실패를 구분합니다.
- [x] 실행 불가능한 외부 추천 launcher는 설정에 적용할 수 없습니다.
- [x] 설치된 제3자 launcher package가 sandbox 코드가 아닌 신뢰된 실행 확장 코드임을 문서화합니다.

### 릴리스 기준

- [x] `CHANGELOG.md`에 개발 중인 `0.3.0` 항목이 존재합니다.
- [x] Readiness 승격 전 `release.toml`이 `0.3.0`, `draft`, development channel, PyPI 비활성화를 선언합니다.
- [x] Release workflow가 audit, lint, strict type check, 전체 테스트, build, 설치 wheel smoke test, checksum을 독립적으로 반복합니다.
- [ ] 완료된 `refac` tree가 미해결 review thread 없이 최종 full readiness validation을 통과합니다.
- [ ] 전용 readiness PR에서 `release.toml`을 `ready`로 변경하고 release 문서를 최종화한 뒤 정확히 검증된 계보를 `main`으로 승격합니다.
- [ ] 정확히 검증된 `main` commit에만 불변 tag `v0.3.0`과 GitHub Release를 생성합니다.
