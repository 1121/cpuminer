import socket
import time
import json
import struct

# Pool Configuration
POOL_URL = "https://www.viabtc.com/"  # Replace with the correct pool hostname
POOL_PORT = 3333  # Replace with the desired port (e.g., 3333, 25, or 443)
WORKER_NAME = "bznbnn.001"  # Replace with your worker name
PASSWORD = "123"  # Replace with your password

# Define Stratum version and protocol commands
STRATUM_VERSION = 0x00000001  # Protocol version
SUBSCRIBE_COMMAND = {
    "id": 1,
    "method": "mining.subscribe",
    "params": []
}

AUTHORIZE_COMMAND = {
    "id": 2,
    "method": "mining.authorize",
    "params": [WORKER_NAME, PASSWORD]
}

# Create a function to send and receive data via the TCP socket
def send_command(sock, command):
    """Send a command to the mining pool."""
    command_json = json.dumps(command) + "\n"
    sock.sendall(command_json.encode("utf-8"))

def receive_response(sock):
    """Receive the response from the mining pool."""
    response = sock.recv(1024).decode("utf-8")
    return response.strip()

# Main function to connect and communicate with the pool
def start_mining():
    """Connect to the pool and start mining."""
    try:
        # Create a TCP socket and connect to the pool
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((POOL_URL, POOL_PORT))

            print(f"[🌐] Connected to pool: {POOL_URL}:{POOL_PORT}")

            # Send the subscribe command to the pool
            send_command(s, SUBSCRIBE_COMMAND)
            response = receive_response(s)
            print(f"[✅] Subscribe response: {response}")

            # Send the authorize command to the pool
            send_command(s, AUTHORIZE_COMMAND)
            response = receive_response(s)
            print(f"[✅] Authorize response: {response}")

            # Start the mining loop (You can adjust this for your mining logic)
            while True:
                # For simplicity, just receive and print pool messages
                pool_message = receive_response(s)
                print(f"[⚙️] Pool message: {pool_message}")

                # Add your mining logic here (e.g., submitting work)
                # You can send "mining.submit" or other commands as per your protocol
                time.sleep(5)  # Simulate a delay (adjust as necessary)

    except Exception as e:
        print(f"[❌] Error: {e}")

if __name__ == "__main__":
    start_mining()
