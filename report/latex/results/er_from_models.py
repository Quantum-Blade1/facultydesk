import sys
from pathlib import Path

from sqlalchemy import Table

from app.infrastructure.db.models import Base

SKIP_TABLES = {"alembic_version"}


def column_line(table: Table, name: str) -> str:
    column = table.c[name]
    kind = column.type.__class__.__name__.lower()
    if kind == "datetime" and getattr(column.type, "timezone", False):
        kind = "timestamptz"
    keys = []
    if column.primary_key:
        keys.append("PK")
    if column.foreign_keys:
        keys.append("FK")
    if column.unique and not column.primary_key:
        keys.append("UK")
    suffix = f" {','.join(keys)}" if keys else ""
    return f"        {kind} {name}{suffix}"


def build() -> str:
    lines = ["erDiagram"]
    tables = [t for t in Base.metadata.sorted_tables if t.name not in SKIP_TABLES]
    for table in tables:
        for column in table.columns:
            for fk in column.foreign_keys:
                parent = fk.column.table.name
                cardinality = "||--o|" if column.unique else "||--o{"
                lines.append(f"    {parent} {cardinality} {table.name} : \"{column.name}\"")
    for table in tables:
        lines.append(f"    {table.name} {{")
        lines.extend(column_line(table, c.name) for c in table.columns)
        lines.append("    }")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    Path(sys.argv[1]).write_text(build(), encoding="utf-8")
