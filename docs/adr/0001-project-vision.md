# ADR-0001 Project Structure

Status: Accepted


## Context

modelctl은 다양한 AI Provider와 Coding Agent를 지원해야 한다.


## Decision

프로젝트를 uv workspace 기반 monorepo로 구성한다.


Structure:

- apps/
    - CLI applications

- packages/
    - reusable libraries


## Consequences

장점:

- Plugin 개발 독립성
- Core 안정성
- PyPI 개별 배포 가능
