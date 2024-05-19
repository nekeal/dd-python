from .nodes import Nodes
from .sorted_nodes import SortedNodes


class GraphTopologicalSort:
    @staticmethod
    def sort(nodes: Nodes) -> SortedNodes:
        return GraphTopologicalSort.create_sorted_nodes_recursively(
            nodes, SortedNodes()
        )

    @staticmethod
    def create_sorted_nodes_recursively(
        remaining_nodes: Nodes, accumulated_sorted_nodes: SortedNodes
    ) -> SortedNodes:
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
