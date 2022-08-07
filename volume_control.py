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

    @property
    def output_muted(self):
        return self.OSVolumeController.output_muted

    @property
    def input_muted(self):
        return self.OSVolumeController.input_muted


    def change_master_volume(self, volume: float):
        self.OSVolumeController.change_master_volume(volume)

    def toggle_master_mute(self):
        self.OSVolumeController.toggle_input_mute()

    def change_input_volume(self, volume: float):
        self.OSVolumeController.change_input_volume(volume)

    def get_input_sinks(self):
        return self.OSVolumeController.input_sinks









p = VolumeController()
print(p.master_volume)
print(p.input_volume)