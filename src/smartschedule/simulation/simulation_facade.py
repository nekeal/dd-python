from dataclasses import dataclass

from smartschedule.optimization.item import Item
from smartschedule.optimization.optimization_facade import OptimizationFacade
from smartschedule.optimization.result import Result
from smartschedule.optimization.total_capacity import TotalCapacity
from smartschedule.optimization.total_weight import TotalWeight
from smartschedule.simulation.simulated_capabilities import SimulatedCapabilities
from smartschedule.simulation.simulated_project import SimulatedProject


@dataclass
class SimulationFacade:
    optimization_facade: OptimizationFacade

    def which_project_with_missing_demands_is_most_profitable_to_allocate_resources_to(
        self,
        projects_simulations: list[SimulatedProject],
        total_capability: SimulatedCapabilities,
    ) -> Result:
        return self.optimization_facade.calculate(
            self.to_items(projects_simulations), self.to_capacity(total_capability)
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
            float(simulated_project.earnings),
            TotalWeight(weights),
        )
