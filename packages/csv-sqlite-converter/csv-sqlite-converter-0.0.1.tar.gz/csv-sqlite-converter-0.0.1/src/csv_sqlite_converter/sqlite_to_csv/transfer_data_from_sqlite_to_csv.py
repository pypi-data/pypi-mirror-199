from pathlib import Path

from ..context_managers.db_manager import SQLite
from ..context_managers.csv_managers import CSVWriter


def fetch_tables(database_path: Path) -> list[str]:
    prompt = """SELECT name
                FROM sqlite_schema
                WHERE type = 'table' AND name NOT LIKE 'sqlite_%';"""

    with SQLite(database_path) as cur:
        cur.execute(prompt)
        tables = [table[0] for table in cur.fetchall()]
        return tables


def fetch_data_from_sqlite(database_path: Path, table: str) -> (list[tuple], list[tuple]):
    prompt_fetch_data = f"SELECT * FROM {table}"
    prompt_fetch_column_names = f"SELECT name FROM pragma_table_info((:table))"
    data_table = {"table": table}

    with SQLite(database_path) as cur:
        cur.execute(prompt_fetch_data)
        fetched_data_sqlite = cur.fetchall()

        cur.execute(prompt_fetch_column_names, data_table)
        # (see: https://www.sqlite.org/pragma.html#pragma_table_info)
        fetched_column_names = [column_info[0] for column_info in cur.fetchall()]
        return fetched_data_sqlite, fetched_column_names


def create_csv_files_dir(database_path: Path, csv_dir_path: Path):
    csv_files_dir = csv_dir_path.joinpath(database_path.stem)
    csv_files_dir.mkdir()
    return csv_files_dir


def import_sqlite_to_csv(database_path: Path, csv_files_dir: Path, table: str) -> None:
    fetched_data_sqlite, fetched_column_names = fetch_data_from_sqlite(database_path, table)

    # create destination of the generated file
    csv_file_name = Path(f"{table}.csv")
    csv_file_path = csv_files_dir.joinpath(csv_file_name)

    with CSVWriter(csv_file_path, fetched_column_names) as csv_writer:
        for column_data in fetched_data_sqlite:
            to_be_written = dict(zip(fetched_column_names, column_data))
            csv_writer.writerow(to_be_written)


def db_mode(database_path: Path) -> str:
    csv_dir_path = Path(input("Copy path to directory where folder with csv files will be stored: ").replace('"', ''))
    if not csv_dir_path.is_dir():
        return "Provided path is incorrect."

    csv_files_dir = create_csv_files_dir(database_path, csv_dir_path)
    status_msg = ""
    for table in fetch_tables(database_path):
        import_sqlite_to_csv(database_path, csv_files_dir, table)
        status_msg += f"Data from {table} table are now stored in {table}.csv.\n"

    return status_msg
