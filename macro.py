import os
import subprocess
from sqlalchemy import Column, Integer, String, Enum
import keyboard
from base import Base
import enum


class MacroType(enum.Enum):
    TERMINAL_COMMAND = 1
    KEYBOARD_SHORTCUT = 2


class Macro(Base):
    __tablename__ = 'macros'
    macro_id = Column(Integer, primary_key=True)
    name = Column(String)
    icon = Column(String)
    macro_type = Column(Enum(MacroType))
    args = Column(String)

    def __init__(self, name: str, icon: str, macro_type: enum.Enum, command: str):
        self.name = name
        self.icon = icon
        self.macro_type = macro_type
        self.args = command

    def execute(self):
        print(self.macro_type)

        match self.macro_type:
            case MacroType.TERMINAL_COMMAND:

                os.system(self.args)
            case MacroType.KEYBOARD_SHORTCUT:

                keyboard.press_and_release(self.args)





