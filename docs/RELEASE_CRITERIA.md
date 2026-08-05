# Development Release Criteria / 개발 버전 완료 기준

## Version / 버전

- Version: `0.3.0`
- Status: **Draft**
- Channel: development release / 개발 버전
- Release branch: `main`
- Development branch: `refac`
- PyPI publication: disabled / 비활성화

## English

Version 0.3.0 is under active development. This checklist records the completion boundary without declaring the version ready for publication.

### Functional criteria

- [x] Save the current provider, model, launcher, and compatibility policy as a named profile.
- [x] List and inspect saved profile snapshots.
- [x] Validate and atomically apply a complete profile snapshot.
- [x] Delete a named profile explicitly and reject unknown names.
- [x] Preserve existing `config`, `use`, `doctor`, `launchers`, and `run` behavior.
- [ ] Add evidence-driven profile portability only after the initial workflow is validated.
- [ ] Define and validate the minimum launcher plugin contract planned for v0.3.0.

### Quality criteria

- [x] Coordinate the workspace, CLI, core, SDK, release manifest, and lockfile at `0.3.0`.
- [x] Keep the release manifest in `draft` during feature development.
- [x] Pass Ruff and focused provider contract tests in primary CI.
- [x] Pass the complete test suite on Ubuntu, macOS, and Windows with Python 3.13.
- [x] Build all wheel and source distributions.
- [x] Install built wheels together and smoke-test installed imports and CLI startup.
- [ ] Complete all remaining v0.3.0 increments and final documentation.
- [ ] Run the final clean dependency audit, release dry-run, and checksum validation.

### Profile safety criteria

- [x] Profiles include only provider, model, launcher, and compatibility policy.
- [x] Profiles never include provider credentials or launcher-managed authentication data.
- [x] Invalid names, malformed snapshots, missing fields, and unexpected fields fail explicitly.
- [x] Provider/model and launcher validation completes before configuration mutation.
- [x] Applying a profile performs one atomic configuration write and preserves unrelated settings.

### Release criteria

- [x] `CHANGELOG.md` contains an active `0.3.0` heading.
- [x] `release.toml` declares `0.3.0`, `draft`, development channel, and disabled PyPI publication.
- [ ] All v0.3.0 completion criteria are satisfied and independently reviewed.
- [ ] A dedicated readiness pull request promotes the exact validated `refac` lineage to `main`.
- [ ] The release workflow independently repeats audit, lint, tests, builds, installed-wheel smoke checks, and checksums.
- [ ] Only the exact validated `main` commit may receive immutable tag `v0.3.0` and its GitHub Release.

## 한국어

버전 0.3.0은 현재 개발 중입니다. 이 체크리스트는 게시 준비 완료를 선언하지 않고 최종 완료 경계를 기록합니다.

### 기능 기준

- [x] 현재 provider, model, launcher, compatibility policy를 이름 있는 profile로 저장합니다.
- [x] 저장한 profile snapshot을 목록으로 확인하고 상세 조회합니다.
- [x] 전체 profile을 먼저 검증한 뒤 원자적으로 적용합니다.
- [x] Profile을 명시적으로 삭제하고 존재하지 않는 이름은 거부합니다.
- [x] 기존 `config`, `use`, `doctor`, `launchers`, `run` 동작을 유지합니다.
- [ ] 첫 workflow 검증 후 실제 필요성이 확인된 profile 이식 기능만 추가합니다.
- [ ] v0.3.0에서 계획한 최소 launcher plugin 계약을 정의하고 검증합니다.

### 품질 기준

- [x] Workspace, CLI, core, SDK, release manifest, lockfile 버전을 `0.3.0`으로 맞춥니다.
- [x] 기능 개발 중 release manifest를 `draft`로 유지합니다.
- [x] Primary CI에서 Ruff와 provider contract 테스트가 통과합니다.
- [x] Python 3.13 기반 Ubuntu, macOS, Windows에서 전체 테스트가 통과합니다.
- [x] 모든 wheel과 source distribution을 빌드합니다.
- [x] 생성한 wheel을 함께 설치하고 package import와 CLI 실행을 smoke test합니다.
- [ ] 남은 v0.3.0 기능과 최종 문서를 완료합니다.
- [ ] 최종 clean dependency audit, release dry-run, checksum 검증을 수행합니다.

### Profile 안전 기준

- [x] Profile에는 provider, model, launcher, compatibility policy만 포함합니다.
- [x] Provider credential과 launcher가 관리하는 인증정보를 profile에 포함하지 않습니다.
- [x] 잘못된 이름, 손상된 snapshot, 누락 필드, 예상하지 않은 필드를 명시적으로 거부합니다.
- [x] Provider/model 및 launcher 검증을 설정 변경 전에 완료합니다.
- [x] Profile 적용은 설정을 한 번만 원자적으로 저장하고 관련 없는 설정을 보존합니다.

### 릴리스 기준

- [x] `CHANGELOG.md`에 개발 중인 `0.3.0` 항목이 존재합니다.
- [x] `release.toml`이 `0.3.0`, `draft`, development channel, PyPI 비활성화를 선언합니다.
- [ ] 모든 v0.3.0 완료 기준을 충족하고 독립 검토합니다.
- [ ] 전용 readiness PR에서 정확히 검증된 `refac` 계보를 `main`으로 승격합니다.
- [ ] Release workflow가 audit, lint, 전체 테스트, build, 설치 wheel smoke test, checksum을 독립적으로 반복합니다.
- [ ] 정확히 검증된 `main` commit에만 불변 tag `v0.3.0`과 GitHub Release를 생성합니다.
