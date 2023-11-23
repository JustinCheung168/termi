# termi
Use your personal computer's keyboard and mouse to manipulate another computer's keyboard and mouse.


## Usage

Install Python3 on both computers, and then install Python dependencies using `python3 -m pip install -r requirements.txt`.

Specify this server's host and a fairly high port number in `config.yaml`.

Launch `/.server.py` on the computer to control.

Then run `./client.py` on the computer whose keyboard and mouse you are using.

You can exit the session using Cmd+Q. The server will continue to run and will be prepared to accept another client connection.

Only tested using Mac personal computer + Linux remote computer. Not designed or tested for another setup yet.
