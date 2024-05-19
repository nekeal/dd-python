from smartschedule.planning.parallelization.stage import Stage
from smartschedule.sorter.node import Node
from smartschedule.sorter.nodes import Nodes


class StagesToNodes:
    """
    This class is responsible for converting a list1
    of Stage objects into a Nodes object.
    """

    @staticmethod
    def calculate(stages: list[Stage]) -> Nodes:
        """
        This method takes a list of Stage objects and returns a Nodes object.
        It creates a dictionary where the keys are the names of the stages and the
        values are new Node objects created with the stage name and the stage itself.
        Then, it iterates over the stages and for each stage, it updates the dictionary
        with the results of the explicit_dependencies and shared_resources methods.


        Args:
            stages: A list of Stage objects.

        Returns: Nodes object representing the stages as a graph.
        """
        result = {stage.name: Node(name=stage.name, content=stage) for stage in stages}

        for i, stage in enumerate(stages):
            result = StagesToNodes.explicit_dependencies(stage, result)
            result = StagesToNodes.shared_resources(stage, stages[i + 1 :], result)

        return Nodes(set(result.values()))

    @staticmethod
    def shared_resources(
        stage: Stage, with_stages: list[Stage], result: dict[str, Node]
    ) -> dict[str, Node]:
        """
        This method updates the dependencies of the node corresponding to
        the current stage based on the shared resources with other stages.
        The stage with fewer resources is considered to
        depend on the stage with more resources.

        Args:
            stage: The current stage.
            with_stages: The list of stages to compare resources with.
            result: The dictionary of nodes.

        Returns:

        """
        for other in with_stages:
            if stage.name != other.name and not set(stage.resources).isdisjoint(
                set(other.resources)
            ):
                if len(other.resources) > len(stage.resources):
                    node = result[stage.name]
                    node = node.depends_on(result[other.name])
                    result[stage.name] = node
                else:
                    node = result[other.name]
                    node = node.depends_on(result[stage.name])
                    result[other.name] = node
        return result

    @staticmethod
    def explicit_dependencies(stage: Stage, result: dict[str, Node]) -> dict[str, Node]:
        """
        This method updates the dependencies of the node corresponding to
        the current stage based on the explicit dependencies of the stage.

        Args:
            stage: The current stage.
            result: The dictionary of nodes.

        Returns: The updated dictionary of nodes.

        """
        node_with_explicit_deps = result[stage.name]
        for explicit_dependency in stage.dependencies:
            node_with_explicit_deps = node_with_explicit_deps.depends_on(
                result[explicit_dependency.name]
            )
        result[stage.name] = node_with_explicit_deps
        return result
