from smartschedule.optimization.item import Item
from smartschedule.optimization.optimization_facade import OptimizationFacade
from smartschedule.optimization.total_capacity import TotalCapacity
from smartschedule.optimization.total_weight import TotalWeight

from tests.optimization.capability_capacity_dimension import (
    CapabilityCapacityDimension,
    CapabilityWeightDimension,
)


class TestOptimization:
    facade = OptimizationFacade()

    def test_nothing_is_chosen_when_no_capacities(self):
        items = [
            Item(
                "Item1",
                100,
                TotalWeight((CapabilityWeightDimension("COMMON SENSE", "Skill"),)),
            ),
            Item(
                "Item2",
                100,
                TotalWeight((CapabilityWeightDimension("THINKING", "Skill"),)),
            ),
        ]

        result = self.facade.calculate(items, TotalCapacity([]))

        assert result.profit == 0
        assert len(result.chosen_items) == 0

    def test_everything_is_chosen_when_all_weights_are_zero(self):
        items = [
            Item("Item1", 200, TotalWeight(())),
            Item("Item2", 100, TotalWeight(())),
        ]

        result = self.facade.calculate(items, TotalCapacity([]))

        assert result.profit == 300
        assert len(result.chosen_items) == 2

    def test_if_enough_capacity_all_items_are_chosen(self):
        items = [
            Item(
                "Item1",
                100,
                TotalWeight((CapabilityWeightDimension("WEB DEVELOPMENT", "Skill"),)),
            ),
            Item(
                "Item2",
                300,
                TotalWeight((CapabilityWeightDimension("WEB DEVELOPMENT", "Skill"),)),
            ),
        ]
        c1 = CapabilityCapacityDimension("anna", "WEB DEVELOPMENT", "Skill")
        c2 = CapabilityCapacityDimension("zbyniu", "WEB DEVELOPMENT", "Skill")

        result = self.facade.calculate(items, TotalCapacity((c1, c2)))

        assert result.profit == 400
        assert len(result.chosen_items) == 2

    def test_most_valuable_items_are_chosen(self):
        item1 = Item(
            "Item1", 100, TotalWeight((CapabilityWeightDimension("JAVA", "Skill"),))
        )
        item2 = Item(
            "Item2", 500, TotalWeight((CapabilityWeightDimension("JAVA", "Skill"),))
        )
        item3 = Item(
            "Item3", 300, TotalWeight((CapabilityWeightDimension("JAVA", "Skill"),))
        )
        c1 = CapabilityCapacityDimension("anna", "JAVA", "Skill")
        c2 = CapabilityCapacityDimension("zbyniu", "JAVA", "Skill")

        result = self.facade.calculate([item1, item2, item3], TotalCapacity([c1, c2]))

        assert result.profit == 800
        assert len(result.chosen_items) == 2
        assert len(result.item_to_capacities[item3]) == 1
        assert (
            c1 in result.item_to_capacities[item3]
            or c2 in result.item_to_capacities[item3]
        )
        assert len(result.item_to_capacities[item2]) == 1
        assert (
            c1 in result.item_to_capacities[item2]
            or c2 in result.item_to_capacities[item2]
        )
        assert item1 not in result.item_to_capacities
