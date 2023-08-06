# CSV-SQLite Converter
The CSV-SQLite Convert allows to store data both from SQLite database in csv files and from csv files in a SQLite database.

## Installation
You can install CSV-SQLite Converter from PyPi (in the future).
    
    python -m pip install csv_sqlite_converter

The converter supports Python 3.10 and higher.

## How to use
The converter is a command line tool. To use it, run:

    python -m csv_sqlite_converter

And the following should appear:
    
    >>> Choose one of the following:
            "db" to transfer data from a database to csv files
            "csv" to transfer data from csv files to a database
            "stop" to stop
        > 

where:

### "db" 
allows to transfer data from a database to csv files. **It needs two paths**: to the database and folder where csv files can be stored. After choosing this option the following appears:
    
    >>> Copy path to database: <provide/here/path/to/database.db>
    >>> Copy path to directory where folder with csv files will be stored: <provide/path/to/a/folder>
    >>> Data from [name_of_table] table are now stored in [name_of_table].csv.
    >>> Data from [name_of_another_table] table are now stored in [name_of_another_table].csv.
    >>> ...

### "csv"
allows to transfer data from csv files to a database. **It needs two paths**: to csv files with data and the database to write to. However, csv files **must follow a very precise structure**:
```
.
+-- csv1.csv
+-- csv2.csv
+-- csv3.csv
```
where: 
1. the name of the root folder matches the name of the database file
2. names of csv files match names of tables in the database files (ex. students.csv holds data for a table named students)

After choosing this option the following appears:

    >>> Copy path to database: <provide/here/path/to/database.db>
    >>> Copy path to directory with csv files: <provide/path/to/a/folder/with/csv/files>
    >>> File [name_of_csv_file] processed successfully.
    >>> File [name_of_another_csv_file] processed successfully.
    >>> ...   

### "stop"
stops the execution of the package.
