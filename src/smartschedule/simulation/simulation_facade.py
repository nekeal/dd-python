from smartschedule.simulation.available_resource_capability import (
    AvailableResourceCapability,
)
from smartschedule.simulation.demands import Demands
from smartschedule.simulation.result import Result
from smartschedule.simulation.simulated_capabilities import SimulatedCapabilities
from smartschedule.simulation.simulated_project import SimulatedProject


class SimulationFacade:
    def which_project_with_missing_demands_is_most_profitable_to_allocate_resources_to(
        self,
        projects_simulations: list[SimulatedProject],
        total_capability: SimulatedCapabilities,
    ) -> Result:
        list_ = total_capability.capabilities
        capacities_size = len(list_)
        dp = [0.0] * (capacities_size + 1)
        chosen_items_list: list[list[SimulatedProject]] = [
            [] for _ in range(capacities_size + 1)
        ]
        allocated_capacities_list: list[set[AvailableResourceCapability]] = [
            set() for _ in range(capacities_size + 1)
        ]

        automatically_included_items = [
            p for p in projects_simulations if p.all_demands_satisfied
        ]
        guaranteed_value = sum(p.earnings for p in automatically_included_items)

        all_availabilities = list(list_)
        item_to_capacities_map = {}

        for project in sorted(
            projects_simulations, key=lambda p: p.earnings, reverse=True
        ):
            chosen_capacities = self.match_capacities(
                project.missing_demands, all_availabilities
            )
            all_availabilities = [
                a for a in all_availabilities if a not in chosen_capacities
            ]

            if not chosen_capacities:
                continue

            sum_value = project.earnings
            chosen_capacities_count = len(chosen_capacities)

            for j in range(capacities_size, chosen_capacities_count - 1, -1):
                if dp[j] < sum_value + dp[j - chosen_capacities_count]:
                    dp[j] = sum_value + dp[j - chosen_capacities_count]
                    chosen_items_list[j] = chosen_items_list[
                        j - chosen_capacities_count
                    ] + [project]
                    allocated_capacities_list[j].update(chosen_capacities)

            item_to_capacities_map[project] = set(chosen_capacities)

        chosen_items_list[capacities_size].extend(automatically_included_items)
        return Result(
            dp[capacities_size] + guaranteed_value,
            chosen_items_list[capacities_size],
            item_to_capacities_map,
        )

    @staticmethod
    def match_capacities(
        demands: Demands, available_capacities: list[AvailableResourceCapability]
    ) -> list[AvailableResourceCapability]:
        result = []
        for single_demand in demands.all:
            matching_capacity = next(
                (c for c in available_capacities if single_demand.is_satisfied_by(c)),
                None,
            )

            if matching_capacity is not None:
                result.append(matching_capacity)
            else:
                return []

        return result
