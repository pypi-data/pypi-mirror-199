from pathlib import Path

import pytest

from .constants_tests import DATABASE
from csv_sqlite_converter.validation import db_input_validation


@pytest.mark.dbvalidation
@pytest.mark.parametrize("table, exp_result", [
    ("faces", True),
    ("facestype", True),
    ("nofaces", False)
])
def test_table_exists(table: str, exp_result: bool):
    validated = db_input_validation.table_exists(DATABASE, table)

    assert validated is exp_result


@pytest.mark.dbvalidation
@pytest.mark.parametrize("path, exp_extension, exp_bool", [
    (Path("random.db"), (".db",), True),
    (Path("random.csv"), (".csv", ".txt"), True),
    (Path("random.txt"), (".csv", ".txt"), True),
    (Path("random_no_extension"), (".csv", ".txt"), False),
    (Path("random_no_extension"), (".db",), False)
])
def test_is_extension_correct(path, exp_extension, exp_bool):
    result = db_input_validation.is_extension_correct(path, exp_extension)

    assert result is exp_bool


@pytest.mark.dbvalidation
@pytest.mark.parametrize("table, columns_list, exp_bool", [
    ("faces", ['number', 'photo', 'id'], True),
    ("facestype", ['id', 'type_of_face'], True),
    ("faces", ['photo', 'number', 'id'], False),
    ("faces", ['number', 'photo', 'ids'], False),
    ("facestype", ['type_of_face', 'id'], False),
    ("facestype", ['ids', 'type_of_face'], False)
])
def test_columns_are_correct(table, columns_list, exp_bool):
    result = db_input_validation.columns_are_correct(DATABASE, table, columns_list)

    assert result is exp_bool
