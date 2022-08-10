import json, subprocess, runpy, pyautogui
from sqlalchemy import Column, Integer, String, Enum
import keyboard
from base import Base
import enum


class MacroType(enum.Enum):
    TERMINAL_COMMAND = 1
    KEYBOARD_SHORTCUT = 2
    PYTHON_SCRIPT = 3


class Macro(Base):
    __tablename__ = 'macros'
    macro_id = Column(Integer, primary_key=True)
    name = Column(String)
    icon = Column(String)
    macro_type = Column(Enum(MacroType))
    args = Column(String)

    def __init__(self, name: str, icon: str, macro_type: enum.Enum, args: str):
        self.name = name
        self.icon = icon
        self.macro_type = macro_type
        self.args = args

    def execute(self):
        print(self.macro_type)
        args: list[str] = json.loads(self.args)
        print(args)

        match self.macro_type:

            case MacroType.TERMINAL_COMMAND:
                subprocess.run(args)

            case MacroType.KEYBOARD_SHORTCUT:
                pyautogui.hotkey(*args)

            case MacroType.PYTHON_SCRIPT:
                path_name = ''.join(args)
                runpy.run_path(path_name)







