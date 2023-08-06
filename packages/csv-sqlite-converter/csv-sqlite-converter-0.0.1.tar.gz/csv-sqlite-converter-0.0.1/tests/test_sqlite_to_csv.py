import pytest

from csv_sqlite_converter.sqlite_to_csv import transfer_data_from_sqlite_to_csv
from .constants_tests import (
    TESTS_DIR_PATH,
    DATABASE,
    FACES_TABLE_CONTENT,
    FACES_TABLE_COLUMNS,
    FACESTYPE_TABLE_CONTENT,
    FACESTYPE_TABLE_COLUMNS
)


@pytest.mark.sqlitecsv
def test_fetch_tables():
    tables = transfer_data_from_sqlite_to_csv.fetch_tables(DATABASE)

    assert tables == ['facestype', 'faces']


@pytest.mark.sqlitecsv
@pytest.mark.parametrize("table, exp_content, exp_columns", [
    ("faces", FACES_TABLE_CONTENT, FACES_TABLE_COLUMNS),
    ("facestype", FACESTYPE_TABLE_CONTENT, FACESTYPE_TABLE_COLUMNS)
])
def test_fetch_data_from_sqlite(table, exp_content, exp_columns):
    content, columns = transfer_data_from_sqlite_to_csv.fetch_data_from_sqlite(DATABASE, table)

    assert content == exp_content
    assert columns == exp_columns


@pytest.mark.sqlitecsv
@pytest.mark.parametrize("db_path, exp_path", [
    (TESTS_DIR_PATH.joinpath("test/test.db"), TESTS_DIR_PATH.joinpath("test")),
    (TESTS_DIR_PATH.joinpath("test/text2.db"), TESTS_DIR_PATH.joinpath("text2"))
])
def test_create_csv_files_dir(db_path, exp_path):
    generated_path = transfer_data_from_sqlite_to_csv.create_csv_files_dir(db_path, TESTS_DIR_PATH)

    assert generated_path == exp_path


@pytest.mark.sqlitecsv
def test_rm_dir_not_an_actual_test():
    TESTS_DIR_PATH.joinpath("test").rmdir()
    TESTS_DIR_PATH.joinpath("text2").rmdir()
