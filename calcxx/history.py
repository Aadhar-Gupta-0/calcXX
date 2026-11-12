"""Local, bounded in-memory calculation history."""
from dataclasses import dataclass, field

MAX_ITEMS = 30


@dataclass
class History:
    items: list[tuple[str, str]] = field(default_factory=list)

    def record(self, expression: str, result: str) -> None:
        self.items.insert(0, (str(expression)[:240], str(result)[:100]))
        del self.items[MAX_ITEMS:]

    def clear(self) -> None:
        self.items.clear()
