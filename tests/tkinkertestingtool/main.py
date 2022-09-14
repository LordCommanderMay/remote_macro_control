import tkinter as tk

import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:5566")

def mute_output():
	    packet = json.dumps({"action" : "toggle_master_mute"})
	    socket.send_string(packet)
	    

app = tk.Tk()

tk.Button(text="mute output", command=mute_output).pack(expand=True, fill='both')

tk.Button(text="vol +", command=print).pack(expand=True, fill='both')

tk.Button(text="vol -", command=print).pack(expand=True, fill='both')

tk.Button(text="mute input", command=print).pack(expand=True, fill='both')

tk.Button(text="vol +", command=print).pack(expand=True, fill='both')

tk.Button(text="vol -", command=print).pack(expand=True, fill='both')

text = tk.Text()
text.pack()
tk.Button(text="run macro").pack(expand=True, fill='both')

def run_macro():
	macro_id = int(text.get("1.0", "end-1c"))
	packet = json.dumps({"action" : "run_macro",
	"macro_id" : macro_id})
	socket.send_string(packet)
	
tk.Button(text="run macro", command=run_macro).pack(expand=True, fill='both')	

while 1:
	app.update()

