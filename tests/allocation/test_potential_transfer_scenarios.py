from datetime import timedelta
from uuid import uuid4

from smartschedule.allocation.allocated_capability import AllocatedCapability
from smartschedule.allocation.allocation_facade import AllocationFacade
from smartschedule.allocation.demand import Demand
from smartschedule.allocation.demands import Demands
from smartschedule.allocation.project import Project
from smartschedule.allocation.projects import Projects
from smartschedule.optimization.optimization_facade import OptimizationFacade
from smartschedule.shared.capability.capability import Capability
from smartschedule.shared.time_slot import TimeSlot
from smartschedule.simulation.simulation_facade import SimulationFacade


class TestPotentialTransferScenarios:
    JAN_1 = TimeSlot.create_daily_time_slot_at_utc(2021, 1, 1)
    FIFTEEN_MINUTES_IN_JAN = TimeSlot(JAN_1.from_, JAN_1.from_ + timedelta(minutes=15))
    DEMAND_FOR_JAVA_JUST_FOR_15MIN_IN_JAN = Demands(
        [Demand(Capability.skill("JAVA-MID"), FIFTEEN_MINUTES_IN_JAN)]
    )
    DEMAND_FOR_JAVA_MID_IN_JAN = Demands([Demand(Capability.skill("JAVA-MID"), JAN_1)])
    DEMANDS_FOR_JAVA_AND_PYTHON_IN_JAN = Demands(
        [
            Demand(Capability.skill("JAVA-MID"), JAN_1),
            Demand(Capability.skill("PYTHON-MID"), JAN_1),
        ]
    )

    BANKING_SOFT_ID = uuid4()
    INSURANCE_SOFT_ID = uuid4()
    STASZEK_JAVA_MID = AllocatedCapability(uuid4(), Capability.skill("JAVA-MID"), JAN_1)

    simulation_facade = AllocationFacade(SimulationFacade(OptimizationFacade()))

    def test_simulates_moving_capabilities_to_different_project(self):
        # given
        banking_soft = Project(self.DEMAND_FOR_JAVA_MID_IN_JAN, 9)
        insurance_soft = Project(self.DEMAND_FOR_JAVA_MID_IN_JAN, 90)
        projects = Projects(
            {
                self.BANKING_SOFT_ID: banking_soft,
                self.INSURANCE_SOFT_ID: insurance_soft,
            },
        )
        # and
        banking_soft.add(self.STASZEK_JAVA_MID)

        result = self.simulation_facade.check_potential_transfer(
            projects,
            self.BANKING_SOFT_ID,
            self.INSURANCE_SOFT_ID,
            self.STASZEK_JAVA_MID,
            self.JAN_1,
        )

        assert result == 81

    def test_simulates_moving_capabilities_to_different_project_just_for_a_while(self):
        banking_soft = Project(self.DEMAND_FOR_JAVA_MID_IN_JAN, 9)
        insurance_soft = Project(self.DEMAND_FOR_JAVA_JUST_FOR_15MIN_IN_JAN, 99)
        projects = Projects(
            {self.BANKING_SOFT_ID: banking_soft, self.INSURANCE_SOFT_ID: insurance_soft}
        )
        banking_soft.add(self.STASZEK_JAVA_MID)

        result = self.simulation_facade.check_potential_transfer(
            projects,
            self.BANKING_SOFT_ID,
            self.INSURANCE_SOFT_ID,
            self.STASZEK_JAVA_MID,
            self.FIFTEEN_MINUTES_IN_JAN,
        )

        assert result == 90

    def test_the_move_gives_zero_profit_when_there_are_still_missing_demands(self):
        banking_soft = Project(self.DEMAND_FOR_JAVA_MID_IN_JAN, 9)
        insurance_soft = Project(self.DEMANDS_FOR_JAVA_AND_PYTHON_IN_JAN, 99)
        projects = Projects(
            {self.BANKING_SOFT_ID: banking_soft, self.INSURANCE_SOFT_ID: insurance_soft}
        )
        banking_soft.add(self.STASZEK_JAVA_MID)

        result = self.simulation_facade.check_potential_transfer(
            projects,
            self.BANKING_SOFT_ID,
            self.INSURANCE_SOFT_ID,
            self.STASZEK_JAVA_MID,
            self.JAN_1,
        )

        assert result == -9
