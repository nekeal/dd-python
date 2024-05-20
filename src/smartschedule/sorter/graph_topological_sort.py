from typing import Generic, TypeVar

from smartschedule.sorter.nodes import Nodes
from smartschedule.sorter.sorted_nodes import SortedNodes

T = TypeVar("T")


class GraphTopologicalSort(Generic[T]):
    @staticmethod
    def sort(nodes: Nodes[T]) -> SortedNodes[T]:
        return GraphTopologicalSort.create_sorted_nodes_recursively(
            nodes, SortedNodes()
        )

    @staticmethod
    def create_sorted_nodes_recursively(
        remaining_nodes: Nodes[T], accumulated_sorted_nodes: SortedNodes[T]
    ) -> SortedNodes[T]:
        already_processed_nodes = [
            node
            for sorted_nodes in accumulated_sorted_nodes.all
            for node in sorted_nodes.all
        ]
        nodes_without_dependencies = remaining_nodes.with_all_dependencies_present_in(
            already_processed_nodes
        )

        if not nodes_without_dependencies.all:
            return accumulated_sorted_nodes

        new_sorted_nodes = accumulated_sorted_nodes.add(nodes_without_dependencies)
        remaining_nodes = remaining_nodes.remove_all(nodes_without_dependencies.all)
        return GraphTopologicalSort.create_sorted_nodes_recursively(
            remaining_nodes, new_sorted_nodes
        )
