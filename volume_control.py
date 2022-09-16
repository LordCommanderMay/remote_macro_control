import platform
import json


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
                from windows.windows_volume_control import WindowsVolumeController
                self.OSVolumeController = WindowsVolumeController()
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
        self.OSVolumeController.toggle_mute_master_volume()

    def change_input_volume(self, volume: float):
        self.OSVolumeController.change_input_volume(volume)

    def toggle_input_mute(self):
        self.OSVolumeController.toggle_input_mute()

    def get_app_volume_controllers(self):
        return self.OSVolumeController.app_controllers

    def get_volume_data_json(self):
        packet = {
            "action": 'sent_data',
            "data": {
                "master_volume": self.master_volume,
                "output_muted": self.output_muted,
                "input_volume": self.input_volume,
                "input_muteed": self.input_muted,
                "app_controllers": []

            }
        }
        if platform.system() == "Darwin":
            pass
        else:
            for app in self.get_app_volume_controllers():
                packet['data']['app_controllers'].append(app.to_dict())

        return json.dumps(packet)
