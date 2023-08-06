import os
import tempfile
from shutil import which

from yapyfuzz.handler import ListHandler, SQLiteHandler

# constants
FZF_URL = "https://github.com/junegunn/fzf"


class Fuzzy:
    def __init__(
        self, handler: ListHandler | SQLiteHandler, exec_path=None
    ):
        self.input_file = None
        self.output_file = None
        self.handler = handler

        if exec_path:
            self.exec_path = exec_path
        elif not which("fzf") and not exec_path:
            raise SystemError(f"Cannot find 'fzf' installed on PATH. ({FZF_URL})")
        else:
            self.exec_path = "fzf"

    def get_selection(self, fzf_options=""):
        input = self.handler.get_utf8_str()
        selection = []

        with tempfile.NamedTemporaryFile(delete=False) as input_file:
            with tempfile.NamedTemporaryFile(delete=False) as output_file:
                # Create a temp file with list entries as lines
                input_file.write(input)
                input_file.flush()

        # Invoke fzf externally and write to output file
        os.system(
            f'{self.exec_path} {fzf_options} < "{input_file.name}" > "{output_file.name}"'
        )

        # get selected options
        with open(output_file.name, encoding="utf-8") as f:
            for line in f:
                selection.append(line.strip("\n"))

        os.unlink(input_file.name)
        os.unlink(output_file.name)

        return selection
