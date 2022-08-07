import subprocess
from sqlalchemy import  Column, Integer, String

class Macro:
    def __init__(self, macro_id, name, args: list[str] or None):
        self.macro_id = macro_id
        self.name = name
        self.args = args

    def exacute(self):
        process = subprocess.run(self.args, check=True)
