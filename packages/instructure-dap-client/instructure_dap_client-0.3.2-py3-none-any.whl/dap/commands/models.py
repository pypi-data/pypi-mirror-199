from dataclasses import dataclass

from ..dap_types import JobID, ObjectID


@dataclass
class ContextAwareObject:
    id: ObjectID
    index: int
    total_count: int
    job_id: JobID

    def __str__(self) -> str:
        return f"[object {self.index + 1}/{self.total_count} - job {self.job_id}]"
