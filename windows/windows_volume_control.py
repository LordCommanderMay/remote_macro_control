import itertools
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from pycaw.utils import AudioSession



class AppVolumeController:
    app_id: int
    app_name: str
    _session: AudioSession
    icon_name: str or None
    volume: float
    mute: bool
    id_iter = itertools.count()




    def __init__(self, session: AudioSession):


        self.app_id = next(AppVolumeController.id_iter)
        if session.DisplayName == "@%SystemRoot%\System32\AudioSrv.Dll,-202":
            self.app_name = "System  Sounds"
        else:
            self.app_name = session.Process.name().replace(".exe", '')
        self._volume_controller = session.SimpleAudioVolume
        self._session = session
        self.icon_name = "Not Yet Implemented"  # <---------------- FIx me
        self.volume = self._volume_controller.GetMasterVolume()
        self.mute = bool(self._volume_controller.GetMute())

    def toggle_mute(self):
        if self.mute:
            self.pulse_pointer.mute(self.sink_input_obj, False)
        else:
            self.pulse_pointer.mute(self.sink_input_obj, True)

    def __dict__(self):
        return {
            "app_id": self.app_id,
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


class WindowsVolumeController:
    master_volume: float
    input_volume: float
    output_muted: bool
    input_muted: bool
    app_controllers: list[AppVolumeController]

    def __init__(self):

        devices = AudioUtilities.GetSpeakers()
        mic_devices = AudioUtilities.GetMicrophone()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        mic_interface = mic_devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.windows_speaker_controller = cast(interface, POINTER(IAudioEndpointVolume))
        self.windows_microphone_controller = cast(mic_interface, POINTER(IAudioEndpointVolume))

        # output
        self.output_muted = bool(self.windows_speaker_controller.GetMute())
        self.master_volume = speaker_percent2db.index(self.windows_speaker_controller.GetMasterVolumeLevel())

        # input
        self.input_muted = bool(self.windows_microphone_controller.GetMute())

        self.input_volume = mic_db2percent.index(self.windows_microphone_controller.GetMasterVolumeLevel())

        # apps
        self.app_controllers = self.get_app_volume_controllers()


    def get_app_volume_controllers(self) -> list[AppVolumeController]:
        apps_volume_controller_list: list[AppVolumeController] = []
        sessions = AudioUtilities.GetAllSessions()
        for app in sessions:
            apps_volume_controller_list.append(AppVolumeController(app))

        #resets id counter
        AppVolumeController.id_iter = itertools.count()
        return apps_volume_controller_list

    def change_master_volume(self, volume: float):
        self.windows_speaker_controller.SetMasterVolumeLevel(speaker_percent2db[int(volume)], None)

    def change_input_volume(self, volume: float):
        pass

    def toggle_mute_master_volume(self):
        if self.output_muted:
            self.windows_speaker_controller.SetMute(0, None)
        else:
            self.windows_speaker_controller.SetMute(1, None)

    def toggle_input_mute(self):
        if self.input_muted:
            self.windows_microphone_controller.SetMute(0, None)
        else:
            self.windows_microphone_controller.SetMute(1, None)


speaker_percent2db = [-96.0,
                      -67.4974136352539,
                      -58.173828125,
                      -52.437278747558594,
                      -48.282318115234375,
                      -45.02272033691406,
                      -42.34019088745117,
                      -40.06081008911133,
                      -38.07908630371094,
                      -36.32617950439453,
                      -34.75468063354492,
                      -33.33053970336914,
                      -32.02846908569336,
                      -30.829191207885742,
                      -29.7176513671875,
                      -28.681884765625,
                      -27.71221923828125,
                      -26.800716400146484,
                      -25.940793991088867,
                      -25.126928329467773,
                      -24.35443115234375,
                      -23.61930274963379,
                      -22.918092727661133,
                      -22.2478084564209,
                      -21.605838775634766,
                      -20.989887237548828,
                      -20.397926330566406,
                      -19.828153610229492,
                      -19.278972625732422,
                      -18.748943328857422,
                      -18.236774444580078,
                      -17.741300582885742,
                      -17.261470794677734,
                      -16.796323776245117,
                      -16.344989776611328,
                      -15.906672477722168,
                      -15.480639457702637,
                      -15.06622314453125,
                      -14.662806510925293,
                      -14.269820213317871,
                      -13.886737823486328,
                      -13.513073921203613,
                      -13.148375511169434,
                      -12.792222023010254,
                      -12.444223403930664,
                      -12.10401439666748,
                      -11.771252632141113,
                      -11.445619583129883,
                      -11.12681770324707,
                      -10.814563751220703,
                      -10.508596420288086,
                      -10.20866584777832,
                      -9.914539337158203,
                      -9.625996589660645,
                      -9.342827796936035,
                      -9.064839363098145,
                      -8.791844367980957,
                      -8.523664474487305,
                      -8.260135650634766,
                      -8.001096725463867,
                      -7.746397495269775,
                      -7.49589729309082,
                      -7.249458312988281,
                      -7.006951332092285,
                      -6.768252372741699,
                      -6.5332441329956055,
                      -6.301812648773193,
                      -6.073853492736816,
                      -5.849262237548828,
                      -5.627941608428955,
                      -5.409796714782715,
                      -5.194738864898682,
                      -4.982679843902588,
                      -4.7735395431518555,
                      -4.567237854003906,
                      -4.363698959350586,
                      -4.162849426269531,
                      -3.9646193981170654,
                      -3.7689411640167236,
                      -3.5757486820220947,
                      -3.384982109069824,
                      -3.196580171585083,
                      -3.0104846954345703,
                      -2.8266398906707764,
                      -2.6449923515319824,
                      -2.4654886722564697,
                      -2.288081407546997,
                      -2.1127207279205322,
                      -1.9393599033355713,
                      -1.7679541110992432,
                      -1.5984597206115723,
                      -1.4308334589004517,
                      -1.2650364637374878,
                      -1.101028561592102,
                      -0.9387713074684143,
                      -0.7782278060913086,
                      -0.6193622946739197,
                      -0.4621390104293823,
                      -0.3065262734889984,
                      -0.15249048173427582,
                      0.0]

mic_db2percent = [18.0,
                  18.138399124145508,
                  18.27806854248047,
                  18.419034957885742,
                  18.56131935119629,
                  18.7049503326416,
                  18.84994888305664,
                  18.99634552001953,
                  19.144166946411133,
                  19.293437957763672,
                  19.444190979003906,
                  19.596452713012695,
                  19.750255584716797,
                  19.905630111694336,
                  20.062610626220703,
                  20.221227645874023,
                  20.381519317626953,
                  20.54351806640625,
                  20.70726203918457,
                  20.87278938293457,
                  21.040138244628906,
                  21.2093505859375,
                  21.380468368530273,
                  21.55353546142578,
                  21.728593826293945,
                  21.90569305419922,
                  22.08487892150879,
                  22.266202926635742,
                  22.449716567993164,
                  22.63547134399414,
                  22.82352638244629,
                  23.013935089111328,
                  23.20676040649414,
                  23.402063369750977,
                  23.59990692138672,
                  23.80036163330078,
                  24.003494262695312,
                  24.20937728881836,
                  24.418088912963867,
                  24.62970542907715,
                  24.844310760498047,
                  25.061986923217773,
                  25.282827377319336,
                  25.506925582885742,
                  25.734375,
                  25.96527862548828,
                  26.199745178222656,
                  26.437885284423828,
                  26.6798152923584,
                  26.9256591796875,
                  27.17554473876953,
                  27.42960548400879,
                  27.687986373901367,
                  27.950834274291992,
                  28.21830940246582,
                  28.490575790405273,
                  28.767805099487305,
                  29.050186157226562,
                  29.337913513183594,
                  29.63119125366211,
                  29.930240631103516,
                  30.23529052734375,
                  30.546586990356445,
                  30.86439323425293,
                  31.18898582458496,
                  31.520662307739258,
                  31.859739303588867,
                  32.20655059814453,
                  32.561458587646484,
                  32.92485427856445,
                  33.297149658203125,
                  33.678794860839844,
                  34.07027053833008,
                  34.47209167480469,
                  34.88482666015625,
                  35.30908203125,
                  35.74551773071289,
                  36.19485855102539,
                  36.65788650512695,
                  37.13546371459961,
                  37.628536224365234,
                  38.13813781738281,
                  38.6654167175293,
                  39.211647033691406,
                  39.77824401855469,
                  40.36677932739258,
                  40.97902297973633,
                  41.616966247558594,
                  42.282859802246094,
                  42.97926712036133,
                  43.7091178894043,
                  44.475791931152344,
                  45.28319549560547,
                  46.135902404785156,
                  47.039306640625,
                  47.99980926513672,
                  49.02512741088867,
                  50.12464904785156,
                  51.30994415283203,
                  52.59553909301758,
                  54.0, ]
