from volume_control import SinkInputs
import json


def create_packet(input_sink_link: list[SinkInputs]) -> bytes:
    packet = {
        "action": 'sent_data',
        "data": []
    }
    for sink_input in input_sink_link:
        packet['data'].append(sink_input.to_dict())

    return bytes(json.dumps(packet), 'utf-8')


