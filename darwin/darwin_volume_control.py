import osascript


class DarwinVolumeController:
    """Volume Controls for mac os using apple scripts use by Volume Control class for darwin controllers"""
    master_volume: float
    input_volume: float
    output_muted: bool
    input_muted: bool

    input_sinks = None

    def __init__(self):
        try:
            self.master_volume = float(osascript.run("output volume of(get volume settings)")[1])
        except ValueError:  # fixed bug that caused crash when macbook was using hdmi audio output
            self.master_volume = 0
        self.input_volume = float(osascript.run("input volume of (get volume settings)")[1])
        self.output_muted = osascript.run("output muted of (get volume settings)")[1] == 'true'
        self.input_muted = False  # may cause a bug needs to be tested


    def change_master_volume(self, volume: float):
        osascript.run(f"set volume output volume {volume}")


    def change_input_volume(self, volume: float):
        osascript.run(f"set volume input volume {volume}")

    def toggle_mute_master_volume(self):
        print(self.output_muted)
        if self.output_muted:
            osascript.run("set volume without output muted", background=True)
            self.master_volume = False
        else:
            osascript.run("set volume with output muted")
            self.master_volume = True

    def toggle_input_mute(self):
        # mac os does not have a good way of doing this
        raise NotImplementedError()
