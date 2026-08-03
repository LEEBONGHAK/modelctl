# Development Release Criteria / 개발 버전 완료 기준

## Version / 버전

- Version: `0.1.0`
- Status: **Ready**
- Channel: development release / 개발 버전
- PyPI publication: disabled / 비활성화

## English

A development version is complete only when all criteria below are satisfied on the commit that receives the tag.

### Functional criteria

- The OpenRouter credential, model synchronization, selection, launcher selection, diagnostics, and execution workflow is implemented.
- Interactive and non-interactive provider/model selection are both covered by regression tests.
- Claude Code, Gemini CLI, Codex CLI, and Aider launchers remain installable and invokable through the shared launcher service.
- Aider translates OpenRouter model identifiers without changing non-OpenRouter identifiers.

### Quality criteria

- All three package versions match the release manifest and tag.
- Locked dependencies pass `uv audit --locked`.
- Ruff passes.
- The complete pytest suite passes on Linux, macOS, and Windows with Python 3.13.
- Wheels and source distributions build without workspace source overrides.
- Built wheels install together in an isolated Python 3.13 environment.
- Installed package imports, `modelctl version`, and `modelctl --help` succeed.

### Security criteria

- Credentials use the operating-system keyring by default.
- Unencrypted credential fallback requires explicit user approval and private local file permissions.
- Protected configuration and credential files use atomic writes and reject symbolic-link paths.
- Release workflow inputs are validated before they reach shell commands or workflow outputs.
- Third-party GitHub Actions are pinned to immutable commit SHAs.
- PyPI publication code and OIDC write permission are absent.

### Release criteria

- `CHANGELOG.md` contains the exact release version.
- The tagged commit is contained in `refac`.
- The release workflow independently runs dependency audit, lint, tests, build, and installed-wheel smoke checks.
- The release workflow creates the tag only from a successful trusted `refac` push marked `status = "ready"` in `release.toml`.
- A GitHub Release attaches all distributions and `SHA256SUMS`.
- Existing tags or GitHub Release assets are never overwritten.

## 한국어

개발 버전은 tag가 지정되는 commit에서 아래 기준을 모두 충족해야 완료된 것으로 판단합니다.

### 기능 기준

- OpenRouter credential 저장, 모델 동기화, 모델 선택, launcher 선택, 진단, 실행 흐름이 구현되어야 합니다.
- 대화형 및 비대화형 provider·model 선택이 모두 회귀 테스트로 검증되어야 합니다.
- Claude Code, Gemini CLI, Codex CLI, Aider를 공통 launcher service로 실행할 수 있어야 합니다.
- Aider는 OpenRouter model ID만 변환하고 다른 provider의 model ID는 변경하지 않아야 합니다.

### 품질 기준

- 세 package 버전이 release manifest 및 tag와 일치해야 합니다.
- `uv audit --locked`가 통과해야 합니다.
- Ruff가 통과해야 합니다.
- 전체 pytest suite가 Python 3.13 기반 Linux, macOS, Windows에서 통과해야 합니다.
- Workspace source override 없이 wheel과 source distribution을 빌드할 수 있어야 합니다.
- 생성한 wheel을 격리된 Python 3.13 환경에 함께 설치할 수 있어야 합니다.
- 설치된 package import, `modelctl version`, `modelctl --help`가 성공해야 합니다.

### 보안 기준

- Credential은 운영체제 keyring을 기본 저장소로 사용해야 합니다.
- 암호화되지 않은 credential fallback은 명시적 승인과 private local file 권한을 요구해야 합니다.
- 보호 대상 설정·credential 파일은 원자적 저장을 사용하고 symbolic-link 경로를 거부해야 합니다.
- Release workflow 입력은 shell command나 workflow output에 전달되기 전에 검증되어야 합니다.
- 외부 GitHub Actions는 변경 불가능한 commit SHA로 고정되어야 합니다.
- PyPI 게시 코드와 OIDC write 권한이 없어야 합니다.

### 릴리스 기준

- `CHANGELOG.md`에 정확한 release version이 존재해야 합니다.
- Tag 대상 commit이 `refac`에 포함되어야 합니다.
- Release workflow가 dependency audit, lint, test, build, 설치된 wheel smoke 검증을 독립적으로 수행해야 합니다.
- `release.toml`의 `status = "ready"`가 지정된 신뢰된 `refac` push가 모든 검증을 통과한 경우에만 tag를 생성해야 합니다.
- GitHub Release에 모든 배포 파일과 `SHA256SUMS`를 첨부해야 합니다.
- 기존 tag나 GitHub Release asset을 덮어쓰지 않아야 합니다.
