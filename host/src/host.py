"""
Blender Render Cloud - Host
(C) 2024 - EinsMalte on GitHub
"""

version: str = "0.0.1" # Version of the program
terminal_width: int = 80 # Width of the terminal for formatting
artificial_delay: float = 0 # Makes the program wait to make it seem like it's doing something

print("Blender Render Cloud - Host".center(terminal_width))
print(f"Version: {version}".center(terminal_width))
print("-" * terminal_width)

# Import required modules
import random
import netifaces
import socket
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import os
import webbrowser


"""
GET IP ADDRESSES

Get all IP addresses and broadcast addresses of the host for maximum compatibility (IPv4 only, but let marketing worry about that)
"""
def get_ip_addresses():
    ip_addresses = []
    broadcast_addresses = []

    # Get all network interfaces
    for interface in netifaces.interfaces():
        # Get all addresses for the current interface
        for link in netifaces.ifaddresses(interface).get(netifaces.AF_INET, []):
            # Add the IP and broadcast addresses to the respective lists
            ip_addresses.append(link['addr'])
            broadcast_addresses.append(link['broadcast'])

    return ip_addresses, broadcast_addresses
def sendBroadcast(addresses: list, port: int, message: str):
    for address in addresses:
        # Create a UDP socket
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Set the socket to broadcast mode
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            # Send the message to the broadcast address
            s.sendto(message.encode(), (address, port))

print("\rStatus: Getting IP addresses...".ljust(terminal_width), end="")
ip_addresses, broadcast_addresses = get_ip_addresses()
print("\rStatus: Getting IP addresses... (complete)".ljust(terminal_width), end="")
time.sleep(artificial_delay)


"""
FRONTEND SERVER

The GUI of the host because I am too lazy to make a GUI in Python
"""

nodes: int = 0 # Number of nodes connected to the host
class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/nodeCount':
            nodes = random.randint(0, 10)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(str(nodes).encode())
        elif self.path == '/queueSize':
            queue = random.randint(0, 10)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(str(queue).encode())
        elif self.path == '/jobPercentage':
            percentage = random.randint(0, 100)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(str(percentage).encode())
        else:
            super().do_GET()

def start_server(ip, port):
    server_address = (ip, port)
    httpd = HTTPServer(server_address, CustomHTTPRequestHandler)
    httpd.serve_forever()

print("\rStatus: Starting frontend server...".ljust(terminal_width), end="")
# Define the directory to be served
web_dir = os.path.join(os.path.dirname(__file__), 'front')
os.chdir(web_dir)

# Start a new server for each IP address
for ip in ip_addresses:
    threading.Thread(target=start_server, args=(ip, 8000)).start()

print("\rStatus: Starting frontend server... (complete)".ljust(terminal_width), end="")
webbrowser.open("http://localhost:8000") # Open the browser to the frontend
time.sleep(artificial_delay)

time.sleep(600) # Wait for 10 minutes before closing the program
