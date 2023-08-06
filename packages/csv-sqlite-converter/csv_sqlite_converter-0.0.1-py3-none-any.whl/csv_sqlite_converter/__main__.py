from pathlib import Path

from .sqlite_to_csv.transfer_data_from_sqlite_to_csv import db_mode
from .csv_to_sqlite.transfer_data_from_csv_to_sqlite import csv_mode
from .validation import db_input_validation


def main() -> None:
    mode = ""

    while mode != "stop":
        mode = input("""
Choose one of the following:
\t1. "db" to transfer data from a database to csv files
\t2. "csv" to transfer data from a csv files to a database
\t3. "stop" to stop
> """).lower()

        if mode == "stop":
            break

        # get db_path
        database_path = Path(input("Copy path to database: ").replace('"', ''))

        if not database_path.is_file() or not db_input_validation.is_extension_correct(database_path, (".db",)):
            print("Provided path is incorrect.")
            continue

        if mode == "db":
            status_msg = db_mode(database_path)
            print(status_msg)
        elif mode == "csv":
            status_msg = csv_mode(database_path)
            print(status_msg)
        else:
            print("Chosen mode is incorrect.")


if __name__ == "__main__":
    main()
