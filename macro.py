import json, subprocess, runpy, pyautogui
import os
import platform
import webbrowser
from sqlalchemy import Column, Integer, String, Enum
import keyboard
from base import Base
import enum


class MacroType(enum.Enum):
    TERMINAL_COMMAND = 1
    KEYBOARD_SHORTCUT = 2
    PYTHON_SCRIPT = 3
    OPEN_WEBPAGE = 4
    RUN_PROGRAM = 5
    RUN_STEAM_GAME = 6



class Macro(Base):
    __tablename__ = 'macros'
    macro_id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(String)
    color = Column(String)
    icon = Column(String)
    macro_type = Column(Enum(MacroType))
    args = Column(String)

    def __init__(self, name:  str, desc: str, color : str, icon: str, macro_type: enum.Enum, args: str):
        self.name = name
        self.desc = desc
        self.color
        self.icon = icon
        self.macro_type = macro_type
        self.args = args

    def execute(self):
        print(self.macro_type)
        args: list[str] = json.loads(self.args)
        print(args)

        match self.macro_type:

            case MacroType.TERMINAL_COMMAND:
                subprocess.Popen(args, shell=True)

            case MacroType.KEYBOARD_SHORTCUT:
                pyautogui.hotkey(*args)

            case MacroType.PYTHON_SCRIPT:
                subprocess.Popen(['python', args[0]], shell=True)

            case MacroType.OPEN_WEBPAGE:
                pass  # web browswe doesnt work on windows it freezes program

            case MacroType.RUN_PROGRAM:
                subprocess.run(args)

            case MacroType.RUN_STEAM_GAME:
                game_id = args[0]
                subprocess.call(f"steam steam://rungameid/{game_id}", shell=True)
