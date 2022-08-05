import pulsectl
import random

ids : list[hex] = []


class SinkInputs:
    sink_id: bytes
    pulse_pointer: pulsectl.Pulse
    sink_input_obj: pulsectl.pulsectl.PulseSinkInputInfo
    app_name: str
    icon_name: str or None
    volume: float
    mute: bool

    def __init__(self, pulse_pointer, sink_input: pulsectl.pulsectl.PulseSinkInputInfo):
        def gen_id():
            return_id: bytes = random.randbytes(4)
            if return_id in ids:
                gen_id()
            else:
                return return_id

        self.id = gen_id()
        self.pulse_pointer = pulse_pointer
        self.sink_input_obj = sink_input
        self.app_name = sink_input.proplist["application.name"]
        try:
            self.icon_name = sink_input.proplist["media.icon_name"]
        except KeyError:
            try:
                self.icon_name = sink_input.proplist["application.icon_name"]
            except KeyError:
                self.icon_name = None
        self.volume = sink_input.volume.values[0]  # support for only one channel at the moment
        self.mute = False  # initial value might need to come up with a way to check it properly

    def change_volume(self, volume_level: float):

        self.pulse_pointer.volume_set_all_chans(self.sink_input_obj, volume_level)
        self.volume = volume_level

    def toggle_mute(self):
        if self.mute:
            self.pulse_pointer.mute(self.sink_input_obj, False)
        else:
            self.pulse_pointer.mute(self.sink_input_obj, True)

    def __dict__(self):
        return {
            "app_name": self.app_name,
            "icon_name": self.icon_name,
            "volume": self.volume,
            "muted": self.mute
        }

    def to_dict(self):
        return self.__dict__()

    def __str__(self):
        return str(self.__dict__())

    def __repr__(self):
        return self.__str__()
