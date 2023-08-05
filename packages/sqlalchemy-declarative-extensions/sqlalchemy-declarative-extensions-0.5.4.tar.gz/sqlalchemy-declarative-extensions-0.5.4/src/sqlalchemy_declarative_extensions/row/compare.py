from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Union

from sqlalchemy import MetaData, Table, tuple_
from sqlalchemy.engine.base import Connection

from sqlalchemy_declarative_extensions.dialects import check_table_exists
from sqlalchemy_declarative_extensions.row.base import Row, Rows
from sqlalchemy_declarative_extensions.sqlalchemy import row_to_dict


@dataclass
class InsertRowOp:
    table: str
    values: dict[str, Any]

    @classmethod
    def insert_table_row(cls, operations, table, values):
        op = cls(table, values)
        return operations.invoke(op)

    def render(self, conn: Connection):
        table = get_table(conn, self.table)
        return table.insert().values(self.values)

    def reverse(self):
        return DeleteRowOp(self.table, self.values)


@dataclass
class UpdateRowOp:
    table: str
    from_values: dict[str, Any]
    to_values: dict[str, Any]

    @classmethod
    def update_table_row(cls, operations, table, from_values, to_values):
        op = cls(table, from_values, to_values)
        return operations.invoke(op)

    def render(self, conn: Connection):
        table = get_table(conn, self.table)

        primary_key_columns = [c.name for c in table.primary_key.columns]
        where = [
            table.c[c] == v
            for c, v in self.to_values.items()
            if c in primary_key_columns
        ]
        values = {
            c: v for c, v in self.to_values.items() if c not in primary_key_columns
        }
        return table.update().where(*where).values(**values)

    def reverse(self):
        return UpdateRowOp(self.table, self.to_values, self.from_values)


@dataclass
class DeleteRowOp:
    table: str
    values: dict[str, Any]

    @classmethod
    def delete_table_row(cls, operations, table, values):
        op = cls(table, values)
        return operations.invoke(op)

    def render(self, conn: Connection):
        table = get_table(conn, self.table)

        primary_key_columns = [c.name for c in table.primary_key.columns]
        where = [
            table.c[c] == v for c, v in self.values.items() if c in primary_key_columns
        ]
        return table.delete().where(*where)

    def reverse(self):
        return InsertRowOp(self.table, self.values)


def get_table(conn: Connection, tablename: str):
    m = MetaData()

    try:
        schema, table = tablename.split(".", 1)
    except ValueError:
        table = tablename
        schema = None

    m.reflect(conn, schema=schema, only=[table])
    return m.tables[tablename]


RowOp = Union[InsertRowOp, UpdateRowOp, DeleteRowOp]


def compare_rows(connection: Connection, metadata: MetaData, rows: Rows) -> list[RowOp]:
    result: list[RowOp] = []

    rows_by_table: dict[Table, list[Row]] = {}
    for row in rows:
        table = metadata.tables.get(row.qualified_name)
        if table is None:
            raise ValueError(f"Unknown table: {row.qualified_name}")

        rows_by_table.setdefault(table, []).append(row)

        primary_key_columns = [c.name for c in table.primary_key.columns]

        if set(primary_key_columns) - row.column_values.keys():
            raise ValueError(
                f"Row is missing primary key values required to declaratively specify: {row}"
            )

        column_filters = [
            c == row.column_values[c.name] for c in table.primary_key.columns
        ]

        # If the table doesn't exist yet, we can likely assume it's being autogenerated
        # in the current revision and as such, will just emit insert statements.
        table_exists = check_table_exists(
            connection,
            table.name,
            schema=table.schema or connection.dialect.default_schema_name,
        )

        record = None
        if table_exists:
            record = connection.execute(
                table.select().where(*column_filters).limit(1)
            ).first()

        if record:
            row_keys = row.column_values.keys()
            record_dict = {
                k: v for k, v in row_to_dict(record).items() if k in row_keys
            }
            if row.column_values == record_dict:
                continue

            result.append(
                UpdateRowOp(
                    row.qualified_name,
                    from_values=record_dict,
                    to_values=row.column_values,
                )
            )
        else:
            result.append(InsertRowOp(row.qualified_name, values=row.column_values))

    if not rows.ignore_unspecified:
        for table_name in rows.included_tables:
            table = metadata.tables[table_name]
            rows_by_table.setdefault(table, [])

        for table, row_list in rows_by_table.items():
            table_exists = check_table_exists(
                connection,
                table.name,
                schema=table.schema or connection.dialect.default_schema_name,
            )
            if not table_exists:
                continue

            primary_key_columns = [c.name for c in table.primary_key.columns]
            primary_key_values = [
                tuple(row.column_values[c] for c in primary_key_columns)
                for row in row_list
            ]
            to_delete = connection.execute(
                table.select().where(
                    tuple_(*table.primary_key.columns).notin_(primary_key_values)
                )
            ).fetchall()

            for record in to_delete:
                op = DeleteRowOp(table.fullname, row_to_dict(record))
                result.append(op)

    return result
