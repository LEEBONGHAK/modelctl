# Releasing modelctl / modelctl 릴리스

This document describes coordinated GitHub Releases for the `modelctl`, `modelctl-core`, and `modelctl-sdk` Python distributions.

이 문서는 `modelctl`, `modelctl-core`, `modelctl-sdk` Python 배포물의 통합 GitHub Release 절차를 설명합니다.

## English

### Current publication policy

- Completed versions may receive an annotated `v*` tag.
- A validated tag creates a new GitHub Release with distributions and `SHA256SUMS`.
- Existing GitHub Release assets are never overwritten by the workflow.
- **PyPI publication is not configured and no PyPI publishing job exists.**
- The workflow never creates a tag automatically. A maintainer must explicitly decide that the version is complete.

### Version requirements

All three package versions must match:

```text
apps/modelctl/pyproject.toml
packages/core/pyproject.toml
packages/sdk/pyproject.toml
```

The tag must equal the coordinated version with a `v` prefix. Package version `0.1.0` accepts only `v0.1.0`.

```bash
python scripts/release_validation.py
python scripts/release_validation.py --tag v0.1.0
```

### Pull-request and manual dry run

The `Release` workflow validates relevant pull requests and manual tag proposals without publishing anything. It:

- verifies coordinated package versions and the proposed tag
- treats the manual tag as untrusted input and validates it before exporting outputs
- builds wheel and source distributions with workspace overrides disabled
- installs wheels in a fresh Python 3.13 environment
- imports all installed packages and starts the installed CLI
- generates SHA-256 checksums
- uploads a temporary workflow artifact

### Tagging a completed version

After the version is complete, all checks pass, and the release commit is merged into `refac`:

```bash
git switch refac
git pull
git tag -a v0.1.0 -m "v0.1.0"
git push origin v0.1.0
```

The tag workflow rejects releases when:

- the tag does not exactly match all package versions
- the tagged commit is not contained in `refac`
- build, installation, import, CLI, or checksum validation fails
- a GitHub Release already exists for the tag

A successful run creates one immutable GitHub Release with generated notes, six Python distribution files, and `SHA256SUMS`.

### PyPI

PyPI publication is intentionally deferred. Enabling it later requires a separate reviewed pull request, package-name ownership confirmation, a dedicated protected environment, Trusted Publishing configuration, and a dry-run plan. Creating a GitHub tag does not publish anything to PyPI.

## 한국어

### 현재 게시 정책

- 완성된 버전에는 annotated `v*` tag를 생성할 수 있습니다.
- 검증된 tag는 배포물과 `SHA256SUMS`가 포함된 새로운 GitHub Release를 생성합니다.
- Workflow는 기존 GitHub Release asset을 덮어쓰지 않습니다.
- **PyPI 게시는 구성되어 있지 않으며 PyPI 게시 job도 존재하지 않습니다.**
- Workflow가 tag를 자동으로 만들지 않습니다. Maintainer가 해당 버전의 완성을 명시적으로 판단해야 합니다.

### 버전 요구사항

다음 세 패키지의 버전은 모두 같아야 합니다.

```text
apps/modelctl/pyproject.toml
packages/core/pyproject.toml
packages/sdk/pyproject.toml
```

Tag는 통합 버전 앞에 `v`를 붙인 값과 정확히 같아야 합니다. 패키지 버전이 `0.1.0`이면 `v0.1.0`만 허용됩니다.

```bash
python scripts/release_validation.py
python scripts/release_validation.py --tag v0.1.0
```

### Pull Request 및 수동 dry run

`Release` workflow는 관련 Pull Request와 수동 tag 제안을 외부 게시 없이 검증합니다.

- 세 패키지 버전과 제안된 tag 검증
- 수동 tag 입력을 신뢰하지 않고 output으로 내보내기 전에 검증
- Workspace override를 제외한 wheel·source distribution 빌드
- 새로운 Python 3.13 환경에 wheel 설치
- 설치된 모든 패키지 import와 설치된 CLI 시작 검증
- SHA-256 checksum 생성
- 임시 workflow artifact 업로드

### 완성 버전 tag 생성

버전이 완성되고 모든 검사가 통과했으며 release commit이 `refac`에 병합된 후 다음처럼 tag를 생성합니다.

```bash
git switch refac
git pull
git tag -a v0.1.0 -m "v0.1.0"
git push origin v0.1.0
```

다음 조건에서는 release가 거부됩니다.

- Tag가 세 패키지 버전과 정확히 일치하지 않는 경우
- Tag commit이 `refac`에 포함되지 않은 경우
- Build, 설치, import, CLI, checksum 검증이 실패한 경우
- 해당 tag의 GitHub Release가 이미 존재하는 경우

성공하면 자동 생성 release note, 여섯 개의 Python 배포 파일, `SHA256SUMS`가 포함된 하나의 불변 GitHub Release가 생성됩니다.

### PyPI

PyPI 게시는 의도적으로 연기했습니다. 나중에 활성화하려면 package name 소유권 확인, 보호된 전용 environment, Trusted Publishing 설정, dry-run 계획을 포함한 별도 검토 PR이 필요합니다. GitHub tag를 생성해도 PyPI에는 아무것도 게시되지 않습니다.
