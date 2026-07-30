# ADR-0003 : Tech Stack

## python version

권장: Python 3.13

이유:

- 3.12는 곧 지원 종료 시점이 가까워지고
- 3.14는 아직 일부 라이브러리 호환성이 완전히 안정적이지 않습니다.
- 3.13은 현재 생태계 지원이 가장 좋은 선택입니다.

## package manager

```
uv
```

이유:

- 매우 빠른 설치
- lockfile 지원
- workspace 지원
- monorepo 친화적
