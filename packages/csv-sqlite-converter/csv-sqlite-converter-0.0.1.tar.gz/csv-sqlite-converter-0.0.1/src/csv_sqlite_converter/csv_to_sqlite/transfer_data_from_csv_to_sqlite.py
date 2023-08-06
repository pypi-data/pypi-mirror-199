from pathlib import Path

from ..validation import db_input_validation
from ..context_managers.db_manager import SQLite
from ..context_managers.csv_managers import CSVReader
from .input_checks import check_input_and_insert_into_db


def construct_query(table: str, fieldnames: list[str]) -> str:
    columns = ', '.join(fieldnames)
    placeholders = ', '.join('?' * len(fieldnames))

    return f"INSERT INTO {table}({columns}) VALUES({placeholders})"


def transfer_data_to_tuple(csv_row: dict[str: str], fieldnames: list[str]) -> tuple:
    data_generator = []
    for fieldname in fieldnames:
        try:
            data_generator.append(int(csv_row[fieldname]))  # number strings must be converted to int
        except ValueError:
            data_generator.append(csv_row[fieldname])
    return tuple(data_generator)


def insert_into_db(database_path: Path, prompt: str, csv_row: dict[str: str], fieldnames: list[str]):
    data = transfer_data_to_tuple(csv_row, fieldnames)
    with SQLite(database_path) as cur:
        cur.execute(prompt, data)


def manage_csv_file(database_path: Path, csv_file: Path) -> str:
    with CSVReader(csv_file) as csv_reader:
        fieldnames = csv_reader.fieldnames
        if not db_input_validation.columns_are_correct(database_path, csv_file.stem, fieldnames):
            return f"{csv_file} columns ({fieldnames}) does not match columns in database."
        insert_query = construct_query(csv_file.stem, fieldnames)

        for csv_row in csv_reader:
            insert_into_db(
                database_path,
                insert_query,
                csv_row,
                fieldnames
            )
        return f"File {csv_file} processed successfully."


def csv_mode(database_path: Path) -> str:
    csv_dir_path = Path(input("Copy path to directory with csv files: ").replace('"', ''))
    if not csv_dir_path.is_dir():
        return "Provided path is incorrect."

    status_msg = ""
    for csv_file in csv_dir_path.iterdir():
        csv_management_message = check_input_and_insert_into_db(
            database_path,
            csv_file
        )

        status_msg += f"{csv_management_message}\n"

    return status_msg
