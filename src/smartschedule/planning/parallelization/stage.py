import dataclasses
from collections.abc import Iterable
from datetime import timedelta
from typing import Any, Self


@dataclasses.dataclass
class ResourceName:
    name: str


@dataclasses.dataclass
class Stage:
    name: str
    dependencies: set[Self] = dataclasses.field(default_factory=set, init=False)
    resources: set[ResourceName] = dataclasses.field(default_factory=set, init=False)
    duration: timedelta = dataclasses.field(default=timedelta(), init=False)

    def depends_on(self, stage: Self | Iterable[Self]) -> Self:
        if isinstance(stage, Iterable):
            self.dependencies.update(stage)
        else:
            self.dependencies.add(stage)
        return self

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
