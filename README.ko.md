# modelctl

[English](README.md) | [한국어](README.ko.md)

**AI 모델과 코딩 에이전트를 통합 관리하는 범용 control plane입니다.**

`modelctl`은 AI provider와 모델 선택, credential 및 기본 설정 관리, 로컬 환경 진단, 여러 코딩 에이전트 CLI 실행을 하나의 명령 체계로 제공합니다.

> 현재 완성된 개발 버전은 `0.1.0`입니다. `0.2.0`은 `refac`에서 draft 상태로 개발 중이며 `main`은 공식 릴리스 브랜치로 유지합니다.

## 현재 동작하는 기능

- OpenRouter credential 저장과 모델 동기화
- 대화형·비대화형 provider/model 선택
- Provider, model, launcher, compatibility policy 기본값 영속화
- Claude Code, Gemini CLI, Codex CLI, Aider launcher
- Shell 실행 없이 네이티브 인자 전달
- Launcher 목록, 설치 상태 확인, 선택
- Provider-aware launcher 추천과 명시적인 안전 적용 단계
- Launcher 실행 전에 적용하는 `warn` 또는 `strict` 호환성 정책
- 실행 1회에만 적용하는 strict/warn override
- 읽기 전용 호환성 remediation 계획과 명시적 안전 적용
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

### 3. Launcher 선택·추천·remediation

```bash
modelctl launchers list
modelctl launchers recommend
modelctl launchers recommend --apply
modelctl launchers remediate
modelctl launchers remediate --apply
modelctl launchers use aider
```

`recommend`는 현재 launcher의 호환 여부와 관계없이 선택한 provider와 model에 적합한 launcher를 제안합니다. `remediate`는 현재 active launcher를 평가하고 알려진 호환성 불일치가 있을 때만 변경 계획을 만듭니다.

두 명령 모두 기본적으로 읽기 전용입니다. `--apply`를 지정한 경우에만 권장 launcher가 `PATH`에 설치되어 있을 때 설정을 변경합니다. Remediation은 소프트웨어를 설치하거나 provider·model을 바꾸거나 launcher를 실행하지 않습니다.

| ID | 코딩 에이전트 | Native provider | 기본 명령 |
| --- | --- | --- | --- |
| `claude` | Claude Code | Anthropic | `claude --model <model>` |
| `gemini` | Gemini CLI | Google | `gemini --model <model>` |
| `codex` | Codex CLI | OpenAI | `codex --model <model>` |
| `aider` | Aider | 여러 provider | `aider --model <model>` |

### 4. 호환성 정책 설정 및 실행

저장된 정책의 기본값은 기존 동작을 유지하는 `warn`입니다. 자동화나 안전이 중요한 실행에서 알려진 provider/launcher 불일치를 거부해야 한다면 `strict`를 기본값으로 설정할 수 있습니다.

```bash
modelctl config set compatibility-policy warn
modelctl config set compatibility-policy strict
```

저장된 정책으로 실행합니다.

```bash
modelctl doctor
modelctl run
```

설정을 바꾸지 않고 이번 실행에만 정책을 덮어쓸 수 있습니다.

```bash
modelctl run --strict-compatibility
modelctl run --warn-compatibility
```

Strict 실행은 알려진 비호환 조합에서 subprocess를 생성하기 전에 종료합니다. Warn 실행은 호환성 경고를 표시한 뒤 계속 진행합니다. 호환성 경고는 `modelctl launchers remediate`를 안내하므로 실제 변경 전에 권장 launcher와 변경 계획을 검토할 수 있습니다.

`run` 뒤에서 modelctl 옵션이 아닌 값은 launcher에 그대로 전달됩니다.

```bash
modelctl run --continue
modelctl run --sandbox workspace-write
modelctl run --strict-compatibility --sandbox workspace-write
modelctl run --no-auto-commits
```

Launcher에 전달하려는 인자 이름이 modelctl 옵션과 충돌하는 경우 `--` 뒤에 배치하세요.

## OpenRouter 호환성

Claude Code, Gemini CLI, Codex CLI는 각각 자체 provider용 네이티브 client입니다. 기본 `warn` 정책에서는 다른 provider의 모델을 전달해도 실행을 차단하지 않고 경고를 표시합니다. 저장 정책을 `strict`로 바꾸거나 `--strict-compatibility`를 추가하면 해당 실행을 거부합니다.

현재 OpenRouter 자동 연동은 Aider를 사용합니다. Launcher를 임의로 변경하기보다 capability 기반 remediation 계획을 먼저 확인하고 적용할 수 있습니다.

```bash
modelctl config set provider openrouter
modelctl config set model anthropic/claude-sonnet-4
modelctl launchers remediate
modelctl launchers remediate --apply
modelctl config set compatibility-policy strict
modelctl run
```

계획 적용 후 실행 결과는 다음과 같습니다.

```bash
aider --model openrouter/anthropic/claude-sonnet-4
```

## 설정과 로컬 데이터

```bash
modelctl config show
modelctl config set provider openrouter
modelctl config set model anthropic/claude-sonnet-4
modelctl config set launcher aider
modelctl config set compatibility-policy strict
```

지원되는 호환성 정책은 정확히 `warn`과 `strict` 두 가지입니다. 잘못 저장된 값은 실행 강도를 임의로 낮추거나 높이지 않고 명시적으로 오류 처리합니다.

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
python scripts/release_validation.py --tag v0.2.0
```

현재 `0.2.0` manifest는 `draft`이므로 release를 게시할 수 없습니다. 명시적으로 `ready`로 전환한 뒤 신뢰된 `main` push 또는 검토된 `main` 대상 Pull Request 병합은 다음 검증을 독립적으로 통과해야 합니다.

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

- 추가로 안전성이 검증된 조치가 생긴 뒤 launcher 선택 외 remediation으로 확장
- OpenRouter 외 capability를 검증할 native provider 연동 추가
- 완성된 사용자 흐름과 테스트를 전제로 한 profile 관리
- 별도 검토를 거치는 PyPI 게시 milestone
