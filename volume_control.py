import platform

class VolumeController:

    __init__(self):
    match platform.system():
        case "Linux":
            from linux.linux_volume_control import SinkInput
        case "Darwin":
            pass
        case "Windows":
            pass
        case _:
            raise OSError("OS not supported!")