from dataclasses import dataclass, field
from typing import Generic, TypeVar

from smartschedule.sorter.nodes import Nodes

T = TypeVar("T")


@dataclass
class SortedNodes(Generic[T]):
    all: list[Nodes[T]] = field(default_factory=list)

    def add(self, new_nodes: Nodes[T]) -> "SortedNodes[T]":
        return SortedNodes(self.all + [new_nodes])
