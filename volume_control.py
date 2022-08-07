import platform

class VolumeController:

    def __init__(self):
        match platform.system():
            case "Linux":
                from linux.linux_volume_control import LinuxVolumeController
                self.OSVolumeController = LinuxVolumeController()
            case "Darwin":
                from darwin.darwin_volume_control import DarwinVolumeController
                self.OSVolumeController = DarwinVolumeController()
            case "Windows":
                raise NotImplementedError("Windows support has not been added yet")
            case _:
                raise OSError("OS not supported!")

        @property
        def master_volume(self):
            return self.OSVolumeController.master_volume

        @property
        def input_volume(self):
            return self.OSVolumeController.input_volume


