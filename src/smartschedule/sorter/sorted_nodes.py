from dataclasses import dataclass, field

from smartschedule.sorter.nodes import Nodes


@dataclass
class SortedNodes:
    all: list[Nodes] = field(default_factory=list)

    def add(self, new_nodes: Nodes) -> "SortedNodes":
        return SortedNodes(self.all + [new_nodes])
