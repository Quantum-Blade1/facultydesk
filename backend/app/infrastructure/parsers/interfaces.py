from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import time
from typing import Any


@dataclass(frozen=True)
class RawCell:
    row: int
    col: int
    text: str
    col_span: int = 1
    row_span: int = 1


@dataclass(frozen=True)
class ParsedSlotCandidate:
    weekday: int
    start_time: time
    end_time: time
    course_code: str
    section_name: str | None
    room_code: str | None
    raw_initials: list[str]
    source_cell: str


@dataclass
class ParseResult:
    candidates: list[ParsedSlotCandidate] = field(default_factory=list)
    unparsed_cells: list[dict[str, Any]] = field(default_factory=list)


class TimetableParser(ABC):
    @abstractmethod
    def parse(self, content: bytes) -> ParseResult:
        """Parse raw file bytes into parsed slot candidates and unparsed cell issues."""
