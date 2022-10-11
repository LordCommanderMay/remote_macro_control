import pyautogui as gui


def media_action(key: str):
    match key:

        case "up":
            gui.press("up")

        case "down":
            gui.press("down")

        case "left":
            gui.press("left")

        case "down":
            gui.press("left")

        case "enter":
            gui.press("enter")

        case "playpause":
            gui.press("playpause")

        case "pause":
            gui.press("pause")

        case "nexttrack":
            gui.press("nexttrack")

        case "prevtrack":
            gui.press("prevtrack")

        case "browser-back":
            gui.press("browser-back")

        case "select":
            gui.press("select"),

        case "volumeup":
            gui.press("volumeup")

        case "volumedown":
            gui.press("volumedown")

