from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from qb_widget.services.aiida import NodeType


@dataclass(frozen=True)
class NodeModel:
    id: UUID
    type: NodeType = NodeType()
    relationship: str | None = None
    is_root: bool = False

    def is_valid(self) -> bool:
        return self.type.is_valid()
