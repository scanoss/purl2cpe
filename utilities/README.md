# Introduction
This folder contains utility/helper scripts to best leverage the purl2cpe project.

## SQLite Loader
The [sqlite_loader.py](sqlite_loader.py) is a Python script that loads the [data](../data) folder into an SQLite database.

The script will build a database file called `purl2cpe.db` (by default) inside which it will create a table called `purl2cpe`.
It will then iterate through all files inside the data folder and insert in the purl2cpe table all PURL|CPE pairs.

### Requirements
Python 3.7 or higher.

The dependencies can be found in the [requirements.txt](requirements.txt) file.

To install dependencies, run:
```bash
pip3 install -r requirements.txt
```

### Usage
To run the SQLite Loader, please call it from the CLI using:
```shell
python3 sqlite_loader.py --help
```

To process the `data` folder in its entirety, please use the following command:
```shell
python3 sqlite_loader.py ../data
```

Or to get a sub-set, just specify a specific vendor folder:
```shell
python3 sqlite_loader.py ../data/pivotal
```

To write the results to a different SQLite file use:
```shell
python3 sqlite_loader.py ../data/pivotal -o custom-sqlite.db
```

To run in quiet mode, simply add `--quiet`.

### SQLite Consumption
To query the database, load it using:
```shell
sqlite3 purl2cpe.db

```
To query data within, please use:
```sqlite
select cpe from purl2cpe where purl = 'pkg:github/aerospike/aerospike-server';
```
