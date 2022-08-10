import itertools
import pulsectl


class SinkInput:
    sink_id: int
    pulse_pointer: pulsectl.Pulse
    sink_input_obj: pulsectl.pulsectl.PulseSinkInputInfo
    app_name: str
    icon_name: str or None
    volume: float
    mute: bool

    id_iter = itertools.count()

    def __init__(self, pulse_pointer, sink_input: pulsectl.pulsectl.PulseSinkInputInfo):

        self.sink_id = next(SinkInput.id_iter)
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
            "sink_id": self.sink_id,
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


def get_master_output():
    raise NotImplementedError()


def get_main_inputs():
    raise NotImplementedError


def get_sink_inputs(pulse: pulsectl.Pulse) -> list[SinkInput]:
    sink_inputs_list: list[SinkInput] = []
    print(pulse.server_info().default_sink_name)

    for sink_input in pulse.sink_input_list():
        sink_inputs_list.append(SinkInput(pulse, sink_input))

    return sink_inputs_list


class LinuxVolumeController:
    master_volume: float
    input_volume: float
    output_muted: bool
    input_muted: bool
    _sink: pulsectl.pulsectl.PulseSinkInfo
    input_sinks: list[SinkInput]

    def __init__(self):
        self._pulse = pulsectl.Pulse('Remote Macro Control')
        self.input_sinks = get_sink_inputs(self._pulse)
        self._sink = self._pulse.get_sink_by_name(self._pulse.server_info().default_sink_name)
        self._input = self._pulse.get_source_by_name(self._pulse.server_info().default_source_name)
        self.output_muted = self._sink.mute
        self.master_volume = float(self._sink.base_volume) * 100  # sink_volume is 0.0 - 1.0
        self.input_volume = float(self._sink.base_volume) * 100  # ^^^^
        self.input_muted = self._input.mute

    def __del__(self):
        self._pulse.close()


    def change_master_volume(self, volume: float):
        self._pulse.volume_set(self._sink, (volume / 100, volume / 100))

    def change_input_volume(self, volume: float):
        self._pulse.source_volume_set(self, (volume / 100, volume / 100))

    def toggle_mute_master_volume(self):
        if self.output_muted:
            self._pulse.mute(self._sink, False)
        else:
            self._pulse.mute(self._sink, True)

    def toggle_input_mute(self):
        if self.input_muted:
            self._pulse.mute(self._input, False)
        else:
            self._pulse.mute(self._input, True)
