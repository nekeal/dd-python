import math
from dataclasses import dataclass

from smartschedule.optimization.item import Item
from smartschedule.optimization.optimization_facade import OptimizationFacade
from smartschedule.optimization.result import Result
from smartschedule.optimization.total_capacity import TotalCapacity
from smartschedule.optimization.total_weight import TotalWeight
from smartschedule.simulation.additional_priced_capability import (
    AdditionalPricedCapability,
)
from smartschedule.simulation.simulated_capabilities import SimulatedCapabilities
from smartschedule.simulation.simulated_project import SimulatedProject


def reversed_comparator(a: Item, b: Item) -> int:
    return int(math.copysign(1, b.value - a.value))


@dataclass
class SimulationFacade:
    optimization_facade: OptimizationFacade

    def profit_after_buying_new_capability(
        self,
        projects_simulations: list[SimulatedProject],
        capabilities_without_new_one: SimulatedCapabilities,
        new_priced_capability: AdditionalPricedCapability,
    ) -> float:
        capabilities_with_new_resource = capabilities_without_new_one.add(
            new_priced_capability.available_resource_capability
        )
        result_without = self.optimization_facade.calculate(
            self.to_items(projects_simulations),
            self.to_capacity(capabilities_without_new_one),
            reversed_comparator,
        )
        result_with = self.optimization_facade.calculate(
            self.to_items(projects_simulations),
            self.to_capacity(capabilities_with_new_resource),
            reversed_comparator,
        )
        return (
            result_with.profit - new_priced_capability.value
        ) - result_without.profit

    def which_project_with_missing_demands_is_most_profitable_to_allocate_resources_to(
        self,
        projects_simulations: list[SimulatedProject],
        total_capability: SimulatedCapabilities,
    ) -> Result:
        return self.optimization_facade.calculate(
            self.to_items(projects_simulations),
            self.to_capacity(total_capability),
            reversed_comparator,
        )

    @staticmethod
    def to_capacity(simulated_capabilities: SimulatedCapabilities) -> TotalCapacity:
        capabilities = simulated_capabilities.capabilities
        capacity_dimensions = list(capabilities)
        return TotalCapacity(capacity_dimensions)

    def to_items(self, projects_simulations: list[SimulatedProject]) -> list[Item]:
        return [
            self.to_item(simulated_project)
            for simulated_project in projects_simulations
        ]

    @staticmethod
    def to_item(simulated_project: SimulatedProject) -> Item:
        missing_demands = simulated_project.missing_demands.all
        weights = tuple(missing_demands)
        return Item(
            str(simulated_project.project_id),
            float(simulated_project.calculate_value()),
            TotalWeight(weights),
        )
