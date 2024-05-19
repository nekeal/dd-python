from dataclasses import dataclass, field
from typing import Any

from smartschedule.planning.parallelization.stage import Stage
from smartschedule.sorter.nodes import Nodes


@dataclass(frozen=True)
class Node:
    name: str  # unique identifier
    dependencies: "Nodes" = field(default_factory=lambda: Nodes())
    content: Stage = field(kw_only=True, default=None)  # type: ignore[assignment] # currently it should not happen that content is None

    def depends_on(self, node: "Node") -> "Node":
        return Node(self.name, self.dependencies.add(node), content=self.content)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Node):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
