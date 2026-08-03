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

## Document format / 문서 형식

Every PR record includes:

각 PR 기록에는 다음 항목이 포함됩니다.

- Pull request URL, branch information, merge date, and merge commit / PR URL, branch 정보, 병합일, 병합 commit
- Context and problem statement / 배경과 문제
- Implemented changes / 구현 변경 사항
- Validation and outcome / 검증 및 결과
- Deferred work or architectural impact when relevant / 관련 후속 작업과 아키텍처 영향

New pull requests should add the next numbered document and update this index in the same PR.

새 Pull Request는 같은 PR 안에서 다음 번호의 문서를 추가하고 이 인덱스를 갱신하는 것을 원칙으로 합니다.
