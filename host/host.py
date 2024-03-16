# Blender Render Cloud host
# (c) 2024 EinsMalte

# Features:
# - Send .blend files to nodes (clients)
# - Receive rendered images from nodes
# - Receive node status updates
# - Manage nodes
# - interact with user via cli

# Import ../global/dashbord.py
import sys
import time
sys.path.append('common/')
import dashboard
import socket
import http.server
import socketserver
import threading

# Greet the user
print("\n"*3)
print("--------------------")
print("Blender Render Cloud")
print("--------------------\n")

dashboard.printOut()
dashboard.title = "Render Cloud Host"
dashboard.addLine("Status", "Initializing...")

getRequests: int = 0
postRequests: int = 0

# Initialize the host
# Get the host's IP
host_ip = socket.gethostbyname(socket.gethostname())

# Add the host IP to the dashboard
dashboard.addLine("IP", host_ip)

port = 8080
dashboard.changeValue("Status", "Starting server on port " + str(port))

class CustomHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global getRequests
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'GET request received')
        getRequests += 1
        dashboard.changeValue("- GET Requests", getRequests)

    def do_POST(self):
        global postRequests
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'- POST request received')
        postRequests += 1
        dashboard.changeValue("- POST Requests", postRequests)

# Start the HTTP server with the custom handler
portAvailable = False
startAvailibility = time.time()
while not portAvailable:
    try:
        CustomHandler.log_message = lambda *args: None
        httpd = socketserver.TCPServer(("", port), CustomHandler)
        portAvailable = True
    except OSError:
        dashboard.changeValue("Status", f"Port already in use...({time.time() - startAvailibility:.0f} s)")
        time.sleep(1)

# Get the host's hostname and port
hostname = socket.gethostname()
# Turn the hostname into an IP (currently is the name of device)
hostname = socket.gethostbyname(hostname)
host_ip = f"{hostname}:{port}"

# Update the IP value in the dashboard
dashboard.changeValue("IP", host_ip)

# Start the server
dashboard.changeValue("Status", f"Starting server on {host_ip}")
dashboard.addLine("Server", "")
dashboard.addLine("- GET Requests", "0")
dashboard.addLine("- POST Requests", "0")


# Start the server in a new thread
def startServer():
    httpd.serve_forever()

serverThread = threading.Thread(target=startServer)
serverThread.start()

dashboard.changeValue("Status", "Ready")

