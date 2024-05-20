from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from smartschedule.sorter.nodes import Nodes

T = TypeVar("T")


@dataclass(frozen=True)
class Node(Generic[T]):
    name: str  # unique identifier
    dependencies: "Nodes[T]" = field(default_factory=lambda: Nodes())
    content: T = field(kw_only=True, default=None)  # type: ignore[assignment] # currently it should not happen that content is None

    def depends_on(self, node: "Node[T]") -> "Node[T]":
        return Node(self.name, self.dependencies.add(node), content=self.content)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Node):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
