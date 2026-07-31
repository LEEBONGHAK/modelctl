from typing import Sequence

import questionary


class FzfSelector:
    def select(self, title: str, items: Sequence[str]) -> str | None:

        if not items:
            return None

        return questionary.select(title, choices=list(items)).ask()
