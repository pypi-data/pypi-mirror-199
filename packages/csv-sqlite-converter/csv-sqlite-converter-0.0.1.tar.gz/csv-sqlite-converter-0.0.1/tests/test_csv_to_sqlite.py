import pytest

from csv_sqlite_converter.csv_to_sqlite import transfer_data_from_csv_to_sqlite


@pytest.mark.csvsqlite
@pytest.mark.parametrize("table, fieldnames, exp_query", [
    ("faces", ['number', 'photo', 'id'], "INSERT INTO faces(number, photo, id) VALUES(?, ?, ?)"),
    ("facestype", ['id', 'type_of_face'], "INSERT INTO facestype(id, type_of_face) VALUES(?, ?)")
])
def test_construct_query(table, fieldnames, exp_query):
    query = transfer_data_from_csv_to_sqlite.construct_query(table, fieldnames)

    assert query == exp_query


@pytest.mark.csvsqlite
@pytest.mark.parametrize("csv_row, fieldnames, exp_data", [
    (
        {"number": "1", "photo": b"\\xcc\\xcc\\xc4\\xcc[p\\x04C\\xbc\\xc5p,3\\xc2", "id": "1"},
        ["number", "photo", "id"],
        (1, b"\\xcc\\xcc\\xc4\\xcc[p\\x04C\\xbc\\xc5p,3\\xc2", 1)
    ),
    (
        {"number": "3", "photo": b"n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00d\x00\x00\x00k\x08", "id": "2"},
        ["number", "photo", "id"],
        (3, b"n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00d\x00\x00\x00k\x08", 2)
    ),
    (
        {'id': '1', 'type_of_face': 'intermediate'},
        ['id', 'type_of_face'],
        (1, "intermediate")
    ),
    (
        {'id': '2', 'type_of_face': 'scowl'},
        ['id', 'type_of_face'],
        (2, "scowl")
    ),
    (
        {'id': '3', 'type_of_face': 'smile'},
        ['id', 'type_of_face'],
        (3, "smile")
    )

])
def test_transfer_data_to_tuple(csv_row, fieldnames, exp_data):
    data = transfer_data_from_csv_to_sqlite.transfer_data_to_tuple(csv_row, fieldnames)

    assert data == exp_data
