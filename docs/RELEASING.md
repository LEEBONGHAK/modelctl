# Releasing modelctl / modelctl 릴리스

This document describes the coordinated release process for the `modelctl`, `modelctl-core`, and `modelctl-sdk` Python distributions.

이 문서는 `modelctl`, `modelctl-core`, `modelctl-sdk` Python 배포물의 통합 릴리스 절차를 설명합니다.

## English

### Safety model

A release is split into three gates:

1. Every pull request that changes release configuration runs a dry-run validation and artifact build.
2. A pushed `v*` tag creates or updates a GitHub Release and attaches the verified distributions and `SHA256SUMS`.
3. PyPI publication runs only when the repository variable `PUBLISH_TO_PYPI` is exactly `true` and the `pypi` environment is configured for Trusted Publishing.

The workflow never creates a tag. A maintainer must create and push the tag explicitly after reviewing the version change.

### Version requirements

All three package versions must match:

```text
apps/modelctl/pyproject.toml
packages/core/pyproject.toml
packages/sdk/pyproject.toml
```

The release tag must be the same version with a `v` prefix. For package version `0.1.0`, the only accepted tag is `v0.1.0`.

Validate locally:

```bash
python scripts/release_validation.py
python scripts/release_validation.py --tag v0.1.0
```

### Dry-run validation

The `Release` workflow runs on relevant pull requests and can also be started manually with a tag value. Dry runs perform the following operations without creating a release or publishing packages:

- verify coordinated package versions
- verify the proposed tag
- build all wheels and source distributions with workspace source overrides disabled
- install the wheels in a fresh Python 3.13 environment
- import all three installed packages
- execute the installed `modelctl version` and `modelctl --help`
- generate SHA-256 checksums
- upload a temporary workflow artifact

### Creating a GitHub Release

After the release commit is merged into `refac`:

```bash
git switch refac
git pull
git tag -a v0.1.0 -m "v0.1.0"
git push origin v0.1.0
```

The workflow rejects a tag when:

- its value does not match the three package versions
- the tagged commit is not contained in `refac`
- artifact build or installed-wheel smoke validation fails

A successful tag run creates a GitHub Release with generated notes, six Python distribution files, and `SHA256SUMS`.

### Enabling PyPI publication

Keep PyPI publication disabled until all of the following are ready:

1. Confirm that the three project names can be registered or are already controlled by the project owner.
2. Create the GitHub repository environment named `pypi`.
3. Configure PyPI Trusted Publishers for this repository, workflow file, and environment.
4. Add the repository Actions variable `PUBLISH_TO_PYPI` with the value `true`.

Removing the variable or setting it to any value other than `true` leaves GitHub Release publication enabled while skipping PyPI.

## 한국어

### 안전 구조

릴리스는 세 단계의 gate로 분리됩니다.

1. 릴리스 설정을 변경하는 모든 Pull Request에서 dry-run 검증과 배포물 빌드를 수행합니다.
2. `v*` 태그가 push되면 검증된 배포물과 `SHA256SUMS`를 첨부한 GitHub Release를 생성하거나 갱신합니다.
3. Repository variable `PUBLISH_TO_PYPI`가 정확히 `true`이고 `pypi` environment에 Trusted Publishing이 구성된 경우에만 PyPI 게시를 수행합니다.

Workflow는 태그를 자동 생성하지 않습니다. 버전 변경을 검토한 maintainer가 명시적으로 태그를 생성하고 push해야 합니다.

### 버전 요구사항

다음 세 패키지의 버전은 모두 같아야 합니다.

```text
apps/modelctl/pyproject.toml
packages/core/pyproject.toml
packages/sdk/pyproject.toml
```

Release tag는 패키지 버전 앞에 `v`를 붙인 값이어야 합니다. 패키지 버전이 `0.1.0`이면 허용되는 태그는 `v0.1.0`뿐입니다.

로컬 검증 명령은 다음과 같습니다.

```bash
python scripts/release_validation.py
python scripts/release_validation.py --tag v0.1.0
```

### Dry-run 검증

`Release` workflow는 관련 Pull Request에서 실행되며 tag 값을 입력해 수동 실행할 수도 있습니다. Dry-run에서는 release 생성이나 package 게시 없이 다음을 수행합니다.

- 세 패키지 버전 일치 검증
- 제안된 tag 검증
- Workspace source override를 제외한 wheel·source distribution 빌드
- 새로운 Python 3.13 환경에 wheel 설치
- 설치된 세 패키지 import
- 설치된 `modelctl version`, `modelctl --help` 실행
- SHA-256 checksum 생성
- 임시 workflow artifact 업로드

### GitHub Release 생성

Release commit이 `refac`에 병합된 후 다음과 같이 태그를 생성합니다.

```bash
git switch refac
git pull
git tag -a v0.1.0 -m "v0.1.0"
git push origin v0.1.0
```

다음 경우 workflow가 태그를 거부합니다.

- Tag 값과 세 패키지 버전이 일치하지 않는 경우
- Tag 대상 commit이 `refac`에 포함되지 않은 경우
- 배포물 빌드 또는 설치된 wheel smoke 검증이 실패한 경우

성공하면 자동 생성 release note, 여섯 개의 Python 배포 파일, `SHA256SUMS`를 포함한 GitHub Release가 생성됩니다.

### PyPI 게시 활성화

다음 준비가 모두 끝날 때까지 PyPI 게시는 비활성 상태로 유지합니다.

1. 세 project name을 등록할 수 있거나 프로젝트 소유자가 이미 관리하고 있는지 확인합니다.
2. GitHub repository에 `pypi` environment를 생성합니다.
3. 이 repository, workflow file, environment를 대상으로 PyPI Trusted Publisher를 구성합니다.
4. Repository Actions variable `PUBLISH_TO_PYPI`를 만들고 값을 `true`로 설정합니다.

Variable을 삭제하거나 `true`가 아닌 값으로 설정하면 GitHub Release 생성은 유지하면서 PyPI 게시만 건너뜁니다.
