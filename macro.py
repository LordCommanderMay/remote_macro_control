import subprocess
from sqlalchemy import Column, Integer, String, Enum
from base import Base
import enum


class MacroType(enum.Enum):
    TERMINAL_COMMAND = 1


class Macro(Base):
    __tablename__ = 'macros'
    macro_id = Column(Integer, Primary_key=True)
    name = Column(String)
    icon = Column(String)
    macro_type = Column(Enum)
    command = Column(String)

    def __init__(self, name: str, icon: str, macro_type: enum.Enum, command: str):
        self.name = name
        self.icon = icon
        self.macro_type = macro_type
        self.command = command

    def execute(self):

        match self.macro_type:
            case MacroType.TERMINAL_COMMAND:
                process = subprocess.run(self.args, check=True)

