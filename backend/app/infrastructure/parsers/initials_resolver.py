from dataclasses import dataclass
from uuid import UUID

from rapidfuzz.distance import Levenshtein

from app.domain.entities import FacultyProfile


@dataclass(frozen=True)
class ResolutionOutcome:
    status: str
    faculty_id: UUID | None = None
    candidate_initials: str | None = None
    similarity: float = 0.0
    error_detail: str | None = None


def normalized_similarity(a: str, b: str) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    max_len = max(len(a), len(b))
    dist = Levenshtein.distance(a, b)
    return 1.0 - (dist / max_len)


class InitialsResolver:
    SIMILARITY_THRESHOLD: float = 0.85
    MARGIN_THRESHOLD: float = 0.10

    def __init__(self, profiles: list[FacultyProfile]) -> None:
        self._profiles = profiles

    def resolve(self, raw_token: str) -> ResolutionOutcome:
        token = raw_token.strip().upper()
        if not token:
            return ResolutionOutcome(
                status="UNRESOLVED",
                error_detail="Empty initials token",
            )

        exact_matches = [
            p for p in self._profiles if p.initials.value.upper() == token
        ]
        if len(exact_matches) == 1:
            match = exact_matches[0]
            return ResolutionOutcome(
                status="RESOLVED",
                faculty_id=match.id,
                candidate_initials=match.initials.value,
                similarity=1.0,
            )
        if len(exact_matches) > 1:
            return ResolutionOutcome(
                status="AMBIGUOUS",
                error_detail=f"Multiple faculty share initials '{token}'",
            )

        alias_matches = [
            p
            for p in self._profiles
            if any(alias.strip().upper() == token for alias in p.aliases)
        ]
        if len(alias_matches) == 1:
            match = alias_matches[0]
            return ResolutionOutcome(
                status="RESOLVED",
                faculty_id=match.id,
                candidate_initials=match.initials.value,
                similarity=1.0,
            )
        if len(alias_matches) > 1:
            return ResolutionOutcome(
                status="AMBIGUOUS",
                error_detail=f"Multiple faculty match alias '{token}'",
            )

        if not self._profiles:
            return ResolutionOutcome(
                status="UNRESOLVED",
                error_detail=f"No faculty registered in department for token '{token}'",
            )

        scored: list[tuple[FacultyProfile, float]] = []
        for p in self._profiles:
            sim = normalized_similarity(token, p.initials.value.upper())
            scored.append((p, sim))

        scored.sort(key=lambda x: x[1], reverse=True)
        best_profile, best_score = scored[0]
        second_score = scored[1][1] if len(scored) > 1 else 0.0
        margin = best_score - second_score

        if best_score >= self.SIMILARITY_THRESHOLD and margin >= self.MARGIN_THRESHOLD:
            return ResolutionOutcome(
                status="RESOLVED",
                faculty_id=best_profile.id,
                candidate_initials=best_profile.initials.value,
                similarity=best_score,
            )

        if best_score >= 0.50:
            candidate_val = best_profile.initials.value
            return ResolutionOutcome(
                status="AMBIGUOUS",
                similarity=best_score,
                error_detail=(
                    f"Ambiguous initials match for '{token}'. "
                    f"Best candidate '{candidate_val}' "
                    f"similarity={best_score:.2f}, margin={margin:.2f}"
                ),
            )

        return ResolutionOutcome(
            status="UNRESOLVED",
            similarity=best_score,
            error_detail=f"Initials '{token}' could not be resolved to any faculty profile",
        )
