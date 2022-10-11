import json
import time

import _ctypes
import pyautogui
import zmq
import media_controls
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

    last_packet = None
    update_volume = True
    last_update = time.time()
    volume_controller = VolumeController()

    while True:
        # update macros
        macros = session.query(macro.Macro)

        # audio date updates --maybe refactor to static class
        if time.time() > last_update + .05:
            # only update audio controller ever .05 secs
            # volume_controller will throw c-shared errors if rebuilt every loop
            last_update = time.time()  # reset the time
            if update_volume:
                # update_volume is set to false when a change occurs to
                #  volume slider on the gui to prevent the gui from rebuilding.
                #  without this the gui will rebuild the slider every time the volume is changed
                # which causes the slider act strangely
                volume_controller = VolumeController()  # updates audio control data
                packet = volume_controller.get_volume_data_json()
                if packet != last_packet:
                    # only sends audio control data update if data is different from last cycle
                    socket.send_string(packet)  # sends audio data packet to gui
                    last_packet = packet  # replaces packet for boolean check
            update_volume = True  # resets update volume so updating can occur after a volume change

        # Message Actions
        try:  # try to recive message do not block if there is no message
            message = socket.recv(flags=zmq.NOBLOCK)
        except zmq.Again:
            message = None

        if message is not None: #if message is not emtpy do somthing!

            # (message)
            recv_data_packet = json.loads(message.decode("utf-8"))
            # print(recv_data_packet)
            # (recv_data_packet["action"])

            match recv_data_packet["action"]:
                case 'send_data':

                    # (volume_controller.output_muted)

                    packet = volume_controller.get_volume_data_json()
                    socket.send_string(packet)

                case 'change_master_volume':
                    try:
                        volume_controller.change_master_volume(recv_data_packet['volume']),
                    except _ctypes.COMError:
                        pass
                    except OSError:
                        pass
                    update_volume = False

                case 'toggle_master_mute':
                    volume_controller.toggle_master_mute()

                case 'toggle_mic_mute':
                    volume_controller.toggle_input_mute()

                case "change_app_volume":
                    for sink_input in volume_controller.get_app_volume_controllers():

                        if sink_input.app_id == recv_data_packet["appId"]:
                            sink_input.change_volume(recv_data_packet["volume"])

                case "toggle_app_mute":
                    for sink_input in volume_controller.get_app_volume_controllers():
                        if sink_input.app_id == recv_data_packet["app_id"]:
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

                case "media_actions":
                    media_controls.media_action(recv_data_packet["key"])

                case "touchpad":

                    x = recv_data_packet["x"]
                    y = recv_data_packet["y"]
                    pyautogui.move(x * 2, y * 2, _pause=False)

                case "left_click":
                    pyautogui.click()

        session.commit()
        session.close()


if __name__ == '__main__':
    main()
