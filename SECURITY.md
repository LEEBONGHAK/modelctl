# Security Policy / 보안 정책

## Supported versions / 지원 버전

`modelctl` is currently pre-release. Security fixes are applied to the active `refac` branch and to the newest GitHub Release after releases begin.

`modelctl`은 현재 pre-release입니다. 보안 수정은 활성 `refac` branch와 향후 생성되는 가장 최신 GitHub Release에 적용합니다.

## Reporting a vulnerability / 취약점 제보

Do not include API keys, credentials, exploit payloads, or sensitive local paths in a public issue.

공개 issue에 API key, credential, 실제 공격 payload, 민감한 로컬 경로를 포함하지 마세요.

Use GitHub Private Vulnerability Reporting when it is available for this repository. When private reporting is unavailable, open a minimal public issue that asks the maintainer for a private contact channel without disclosing technical exploit details.

저장소에서 GitHub Private Vulnerability Reporting을 사용할 수 있으면 해당 기능을 사용하세요. 비공개 제보 기능을 사용할 수 없다면 기술적인 공격 세부사항을 공개하지 말고 maintainer에게 비공개 연락 수단을 요청하는 최소한의 issue만 작성하세요.

Include the affected version or commit, operating system, impact, reproduction prerequisites, and a safe proof of concept that does not expose real secrets.

영향받는 버전 또는 commit, 운영체제, 영향, 재현 전제조건, 실제 secret을 노출하지 않는 안전한 proof of concept를 포함하세요.

## Credential storage / Credential 저장

Credential lookup order:

Credential 조회 순서:

1. Environment variable such as `MODELCTL_OPENROUTER` / `MODELCTL_OPENROUTER`와 같은 환경변수
2. Operating-system keyring / 운영체제 keyring
3. Explicitly approved local-file fallback / 명시적으로 승인한 로컬 파일 fallback

The default login flow stores credentials in the operating-system keyring. A keyring failure does not silently downgrade to plaintext storage. The user must explicitly pass `--allow-plaintext-fallback`.

기본 로그인 흐름은 credential을 운영체제 keyring에 저장합니다. Keyring 실패 시 평문 파일 저장으로 자동 전환하지 않으며 사용자가 `--allow-plaintext-fallback`을 명시해야 합니다.

The fallback is unencrypted plaintext even though writes are atomic, symbolic links are rejected, and POSIX permissions are restricted to the current user. Treat the fallback as a compatibility option, not equivalent protection to a keyring.

Fallback은 원자적으로 저장되고 symbolic link를 거부하며 POSIX 권한이 현재 사용자로 제한되지만, 내용은 암호화되지 않은 평문입니다. Keyring과 동등한 보호 수단이 아니라 호환성 옵션으로 취급하세요.

## Execution model / 실행 모델

Coding-agent commands are constructed as argument lists and executed without a shell. Native launcher arguments are user-controlled and are intentionally forwarded to the selected third-party CLI. Review the selected agent's own security model before granting filesystem, network, tool, or approval permissions.

코딩 에이전트 명령은 인자 목록으로 구성되며 shell 없이 실행됩니다. 네이티브 launcher 인자는 사용자 입력으로 선택된 외부 CLI에 의도적으로 전달됩니다. 파일시스템, 네트워크, 도구, 승인 권한을 부여하기 전에 해당 에이전트의 보안 모델을 확인하세요.

## Release and supply chain / 릴리스와 공급망

- External GitHub Actions are pinned to full commit SHAs. / 외부 GitHub Actions는 전체 commit SHA로 고정합니다.
- Workflows use least-privilege repository permissions. / Workflow는 최소 repository 권한을 사용합니다.
- Locked dependencies are audited in CI. / Lockfile dependency를 CI에서 audit합니다.
- Release tags must match all package versions and point to a commit contained in `refac`. / Release tag는 모든 package 버전과 일치하고 `refac`에 포함된 commit을 가리켜야 합니다.
- Existing release assets are not overwritten. / 기존 release asset을 덮어쓰지 않습니다.
- PyPI publishing is disabled. / PyPI 게시는 비활성화되어 있습니다.

## Scope and limitations / 범위와 한계

The repository uses automated tests, dependency auditing, manual source review, restrictive local-file handling, and release validation. These controls reduce known risks but do not prove the absence of vulnerabilities and do not replace an independent penetration test, threat-model review, or formal code audit.

이 저장소는 자동 테스트, dependency audit, 수동 source review, 제한적인 로컬 파일 처리, release 검증을 사용합니다. 이러한 통제는 알려진 위험을 줄이지만 취약점이 없음을 증명하지 않으며 독립적인 침투 테스트, threat model 검토, 정식 code audit를 대체하지 않습니다.
