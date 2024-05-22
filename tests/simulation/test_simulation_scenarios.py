import uuid

from smartschedule.simulation.available_resource_capability import (
    AvailableResourceCapability,
)
from smartschedule.simulation.capability import Capability
from smartschedule.simulation.demand import Demand
from smartschedule.simulation.project_id import ProjectId
from smartschedule.simulation.simulation_facade import SimulationFacade
from smartschedule.simulation.time_slot import TimeSlot

from tests.simulation.available_capabilities_builder import AvailableCapabilitiesBuilder
from tests.simulation.simulated_projects_builder import SimulatedProjectsBuilder


class TestSimulationScenarios:
    JAN_1 = TimeSlot.create_daily_time_slot_at_utc(2021, 1, 1)
    PROJECT_1 = ProjectId()
    PROJECT_2 = ProjectId()
    PROJECT_3 = ProjectId()
    STASZEK = uuid.uuid4()
    LEON = uuid.uuid4()

    simulation_facade = SimulationFacade()

    def test_picks_optimal_project_based_on_earnings(self):
        simulated_projects = (
            self.simulated_projects()
            .with_project(self.PROJECT_1)
            .that_requires(Demand.demand_for(Capability.skill("JAVA-MID"), self.JAN_1))
            .that_can_earn(9)
            .with_project(self.PROJECT_2)
            .that_requires(Demand.demand_for(Capability.skill("JAVA-MID"), self.JAN_1))
            .that_can_earn(99)
            .with_project(self.PROJECT_3)
            .that_requires(Demand.demand_for(Capability.skill("JAVA-MID"), self.JAN_1))
            .that_can_earn(2)
            .build()
        )

        simulated_availability = (
            self.simulated_capabilities()
            .with_employee(self.STASZEK)
            .that_brings(Capability.skill("JAVA-MID"))
            .that_is_available_at(self.JAN_1)
            .with_employee(self.LEON)
            .that_brings(Capability.skill("JAVA-MID"))
            .that_is_available_at(self.JAN_1)
            .build()
        )

        result = self.simulation_facade.which_project_with_missing_demands_is_most_profitable_to_allocate_resources_to(  # noqa
            simulated_projects, simulated_availability
        )

        assert result.profit == 108
        assert len(result.chosen_projects) == 2

    def test_picks_all_when_enough_capabilities(self):
        simulated_projects = (
            self.simulated_projects()
            .with_project(self.PROJECT_1)
            .that_requires(Demand.demand_for(Capability.skill("JAVA-MID"), self.JAN_1))
            .that_can_earn(99)
            .build()
        )

        simulated_availability = (
            self.simulated_capabilities()
            .with_employee(self.STASZEK)
            .that_brings(Capability.skill("JAVA-MID"))
            .that_is_available_at(self.JAN_1)
            .with_employee(self.LEON)
            .that_brings(Capability.skill("JAVA-MID"))
            .that_is_available_at(self.JAN_1)
            .build()
        )

        result = self.simulation_facade.which_project_with_missing_demands_is_most_profitable_to_allocate_resources_to(  # noqa E501
            simulated_projects, simulated_availability
        )

        assert result.profit == 99
        assert len(result.chosen_projects) == 1

    def test_can_simulate_having_extra_resources(self):
        simulated_projects = (
            self.simulated_projects()
            .with_project(self.PROJECT_1)
            .that_requires(
                Demand.demand_for(Capability.skill("YT DRAMA COMMENTS"), self.JAN_1)
            )
            .that_can_earn(9)
            .with_project(self.PROJECT_2)
            .that_requires(
                Demand.demand_for(Capability.skill("YT DRAMA COMMENTS"), self.JAN_1)
            )
            .that_can_earn(99)
            .build()
        )

        simulated_availability = (
            self.simulated_capabilities()
            .with_employee(self.STASZEK)
            .that_brings(Capability.skill("YT DRAMA COMMENTS"))
            .that_is_available_at(self.JAN_1)
            .build()
        )

        extra_capability = AvailableResourceCapability(
            uuid.uuid4(), Capability.skill("YT DRAMA COMMENTS"), self.JAN_1
        )

        result_without_extra_resource = self.simulation_facade.which_project_with_missing_demands_is_most_profitable_to_allocate_resources_to(  # noqa E501
            simulated_projects, simulated_availability
        )
        result_with_extra_resource = self.simulation_facade.which_project_with_missing_demands_is_most_profitable_to_allocate_resources_to(  # noqa E501
            simulated_projects, simulated_availability.add(extra_capability)
        )

        assert result_without_extra_resource.profit == 99
        assert result_with_extra_resource.profit == 108

    @staticmethod
    def simulated_projects() -> SimulatedProjectsBuilder:
        return SimulatedProjectsBuilder()

    @staticmethod
    def simulated_capabilities() -> AvailableCapabilitiesBuilder:
        return AvailableCapabilitiesBuilder()
