# Owner Release Command / 소유자 릴리스 명령

This fallback is used when a GitHub App or connector merges a validated release pull request but GitHub does not emit the expected push or merged-pull-request workflow event.

GitHub App 또는 connector가 검증된 release Pull Request를 병합했지만 예상한 push 또는 병합 이벤트 workflow가 발생하지 않을 때 사용하는 fallback입니다.

## English

### Command

The repository owner comments on the already merged release pull request:

```text
/release v0.2.0
```

The command is not a shortcut around validation. It starts a separate workflow that repeats the complete release process against the pull request's exact merge commit.

### Required trust checks

The workflow requires all of the following:

- the event is a newly created pull-request comment
- GitHub reports the comment author association as `OWNER`
- the command begins with `/release ` and the remaining tag passes `release_validation.py`
- the referenced pull request is actually merged
- the pull request base branch is exactly `main`
- the merge commit SHA has a valid 40-character hexadecimal form
- the merge commit is contained in `origin/main`
- `release.toml` reports `status = "ready"`

The workflow checks out the merge commit, never the pull-request head branch.

### Repeated validation

Before publication, the workflow reruns:

```bash
uv sync --all-packages --locked
uv audit --locked
uv run ruff check .
uv run pytest
uv build packages/core --out-dir dist --no-sources
uv build packages/sdk --out-dir dist --no-sources
uv build apps/modelctl --out-dir dist --no-sources
```

It then installs all wheels in an isolated Python 3.13 environment, verifies imports and the installed CLI, and generates `SHA256SUMS`.

### Publication safety

- The validation job is read-only.
- Only the publication job receives `contents: write` after all gates succeed.
- Existing tags are never moved.
- Existing GitHub Releases and assets are never overwritten.
- PyPI publication and OIDC publishing permission remain absent.

## 한국어

### 명령

저장소 소유자가 이미 병합된 release Pull Request에 다음 댓글을 작성합니다.

```text
/release v0.2.0
```

이 명령은 검증을 우회하는 단축 경로가 아닙니다. 별도 workflow가 Pull Request의 정확한 merge commit을 대상으로 전체 release 절차를 다시 수행합니다.

### 필수 신뢰 검증

Workflow는 다음 조건을 모두 요구합니다.

- 새로 생성된 Pull Request 댓글 이벤트일 것
- GitHub가 댓글 작성자의 association을 `OWNER`로 판정할 것
- 명령이 `/release `로 시작하고 나머지 tag가 `release_validation.py`를 통과할 것
- 대상 Pull Request가 실제로 병합됐을 것
- Pull Request base branch가 정확히 `main`일 것
- Merge commit SHA가 40자리 16진수 형식일 것
- Merge commit이 `origin/main`에 포함될 것
- `release.toml`의 상태가 `status = "ready"`일 것

Workflow는 Pull Request head branch가 아니라 merge commit을 checkout합니다.

### 반복 검증

게시 전에 다음 명령을 다시 실행합니다.

```bash
uv sync --all-packages --locked
uv audit --locked
uv run ruff check .
uv run pytest
uv build packages/core --out-dir dist --no-sources
uv build packages/sdk --out-dir dist --no-sources
uv build apps/modelctl --out-dir dist --no-sources
```

이후 격리된 Python 3.13 환경에 모든 wheel을 설치하고 package import, 설치된 CLI, `SHA256SUMS` 생성을 검증합니다.

### 게시 안전성

- 검증 job은 읽기 전용입니다.
- 모든 gate가 성공한 이후 publication job에만 `contents: write` 권한을 부여합니다.
- 기존 tag는 이동하지 않습니다.
- 기존 GitHub Release와 asset은 덮어쓰지 않습니다.
- PyPI 게시 및 OIDC 게시 권한은 계속 존재하지 않습니다.
