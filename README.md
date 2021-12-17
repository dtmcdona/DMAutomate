<center><h1> DMAutomate </h1>
<b> by David McDonald </b></center>
<br>

This repo is a collection of Python programs used to:
1. Record, play, edit, and randomize macros
2. Share your screen with another computer
3. Locate images/text on in an image or screenshot
4. Read and store screen information

Currently the system is mainly different sections and tools that will be combined later with a GUI.

The file "main.py" is currently connected to macrofilecontroller.py and macromenuview.py
These two scripts are responsible for recording of mouse/keyboard, playback of recordings, randomized playback, read/write of files, and editting.

Screenshare_client.py and screenshare_server.py are able to capture screenshot images and send to the client and return input.
<b> Current features: </b>
1. The client recieves screenshots then creates a video from these screenshots.
2. The client records mouse/keyboard input and sends it back the server.
3. The server currently just prints the client input to the console for testing on 1 computer.
These two files have been tested with a Ubuntu and Windows 10 connected to a pinephone (pine64) running Manjero Phosh Linux.

The screenreader file is responsible for capturing relevent information on the screen.
<br>
<b> Current features: </b>
1. Identifies various images on a screen and returns the (x, y) coordinates.
2. Catalog objects by a given name and store for future use and return an array of all those objects on a screen.
3. Reads text on the screen and store them in arrays via reflection algorythm opposed to an injection algorythm. 
4. Combining each char of text on an image to form groupings based on proximity to other characters.
This new features can be used to decode the current status of the progression of a macro or script after a given action.

<b>Note:</b>
I will be working more on screenreader.py a lot more in the future to expand its functionality.