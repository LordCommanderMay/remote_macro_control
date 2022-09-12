import json
import os

import zmq
from volume_control import VolumeController
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from base import Base
import socket as Socket
import macro, logging, coloredlogs, socket
from log import logger

def main():

    # logger.debug("this is a debugging message")
    # logger.info("this is an informational message")
    # logger.warning("this is a warning message")
    # logger.error("this is an error message")
    # logger.critical("this is a critical message")

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
        for x in macros:
            print(x.macro_type)

        volume_controller = VolumeController()
        print(volume_controller.master_volume)

        message = socket.recv()
        recv_data_packet = json.loads(message.decode("utf-8"))
        print(recv_data_packet["action"])

        match recv_data_packet["action"]:
            case 'send_data':
                print(volume_controller.output_muted)
                packet = volume_controller.get_volume_data_json()
                socket.send_string(packet)

            case 'change_master_volume':
                volume_controller.change_master_volume(recv_data_packet['volume'])

            case 'toggle_master_mute':
                volume_controller.toggle_master_mute()

            case 'toggle_mic_mute':
                volume_controller.toggle_input_mute()

            case "change_volume_input_sink":
                for sink_input in VolumeController.get_input_sinks():
                    if sink_input.sink_id == recv_data_packet["sink_id"]:
                        sink_input.change_volume(recv_data_packet["volume"])

            case "toggle_mute_input_sink":
                for sink_input in VolumeController.get_input_sinks():
                    if sink_input.sink_id == recv_data_packet["sink_id"]:
                        sink_input.toggle_mute()

            case "run_macro":
                for macro_ in macros:
                    if recv_data_packet["macro_id"] == macro_.macro_id:
                        macro_.execute()

        session.commit()
        session.close()


if __name__ == '__main__':
    main()
