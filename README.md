
# 2025_01_01_MegaMaskSignInHandshake_Python

Python package to create Ethereum MetaMask-compatible WebSocket connections from handshake.

### Guest User

I wanted to implement a guest system to make it easier to use, but it made the code unnecessarily complex.  
If you want to allow guests, create one server specifically for guests and another for regular users.
Then, use a script to add guests more easily to your Git claim repository.
The issue with guests is the duality of the problem: 
- you need the ability to kick users who harm the server.
- With guests, this becomes a more complicated situation to manage.

This tool should be in a KISS use.

### Handshake Process

- **User**: Connect to the server  
- **Server**: Send `SIGN:GUIDTOSIGN`  
- **User**: Sign it using [this tool](https://github.com/EloiStree/SignMetaMaskTextHere) or DIY
- **User**: Send `GUIDTOSIGN|PUBLICADDRESS|SIGNEDMESSAGE`  
- **Server**:  
  - Check the received signed message to extract and compare the address  
    - Close connection if there is an error
  - Check if ADDRESS is allowed on server.
    - Close connection if there is an error
  - Send `Hello (INDEX_INTEGER): PUBLICADDRESS` if the handshake succeeds  
  - Set the user as verified   

### Additional Notes for IID Servers

- Any message larger than 16 bytes will result in a server kick.  
- Any text sent after verification will also result in a server kick.  
