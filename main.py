import json
import time
import pulsectl
import zmq
from data_packet import create_packet
from sinkinput import SinkInputs


def main():
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind("tcp://*:5566")

    sink_inputs_list: list[SinkInputs] = []

    while True:
        with pulsectl.Pulse('volume-increase') as pulse:
            print(pulse.server_info().default_sink_name)

            for sink_input in pulse.sink_input_list():
                sink_inputs_list.append(SinkInputs(pulse, sink_input))
            message = socket.recv()
            print(message)
            recv_data_packet = json.loads(message.decode("utf-8"))
            print(recv_data_packet["action"])
            match recv_data_packet["action"]:
                case 'send_data':
                    print("moose")
                    packet = create_packet(sink_inputs_list)
                    socket.send(packet)

                case "change_volume_input_sink":
                    for sink_input in sink_inputs_list:
                        if sink_input.sink_id == recv_data_packet["sink_id"]:
                            sink_input.change_volume(recv_data_packet["volume"])

                case "toggle_mute_input_sink":
                    for sink_input in sink_inputs_list:
                        if sink_input.sink_id == recv_data_packet["sink_id"]:
                            sink_input.toggle_mute()

        sink_inputs_list.clear()



if __name__ == '__main__':
    main()

