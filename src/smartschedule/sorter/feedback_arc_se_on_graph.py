from dataclasses import dataclass

from .node import Node


@dataclass
class Edge:
    source: int
    target: int


class FeedbackArcSetOnGraph:
    """
    This class provides methods to calculate feedback edges in a graph
    and create an adjacency list from a list of nodes.
    """

    @staticmethod
    def calculate(initial_nodes: list[Node]) -> list[Edge]:
        """
        This method calculates the feedback edges in a graph
        represented by the given list of nodes.

        Parameters:
        initial_nodes: A list of nodes representing the graph.

        Returns: A list of feedback edges in the graph.
        """
        adjacency_list = FeedbackArcSetOnGraph.create_adjacency_list(initial_nodes)
        v = len(adjacency_list)
        feedback_edges = []
        visited = [0] * (v + 1)
        for i, neighbours in adjacency_list.items():
            if neighbours:
                visited[i] = 1
                for j in neighbours:
                    if visited[j] == 1:
                        feedback_edges.append(Edge(i, j))
                    else:
                        visited[j] = 1
        return feedback_edges

    @staticmethod
    def create_adjacency_list(initial_nodes: list[Node]) -> dict[int, list[int]]:
        adjacency_list: dict[int, list[int]] = {
            i: [] for i in range(1, len(initial_nodes) + 1)
        }
        for i, node in enumerate(initial_nodes, start=1):
            dependencies = [
                initial_nodes.index(dependency) + 1
                for dependency in node.dependencies.nodes
            ]
            adjacency_list[i] = dependencies
        return adjacency_list
