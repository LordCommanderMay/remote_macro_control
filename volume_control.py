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
        self.OSVolumeController.toggle_mute_master_volume()

    def change_input_volume(self, volume: float):
        self.OSVolumeController.change_input_volume(volume)

    def toggle_input_mute(self):
        self.OSVolumeController.toggle_input_mute()

    def get_input_sinks(self):
        return self.OSVolumeController.input_sinks

    def get_volume_data_json(self):
            packet = {
                "action": 'sent_data',
                "data": {
                    "master_volume" :  self.master_volume,
                    "output_muted" : self.output_muted,
                    "input_volume" : self.input_volume,
                    "input_muteed" : self.input_muted,
                    "sink_inputs" : []

                }
            }
            if platform.system() == "Darwin":
                pass
            else:
                for sink_input in self.get_input_sinks():
                    packet['data']['sink_inputs'].append(sink_input.to_dict())

            return json.dumps(packet)









