from smartschedule.sorter.feedback_arc_se_on_graph import Edge, FeedbackArcSetOnGraph
from smartschedule.sorter.node import Node


class TestFeedbackArcSetOnGraph:
    def test_can_find_minimum_number_of_edges_to_remove_to_make_the_graph_acyclic(self):
        # Given
        node1 = Node("1")
        node2 = Node("2")
        node3 = Node("3")
        node4 = Node("4")
        node1 = node1.depends_on(node2)
        node2 = node2.depends_on(node3)
        node4 = node4.depends_on(node3)
        node1 = node1.depends_on(node4)
        node3 = node3.depends_on(node1)

        # When
        to_remove = FeedbackArcSetOnGraph.calculate([node1, node2, node3, node4])

        # Then
        assert len(to_remove) == 2
        assert Edge(3, 1) in to_remove
        assert Edge(4, 3) in to_remove

    def test_when_graph_is_acyclic_there_is_nothing_to_remove(self):
        # Given
        node1 = Node("1")
        node2 = Node("2")
        node3 = Node("3")
        node4 = Node("4")
        node1 = node1.depends_on(node2)
        node2 = node2.depends_on(node3)
        node1 = node1.depends_on(node4)

        # When
        to_remove = FeedbackArcSetOnGraph.calculate([node1, node2, node3, node4])

        # Then
        assert to_remove == []
