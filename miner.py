import json
import socket
import subprocess
import hashlib

# Mining pool details
POOL_URL = "stratum+tcp://btc.viabtc.io:3333"
USERNAME = "bznbnn.001"
PASSWORD = "123"
PAYOUT_ADDRESS = "bc1qsf5hfv7hd3jw22lzdwc7pm9yuru5trw8xd9h2f"

# Initialize Stratum connection
def create_stratum_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("btc.viabtc.io", 3333))
    return s

def send_json_rpc_request(s, method, params):
    req = json.dumps({
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }) + "\n"
    s.send(req.encode())

def handle_job(job):
    # This is where the job is parsed
    # Start miner with the job data
    # Example: running cpuminer with the job parameters
    miner_cmd = [
        "cpuminer", 
        "-o", POOL_URL, 
        "-u", USERNAME, 
        "-p", PASSWORD,
        "--coin", "btc"
    ]
    process = subprocess.Popen(miner_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    print(out.decode())

def main():
    # Establish Stratum connection
    s = create_stratum_connection()

    # Authenticate
    send_json_rpc_request(s, "mining.subscribe", [])
    send_json_rpc_request(s, "mining.authorize", [USERNAME, PASSWORD])

    while True:
        # Receive and handle mining jobs
        data = s.recv(1024).decode('utf-8')
        if data:
            job = json.loads(data)
            print("Received job:", job)
            handle_job(job)

if __name__ == "__main__":
    main()
