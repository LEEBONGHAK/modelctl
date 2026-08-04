# Google Gemini provider / Google Gemini provider 연동

## English

### Scope

The Google provider synchronizes the official Gemini API model catalog into modelctl and connects provider selection to the existing Gemini CLI recommendation, strict compatibility policy, and remediation workflow.

The provider uses:

- Provider ID: `google`
- API base URL: `https://generativelanguage.googleapis.com/v1beta`
- Model endpoint: `GET /models`
- Authentication header: `x-goog-api-key`
- Page size: up to 1,000 models

Pagination is bounded and rejects malformed responses, invalid or repeated page tokens, and excessive page counts.

### Credential resolution

Google Gemini credentials are resolved in this order:

1. `MODELCTL_GOOGLE`
2. `GOOGLE_API_KEY`
3. `GEMINI_API_KEY`
4. Operating-system keyring entry saved by modelctl
5. Explicitly accepted user-private plaintext fallback file

The ordering of the two official variables follows the Gemini API client behavior: `GOOGLE_API_KEY` takes precedence when both official variables are set.

Store a credential with modelctl:

```bash
modelctl auth login google
```

Or use an official environment variable:

```bash
export GOOGLE_API_KEY=your-api-key
# or
export GEMINI_API_KEY=your-api-key
```

### Synchronize and select

```bash
modelctl models sync google
modelctl use --provider google --model gemini-3.5-flash
```

The provider keeps only models whose `supportedGenerationMethods` include `generateContent`. Embedding-only and other non-generative models are excluded from the coding-agent selection catalog.

The mapper stores the normalized model ID without the `models/` resource prefix, display name, maximum input tokens, generation support, and thinking capability. The Models API response does not provide pricing, so prompt and completion prices remain zero. Vision support is left false because this catalog response does not declare input modalities.

### Launcher workflow

```bash
modelctl launchers recommend
modelctl launchers remediate
modelctl config set compatibility-policy strict
modelctl run
```

For provider `google`, modelctl recommends the native `gemini` launcher. A mismatched active launcher can be previewed and changed explicitly with:

```bash
modelctl launchers remediate
modelctl launchers remediate --apply
```

### Authentication boundary

The Google API credential managed by modelctl is used for model-catalog synchronization. Gemini CLI continues to use its own supported authentication methods. modelctl does not copy a stored API key into a subprocess environment automatically.

## 한국어

### 범위

Google provider는 공식 Gemini API 모델 catalog를 modelctl에 동기화하고, 선택한 provider를 기존 Gemini CLI 추천, strict 호환성 정책, remediation 흐름에 연결합니다.

사용하는 API 계약은 다음과 같습니다.

- Provider ID: `google`
- API base URL: `https://generativelanguage.googleapis.com/v1beta`
- 모델 endpoint: `GET /models`
- 인증 header: `x-goog-api-key`
- 페이지 크기: 최대 1,000개 모델

Pagination은 최대 페이지 수를 제한하며 잘못된 응답, 유효하지 않거나 반복된 page token, 과도한 페이지 수를 명시적으로 거부합니다.

### Credential 조회 순서

Google Gemini credential은 다음 순서로 조회합니다.

1. `MODELCTL_GOOGLE`
2. `GOOGLE_API_KEY`
3. `GEMINI_API_KEY`
4. modelctl이 운영체제 keyring에 저장한 값
5. 사용자가 명시적으로 허용한 사용자 전용 평문 fallback 파일

두 공식 환경변수가 모두 설정된 경우 Gemini API client 동작과 동일하게 `GOOGLE_API_KEY`가 우선합니다.

modelctl에 credential을 저장할 수 있습니다.

```bash
modelctl auth login google
```

또는 공식 환경변수를 사용할 수 있습니다.

```bash
export GOOGLE_API_KEY=your-api-key
# 또는
export GEMINI_API_KEY=your-api-key
```

### 동기화 및 선택

```bash
modelctl models sync google
modelctl use --provider google --model gemini-3.5-flash
```

Provider는 `supportedGenerationMethods`에 `generateContent`가 포함된 모델만 유지합니다. Embedding 전용 모델과 기타 비생성 모델은 coding-agent 선택 catalog에서 제외합니다.

Mapper는 `models/` resource prefix를 제거한 모델 ID, 표시 이름, 최대 입력 token, 생성 지원, thinking capability를 저장합니다. Models API 응답은 가격 정보를 제공하지 않으므로 prompt와 completion 가격은 0으로 유지합니다. 이 catalog 응답은 입력 modality를 선언하지 않으므로 vision 지원은 false로 둡니다.

### Launcher 흐름

```bash
modelctl launchers recommend
modelctl launchers remediate
modelctl config set compatibility-policy strict
modelctl run
```

`google` provider에는 native `gemini` launcher가 추천됩니다. 현재 launcher가 불일치하는 경우 다음 명령으로 변경 계획을 확인하고 명시적으로 적용할 수 있습니다.

```bash
modelctl launchers remediate
modelctl launchers remediate --apply
```

### 인증 경계

modelctl이 관리하는 Google API credential은 모델 catalog 동기화에 사용합니다. Gemini CLI는 자체적으로 지원하는 인증 방식을 계속 사용합니다. modelctl은 저장된 API key를 subprocess 환경에 자동 복사하지 않습니다.
