# Anthropic provider / Anthropic provider 연동

## English

### Scope

The Anthropic provider synchronizes the official Anthropic model catalog into modelctl and connects that provider selection to the existing Claude Code launcher recommendation, strict compatibility policy, and remediation workflow.

The provider uses:

- API base URL: `https://api.anthropic.com/v1`
- Model endpoint: `GET /models`
- Authentication header: `x-api-key`
- Version header: `anthropic-version: 2023-06-01`
- Page size: up to 1,000 models

Pagination is bounded and rejects malformed responses, missing cursors, repeated cursors, and excessive page counts.

### Credential resolution

Anthropic credentials are resolved in this order:

1. `MODELCTL_ANTHROPIC`
2. `ANTHROPIC_API_KEY`
3. Operating-system keyring entry saved by modelctl
4. Explicitly accepted user-private plaintext fallback file

Store a credential with modelctl:

```bash
modelctl auth login anthropic
```

Or supply the official Anthropic environment variable:

```bash
export ANTHROPIC_API_KEY=your-api-key
```

### Synchronize and select

```bash
modelctl models sync anthropic
modelctl use --provider anthropic --model claude-opus-4-6
```

The catalog mapper stores the model ID, display name, maximum input tokens, image-input capability, and thinking capability. Anthropic's Models API does not provide model pricing in this response, so modelctl stores zero for prompt and completion prices.

### Launcher workflow

```bash
modelctl launchers recommend
modelctl launchers remediate
modelctl config set compatibility-policy strict
modelctl run
```

For provider `anthropic`, modelctl recommends the native `claude` launcher. A mismatched active launcher can be previewed and changed explicitly with:

```bash
modelctl launchers remediate
modelctl launchers remediate --apply
```

### Authentication boundary

The Anthropic credential managed by modelctl is used for model-catalog synchronization. Claude Code continues to use its own supported authentication methods. modelctl does not copy a stored API key into a subprocess environment automatically.

This separation avoids silently exposing stored credentials to child processes and keeps launcher authentication behavior consistent with the native CLI.

## 한국어

### 범위

Anthropic provider는 공식 Anthropic 모델 catalog를 modelctl에 동기화하고, 선택된 provider를 기존 Claude Code launcher 추천, strict 호환성 정책, remediation 흐름에 연결합니다.

사용하는 API 계약은 다음과 같습니다.

- API base URL: `https://api.anthropic.com/v1`
- 모델 endpoint: `GET /models`
- 인증 header: `x-api-key`
- 버전 header: `anthropic-version: 2023-06-01`
- 페이지 크기: 최대 1,000개 모델

Pagination은 최대 페이지 수를 제한하며 잘못된 응답, 누락된 cursor, 반복 cursor, 과도한 페이지 수를 명시적으로 거부합니다.

### Credential 조회 순서

Anthropic credential은 다음 순서로 조회합니다.

1. `MODELCTL_ANTHROPIC`
2. `ANTHROPIC_API_KEY`
3. modelctl이 운영체제 keyring에 저장한 값
4. 사용자가 명시적으로 허용한 사용자 전용 평문 fallback 파일

modelctl에 credential을 저장할 수 있습니다.

```bash
modelctl auth login anthropic
```

또는 Anthropic 공식 환경변수를 사용할 수 있습니다.

```bash
export ANTHROPIC_API_KEY=your-api-key
```

### 동기화 및 선택

```bash
modelctl models sync anthropic
modelctl use --provider anthropic --model claude-opus-4-6
```

Catalog mapper는 모델 ID, 표시 이름, 최대 입력 token, 이미지 입력 capability, thinking capability를 저장합니다. Anthropic Models API 응답은 가격 정보를 제공하지 않으므로 prompt와 completion 가격은 0으로 저장합니다.

### Launcher 흐름

```bash
modelctl launchers recommend
modelctl launchers remediate
modelctl config set compatibility-policy strict
modelctl run
```

`anthropic` provider에는 native `claude` launcher가 추천됩니다. 현재 launcher가 불일치하는 경우 다음 명령으로 변경 계획을 확인하고 명시적으로 적용할 수 있습니다.

```bash
modelctl launchers remediate
modelctl launchers remediate --apply
```

### 인증 경계

modelctl이 관리하는 Anthropic credential은 모델 catalog 동기화에 사용합니다. Claude Code는 자체적으로 지원하는 인증 방식을 계속 사용합니다. modelctl은 저장된 API key를 subprocess 환경에 자동 복사하지 않습니다.

이 분리는 저장된 credential이 child process에 조용히 노출되는 것을 방지하고 native CLI의 인증 동작을 유지합니다.
