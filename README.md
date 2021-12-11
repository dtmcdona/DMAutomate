# DMAutomate
Python program used to make and play macros.

Currently the system is mainly different sections and tools that will be combined later with a GUI.

The file "main.py" is currently connected to macrofilecontroller.py and macromenuview.py
These two scripts are responsible for recording of mouse/keyboard, playback of recordings, randomized playback, read/write of files, and editting.

Screenshare_client.py and screenshare_server.py are able to capture screenshot images and send to the client and return input.
1. The client recieves screenshots then creates a video from these screenshots.
2. The client records mouse/keyboard input and sends it back the server.
3. The server currently just prints the client input to the console for testing on 1 computer.
These two files have been tested with a Ubuntu and Windows 10 connected to a pinephone (pine64) running Manjero Phosh Linux.

The screenreader file is responsible for capturing relevent information on the screen.
Currently it can identify varius images on a screen and return the (x, y) coordinates.
It can also catalog objects by a given name and store for future use and return an array of all those objects on a screen.
I will be working more on this file a lot more in the future to expand its functionality.