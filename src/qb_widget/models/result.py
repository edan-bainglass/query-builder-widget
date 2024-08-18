from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ResultModel:
    id: int
    content: str
