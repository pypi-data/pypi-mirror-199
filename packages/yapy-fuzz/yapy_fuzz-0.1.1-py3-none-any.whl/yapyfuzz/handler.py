from abc import ABC
import psycopg2
import pandas as pd
import tempfile

import os


class Handler(ABC):
    def reader(self) -> None:
        pass

    def get_utf8_str(self) -> None:
        pass


class ListHandler(Handler):
    def reader(self, choices, delimiter="\n") -> str:
        # convert a list to a string [ 1, 2, 3 ] => "1\n2\n3"
        self.output = delimiter.join(map(str, choices))

    def get_utf8_str(self) -> None:
        return self.output.encode("utf-8")


class SQLiteHandler(Handler):
    def reader(self, name: str, query: str) -> str:
        self.output = os.popen(f'sqlite3 {name} "{query}"').read()

    def get_utf8_str(self) -> None:
        return self.output.encode("utf-8")


class PostgresHandler(Handler):
    def reader(self, query: str, **kwargs) -> str:
        with psycopg2.connect(
            **kwargs,
        ) as connection:
            connection.autocommit = True

            self.df = pd.read_sql(query, con=connection)

    def get_utf8_str(self) -> None:
        self.df_string = []
        with tempfile.NamedTemporaryFile(mode="r+", delete=False) as output_file:
            # Create a temp file with list entries as lines
            self.df.to_csv(output_file, index=False)

        with open(output_file.name, encoding="utf-8") as f:
            for line in f:
                self.df_string.append(line)

        self.df_string = "".join(map(str, self.df_string))
        os.unlink(output_file.name)

        return self.df_string.encode("utf-8")

