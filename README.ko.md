# modelctl

[English](README.md) | [한국어](README.ko.md)

**AI 모델과 코딩 에이전트를 통합 관리하는 범용 control plane입니다.**

`modelctl`은 AI provider와 모델 선택, 로컬 credential과 기본 설정 관리, 호환성 진단, 여러 코딩 에이전트 CLI 실행을 하나의 명령 체계로 제공합니다.

> 현재 개발 버전은 `0.3.0`(`draft`)이며 최신 ready release는 `0.2.0`입니다. `main`은 공식 release branch이고 PyPI 게시는 비활성화되어 있습니다.

## v0.3.0 개발 현황

첫 번째 v0.3.0 increment로 이름 있는 설정 profile을 추가했습니다.

- provider, model, launcher, compatibility policy를 하나의 snapshot으로 저장
- 저장한 profile 목록과 상세 내용 조회
- 전체 snapshot을 검증한 뒤 설정을 한 번만 원자적으로 저장
- 손상된 profile과 예상하지 않은 필드 거부
- credential과 launcher 인증정보를 profile에서 제외
- 기존 선택, 진단, remediation, 실행 동작 유지

현재 increment는 Ruff, package 검증, 설치 wheel smoke test와 Python 3.13 기반 Ubuntu·macOS·Windows의 전체 150개 테스트를 통과합니다.

## v0.2.0 주요 기능

- OpenRouter, Anthropic, Google Gemini, OpenAI 모델 catalog
- Claude Code, Gemini CLI, Codex CLI, Aider launcher
- 대화형·비대화형 provider/model 선택
- Provider-aware launcher 추천
- 미리보기 우선 호환성 remediation과 명시적 안전 적용
- 저장 가능한 `warn`·`strict` 정책과 실행 1회 override
- Shell 없이 native launcher 인자 전달
- Keyring 우선 credential 저장과 명시적 평문 fallback
- Provider credential과 launcher 인증 분리
- 패치된 `cryptography 50.0.0`과 advisory 예외 없는 dependency audit
- SHA-256 checksum을 포함한 불변 GitHub Release artifact

프로젝트 상태는 [`docs/PROGRESS.md`](docs/PROGRESS.md), PR별 영문·한국어 기록은 [`docs/pull-requests/README.md`](docs/pull-requests/README.md)를 참고하세요.

## 저장소에서 설치

이 저장소는 Python 3.13 이상을 사용하는 uv workspace입니다.

```bash
git clone https://github.com/LEEBONGHAK/modelctl.git
cd modelctl
git switch main
uv sync --all-packages --locked
uv run modelctl --help
```

## Provider별 사용 흐름

### OpenRouter + Aider

```bash
modelctl auth login openrouter
modelctl models sync openrouter
modelctl use --provider openrouter --model anthropic/claude-sonnet-4
modelctl launchers remediate
modelctl launchers remediate --apply
modelctl config set compatibility-policy strict
modelctl run
```

Aider에는 다음 ID가 전달됩니다.

```text
openrouter/anthropic/claude-sonnet-4
```

### Anthropic + Claude Code

```bash
modelctl auth login anthropic
modelctl models sync anthropic
modelctl use --provider anthropic --model claude-opus-4-6
modelctl launchers recommend
modelctl config set compatibility-policy strict
modelctl run
```

Catalog 동기화에는 저장 credential 대신 `ANTHROPIC_API_KEY`를 사용할 수 있습니다.

### Google Gemini + Gemini CLI

```bash
modelctl auth login google
modelctl models sync google
modelctl use --provider google --model gemini-3.5-flash
modelctl launchers recommend
modelctl config set compatibility-policy strict
modelctl run
```

환경변수 우선순위는 `MODELCTL_GOOGLE`, `GOOGLE_API_KEY`, `GEMINI_API_KEY`입니다.

### OpenAI + Codex CLI

```bash
modelctl auth login openai
modelctl models sync openai
modelctl use --provider openai --model gpt-5.6
modelctl launchers recommend
modelctl config set compatibility-policy strict
modelctl run
```

Catalog 동기화에는 저장 credential 대신 `OPENAI_API_KEY`를 사용할 수 있습니다.

modelctl이 관리하는 provider credential은 catalog 동기화에만 사용합니다. Keyring의 secret을 launcher subprocess 환경으로 복사하지 않으며 각 코딩 에이전트 CLI가 자체 인증 흐름을 관리합니다.

## 이름 있는 Profile

현재 적용된 provider, model, launcher, compatibility policy를 저장합니다.

```bash
modelctl profiles save work
modelctl profiles list
modelctl profiles show work
modelctl profiles use work
modelctl profiles delete work
```

Profile 이름은 소문자로 정규화하며 문자, 숫자, 마침표, 밑줄, 하이픈을 사용할 수 있습니다. Profile 적용 전 provider/model과 launcher를 모두 검증하고 설정을 한 번만 원자적으로 저장합니다. 관련 없는 설정과 다른 profile은 그대로 보존합니다.

Profile에는 credential, 환경변수 secret, launcher가 관리하는 인증정보를 포함하지 않습니다. 손상되거나 일부 필드가 누락되거나 예상하지 않은 필드가 추가된 profile은 명시적으로 거부합니다.

## Launcher 관리

```bash
modelctl launchers list
modelctl launchers recommend
modelctl launchers recommend --apply
modelctl launchers remediate
modelctl launchers remediate --apply
modelctl launchers use aider
```

| ID | 코딩 에이전트 | Native provider | 기본 실행 |
| --- | --- | --- | --- |
| `claude` | Claude Code | Anthropic | `claude --model <model>` |
| `gemini` | Gemini CLI | Google | `gemini --model <model>` |
| `codex` | Codex CLI | OpenAI | `codex --model <model>` |
| `aider` | Aider | 변환 provider | `aider --model <model>` |

`recommend`는 capability가 맞는 launcher를 제안합니다. `remediate`는 현재 launcher에 알려진 불일치가 있을 때만 변경 계획을 만듭니다.

두 명령은 기본적으로 읽기 전용입니다. `--apply`는 설치된 추천 launcher만 선택하며 설정 변경 전에 사용 가능 여부를 검사합니다. 소프트웨어 설치, provider/model 변경, launcher 자동 실행은 하지 않습니다.

## 호환성 정책과 실행

저장 정책의 기본값은 기존 동작을 유지하는 `warn`입니다.

```bash
modelctl config set compatibility-policy warn
modelctl config set compatibility-policy strict
modelctl doctor
modelctl run
```

이번 실행에만 정책을 덮어쓸 수 있습니다.

```bash
modelctl run --strict-compatibility
modelctl run --warn-compatibility
```

`run` 뒤에서 modelctl 옵션이 아닌 값은 선택한 launcher에 그대로 전달합니다.

```bash
modelctl run --continue
modelctl run --sandbox workspace-write
modelctl run --strict-compatibility --sandbox workspace-write
modelctl run --no-auto-commits
```

Launcher 인자 이름이 modelctl 옵션과 충돌하면 `--` 뒤에 배치하세요.

## Credential과 로컬 데이터

기본 로그인 흐름은 운영체제 keyring에 credential을 저장하며 평문 저장으로 자동 전환하지 않습니다.

```bash
modelctl auth login openrouter --allow-plaintext-fallback
```

명시적으로 승인한 fallback은 암호화되지 않은 평문입니다. 보호 경로는 원자적으로 저장하고 symbolic link를 거부하며 POSIX에서 directory `0700`, file `0600` 권한을 사용합니다.

```text
~/.config/modelctl/config.json
~/.config/modelctl/credentials.json   # 명시적 fallback 사용 시에만 생성
~/.local/share/modelctl/modelctl.db
```

이름 있는 profile은 `config.json` 내부에 저장하며 `credentials.json`이나 운영체제 keyring의 값을 참조하거나 복사하지 않습니다.

## 개발 및 검증

```bash
uv sync --all-packages --locked
uv audit --locked
uv run ruff check .
uv run pytest
python scripts/release_validation.py
```

GitHub Actions는 provider contract 테스트, Ubuntu·macOS·Windows 전체 pytest, 모든 배포물 build, 격리 환경 wheel 설치, release metadata, checksum 생성을 독립적으로 검증합니다.

## 릴리스 정책

Release 결정은 [`release.toml`](release.toml), 변경 사항은 [`CHANGELOG.md`](CHANGELOG.md), 완료 기준은 [`docs/RELEASE_CRITERIA.md`](docs/RELEASE_CRITERIA.md)에서 관리합니다.

`0.3.0` manifest는 `draft`이므로 기능 PR에서 게시할 수 없습니다. 최신 ready release는 `main`의 `0.2.0`입니다. 향후 전용 readiness PR에서 모든 v0.3.0 완료 기준을 충족해야 승격과 게시가 가능합니다.

기존 tag와 release asset은 덮어쓰지 않습니다. **어떤 workflow도 PyPI에 package를 게시하지 않습니다.** 자세한 절차는 [`docs/RELEASING.md`](docs/RELEASING.md)를 참고하세요.

## 프로젝트 구조

```text
apps/modelctl/       Typer CLI 애플리케이션
packages/core/       runtime service, credential, provider, repository, launcher
packages/sdk/        SDK 기반
scripts/             release 검증 helper
tests/               회귀, 통합, 패키징, 보안 테스트
docs/                provider, 프로젝트, 릴리스, 보안, PR 문서
```

## 보안

Credential 동작, 취약점 제보, dependency 보안, release 신뢰 경계, 알려진 한계는 [`SECURITY.md`](SECURITY.md)를 참고하세요.

## 남은 v0.3.0 로드맵

- 검증된 workflow에서 실제 필요성이 확인된 profile 이식 기능만 추가
- 최소 범위의 versioned launcher plugin SDK 계약 정의
- 임의 filesystem import나 자동 download 없이 설치된 launcher plugin 탐색
- Plugin 진단과 static type check를 별도 milestone로 도입
- PyPI Trusted Publishing 별도 검토
