import asyncio
import random
import websockets

# pip install web3
from web3 import Web3
import os
from eth_account.messages import encode_defunct
import uuid
import time
import struct
import threading


ntp_server = "time.google.com"
def get_ntp_time():
    import ntplib
    from time import ctime
    c = ntplib.NTPClient()
    response = c.request(ntp_server, version=3)
    return response.tx_time
def get_ntp_time_from_local():
    global millisecond_diff
    return time.time()*1000+millisecond_diff
ntp_timestmap = get_ntp_time()*1000
local_timestamp = time.time()*1000
millisecond_diff = ntp_timestmap-local_timestamp
print(f"ntp_timestmap: {ntp_timestmap}")
print(f"local_timestamp: {local_timestamp}")
print(f"diff: {millisecond_diff}")




# Generate a random private key
# private_key = os.urandom(32).hex()

# https://eloistree.github.io/apint.io/js/get/create_metamask_wallet.html
private_key = "0xdf2541a2a722be6211bacfd1f8b15993445914ac8b75b419664c544c7e27323e"
public_address = ""

# Print the private key
print(f"Private Key: {private_key}")

# Create a Web3 instance
w3 = Web3()

# Generate the corresponding public address
account = w3.eth.account.from_key(private_key)
public_address = account.address
print(f"Public Address: {account.address}")

def sign_message(private_key, to_sign):
    m = to_sign
    message_hash = w3.keccak(text=m)
    m = encode_defunct(text=m)
    signed_message = w3.eth.account.sign_message(m, private_key=private_key)
    # Print the signed message
    print(f"Signed Message: {signed_message.signature.hex()}")
    MESSAGE = to_sign
    PUBLIC_ADDRESS = account.address
    SIGNED_MESSAGE = signed_message.signature.hex()
    CLIPBOARDABLE_FORMAT = f"{MESSAGE}|{PUBLIC_ADDRESS}|{SIGNED_MESSAGE}"
    return CLIPBOARDABLE_FORMAT

target_server_websocket=None
given_index_by_server=0


# async def handle_byte_received(bytes_received):
#     global target_server_websocket
#     lenght = len(bytes_received)
#     if lenght ==4:
#         integer= struct.unpack("<i", bytes_received)[0]
#         print(f"Received I: {integer}")
#     elif lenght ==8:
#         index, integer= struct.unpack("<ii", bytes_received)[0]
#         print(f"Received II: {index} {integer}")
#     elif lenght ==12:
#         integer, date= struct.unpack("<iQ", bytes_received)[0]
#         print(f"Received ID: {integer} {date}")
#     elif lenght ==16:
#         index, integer,date= struct.unpack("<iiQ", bytes_received)[0]
#         print(f"Received IID: {index} {integer} {date}")
#     else:
#         print(f"Not IID: {bytes_received}")
            


async def loop_console_send():
    global target_server_websocket
    while True:
        bool_use_console=False
        if bool_use_console:
            message = input("Enter a message to send to the server: ")
            try:
                integer= int(message)
                
                print(f"Sent to server integer: {message}")
                bytes_to_send = struct.pack("<i", integer)
                await target_server_websocket.send(bytes_to_send)
            except:
                continue
        else :
            time.sleep(1)
            random_value= random.randint(0, 100)
            print(f"Sent to server integer: {random_value}")
            bytes_to_send = struct.pack("<i", random_value)
            await target_server_websocket.send(bytes_to_send)

async def connect_to_server():
    global given_index_by_server
    uri = "ws://193.150.14.47:4615"
    async with websockets.connect(uri) as websocket:
        global target_server_websocket
        target_server_websocket=websocket
        bool_is_sign_received=False
        bool_is_hello_received=False
                
        print("Connected to the server")
        while True:
            response = await websocket.recv()
            response = response.strip()
            print (f"Received from server: {response}")
            if not bool_is_sign_received and response.startswith("SIGN:"):
                bool_is_sign_received=True
                to_sign = response[5:]
                print(f"To sign: {to_sign}")
                signed_message = sign_message(private_key, to_sign)
                print(f"Sent Clipboard: {signed_message}")
                await websocket.send(signed_message)
            elif not bool_is_hello_received and response.startswith("HELLO "):
                bool_is_hello_received=True           
                split_response = response.split(" ")
                if len(split_response) == 3:
                    user_index=split_response[1]
                    public_address = split_response[2]
                    given_index_by_server=int(user_index)
                    print (f"Server connected as user {user_index} with public address {public_address}")
                    
            # else:
            #     handle_byte_received(response)
                    
            
            
            # message = input("Enter a message to send to the server: ")
            # await websocket.send(message)
            # response = await websocket.recv()
            # print(f"Received from server: {response}")
            


import traceback

    
def connect_to_server_thread():
    while True:
        try:
            asyncio.run(connect_to_server())
        except Exception as e:
            print(f"Error: {e}\n")
            traceback.print_exc()  # Prints the full stack trace
        print("Waiting 5 seconds to reconnect")
        time.sleep(5)

def loop_console_send_thread():
    while True:
        
        asyncio.run(loop_console_send())
        print("Waiting 5 seconds to reconnect")
        time.sleep(5)

if __name__ == "__main__":
    # Create threads
    thread1 = threading.Thread(target=connect_to_server_thread)
    thread2 = threading.Thread(target=loop_console_send_thread)
    
    # Start threads
    thread1.start()
    thread2.start()
    
    # Wait for threads to complete (optional; keeps main program alive)
    thread1.join()
    thread2.join()
