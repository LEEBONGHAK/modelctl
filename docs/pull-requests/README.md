# Pull Request Documentation / Pull Request 문서

This directory records the implementation history of `modelctl` one pull request at a time. Each document contains both an English version and a Korean version.

이 디렉터리는 `modelctl`의 구현 이력을 Pull Request 단위로 기록합니다. 각 문서에는 영문 버전과 한국어 버전이 함께 포함되어 있습니다.

| PR | Document / 문서 | Main result / 주요 결과 |
| --- | --- | --- |
| #1 | [PR-001.md](PR-001.md) | Runnable top-level model selection and launcher commands / 최상위 모델 선택·launcher 명령 실행 |
| #2 | [PR-002.md](PR-002.md) | Stable lint and test collection / lint·test 수집 안정화 |
| #3 | [PR-003.md](PR-003.md) | Complete Claude Code runner / Claude Code runner 완성 |
| #4 | [PR-004.md](PR-004.md) | Gemini CLI and runtime configuration / Gemini CLI·런타임 설정 |
| #5 | [PR-005.md](PR-005.md) | Codex CLI launcher / Codex CLI launcher |
| #6 | [PR-006.md](PR-006.md) | Provider-aware Aider launcher / provider-aware Aider launcher |
| #7 | [PR-007.md](PR-007.md) | Launcher discovery and selection / launcher 조회·선택 |
| #8 | [PR-008.md](PR-008.md) | Project progress documentation / 프로젝트 진행 문서화 |
| #9 | [PR-009.md](PR-009.md) | Local diagnostics with `modelctl doctor` / `modelctl doctor` 로컬 진단 |
| #10 | [PR-010.md](PR-010.md) | Compatibility feedback / 호환성 피드백 |
| #11 | [PR-011.md](PR-011.md) | Non-interactive provider and model selection / 비대화형 provider·model 선택 |
| #12 | [PR-012.md](PR-012.md) | Linux, macOS, and Windows CI / Linux·macOS·Windows CI |
| #13 | [PR-013.md](PR-013.md) | Installable distribution smoke tests / 설치 가능한 배포물 smoke test |
| #14 | [PR-014.md](PR-014.md) | Bilingual per-PR engineering history / PR별 bilingual 개발 이력 |
| #15 | [PR-015.md](PR-015.md) | Validated tags and GitHub Release automation / tag 검증·GitHub Release 자동화 |
| #16 | [PR-016.md](PR-016.md) | Credential, workflow, and local-state security hardening / credential·workflow·로컬 상태 보안 강화 |
| #17 | [PR-017.md](PR-017.md) | v0.1.0 readiness manifest and complete release gates / v0.1.0 완료 선언·통합 release gate |
| #18 | [PR-018.md](PR-018.md) | Trusted merged-PR release path / 신뢰된 병합 PR 릴리스 경로 |
| #19 | [PR-019.md](PR-019.md) | Promote completed v0.1.0 to main / 완성된 v0.1.0 main 승격 |
| #20 | [PR-020.md](PR-020.md) | Owner-only validated release command / 소유자 전용 검증 릴리스 명령 |
| #21 | [PR-021.md](PR-021.md) | Begin v0.2.0 with launcher recommendations / launcher 추천으로 v0.2.0 시작 |
| #23 | [PR-023.md](PR-023.md) | Strict compatibility execution and native option forwarding / strict 호환성 실행·native 옵션 전달 |
| #24 | [PR-024.md](PR-024.md) | Persisted warn/strict compatibility policy / 영속화된 warn·strict 호환성 정책 |
| #25 | [PR-025.md](PR-025.md) | Capability-driven immutable launcher execution contract / capability 기반 불변 launcher 실행 계약 |
| #26 | [PR-026.md](PR-026.md) | Preview-first compatibility remediation with explicit apply / 미리보기 우선 호환성 remediation·명시적 적용 |
| #27 | [PR-027.md](PR-027.md) | Anthropic native model catalog and Claude Code routing / Anthropic native 모델 catalog·Claude Code 연결 |
| #28 | [PR-028.md](PR-028.md) | Google Gemini native model catalog and Gemini CLI routing / Google Gemini native 모델 catalog·Gemini CLI 연결 |
| #29 | [PR-029.md](PR-029.md) | OpenAI native catalog, Codex routing, and provider CI hardening / OpenAI native catalog·Codex 연결·provider CI 강화 |
| #30 | [PR-030.md](PR-030.md) | Patched cryptography lock and security-issue closure / cryptography 패치 lock·보안 이슈 종료 |
| #31 | [PR-031.md](PR-031.md) | Declare v0.2.0 ready and promote the validated lineage to main / v0.2.0 ready 선언·검증 계보 main 승격 |
| #33 | [PR-033.md](PR-033.md) | Remove stale audit exclusion and enforce clean ready releases / 오래된 audit 예외 제거·clean ready release 강제 |
| #36 | [PR-036.md](PR-036.md) | Begin v0.3.0 with validated named profiles / 검증된 이름 있는 profile로 v0.3.0 시작 |
| #37 | [PR-037.md](PR-037.md) | Versioned public launcher plugin SDK contract / 버전이 명시된 공개 launcher plugin SDK 계약 |
| #38 | [PR-038.md](PR-038.md) | Superseded validated discovery draft, closed unmerged / 검증 후 도구 문제로 대체된 미병합 draft |
| #39 | [PR-039.md](PR-039.md) | Installed launcher entry-point discovery and isolation / 설치 launcher entry-point 탐색·격리 |
| #40 | [PR-040.md](PR-040.md) | Plugin-aware doctor diagnostics and compatibility hardening / plugin-aware doctor 진단·호환성 강화 |
| #41 | [PR-041.md](PR-041.md) | Strict static type-check enforcement for v0.3 boundaries / v0.3 경계 strict static type-check 강제 |
| #42 | [PR-042.md](PR-042.md) | Final v0.3.0 documentation and release-criteria review / v0.3.0 최종 문서·release criteria 검토 |
| #43 | [PR-043.md](PR-043.md) | Declare v0.3.0 ready and promote validated lineage to main / v0.3.0 ready 선언·검증 계보 main 승격 |
| #44 | [PR-044.md](PR-044.md) | Fix first-release tag detection in validated publisher / 검증 publisher의 최초 release tag 탐지 수정 |

## Document format / 문서 형식

Every PR record includes:

각 PR 기록에는 다음 항목이 포함됩니다.

- Pull request URL, branch information, merge date, and merge commit / PR URL, branch 정보, 병합일, 병합 commit
- Context and problem statement / 배경과 문제
- Implemented changes / 구현 변경 사항
- Validation and outcome / 검증 및 결과
- Deferred work or architectural impact when relevant / 관련 후속 작업과 아키텍처 영향

New pull requests should add the next numbered document and update this index in the same PR. Issue numbers may create gaps in the PR sequence.

새 Pull Request는 같은 PR 안에서 다음 번호의 문서를 추가하고 이 index를 갱신하는 것을 원칙으로 합니다. Issue 번호 사용으로 PR 번호가 연속되지 않을 수 있습니다.
