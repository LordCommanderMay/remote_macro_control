import json
import os
import ctypes

import _ctypes
import zmq
from volume_control import VolumeController
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from base import Base
import socket as Socket
import macro, socket
from log import logger


def main():
    logger.info("Creating/Connect To Database...")
    sql_engine = create_engine("sqlite:///database.db", echo=False, future=True)
    Base.metadata.create_all(bind=sql_engine)
    session = sessionmaker(bind=sql_engine)
    session = session()

    logger.info("Success!")

    logger.info(f"Starting ZMQ server on {Socket.gethostbyname(Socket.gethostname())}:5566")
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind("tcp://*:5566")
    logger.info("Success!")

    while True:
        macros = session.query(macro.Macro)
        # for x in macros:
            #(x.macro_type)

        volume_controller = VolumeController()
        #(volume_controller.master_volume)

        message = socket.recv()
        #(message)
        recv_data_packet = json.loads(message.decode("utf-8"))
        #(recv_data_packet["action"])

        match recv_data_packet["action"]:
            case 'send_data':
                #(volume_controller.output_muted)
                packet = volume_controller.get_volume_data_json()
                socket.send_string(packet)

            case 'change_master_volume':
                try:
                    volume_controller.change_master_volume(recv_data_packet['volume']),
                except _ctypes.COMError:
                    pass
                except OSError:
                    pass





            case 'toggle_master_mute':
                volume_controller.toggle_master_mute()

            case 'toggle_mic_mute':
                volume_controller.toggle_input_mute()

            case "change_app_volume":
                for sink_input in VolumeController.get_app_volume_controllers():
                    if sink_input.app_id == recv_data_packet["sink_id"]:
                        sink_input.change_volume(recv_data_packet["volume"])

            case "toggle_mute_app":
                for sink_input in VolumeController.get_app_volume_controllers():
                    if sink_input.app_id == recv_data_packet["sink_id"]:
                        sink_input.toggle_mute()

            case "run_macro":
                for macro_ in macros:
                    if recv_data_packet["macro_id"] == macro_.macro_id:
                        macro_.execute()

            case "create_macro":
                new_macro = recv_data_packet["data"]
                _macro = macro.Macro(
                    name=new_macro['name'],
                    desc=new_macro['desc'],
                    color=new_macro['color'],
                    icon=new_macro['icon'],
                    macro_type=new_macro["macro_type"],
                    args=new_macro['args']

                )
                session.add(_macro)

        session.commit()
        session.close()


if __name__ == '__main__':
    main()
