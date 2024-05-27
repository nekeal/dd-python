from dataclasses import dataclass

from smartschedule.optimization.weight_dimension import WeightDimension


@dataclass(frozen=True)
class TotalWeight:
    components: tuple[WeightDimension, ...]  # type: ignore[type-arg] # we allow implicit WeightDimension[Any]

    @staticmethod
    def zero() -> "TotalWeight":
        return TotalWeight(())

    @staticmethod
    def of(*components: WeightDimension) -> "TotalWeight":  # type: ignore[type-arg] # we allow implicit WeightDimension[Any]
        return TotalWeight(tuple(components))
