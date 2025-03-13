# PyPI: `import iidwshandshake`

__Under construction__

This tool provide code to connect as client to a Integer server of APIntIO.
Python for Raspberry PI server: [https://github.com/EloiStree/2025_01_01_HelloMetaMaskPushToIID](https://github.com/EloiStree/2025_01_01_HelloMetaMaskPushToIID)


This package provide an SHA256 and Ehtereum way to do it.  
(If you look at a Unity3D RSA way, you can go there:  
https://github.com/EloiStree/OpenUPM_WsClientIID.git  )


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




-------------------
# Archived

### Additional Notes for IID Servers

- Any message larger than 16 bytes will result in a server kick.  
- Any text sent after verification will also result in a server kick.  
- If you want hundred of users, you need to kick the one that don't read the manual.
- You need to keep track of bytes use for a index user /minute /hour /day /month
  - See https://github.com/EloiStree/2025_01_01_IndexSpamKicker/blob/main/README.md

### Not Guest User

I wanted to implement a guest system to make it easier to use, but it made the code unnecessarily complex.  
If you want to allow guests, create one server specifically for guests and another for regular users.
Then, use a script to add guests more easily to your Git claim repository.
The issue with guests is the duality of the problem: 
- you need the ability to kick users who harm the server.
- With guests, this becomes a more complicated situation to manage.

This tool should be in a KISS use.
