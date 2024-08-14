from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class NodeModel:
    id: UUID
    type: str = ""
    relationship: str = ""
    is_root: bool = False
