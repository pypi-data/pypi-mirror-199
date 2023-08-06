from pathlib import Path
import csv
import sys
maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)


class CSVWriter:
    """Manages the process of writing to csv files from database"""
    def __init__(self, file_path: Path, fieldnames: list[str]):
        self.file_path = file_path  # make a path to a newly-created file
        self.fieldnames = fieldnames

    def __enter__(self):
        self.file_obj = open(self.file_path, mode="w+")
        self.writer = csv.DictWriter(self.file_obj, self.fieldnames)
        self.writer.writeheader()  # write column names
        return self.writer

    def __exit__(self, type_, value, traceback):
        if self.file_obj:
            self.file_obj.close()


class CSVReader:
    """Manages the process of writing to csv files"""
    def __init__(self, file_path: Path):
        self.file_path = file_path

    def __enter__(self):
        self.file_obj = open(self.file_path, mode="r")
        self.reader = csv.DictReader(self.file_obj)
        return self.reader

    def __exit__(self, type_, value, traceback):
        if self.file_obj:
            self.file_obj.close()


if __name__ == "__main__":
    test_p = Path(r"C:\Users\Mateusz\PycharmProjects\csv-sqlite\generated_csv_files\test.csv")
    with CSVWriter(test_p, ["column1", "column2"]) as csv_file:
        csv_file.writerow({"column1": "data1", "column2": "data2"})
