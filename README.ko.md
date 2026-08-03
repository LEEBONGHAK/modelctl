# modelctl

[English](README.md) | [한국어](README.ko.md)

**AI 모델과 코딩 에이전트를 통합 관리하는 범용 control plane입니다.**

`modelctl`은 AI provider와 모델 선택, credential 및 기본 설정 관리, 로컬 환경 진단, 여러 코딩 에이전트 CLI 실행을 하나의 명령 체계로 제공합니다.

> 현재 완성된 개발 버전은 `0.1.0`입니다. `main`은 공식 릴리스 브랜치이며 다음 버전 개발은 `refac`에서 계속합니다.

## 현재 동작하는 기능

- OpenRouter credential 저장과 모델 동기화
- 대화형·비대화형 provider/model 선택
- Provider, model, launcher 기본값 영속화
- Claude Code, Gemini CLI, Codex CLI, Aider launcher
- Shell 실행 없이 네이티브 인자 전달
- Launcher 목록, 설치 상태 확인, 선택
- `modelctl doctor` 진단 및 호환성 안내
- 운영체제 keyring과 명시적 평문 fallback
- Python 3.13 기반 Linux, macOS, Windows 테스트
- Lockfile dependency audit, Ruff, package build, 설치된 wheel smoke test
- SHA-256 checksum을 포함한 검증된 GitHub Release artifact

프로젝트 상태는 [`docs/PROGRESS.md`](docs/PROGRESS.md), PR별 영문·한국어 기록은 [`docs/pull-requests/README.md`](docs/pull-requests/README.md)를 참고하세요.

## 저장소에서 설치

이 저장소는 Python 3.13 이상을 사용하는 uv workspace입니다. 완성된 릴리스 상태는 `main`을 사용합니다.

```bash
git clone https://github.com/LEEBONGHAK/modelctl.git
cd modelctl
git switch main
uv sync --all-packages --locked
uv run modelctl --help
```

다음 버전을 개발하는 기여자는 `refac`에서 branch를 생성합니다.

## 빠른 시작

### 1. OpenRouter credential 저장

```bash
modelctl auth login openrouter
```

기본 저장소는 운영체제 keyring입니다. Keyring을 사용할 수 없더라도 평문 파일로 자동 전환하지 않습니다. 위험을 이해하고 명시적으로 허용하는 경우에만 로컬 파일 fallback을 사용하세요.

```bash
modelctl auth login openrouter --allow-plaintext-fallback
```

Fallback 파일은 POSIX 환경에서 현재 사용자 전용 권한을 사용하지만 내용은 암호화되지 않은 평문입니다. `MODELCTL_OPENROUTER`와 같은 환경변수도 사용할 수 있습니다.

### 2. 모델 동기화 및 선택

```bash
modelctl models sync openrouter
modelctl use
```

Script와 CI에서는 다음처럼 선택합니다.

```bash
modelctl use \
  --provider openrouter \
  --model anthropic/claude-sonnet-4
```

직접 지정한 값은 provider registry와 동기화된 로컬 catalog를 기준으로 검증됩니다.

### 3. Launcher 선택

```bash
modelctl launchers list
modelctl launchers use aider
```

| ID | 코딩 에이전트 | Native provider | 기본 명령 |
| --- | --- | --- | --- |
| `claude` | Claude Code | Anthropic | `claude --model <model>` |
| `gemini` | Gemini CLI | Google | `gemini --model <model>` |
| `codex` | Codex CLI | OpenAI | `codex --model <model>` |
| `aider` | Aider | 여러 provider | `aider --model <model>` |

### 4. 진단 및 실행

```bash
modelctl doctor
modelctl run
```

`run` 뒤의 값은 문자열 shell 명령이 아니라 인자 목록으로 전달됩니다.

```bash
modelctl run --continue
modelctl run --sandbox workspace-write
modelctl run --no-auto-commits
```

## OpenRouter 호환성

Claude Code, Gemini CLI, Codex CLI는 각각 자체 provider용 네이티브 client입니다. 다른 provider의 모델을 전달하면 `modelctl`은 실행을 차단하지 않고 경고를 표시합니다.

현재 OpenRouter 자동 연동은 Aider를 사용합니다.

```bash
modelctl launchers use aider
modelctl config set provider openrouter
modelctl config set model anthropic/claude-sonnet-4
modelctl run
```

실행 결과는 다음과 같습니다.

```bash
aider --model openrouter/anthropic/claude-sonnet-4
```

## 설정과 로컬 데이터

```bash
modelctl config show
modelctl config set provider openrouter
modelctl config set model anthropic/claude-sonnet-4
modelctl config set launcher aider
```

기본 경로는 다음과 같습니다.

```text
~/.config/modelctl/config.json
~/.config/modelctl/credentials.json   # 명시적 fallback 사용 시에만 생성
~/.local/share/modelctl/modelctl.db
```

보호 대상 파일은 원자적으로 저장합니다. POSIX directory와 file 권한은 각각 `0700`, `0600`으로 제한하고 symbolic-link 경로는 거부합니다.

## 개발 및 보안 검증

```bash
uv sync --all-packages --locked
uv audit --locked
uv run ruff check .
uv run pytest
```

GitHub Actions는 Ubuntu, macOS, Windows 전체 pytest, 모든 배포물 빌드, 격리 환경 wheel 설치, 설치된 CLI 실행도 검증합니다.

## 릴리스 완료 판정

Release 결정은 [`release.toml`](release.toml), 주요 변경 사항은 [`CHANGELOG.md`](CHANGELOG.md), 전체 완료 기준은 [`docs/RELEASE_CRITERIA.md`](docs/RELEASE_CRITERIA.md)에서 관리합니다.

```bash
python scripts/release_validation.py
python scripts/release_validation.py --print-status
python scripts/release_validation.py --tag v0.1.0
```

`status = "ready"`인 신뢰된 `main` push 또는 검토된 `main` 대상 Pull Request 병합은 다음 검증을 독립적으로 통과해야 합니다.

- Package version, manifest, changelog, 문서 일치
- Lockfile dependency audit
- Ruff와 전체 pytest suite
- 배포물 빌드 및 설치된 wheel smoke test
- Checksum 생성

모든 검증이 성공한 경우에만 정확히 해당 `main` commit에 `v<version>` tag를 만들고 하나의 불변 GitHub Release를 게시합니다. 기존 tag와 release asset은 덮어쓰지 않습니다.

**PyPI 게시는 의도적으로 비활성화되어 있습니다.** 어떤 workflow도 PyPI에 package를 게시하지 않습니다. 자세한 내용은 [`docs/RELEASING.md`](docs/RELEASING.md)를 참고하세요.

## 프로젝트 구조

```text
apps/modelctl/       Typer CLI 애플리케이션
packages/core/       runtime service, credential, provider, repository, launcher
packages/sdk/        SDK 기반
scripts/             release 검증 helper
tests/               회귀, 통합, 패키징, 보안 테스트
docs/                프로젝트, 릴리스, 보안, PR 문서
```

## 보안

Credential 동작, 취약점 제보 방법, 지원 버전, 알려진 한계는 [`SECURITY.md`](SECURITY.md)를 참고하세요. 자동 검증은 확인된 위험을 줄이지만 독립적인 침투 테스트나 정식 보안 감사를 대체하지 않습니다.

## 단기 로드맵

- 더 엄격한 호환성 정책과 자동 조치
- Launcher capability와 execution request 리팩터링
- 완성된 사용자 흐름과 테스트를 전제로 한 profile 관리
- 별도 검토를 거치는 PyPI 게시 milestone
