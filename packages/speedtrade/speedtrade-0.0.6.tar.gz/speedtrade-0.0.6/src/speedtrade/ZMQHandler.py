import zmq
import json

from .CommandStructure import CommandStructure

class ZMQHandler:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.setsockopt(zmq.IDENTITY, b"PythonClient")
        self.socket.connect("tcp://127.0.0.1:65355")
        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)

    def send_command(self, source, destination, serialized_metadata, timeout=5000):
        self.socket.send_multipart([b"", source.encode(), destination.encode(), serialized_metadata.encode()])
        
        # Wait for a response with a specified timeout
        events = self.poller.poll(timeout)
        
        if events:
            # A message was received before the timeout
            msg = self.socket.recv_multipart(flags=zmq.NOBLOCK)
            print("Message received:", msg)
        else:
            # Timeout occurred
            print("Timeout occurred. No message received.")        

    def close(self):
        self.poller.unregister(self.socket)
        self.socket.setsockopt(zmq.LINGER, 0)  # Add this line to set the linger option to 0
        self.socket.close()
        self.context.term()
