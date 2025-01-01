
# 2025_01_01_MegaMaskSignInHandshake_Python

**Python package to create Ethereum MetaMask-compatible WebSocket connections from handshake.**

### Handshake Process

- **User**: Connect to the server  
- **Server**: Send `SIGN:GUIDTOSIGN`  
- **User**: Sign it using [this tool](https://github.com/EloiStree/SignMetaMaskTextHere) or DIY
- **User**: Send `SIGNED:GUIDTOSIGN|PUBLICADDRESS|SIGNEDMESSAGE`  
- **Server**:  
  - Check the received signed message to extract and compare the address  
  - Close connection if there is an error  
  - Send `Hello PUBLICADDRESS` if the handshake succeeds  
  - Set the user as verified  
  - Check allowed users  
  - If guests are not allowed and the user is not registered, they are kicked  

### Additional Notes for IID Servers

- Any message larger than 16 bytes will result in a server kick.  
- Any text sent after verification will also result in a server kick.  
