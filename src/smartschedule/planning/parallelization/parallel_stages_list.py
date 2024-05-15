import dataclasses
from typing import Self

from smartschedule.planning.parallelization.parallel_stages import ParallelStages


@dataclasses.dataclass
class ParallelStagesList:
    all: list[ParallelStages] = dataclasses.field(default_factory=list)

    def add(self, parallel_stages: ParallelStages) -> Self:
        return self.__class__(self.all + [parallel_stages])

    def print(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return " | ".join(str(parallel_stages) for parallel_stages in self.all)
