from pathlib import Path
import sqlite3

from ..context_managers.db_manager import SQLite


def table_exists(database_path: Path, table: str) -> bool:
    prompt = f"SELECT * FROM {table}"

    try:
        with SQLite(database_path) as cur:
            cur.execute(prompt)
    except sqlite3.OperationalError:
        return False
    return True


def is_extension_correct(file_path: Path, exp_extension: tuple) -> bool:
    if file_path.suffix in exp_extension:
        return True

    return False


def columns_are_correct(database_path: Path, table: str, csv_columns: list[str]) -> bool:
    prompt = f"SELECT name FROM pragma_table_info((:table))"
    data = {"table": table}

    with SQLite(database_path) as cur:
        cur.execute(prompt, data)
        db_columns = [column_name[0] for column_name in cur.fetchall()]

        return True if csv_columns == db_columns else False
