import dataclasses
from collections.abc import Iterable
from datetime import timedelta
from typing import Any, Self


@dataclasses.dataclass(frozen=True)
class ResourceName:
    name: str


@dataclasses.dataclass
class Stage:
    name: str
    dependencies: set["Stage"] = dataclasses.field(default_factory=set)
    resources: set[ResourceName] = dataclasses.field(default_factory=set)
    duration: timedelta = dataclasses.field(default=timedelta())

    def depends_on(self, stage: Self | Iterable[Self]) -> Self:
        new_dependencies = self.dependencies.copy()
        if isinstance(stage, Iterable):
            new_dependencies.update(stage)
        else:
            new_dependencies.add(stage)
        return self.__class__(
            self.name, new_dependencies, self.resources, self.duration
        )

    def with_chosen_resource_capabilities(self, *resources: ResourceName) -> Self:
        return self.__class__(
            self.name, self.dependencies, set(resources), self.duration
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
