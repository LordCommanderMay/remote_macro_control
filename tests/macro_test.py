import json
import zmq
from volume_control import VolumeController
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from base import Base

context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect('tcp://localhost:5566')


def test_terminal_macro():
    packet = json.dumps(
        {"action": "run_macro",
         "macro_id": 2}
    )
    socket.send_string(packet)
    


test_terminal_macro()
