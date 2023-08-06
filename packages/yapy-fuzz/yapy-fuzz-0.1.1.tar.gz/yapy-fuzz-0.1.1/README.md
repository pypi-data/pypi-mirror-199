Yapy-Fuzz
=======

![](https://img.shields.io/badge/license-MIT-green.svg?style=flat)
<!-- ![https://pypi.python.org/pypi/pyfuzzy](https://img.shields.io/pypi/dm/pyfuzzy.svg?style=flat) -->

##### Yet another python wrapper for *junegunn*'s  [fzf](https://github.com/junegunn/fzf) ***pronunced yaa-pee fuzz*** with handlers for python lists, sqlite3 and postgres

#### Why create another wrapper lib?
I wanted a quick way to do fuzzy search on any data source from text files to databases and I couldn't find a single tool that has support for various different inputs/sources for fzf.

<!-- ![](https://raw.githubusercontent.com/nk412/pyfuzzy/master/pyfuzzy.gif) -->

Requirements
------------

* Python 3.6+
* [fzf](https://github.com/junegunn/fzf)
* sqlite3
* pandas (for postgres support)

*Note*: fzf and sqlite3 must be installed and available on PATH.

Installation
------------
	pip install yapy-fuzz

Usage
-----
    >>> from yapyfuzz.core import Fuzzy
    >>> fzf = Fuzzy()

If `fzf` is not available on PATH, you can specify a location

    >>> fzf = Fuzzy(exec_path="/path/to/fzf")

Initiate a handler depending on your requirements, for e.g., python lists.

    >>> from yapyfuzz.core import ListHandler
    >>> list_handler = ListHandler()
    >>> list_handler.reader(range(0,10))

    >>> fzf = Fuzzy(list_handler)
    >>> fzf.get_selection(list_handler)

SQLite DB Handler

    >>> from yapyfuzz.core import SQLiteHandler
    >>> name = f"{root_dir}/yapy/fuzzy.db"
    >>> query = "select * from albums"
    >>> db_handler = SQLiteHandler()
    >>> db_handler.reader(name, query)

    >>> fp = Fuzzy(db_handler)
    >>> fp.get_selection()

Postgres DB Handler

    >>> from yapyfuzz.core import PostgresHandler

    >>> db_settings = {
        "user":"postgres",
        "password":"postgres",
        "host":"localhost",
        "port":"5432",
        "dbname":"dellstore",
    }

    >>> pg_handler = PostgresHandler()

    >>> pg_handler.reader(query="select * from categories", **db_settings)
    >>> pg_handler.reader(query="select * from inventory", **db_settings)

    >>> fp = Fuzzy(pg_handler)
    >>> fp.get_selection()

You can pass additional arguments to fzf as a second argument

    >>> fzf.prompt(range(0,10), '--multi --cycle')

Input items are written to a temporary file which is then passed to fzf.
The items are delimited with `\n` by default.

License
-------
MIT

Todo
-------
- [X] Add support for postgres db
- [ ] CLI table explorer tool to navigate db and tables

