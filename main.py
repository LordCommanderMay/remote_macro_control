import json
import zmq
from volume_control import VolumeController
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from base import Base

import macro

def main():
    sql_engine = create_engine("sqlite:///database.db", echo=True, future=True)
    Base.metadata.create_all(bind=sql_engine)
    session = sessionmaker(bind=sql_engine)
    session = session()

    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind("tcp://*:5566")
    while True:
        macros = session.query(macro.Macro)
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
            case 'change_master_volume':
                volume_controller.change_master_volume(recv_data_packet['volume'])
            case 'toggle_master_mute':
                volume_controller.toggle_master_mute()

            case "change_volume_input_sink":
                for sink_input in VolumeController.get_input_sinks():
                    if sink_input.sink_id == recv_data_packet["sink_id"]:
                        sink_input.change_volume(recv_data_packet["volume"])

            case "toggle_mute_input_sink":
                for sink_input in VolumeController.get_input_sinks():
                    if sink_input.sink_id == recv_data_packet["sink_id"]:
                        sink_input.toggle_mute()
        session.commit()
        session.close()





if __name__ == '__main__':
    main()
