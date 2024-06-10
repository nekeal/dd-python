from dataclasses import dataclass, field
from functools import partial
from uuid import UUID

from smartschedule.allocation.allocated_capability import AllocatedCapability
from smartschedule.allocation.project import Project
from smartschedule.shared.supplier import Supplier
from smartschedule.shared.time_slot import TimeSlot
from smartschedule.simulation.demand import Demand
from smartschedule.simulation.demands import Demands
from smartschedule.simulation.project_id import ProjectId
from smartschedule.simulation.simulated_project import SimulatedProject


@dataclass(frozen=True)
class Projects:
    projects: dict[UUID, Project] = field(default_factory=dict)

    def transfer(
        self,
        project_from: UUID,
        project_to: UUID,
        capability: AllocatedCapability,
        for_slot: TimeSlot,
    ) -> "Projects":
        from_project = self.projects.get(project_from)
        to_project = self.projects.get(project_to)
        if from_project is None or to_project is None:
            return self
        removed = from_project.remove(capability, for_slot)
        if removed is None:
            return self
        to_project.add(
            AllocatedCapability(removed.resource_id, removed.capability, for_slot)
        )
        return Projects(self.projects)

    def to_simulated_projects(self) -> list[SimulatedProject]:
        result = [
            SimulatedProject(
                ProjectId.from_uuid(entry[0]),
                Supplier(partial(lambda x: x, entry[1].earnings)),
                self.get_missing_demands(entry[1]),
            )
            for entry in self.projects.items()
        ]
        return result

    def get_missing_demands(self, project: Project) -> Demands:
        all_demands = project.missing_demands()
        return Demands(
            tuple(Demand(demand.capability, demand.slot) for demand in all_demands.all)
        )
