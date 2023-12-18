FTP PROJECT 

Done by Carl Nakad (40210586), Ruaid Usmani (40212428)

How to run it: 
- Open the project with three folders in the workspace:
    - Client Folder that contain client program and some files
    - Server Folder that contains server program and no files
    - Controller that contains the control modules

- Have two terminals running. 
    -- Terminal 1 should cd into Server
    -- Terminal 2 should cd into Client

- Run the python code in each terminal with file name and debug flag
    -- Terminal 1: python server.py [Debug Flag] (ON = 1 and OFF = 0)
    -- Terminal 2: python client.py [Debug Flag] (ON = 1 and OFF = 0)
    Note: on Mac, you need to write python3 instead of python. 
    Note: Use updated Python. Preferabbly Python 3.12

- On client side, put files to transfer. You would already have some on client 
    - lol.txt : text file
    - lmao.doc : text file in .doc
    - test.jpg : picture file
    
- Run program as directed

Test cases:
1)
    - run program on TCP with debug flag ON 
    - help 
    - put lol.txt
    - put lmao.doc
    - summary lol.txt
    - change lol.txt lol2.txt
    - get lol2.txt
    - bye
2)
    - rerun program on UDP with debug flag OFF
    - put test.jpg
    - change test.jpg test2.jpg
    - get test2.jpg
    - bye
