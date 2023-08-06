import socket
from .const import COMMANDS

class ZankControlClient:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port

    def send_command(self, command):
        if command not in COMMANDS:
            raise ValueError(f"Invalid command: {command}")

        udp_message = COMMANDS[command].encode('utf-8')
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(udp_message, (self.ip_address, self.port))
        sock.close()