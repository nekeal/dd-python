from abc import abstractmethod
from typing import Generic, TypeVar

from smartschedule.optimization.capacity_dimension import CapacityDimension

T = TypeVar("T", bound=CapacityDimension)  # TODO: make it more strict than Any


class WeightDimension(CapacityDimension, Generic[T]):
    @abstractmethod
    def is_satisfied_by(self, capacity_dimension: T) -> bool:
        pass
