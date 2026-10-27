import heapq
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class Interval:
    id: UUID
    start_utc: datetime
    end_utc: datetime


def intervals_overlap(a: Interval, b: Interval) -> bool:
    return (a.start_utc < b.end_utc) and (b.start_utc < a.end_utc)


def pairwise_clashes(intervals: Sequence[Interval]) -> list[tuple[UUID, UUID]]:
    clashes: list[tuple[UUID, UUID]] = []
    n = len(intervals)
    for i in range(n):
        for j in range(i + 1, n):
            if intervals_overlap(intervals[i], intervals[j]):
                clashes.append((intervals[i].id, intervals[j].id))
    return clashes


class SweepLineClashDetector:
    def detect_clashes(self, intervals: Sequence[Interval]) -> list[tuple[UUID, UUID]]:
        if len(intervals) < 2:
            return []

        sorted_intervals = sorted(intervals, key=lambda x: (x.start_utc, x.end_utc))
        clashes: list[tuple[UUID, UUID]] = []
        heap: list[tuple[datetime, UUID]] = []

        for current in sorted_intervals:
            while heap and heap[0][0] <= current.start_utc:
                heapq.heappop(heap)

            for _, other_id in heap:
                clashes.append((other_id, current.id))

            heapq.heappush(heap, (current.end_utc, current.id))

        return clashes
