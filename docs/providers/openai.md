# OpenAI provider / OpenAI provider 연동

## English

### Scope

The OpenAI provider synchronizes the official OpenAI model catalog into modelctl and connects provider selection to the existing Codex CLI recommendation, strict compatibility policy, and remediation workflow.

The provider uses:

- API base URL: `https://api.openai.com/v1`
- Model endpoint: `GET /models`
- Authentication header: `Authorization: Bearer <api-key>`
- Redirects disabled
- Bounded connect and total timeouts

The Models API returns model IDs, object type, creation time, and owner. It does not provide endpoint capability, context length, modality, or pricing metadata in this response.

### Credential resolution

OpenAI credentials are resolved in this order:

1. `MODELCTL_OPENAI`
2. `OPENAI_API_KEY`
3. Operating-system keyring entry saved by modelctl
4. Explicitly accepted user-private plaintext fallback file

Store a credential with modelctl:

```bash
modelctl auth login openai
```

Or supply the official environment variable:

```bash
export OPENAI_API_KEY=your-api-key
```

### Synchronize and select

```bash
modelctl models sync openai
modelctl use --provider openai --model gpt-5.6
```

Because the Models API does not expose detailed capability metadata, modelctl uses a conservative coding-candidate filter. It includes GPT, o-series, and Codex families while excluding clearly non-coding families such as embeddings, image generation, audio, transcription, text-to-speech, moderation, realtime, search, computer-use, deep-research, Sora, and fine-tuned IDs.

The mapper stores the model ID as both ID and display name. Context length and prices remain zero, and vision support remains false, because those fields cannot be confirmed from this response. Tool support is enabled for accepted coding candidates. Reasoning is enabled for o-series, GPT-5, and Codex IDs.

### Launcher workflow

```bash
modelctl launchers recommend
modelctl launchers remediate
modelctl config set compatibility-policy strict
modelctl run
```

For provider `openai`, modelctl recommends the native `codex` launcher. A mismatched active launcher can be previewed and changed explicitly with:

```bash
modelctl launchers remediate
modelctl launchers remediate --apply
```

### Authentication boundary

The OpenAI credential managed by modelctl is used for model-catalog synchronization. Codex CLI continues to use its own supported authentication methods, including ChatGPT sign-in or separately configured API-key use. modelctl does not copy a stored API key into a subprocess environment automatically.

This separation avoids silently exposing stored credentials to child processes and keeps launcher authentication behavior consistent with the native CLI.

## 한국어

### 범위

OpenAI provider는 공식 OpenAI 모델 catalog를 modelctl에 동기화하고, 선택된 provider를 기존 Codex CLI launcher 추천, strict 호환성 정책, remediation 흐름에 연결합니다.

사용하는 API 계약은 다음과 같습니다.

- API base URL: `https://api.openai.com/v1`
- 모델 endpoint: `GET /models`
- 인증 header: `Authorization: Bearer <api-key>`
- Redirect 비활성화
- 제한된 connect·전체 timeout

Models API 응답은 모델 ID, object type, 생성 시각, owner를 제공합니다. 이 응답에는 endpoint capability, context length, modality, 가격 metadata가 포함되지 않습니다.

### Credential 조회 순서

OpenAI credential은 다음 순서로 조회합니다.

1. `MODELCTL_OPENAI`
2. `OPENAI_API_KEY`
3. modelctl이 운영체제 keyring에 저장한 값
4. 사용자가 명시적으로 허용한 사용자 전용 평문 fallback 파일

modelctl에 credential을 저장할 수 있습니다.

```bash
modelctl auth login openai
```

또는 공식 환경변수를 사용할 수 있습니다.

```bash
export OPENAI_API_KEY=your-api-key
```

### 동기화 및 선택

```bash
modelctl models sync openai
modelctl use --provider openai --model gpt-5.6
```

Models API가 상세 capability metadata를 제공하지 않으므로 modelctl은 보수적인 coding candidate 필터를 사용합니다. GPT, o-series, Codex 계열은 포함하고 embedding, image generation, audio, transcription, TTS, moderation, realtime, search, computer-use, deep-research, Sora, fine-tuned ID처럼 명백히 coding-agent용이 아닌 계열은 제외합니다.

Mapper는 모델 ID를 ID와 표시 이름으로 저장합니다. 이 응답에서 확인할 수 없는 context length와 가격은 0, vision 지원 여부는 false로 유지합니다. 포함된 coding candidate는 tool 지원을 true로 저장하며 o-series, GPT-5, Codex ID는 reasoning 지원을 true로 저장합니다.

### Launcher 흐름

```bash
modelctl launchers recommend
modelctl launchers remediate
modelctl config set compatibility-policy strict
modelctl run
```

`openai` provider에는 native `codex` launcher가 추천됩니다. 현재 launcher가 불일치하는 경우 다음 명령으로 변경 계획을 확인하고 명시적으로 적용할 수 있습니다.

```bash
modelctl launchers remediate
modelctl launchers remediate --apply
```

### 인증 경계

modelctl이 관리하는 OpenAI credential은 모델 catalog 동기화에 사용합니다. Codex CLI는 ChatGPT 로그인 또는 별도로 구성된 API key 사용 등 자체 지원 인증 방식을 계속 사용합니다. modelctl은 저장된 API key를 subprocess 환경에 자동 복사하지 않습니다.

이 분리는 저장된 credential이 child process에 조용히 노출되는 것을 방지하고 native CLI의 인증 동작을 유지합니다.
