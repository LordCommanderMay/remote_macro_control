import osascript


class DarwinVolumeController:
    master_volume: float
    input_volume: float
    input_sinks = None

    def __init__(self):
        self.master_volume = osascript.run("output volume of(get volume settings)")[1]
        self.input_volume = osascript.run("input volume of (get volume settings)")[1]

    def change_master_volume(self, volume: float):
        osascript.run(f"set volume output volume {volume}")


    def change_input_volume(self, volume: float):
        osascript.run(f"set volume input volume {volume}")
