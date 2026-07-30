# modelctl

> **The universal AI model and coding agent control plane**

AI CLI 생태계의 `uv`를 목표로 하는 범용 AI 실행 환경 관리자

---

# 프로젝트 정의

## 한 줄 설명

```text
modelctl은 다양한 AI Coding Agent와 LLM Provider를 하나의 CLI 인터페이스로 관리하는 도구입니다.
```

---

# 사용 예시

```bash
modelctl
```

모델 선택:

```text
Launcher
────────────────────

❯ Claude Code
  Gemini CLI
  Codex CLI
  Aider


Provider
────────────────────

❯ OpenRouter
  Anthropic
  OpenAI
  Google
  Ollama


Model
────────────────────

❯ GPT-5
  Claude Sonnet
  Gemini 2.5 Pro
  DeepSeek V3
```

선택 후:

```text
Launching Claude Code
Provider: OpenRouter
Model: openai/gpt-5
```

---

# Repository 구조

```text
modelctl/

├── src/
│   └── modelctl/
│       │
│       ├── cli.py
│       ├── main.py
│       │
│       ├── core/
│       │   ├── config.py
│       │   ├── database.py
│       │   ├── registry.py
│       │   └── exceptions.py
│       │
│       ├── models/
│       │   ├── model.py
│       │   ├── provider.py
│       │   └── launcher.py
│       │
│       ├── providers/
│       │   ├── base.py
│       │   ├── openrouter.py
│       │   └── anthropic.py
│       │
│       ├── launchers/
│       │   ├── base.py
│       │   └── claude_code.py
│       │
│       ├── services/
│       │   ├── model_service.py
│       │   ├── config_service.py
│       │   └── credential_service.py
│       │
│       └── ui/
│           ├── console.py
│           └── menu.py
│
├── tests/
│
├── docs/
│
├── scripts/
│
├── pyproject.toml
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
└── SECURITY.md
```

---

# v0.1 범위 확정

## 반드시 구현

### CLI

```bash
modelctl init
modelctl doctor
modelctl providers
modelctl models
modelctl run
```

---

### Provider

첫 번째:

✅ OpenRouter

지원:

* 모델 목록 조회
* 모델 캐싱
* API Key 관리
* 모델 선택

---

### Launcher

첫 번째:

✅ Claude Code

지원:

* 설치 확인
* 실행
* 환경 변수 주입
* Provider 연결

---

### Storage

SQLite:

```text
providers
models
launchers
history
favorites
config
```

---

# v0.1 성공 기준

다음 시나리오가 동작하면 성공입니다.

## 1. 설치

```bash
pip install modelctl
```

---

## 2. 초기화

```bash
modelctl init
```

---

## 3. OpenRouter 등록

```bash
modelctl login openrouter
```

---

## 4. 모델 확인

```bash
modelctl models
```

출력:

```
openai/gpt-5
google/gemini-2.5-pro
anthropic/claude-sonnet-4
deepseek/deepseek-chat-v3
...
```

---

## 5. 실행

```bash
modelctl run
```

선택:

```
Claude Code
+
OpenRouter
+
GPT-5
```

↓

Claude Code 실행

---

# 개발 규칙

## Code Style

* Python 3.12+
* Type hint 필수
* Ruff 적용
* Black style
* Docstring 작성

---

## Testing

최소:

* Provider unit test
* Config test
* Database test
* Launcher test

---

## Security

중요: API Key는 절대❌ config.toml 저장하지 않습니다.  
사용:  
✅ Windows Credential Manager
✅ macOS Keychain
✅ Linux Secret Service

via:  
```python
keyring
```

---

# Git Branch 전략

```text
main
 |
 ├── develop
 |
 ├── feature/provider-openrouter
 ├── feature/launcher-claude
 ├── feature/database
 └── feature/cli
```

---

# 기술 스택

- Python 3.12+
- Typer
- Rich
- Pydantic v2
- SQLModel
- httpx
- platformdirs
- keyring (API 키를 OS 자격 증명 저장소에 보관)
- pytest
- Ruff
- GitHub Actions

# 진행방식

## Sprint 0

- 프로젝트 이름 확정
- 아키텍처 문서(ADR)
- 저장소 생성
- 기본 디렉터리
- CI
- 개발 규칙
- 첫 커밋

## Sprint 1

- CLI
- Config
- SQLite
- OpenRouter Provider
- Claude Launcher

## Sprint 2

- 즐겨찾기
- 최근 사용
- Preview
- 프로젝트 설정
- Sprint 3
- Gemini CLI
- Codex CLI
- Ollama
- 플러그인 SDK

---

# Sprint 0 - Repository Bootstrap

## Step 1

- Python 패키지 구조 생성
- CLI 진입점 구성
- 개발 환경 구성
- 기본 명령어 동작

## Step 2

핵심 기반 구조 구현

1. `core/config.py`

- OS별 config path
- TOML 설정
- `modelctl init`

2. `keyring`

- OpenRouter API Key 안전 저장

3. `doctor`

- Python
- Claude Code
- Git
- API Key
- Database 상태 검사

4. GitHub Actions CI

---

# Sprint 1 - Core Engine

다음 구현:

## Provider Interface

```python
class Provider:

    name

    login()

    list_models()

    validate()
```

## 첫 번째 Provider:

### OpenRouter Provider

기능:
```bash
modelctl login openrouter
```

↓

API Key 저장
```bash
modelctl refresh
```

↓

OpenRouter API 호출

↓

SQLite 저장

```bash
modelctl models
```

↓

출력:

```bash
openai/gpt-5
google/gemini-2.5-pro
anthropic/claude-sonnet-4
deepseek/deepseek-chat-v3
...
```

