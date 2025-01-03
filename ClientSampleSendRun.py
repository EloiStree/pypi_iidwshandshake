import asyncio
import random
import os
import time
import struct
import threading
from web3 import Web3
from eth_account.messages import encode_defunct

import tornado.ioloop
import tornado.web
import tornado.websocket
import asyncio
import websockets






######## NTP 3 START ########
ntp_server = "time.google.com"
salt = "CHANGE_BY_RANDOM_PHRASE_YOUR_LIKE"
server_url = "ws://193.150.14.47:4615"

# Will add file read
tornado_tunnel = None
display_private_key = False

import hashlib

def generate_private_key_from_file(file_path, salt):
    try:
        # Read the file in binary mode
        with open(file_path, 'rb') as file:
            file_data = file.read()
        file_data += salt.encode()
        
        # Hash the file data using SHA-256
        hash_object = hashlib.sha256(file_data)
        private_key = hash_object.hexdigest()
        
        # Verify the private key range (optional but recommended)
        private_key_int = int(private_key, 16)
        if not (1 <= private_key_int < 2**256):
            raise ValueError("Generated private key is out of range!")
        
        return private_key
    except FileNotFoundError:
        return "Error: File not found!"
    except Exception as e:
        return f"Error: {e}"

def generate_private_key_from_computer_id(salt):
    import uuid
    computer_id = uuid.getnode()
    print (f"Computer ID: {computer_id}+{salt}")
    private_key = hashlib.sha256(str(computer_id).encode()).hexdigest()
    return private_key



file_path_absolute = "C:/PrivateKey.jpg"
file_path_relative = "PrivateKey.jpg"
file_path=""
if os.path.exists(file_path_absolute):
    private_key = generate_private_key_from_file(file_path_absolute, salt)
elif os.path.exists(file_path_relative):
    private_key = generate_private_key_from_file(file_path_relative, salt)
else:
   private_key = generate_private_key_from_computer_id( salt)
    
## private_key = generate_private_key_from_computer_id( salt)


def get_ntp_time():
    import ntplib
    c = ntplib.NTPClient()
    response = c.request(ntp_server, version=3)
    return response.tx_time

def get_ntp_time_from_local():
    global millisecond_diff
    return time.time() * 1000 + millisecond_diff

ntp_timestmap = get_ntp_time() * 1000
local_timestamp = time.time() * 1000
millisecond_diff = ntp_timestmap - local_timestamp
print(f"ntp_timestmap: {ntp_timestmap}")
print(f"local_timestamp: {local_timestamp}")
print(f"diff: {millisecond_diff}")
######## NTP 3 END ########



######## WEB 3 START ########
public_address = ""


if display_private_key:
    print(f"Private Key: {private_key}")
else:
    print(f"Private Key: {private_key[:4]}...")

w3 = Web3()

account = w3.eth.account.from_key(private_key)
public_address = account.address
print(f"Public Address: {account.address}")

def sign_message(private_key, to_sign):
    m = to_sign
    message_hash = w3.keccak(text=m)
    m = encode_defunct(text=m)
    signed_message = w3.eth.account.sign_message(m, private_key=private_key)
    print(f"Signed Message: {signed_message.signature.hex()}")
    MESSAGE = to_sign
    PUBLIC_ADDRESS = account.address
    SIGNED_MESSAGE = signed_message.signature.hex()
    CLIPBOARDABLE_FORMAT = f"{MESSAGE}|{PUBLIC_ADDRESS}|{SIGNED_MESSAGE}"
    return CLIPBOARDABLE_FORMAT





class AbstractHandShake:
    def __init__(self):    
        self.received_guid=None
        self.signed_guid_sent=None
        self.received_verified_validation = False
        self.public_address_used = None
        self.integer_index_on_server = None
        
    def is_waiting_for_guid(self):
        return self.received_guid is None
    
    def is_waiting_for_validation(self):
        return self.received_guid is not None and self.received_verified_validation is False
    
    def has_sent_signed_guid(self):
        return self.signed_guid_sent is not None
    
    
import tornado.ioloop
import tornado.websocket
import tornado.gen
import time

class ReconnectingWebSocketClient:
    def __init__(self, url):
        self.url = url
        self.ws = None
        self.is_closing = False
        self.public_address = None
        self.integer_index_on_server = None
        self.connected_to_server = False
        self.is_validated = False
        self.bytes_queue = asyncio.Queue()
        self.text_queue = asyncio.Queue()

    def get_public_address(self):
        return self.public_address if self.public_address else ""

    def get_integer_index_on_server(self):
        return self.integer_index_on_server if self.integer_index_on_server else 0

    def is_server_validated_connection(self):
        return self.is_validated 

    def is_connected_to_server(self):
        return self.connected_to_server

    def _reset_connection_state(self):
        self.public_address = None
        self.integer_index_on_server = None
        self.is_validated = False
        self.connected_to_server = False
        
        
    
        
    @tornado.gen.coroutine
    def loop_on_queue(self):
        while True:
            if not self.bytes_queue.empty():
                bytes_message = yield self.bytes_queue.get()
                self.send_bytes_message(bytes_message, protect=False)
            if not self.text_queue.empty():
                text_message = yield self.text_queue.get()
                self.send_text_message(text_message, protect=False)
            yield tornado.gen.sleep(1)

    @tornado.gen.coroutine
    def connect(self):
        while True:  # Keep trying to reconnect forever
            if self.is_closing:
                break
            try:
                print(f"Attempting to connect to {self.url}")
                self.ws = yield tornado.websocket.websocket_connect(self.url)
                self.connected_to_server = True
                print("Connected successfully!")
                yield self.listen()
            except Exception as e:
                self._reset_connection_state()
                print(f"Connection error: {e}")
                print("Reconnecting in 5 seconds...")
                yield tornado.gen.sleep(5)

    @tornado.gen.coroutine
    def listen(self):
        try:
            while not self.is_closing:
                msg = yield self.ws.read_message()
                if msg is None:
                    print("Connection closed by server.")
                    self._reset_connection_state()
                    break
                
                if not self.is_validated:
                    print(f"V: {msg}")
                    if msg.startswith("SIGN:"):
                        to_sign = msg[5:]
                        print(f"To sign: {to_sign}")
                        signed_message = sign_message(private_key, to_sign)
                        print(f"Sent message: {signed_message}")
                        self.send_text_message(signed_message,False)
                        
                    elif msg.startswith("HELLO "):
                        split_response = msg.split(" ")
                        self.is_validated = True
                        if len(split_response) == 3:
                            user_index = split_response[1]
                            public_address = split_response[2]
                            self.integer_index_on_server = int(user_index)
                            self.public_address = public_address
                            print(f"Connected as user {user_index} with public address {public_address}")
                else: 
                    print(f"R: {msg}")
                        
        except Exception as e:
            print(f"Error while listening: {e}")
        self._reset_connection_state()

    def send_text_message(self, message, protect=True):
        if protect==False or (self.is_connected_to_server() and self.is_server_validated_connection()):
            if self.ws:
                try:
                    self.ws.write_message(message)
                    print(f"Sent message: {message}")
                except Exception as e:
                    print(f"Error sending message: {e}")
            else:
                print("Cannot send message, no active connection.")
            
    def send_bytes_message(self, message, protect=True):
        if protect==False or (self.is_connected_to_server() and self.is_server_validated_connection()):
            if self.ws:
                try:
                    self.ws.write_message(message, binary=True)
                    print(f"Sent bytes: {message}")
                except Exception as e:
                    print(f"Error sending bytes: {e}")
            else:
                print("Cannot send bytes, no active connection.")

    def close(self):
        self.is_closing = True
        if self.ws:
            self.ws.close()
        print("WebSocket connection closed.")



import socket
import struct
import time
import random
import threading
import sys


def start_testing(client : ReconnectingWebSocketClient):
    asyncio.set_event_loop(asyncio.new_event_loop())
    while True:
        time.sleep(1)
        if client is not None:
            int_random = random.randint(0, 100)
            print(f"Random: {int_random}")
            bytes = struct.pack("<i", int_random)
            if client.is_connected_to_server() and client.is_server_validated_connection():
                client.send_bytes_message(bytes)
                    
def thread_your_code_here_loop(client : ReconnectingWebSocketClient):
    thread = threading.Thread(target=start_testing, args=(client,))
    thread.daemon = True
    thread.start()
    return thread
        


def start_udp_server_text(client : ReconnectingWebSocketClient, ip_mask="127.0.0.1", lisent_port=3614):
        asyncio.set_event_loop(asyncio.new_event_loop())
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind((ip_mask, lisent_port))
            print(f"UDP Server started on {ip_mask}:{lisent_port}")
            while True:
                data, addr = s.recvfrom(1024)
                print(f"Received from {addr}: {data}")
                text = data.decode("utf-8")
                client.send_text_message(text)
        except Exception as e:
            print(f"Error starting UDP server: {e}")
            sys.exit(1)
def udp_listener_server_udp_text(client : ReconnectingWebSocketClient, ip_mask="127.0.0.1", lisent_port=3614):
    thread = threading.Thread(target=start_udp_server_text, args=(client,ip_mask,lisent_port))
    thread.daemon = True
    thread.start()
    return thread


def start_udp_server_byte(client : ReconnectingWebSocketClient, ip_mask="127.0.0.1", lisent_port=3615):
        asyncio.set_event_loop(asyncio.new_event_loop())
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind((ip_mask, lisent_port))
            print(f"UDP Server started on {ip_mask}:{lisent_port}")
            while True:
                data, addr = s.recvfrom(1024)
                print(f"Received from {addr}: {data}")
                l= len(data)
                if l==4:
                    int_value = struct.unpack("<i", data)[0]
                    bytes= struct.pack("<iQ", int_value, get_ntp_time_from_local())
                    client.send_bytes_message(bytes)
                elif l==8:
                    index,value= struct.unpack("<ii", data)
                    bytes= struct.pack("<iiQ", index, value, get_ntp_time_from_local())
                    client.send_bytes_message(bytes)
                else :
                    client.send_bytes_message(data)
        except Exception as e:
            print(f"Error starting UDP server: {e}")
            sys.exit(1)
def udp_listener_server_udp_byte(client : ReconnectingWebSocketClient, ip_mask="127.0.0.1", lisent_port=3615):
    thread = threading.Thread(target=start_udp_server_byte, args=(client,ip_mask,lisent_port))
    thread.daemon = True
    thread.start()
    return thread


if __name__ == "__main__":
    client = ReconnectingWebSocketClient(server_url)
    udp_listener_server_udp_byte(client)
    udp_listener_server_udp_text(client)
    # thread_your_code_here_loop(client)
    

    def start_client():
        tornado.ioloop.IOLoop.current().run_sync(client.connect)

    try:
        start_client()
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Closing WebSocket client.")
        client.close()
        tornado.ioloop.IOLoop.current().stop()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# ######## WEB 3 STOP ########
# class WebSocketClient:
#     def __init__(self, url):
#         self.url = url
#         self.ws = None
#         self.is_broken=False
#         self.is_verified=False
#         self.address = None
#         self.index = None

#     @tornado.gen.coroutine
#     def connect(self):
#         global global_client, global_client_verified, ioloop
#         try:
#             global_client_verified = False
#             global_client = self
            
#             self.ws = yield tornado.websocket.websocket_connect(self.url)
#             print(f"Connected to {self.url}")
#             self.read_messages()
#         except Exception as e:
#             print(f"Connection error: {e}")
#             global_client_verified = False
#             global_client = None
#             ioloop = None

#     @tornado.gen.coroutine
#     def read_messages(self):
#         while True:
#             try:
#                 msg = yield self.ws.read_message()
#                 if msg is None:
#                     print("Connection closed")
#                     self.is_broken = True
#                     break
#                 print(f"Received: {msg}")
                
#                 if msg.startswith("SIGN:"):
#                     to_sign = msg[5:]
#                     print(f"To sign: {to_sign}")
#                     signed_message = sign_message(private_key, to_sign)
#                     print(f"Sent Clipboard: {signed_message}")
#                     self.send_message(signed_message)
#                 elif msg.startswith("HELLO "):
#                     self.is_verified = True
#                     split_response = msg.split(" ")
#                     if len(split_response) == 3:
#                         user_index = split_response[1]
#                         public_address = split_response[2]
#                         self.address = public_address
#                         given_index_by_server = int(user_index)
#                         self.index = given_index_by_server
#                         print(f"Server connected as user {user_index} with public address {public_address}")
                    
#             except Exception as e:
#                 print(f"Error while reading message: {e}")
#                 break

  

#     @tornado.gen.coroutine
#     def send_message(self, message):
#         try:
#             self.ws.write_message(message)
#             print(f"Sent: {message}")
#         except Exception as e:
#             print(f"Error sending message: {e}")

#     @tornado.gen.coroutine
#     def send_bytes(self, message):
#         try:
#             self.ws.write_message(message, binary=True)
#             print(f"Sent: {message}")
#         except Exception as e:
#             print(f"Error sending message: {e}")
            
            
        
# import tornado.ioloop

# class TornadoTunnel:
#     def __init__(self, url):
#         self.url = url
#         self.client = None
#         self.ioloop = None

#     def stop_thread_and_restart(self):
#         try:
#             self._stop_ioloop()
#             self._reset_client()
#             self.ioloop = tornado.ioloop.IOLoop.current()
#             self.client = WebSocketClient(self.url)
#             self.ioloop.run_sync(self.client.connect)
#             print("Ready to start")
#             self.ioloop.start()
#             print("End")
#         except Exception as e:
#             print(f"Connection error: {e}")
#             self._reset_client()
#             self._stop_ioloop()

#     def kill(self):
       
#         if self.ioloop:
#             self.ioloop.stop()
#             self.ioloop.close(all_fds=True)
#             self.ioloop = None
        
#         print("Kill Client")
#         if self.client:
#             self.client.is_broken = True
#             self.client.ws.close()
#             self.client = None
#         print("Kill ioLoop")
#         self._stop_ioloop()
#         print("Kill End")

#     def _stop_ioloop(self):
#         if self.ioloop:
#             self.ioloop.stop()
#             self.ioloop = None

#     def _reset_client(self):
#         self.client = None


#     def is_alive(self):
#         return not self.client.is_broken

#     def is_verified(self):
#         return self.client.is_verified

#     def get_address(self):
#         return self.client.address

#     def get_index(self):
#         return self.client.index

#     def send_message(self, message):
#         if self.client is not None:
#             self.ioloop.add_callback(self.client.send_message, message)

#     def send_bytes(self, message):
#         if self.client is not None:
#             self.ioloop.add_callback(self.client.send_bytes, message)

  
#     def is_ok(self):
#         return self.client is not None and not self.client.is_broken and self.client.is_verified

#     def is_not_ok(self):
#         return not self.is_ok()
    
#     def is_broken(self):
#         return self.client is None or self.client.is_broken is None or self.client.is_broken
   
    


    
# def push_to_server_for_testing():
#     while True:
#         global tornado_tunnel
#         time.sleep(1)
#         print("Ping")
#         if tornado_tunnel is not None:
#             print("Pong")
#             if tornado_tunnel.is_ok():
#                 print("Pouff")
#                 bytes = struct.pack("<i", random.randint(0, 100))
#                 tornado_tunnel.send_bytes(bytes)
#                 print("Is Ok")
#                 time.sleep(1)


# def thread_keep_pusher_alive():
#     print("THREAD KEEP PUSH ALIVE")
#     while True:
#         push_to_server_for_testing()
        
# def thread_keep_tunnel_alive():
#     print("THREAD KEEP TUNNEL ALIVE")
#     global tornado_tunnel
#     while True:
#         time.sleep(1)
#         if tornado_tunnel is None:
#             print("A")
#             tornado_tunnel = TornadoTunnel(server_url)
#             tornado_tunnel.stop_thread_and_restart()
#             print("B")
#         print("Bou")


# def restart_tunnel_when_broken():
#     global tornado_tunnel
#     while True:
#         time.sleep(1)
#         if tornado_tunnel is not None:
#             if tornado_tunnel.is_broken():
#                 print ("Kill Call")
#                 tornado_tunnel.kill()
#                 tornado_tunnel = None
        

# print("Yo")
# if __name__ == "__main__":
#     thread1 = threading.Thread(target=thread_keep_tunnel_alive) 
#     thread2 = threading.Thread(target=thread_keep_pusher_alive)
#     thread3 = threading.Thread(target=restart_tunnel_when_broken)
#     thread1.start()
#     thread2.start()
#     thread3.start()
#     thread1.join()
#     thread2.join()
#     thread3.join()
        
    
#     while True:
#         time.sleep(1)
#         print(".")
  


