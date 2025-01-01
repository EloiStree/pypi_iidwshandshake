# 2025_01_01_MegaMaskSignInHandshake_Python
Python package to create Ethereum MetaMask-compatible WebSocket connections from handshake.




User: Connect to the server
Server: Send "SIGN:GUIDTOSIGN"
User: Sign it https://github.com/EloiStree/SignMetaMaskTextHere
User: Send "SIGNED:GUIDTOSIGN|PUBLICADDRESS|SIGNEDMESSAGE
Server: Check the received signed message to extract and compare address
Server: Close connection if error
Server: Send "Hello PUBLICADDRESS" if succed to handshake
Server: Set user as verified
Server: Check allowed user
Server: if guest not allowed ad not a user, user kicked


If server is an IID one:
- any bytes more that 16 bytes lead to a kick of the server
- any text after been verified lead to a kick of the server
  
