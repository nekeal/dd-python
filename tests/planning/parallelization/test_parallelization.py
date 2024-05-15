from smartschedule.planning.parallelization.stage import Stage
from smartschedule.planning.parallelization.stage_parallelization import (
    StageParallelization,
)


class TestStageParallelization:
    # everythingCanBeDoneInParallelWhenThereAreNoDependencies
    def test_everything_can_be_done_in_parallel_when_there_are_no_dependencies(self):
        # Given
        stage1 = Stage("Stage 1")
        stage2 = Stage("Stage 2")

        # When
        sorted_stages = StageParallelization().of({stage1, stage2})

        # Then
        assert len(sorted_stages.all) == 1

    def test_simple_dependencies(self):
        # Given
        stage1 = Stage("Stage 1")
        stage2 = Stage("Stage 2")
        stage3 = Stage("Stage 3")
        stage4 = Stage("Stage 4")
        stage2.depends_on(stage1)
        stage3.depends_on(stage1)
        stage4.depends_on(stage2)

        # When
        sorted_stages = StageParallelization().of({stage1, stage2, stage3, stage4})

        # Then
        assert sorted_stages.print() == "Stage 1 | Stage 2, Stage 3 | Stage 4"

    def test_cant_be_done_when_there_is_a_cycle(self):
        # Given
        stage1 = Stage("Stage 1")
        stage2 = Stage("Stage 2")
        stage2.depends_on(stage1)
        stage1.depends_on(stage2)

        # When
        sorted_stages = StageParallelization().of({stage1, stage2})

        # Then
        assert sorted_stages.all == []
