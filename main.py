import json
import time
import zmq
#from data_packet import create_packet
from volume_control import VolumeController


def main():
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind("tcp://*:5566")
    while True:
        volume_controller = VolumeController()
        print(volume_controller.master_volume)
        message = socket.recv()
        recv_data_packet = json.loads(message.decode("utf-8"))
        print(recv_data_packet["action"])
        match recv_data_packet["action"]:
            case 'send_data':
                print(volume_controller.output_muted)
                packet = volume_controller.get_volume_data_json()
                socket.send(packet)
        #
        #     case "change_volume_input_sink":
        #         for sink_input in sink_inputs_list:
        #             if sink_input.sink_id == recv_data_packet["sink_id"]:
        #                 sink_input.change_volume(recv_data_packet["volume"])
        #
        #     case "toggle_mute_input_sink":
        #         for sink_input in sink_inputs_list:
        #             if sink_input.sink_id == recv_data_packet["sink_id"]:
        #                 sink_input.toggle_mute()




if __name__ == '__main__':
    main()
