from uuid import uuid4

from hypothesis import given
from hypothesis import strategies as st

from app.domain import FacultyProfile, Initials
from app.infrastructure.parsers.cell_tokenizer import tokenize_cell
from app.infrastructure.parsers.initials_resolver import (
    InitialsResolver,
    normalized_similarity,
)


@given(
    st.text(alphabet=st.characters(max_codepoint=1000), max_size=50),
    st.text(alphabet=st.characters(max_codepoint=1000), max_size=50),
)
def test_normalized_similarity_properties(a: str, b: str) -> None:
    sim_ab = normalized_similarity(a, b)
    sim_ba = normalized_similarity(b, a)
    assert 0.0 <= sim_ab <= 1.0
    assert abs(sim_ab - sim_ba) < 1e-9
    assert normalized_similarity(a, a) == 1.0


def test_ambiguity_threshold_rejection() -> None:
    dept_id = uuid4()
    p1 = FacultyProfile(
        id=uuid4(),
        user_id=uuid4(),
        department_id=dept_id,
        full_name="Kishore Sharma",
        initials=Initials("KS"),
        email="ks@dept.local",
    )
    p2 = FacultyProfile(
        id=uuid4(),
        user_id=uuid4(),
        department_id=dept_id,
        full_name="Karan Singh Shekhawat",
        initials=Initials("KSS"),
        email="kss@dept.local",
    )
    resolver = InitialsResolver([p1, p2])

    outcome = resolver.resolve("KS5")
    assert outcome.status in ("AMBIGUOUS", "UNRESOLVED")
    assert outcome.status != "RESOLVED"


def test_exact_and_alias_resolution() -> None:
    dept_id = uuid4()
    p1 = FacultyProfile(
        id=uuid4(),
        user_id=uuid4(),
        department_id=dept_id,
        full_name="Krish Kumar Sharma",
        initials=Initials("KKS"),
        aliases=("KRISH", "K_KUMAR"),
        email="kks@dept.local",
    )
    p2 = FacultyProfile(
        id=uuid4(),
        user_id=uuid4(),
        department_id=dept_id,
        full_name="Rohit Sharma",
        initials=Initials("RS"),
        email="rs@dept.local",
    )
    resolver = InitialsResolver([p1, p2])

    res_exact = resolver.resolve("KKS")
    assert res_exact.status == "RESOLVED"
    assert res_exact.faculty_id == p1.id

    res_alias = resolver.resolve("KRISH")
    assert res_alias.status == "RESOLVED"
    assert res_alias.faculty_id == p1.id

    res_lower = resolver.resolve("kks")
    assert res_lower.status == "RESOLVED"
    assert res_lower.faculty_id == p1.id


def test_cell_tokenization_topologies() -> None:
    res1 = tokenize_cell("CN (KKS)")
    assert res1 is not None
    course, sec, room, inits = res1
    assert course == "CN"
    assert sec is None
    assert room is None
    assert inits == ["KKS"]

    res2 = tokenize_cell("DBMS Lab - A1 (RS/PN)")
    assert res2 is not None
    course, sec, room, inits = res2
    assert course == "DBMS Lab"
    assert sec == "A1"
    assert room is None
    assert inits == ["RS", "PN"]

    res3 = tokenize_cell("OOAD KKS 301")
    assert res3 is not None
    course, sec, room, inits = res3
    assert course == "OOAD"
    assert sec is None
    assert room == "301"
    assert inits == ["KKS"]

    res4 = tokenize_cell("SE - B2 (AP & MKS) 204")
    assert res4 is not None
    course, sec, room, inits = res4
    assert course == "SE"
    assert sec == "B2"
    assert room == "204"
    assert inits == ["AP", "MKS"]
