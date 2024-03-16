host = ""

import time
import socket

def main():
    print("\n\n")
    print("-------------------------")
    print("Blender Render Cloud Node")
    print("-------------------------\n")
    host = input("host: ")
    host, port = host.split(":")
    # Connect every 1 s to the server
    while True:
        print("Connecting to server...")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Seperate host and port
            
            print("Host: ", host)
            print("Port: ", port)
            s.connect((host, int(port)))
            print("Connected to server")
            break
        except Exception as e:
            print("Failed to connect to server")
            print(e)
            time.sleep(1)
    
    while True:
        # Check in every 1 s if the server is still connected
        time.sleep(1)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Seperate host and port
            s.connect((host, int(port)))
            print("Server is connected")
        except Exception as e:
            print("Server is disconnected")
            print(e)
            s.close()
            break

if __name__ == '__main__':
    main()