import itertools
from collections.abc import Iterable

from smartschedule.planning.parallelization.parallel_stages import ParallelStages
from smartschedule.planning.parallelization.parallel_stages_list import (
    ParallelStagesList,
)
from smartschedule.planning.parallelization.stage import Stage


class StageParallelization:
    def of(self, stages: set[Stage]) -> ParallelStagesList:
        """Parallelize the given stages."""
        return self._create_sorted_nodes_recursively(stages, ParallelStagesList())

    def _create_sorted_nodes_recursively(
        self, remaining_stages: set[Stage], accumulated_sorted_nodes: ParallelStagesList
    ) -> ParallelStagesList:
        """
        Create a list of parallel stages. It does this by
        recursively sorting the stages based on their dependencies.

        Args:
            remaining_stages: A set of stages that are yet to be sorted
            accumulated_sorted_nodes: sorted nodes that have been processed so far

        Returns:
            ParallelStagesList: A list of parallel stages where stages are only
             processed when all their dependencies have been processed.

        """
        already_processed_nodes: list[Stage] = list(
            itertools.chain.from_iterable(
                node.stages for node in accumulated_sorted_nodes.all
            )
        )
        nodes_without_dependencies = self.with_all_dependencies_present_in(
            remaining_stages, already_processed_nodes
        )
        if not nodes_without_dependencies:
            return accumulated_sorted_nodes

        new_sorted_nodes = accumulated_sorted_nodes.add(
            ParallelStages(nodes_without_dependencies)
        )
        new_remaining_nodes = remaining_stages - nodes_without_dependencies
        return self._create_sorted_nodes_recursively(
            new_remaining_nodes, new_sorted_nodes
        )

    @staticmethod
    def with_all_dependencies_present_in(
        to_check: set[Stage], present_in: Iterable[Stage]
    ) -> set[Stage]:
        """
        Filter out stages that have all dependencies present in the given set.
        Args:
            to_check: A set of stages that we want to filter.
            present_in: A collection of stages that we will check against.

        Returns: A set of stages that have all dependencies present in the given set.
        """
        present_in_set = set(present_in)
        return {node for node in to_check if set(node.dependencies) <= present_in_set}
