from pathlib import Path

from . import transfer_data_from_csv_to_sqlite
from ..validation import db_input_validation


def check_input_and_insert_into_db(database_path: Path, csv_file: Path) -> str:
    """Makes all necessary validation for csv directory and its content as well as
    performs transactions against a database."""
    if not db_input_validation.is_extension_correct(csv_file, (".csv", ".txt")):
        return f"{csv_file} does not have required extension."

    if not db_input_validation.table_exists(database_path, csv_file.stem):
        return f"Incorrect filename for {csv_file} (no such table)."

    csv_management_message = transfer_data_from_csv_to_sqlite.manage_csv_file(database_path, csv_file)

    return csv_management_message
