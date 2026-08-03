# modelctl

[English](README.md) | [한국어](README.ko.md)

**AI 모델과 코딩 에이전트를 통합 관리하는 범용 control plane입니다.**

`modelctl`은 AI provider와 모델 선택, 로컬 설정 관리, 코딩 에이전트 실행을 하나의 CLI로 일관되게 처리하는 **AI 코딩 에이전트의 uv**를 목표로 합니다.

> 개발 상태: 활발히 개발 중인 pre-release입니다. 현재 동작하는 구현은 `refac` branch에 있습니다.

## 현재 동작하는 기능

- OpenRouter credential 저장과 모델 동기화
- `modelctl use`를 통한 대화형·비대화형 provider/model 선택
- Provider, model, launcher 설정 영속화
- Claude Code, Gemini CLI, Codex CLI, Aider launcher
- Shell을 사용하지 않는 네이티브 launcher 인자 전달
- Launcher 목록, 설치 상태 확인, 선택
- `modelctl doctor` 로컬 환경 진단
- Provider/model/launcher 비차단 호환성 경고
- 운영체제 keyring을 이용한 안전한 credential 저장
- Keyring을 사용할 수 없을 때만 명시적으로 허용하는 사용자 전용 평문 fallback
- Linux Ruff 및 lockfile dependency audit
- Python 3.13 기반 Linux, macOS, Windows pytest 검증
- CLI, core, SDK wheel 및 source distribution 빌드
- 설치된 wheel smoke test와 검증된 GitHub Release artifact

전체 구현 이력과 로드맵은 [`docs/PROGRESS.md`](docs/PROGRESS.md), PR별 영문·한국어 기록은 [`docs/pull-requests/README.md`](docs/pull-requests/README.md)를 참고하세요.

## 개발 환경 설치

이 저장소는 Python 3.13 이상을 사용하는 uv workspace입니다.

```bash
git clone https://github.com/LEEBONGHAK/modelctl.git
cd modelctl
git switch refac
uv sync --all-packages --locked
uv run modelctl --help
```

## 빠른 시작

### 1. Provider credential 저장

```bash
modelctl auth login openrouter
```

Credential은 기본적으로 운영체제 keyring에 저장됩니다. Keyring을 사용할 수 없더라도 `modelctl`은 평문 파일 저장으로 자동 전환하지 않습니다.

위험을 이해하고 명시적으로 허용할 때만 보호된 로컬 파일 fallback을 사용할 수 있습니다.

```bash
modelctl auth login openrouter --allow-plaintext-fallback
```

Fallback 파일은 POSIX 운영체제에서 현재 사용자만 읽을 수 있도록 제한되지만, 내용 자체는 **암호화되지 않은 평문**입니다. 가능한 경우 keyring 또는 `MODELCTL_OPENROUTER`와 같은 환경변수를 사용하세요.

### 2. 모델 동기화 및 선택

```bash
modelctl models sync openrouter
modelctl use
```

Script와 CI에서는 다음처럼 비대화형으로 선택할 수 있습니다.

```bash
modelctl use \
  --provider openrouter \
  --model anthropic/claude-sonnet-4
```

`--provider`와 `--model`은 반드시 함께 사용해야 합니다. 직접 지정한 값은 provider registry와 동기화된 로컬 모델 catalog를 기준으로 검증됩니다.

### 3. 코딩 에이전트 launcher 선택

```bash
modelctl launchers list
modelctl launchers use claude
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

`run` 뒤의 인자는 문자열 shell 명령이 아니라 인자 목록으로 네이티브 launcher에 전달됩니다.

```bash
modelctl run --continue
modelctl run --sandbox workspace-write
modelctl run --no-auto-commits
```

## 호환성 안내

Claude Code, Gemini CLI, Codex CLI는 각각 Anthropic, Google, OpenAI의 네이티브 client입니다. 다른 provider에서 선택한 모델을 전달하면 `modelctl`은 실행 전과 `modelctl doctor`에서 비차단 경고를 표시합니다.

OpenRouter 모델 이름을 자동 변환하려면 Aider를 선택하세요.

```bash
modelctl launchers use aider
modelctl config set provider openrouter
modelctl config set model anthropic/claude-sonnet-4
modelctl run
```

실제 실행 명령은 다음과 같습니다.

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

설정과 fallback credential은 임시 파일을 이용해 원자적으로 저장됩니다. POSIX 운영체제에서는 private directory와 file 권한을 각각 `0700`, `0600`으로 제한하며, 보호 대상 경로가 symbolic link이면 접근을 거부합니다.

## 개발 및 보안 검증

```bash
uv sync --all-packages --locked
uv audit --locked
uv run ruff check .
uv run pytest
```

GitHub Actions에서는 다음을 검증합니다.

- Ubuntu에서 Ruff 및 lockfile dependency audit
- Python 3.13 기반 Ubuntu, macOS, Windows 전체 pytest
- 배포물 빌드 및 설치된 wheel smoke test
- Release tag, artifact, checksum 검증
- 외부 GitHub Actions의 전체 commit SHA 고정

## 패키지 및 릴리스 검증

```bash
uv build packages/core --out-dir dist --no-sources
uv build packages/sdk --out-dir dist --no-sources
uv build apps/modelctl --out-dir dist --no-sources
python scripts/release_validation.py --tag v0.1.0
```

세 패키지 버전이 일치하고 release commit이 `refac`에 포함된 완성 버전은 수동으로 tag를 생성할 수 있습니다. 검증된 `v*` tag가 push되면 배포 파일과 `SHA256SUMS`가 포함된 GitHub Release가 생성됩니다.

**PyPI 게시는 의도적으로 비활성화되어 있습니다.** 현재 어떤 workflow job도 PyPI에 package를 게시하지 않습니다. 자세한 절차는 [`docs/RELEASING.md`](docs/RELEASING.md)를 참고하세요.

## 프로젝트 구조

```text
apps/modelctl/       Typer CLI 애플리케이션
packages/core/       runtime service, provider, repository, launcher
packages/sdk/        SDK package 기반
scripts/             저장소 검증 및 release helper
tests/               회귀, 통합, 보안 테스트
docs/                프로젝트, 릴리스, 보안, PR 문서
```

## 보안

Credential 저장 방식, 취약점 제보 방법, 지원 버전, 알려진 한계는 [`SECURITY.md`](SECURITY.md)를 참고하세요. 보안 테스트와 dependency audit는 확인된 위험을 줄이지만, 독립적인 침투 테스트나 정식 보안 평가를 대체하지는 않습니다.

## 단기 로드맵

- 첫 개발 버전 완성 및 tag 생성
- 더 엄격한 호환성 정책과 자동 조치
- 검증된 요구사항을 바탕으로 launcher capability와 execution request 리팩터링
- 핵심 설정 흐름이 안정된 이후 profile 관리 구현
