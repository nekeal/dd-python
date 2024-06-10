import uuid
from dataclasses import dataclass, field
from typing import Any
from uuid import UUID


@dataclass
class ProjectId:
    project_id: UUID = field(default_factory=uuid.uuid4)

    @classmethod
    def from_uuid(cls, project_id: UUID) -> "ProjectId":
        return ProjectId(project_id)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ProjectId):
            return False
        return self.project_id == other.project_id

    def __hash__(self) -> int:
        return hash(self.project_id)
