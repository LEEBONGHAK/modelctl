# Security Policy / 보안 정책

## Supported versions / 지원 버전

`modelctl` is pre-1.0. Security fixes are applied to the active development branch and the newest GitHub Release. Version `0.2.0` is the current ready development release.

`modelctl`은 1.0 이전 단계입니다. 보안 수정은 활성 개발 branch와 가장 최신 GitHub Release에 적용합니다. 현재 ready 개발 릴리스는 `0.2.0`입니다.

## Reporting a vulnerability / 취약점 제보

Do not include API keys, credentials, exploit payloads, or sensitive local paths in a public issue.

공개 issue에 API key, credential, 실제 공격 payload, 민감한 로컬 경로를 포함하지 마세요.

Use GitHub Private Vulnerability Reporting when available. Otherwise, open a minimal public issue asking for a private contact channel without disclosing exploit details.

GitHub Private Vulnerability Reporting을 사용할 수 있으면 해당 기능을 사용하세요. 사용할 수 없다면 공격 세부사항을 공개하지 않고 비공개 연락 수단을 요청하는 최소한의 issue만 작성하세요.

Include the affected version or commit, operating system, impact, reproduction prerequisites, and a safe proof of concept that does not expose real secrets.

영향받는 버전 또는 commit, 운영체제, 영향, 재현 전제조건, 실제 secret을 노출하지 않는 안전한 proof of concept를 포함하세요.

## Credential storage / Credential 저장

Credential lookup order:

1. Provider-specific modelctl environment variable such as `MODELCTL_OPENROUTER`
2. Supported official provider aliases such as `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `GEMINI_API_KEY`, or `OPENAI_API_KEY`
3. Operating-system keyring
4. Explicitly approved local-file fallback

Credential 조회 순서:

1. `MODELCTL_OPENROUTER`와 같은 provider별 modelctl 환경변수
2. `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `GEMINI_API_KEY`, `OPENAI_API_KEY`와 같은 공식 provider alias
3. 운영체제 keyring
4. 명시적으로 승인한 로컬 파일 fallback

The default login flow stores credentials in the operating-system keyring. A keyring failure never silently downgrades to plaintext; the user must explicitly pass `--allow-plaintext-fallback`.

기본 로그인 흐름은 credential을 운영체제 keyring에 저장합니다. Keyring 실패 시 평문 저장으로 자동 전환하지 않으며 `--allow-plaintext-fallback`을 명시해야 합니다.

The fallback is unencrypted plaintext even though writes are atomic, symbolic links are rejected, and POSIX permissions are restricted to the current user. Treat it as a compatibility option, not equivalent protection to a keyring.

Fallback은 원자적으로 저장되고 symbolic link를 거부하며 POSIX 권한을 현재 사용자로 제한하지만 내용은 암호화되지 않은 평문입니다. Keyring과 동등한 보호 수단이 아닌 호환성 옵션입니다.

Provider credentials managed by modelctl are used for catalog synchronization. They are not copied from keyring storage into coding-agent subprocess environments. Each launcher continues to own its supported authentication flow.

modelctl이 관리하는 provider credential은 catalog 동기화에 사용합니다. Keyring의 secret을 코딩 에이전트 subprocess 환경으로 복사하지 않으며 각 launcher가 자체 인증 흐름을 관리합니다.

## Execution model / 실행 모델

Coding-agent commands are constructed as argument lists and executed without a shell. Native launcher arguments are intentionally forwarded to the selected third-party CLI. Review that agent's security model before granting filesystem, network, tool, or approval permissions.

코딩 에이전트 명령은 인자 목록으로 구성하고 shell 없이 실행합니다. Native launcher 인자는 선택한 외부 CLI에 의도적으로 전달됩니다. 파일시스템, 네트워크, 도구, 승인 권한을 부여하기 전에 해당 에이전트의 보안 모델을 확인하세요.

Compatibility recommendation and remediation are read-only by default. `--apply` changes only the selected launcher, refuses an unavailable recommendation, and never installs software or starts a launcher.

호환성 추천과 remediation은 기본적으로 읽기 전용입니다. `--apply`는 선택 launcher만 변경하고 설치되지 않은 추천은 거부하며 소프트웨어 설치나 launcher 실행을 수행하지 않습니다.

## Dependency security / Dependency 보안

Locked dependencies are audited without a retained advisory exclusion. `cryptography` is locked to patched version `50.0.0`, resolving `GHSA-g6cj-pr64-35w5` / `CVE-2026-69247`. Issue #22 was closed after audit, cross-platform tests, packaging, and release dry-run validation passed.

잠긴 dependency는 advisory 예외를 유지하지 않고 audit합니다. `cryptography`는 `GHSA-g6cj-pr64-35w5` / `CVE-2026-69247`을 해결한 패치 버전 `50.0.0`으로 고정했습니다. Audit, cross-platform test, packaging, release dry-run 통과 후 issue #22를 종료했습니다.

## Release and supply chain / 릴리스와 공급망

- External GitHub Actions are pinned to full commit SHAs. / 외부 GitHub Actions는 전체 commit SHA로 고정합니다.
- Workflows use least-privilege repository permissions. / Workflow는 최소 repository 권한을 사용합니다.
- Locked dependencies are audited in primary CI and again by the release workflow. / Lockfile dependency를 primary CI와 release workflow에서 각각 audit합니다.
- Release tags must match all package versions and point to a validated commit contained in `main`. / Release tag는 모든 package version과 일치하고 `main`에 포함된 검증 commit을 가리켜야 합니다.
- Pull-request dry runs do not receive content-write permission. / Pull Request dry-run에는 content write 권한을 부여하지 않습니다.
- Only the final publication job receives `contents: write` after every gate passes. / 모든 gate 통과 후 최종 게시 job에만 `contents: write`를 부여합니다.
- Existing tags and release assets are never overwritten. / 기존 tag와 release asset을 덮어쓰지 않습니다.
- PyPI publishing remains disabled. / PyPI 게시는 비활성화되어 있습니다.

## Scope and limitations / 범위와 한계

Automated tests, dependency auditing, source review, restrictive local-file handling, and release validation reduce known risks but do not prove the absence of vulnerabilities or replace an independent penetration test, threat-model review, or formal code audit.

자동 테스트, dependency audit, source review, 제한적인 로컬 파일 처리, release 검증은 알려진 위험을 줄이지만 취약점이 없음을 증명하거나 독립적인 침투 테스트, threat model 검토, 정식 code audit를 대체하지 않습니다.
