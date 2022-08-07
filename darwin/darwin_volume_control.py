import osascript


class DarwinVolumeController:
    master_volume: float
    input_volume: float
    output_muted: bool
    input_muted: bool

    input_sinks = None

    def __init__(self):
        self.master_volume = float(osascript.run("output volume of(get volume settings)")[1])
        self.input_volume = float(osascript.run("input volume of (get volume settings)")[1])
        self.output_muted = bool(osascript.run("output muted of (get volume settings)")[0])
        self.input_muted = False  # may cause a bug needs to be tested

    def change_master_volume(self, volume: float):
        osascript.run(f"set volume output volume {volume}")

    def change_input_volume(self, volume: float):
        osascript.run(f"set volume input volume {volume}")

    def toggle_mute_master_volume(self):
        if self.output_muted:
            osascript.run("set volume without output muted")
            self.master_volume = False
        else:
            osascript.run("set volume with output muted")
            self.master_volume = True


l = DarwinVolumeController()
osascript.run("set volume with output muted")
print(l.master_volume)
