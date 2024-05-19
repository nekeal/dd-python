import typing
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

if typing.TYPE_CHECKING:
    from smartschedule.sorter.node import Node


@dataclass(frozen=True)
class Nodes:
    nodes: set["Node"] = field(default_factory=set)

    @property
    def all(self) -> frozenset["Node"]:
        return frozenset(self.nodes)

    def add(self, node: "Node") -> "Nodes":
        """
        Add a node to the set of nodes.
        Args:
            node: The node to add

        Returns: A new set of nodes with the added node.
        """
        return Nodes(self.nodes.union({node}))

    def with_all_dependencies_present_in(self, nodes: Iterable["Node"]) -> "Nodes":
        """
        Filter out nodes that have all dependencies present in the given set.
        Args:
            nodes: A set of nodes that we want to filter against.

        Returns: A set of nodes that have all dependencies present in the given set.
        """
        nodes_set = set(nodes)
        return Nodes({n for n in self.nodes if n.dependencies.nodes <= nodes_set})

    def remove_all(self, nodes: set["Node"] | frozenset["Node"]) -> "Nodes":
        """
        Remove a set of nodes from the current set of nodes.
        Args:
            nodes: The set of nodes to remove.

        Returns: A new set of nodes with the given nodes removed.
        """
        return Nodes(self.nodes.difference(nodes))

    def __str__(self) -> str:
        return f"Nodes: {self.nodes}"

    def __hash__(self) -> int:
        return hash(self.all)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Nodes):
            return False
        return self.all == other.all
