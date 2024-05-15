import dataclasses

from smartschedule.planning.parallelization.stage import Stage


@dataclasses.dataclass
class ParallelStages:
    stages: set[Stage]

    def print(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return ", ".join(sorted(stage.name for stage in self.stages))
