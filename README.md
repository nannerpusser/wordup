*Update: Completely reworked app and added word value as filterable treeview display. Of course tile values are not constants all the time and although there are base values, conditions and multipliers apply on a per-game basis. So value is approximate until I actually implement OCR for input automation and can pull values off each tile in real-time. Use app.py for now even if it isn't very pretty yet. It works better and I am updating the UI soon.*

*Also update: Have compiled this into a single executable, but because PyInstaller/AutoPy2Exe are the way they are and compression isn't an option, the filesize is ~30MB. Above allowable GitHub upload size for a single file, so it's on a public Drive until I figure out what I wanna do to shrink it or whatever. If you really want it, msg me and I'll provide the link.*


## Wordament Solver App with GUI
Description:

This Wordament Solver app allows users to input a 4x4 board of letters and find valid words from the board based on a provided dictionary. The dictionary is the standard OSPD Scrabble dictionary, commonly found as ``twl06.txt``. This means you will encounter invalid words at times since Wordament has an internal dictionary that is nearly identical, but not quite. If you can get Microsoft to share their dictionary, I thank you in advance.

Features:
- Cross-platform (Linux and Windows). No DPI awareness on linux and depending on your WM, complete disregard for window size constraints. 
- Input a 4x4 board of letters as they appear on the tile.
- Handles all special tiles: double-letters aka. digrams, either/or tiles, prefix and suffix tiles of each type (**- and ***-, or vice versa). Now with proper either/or handling that doesn't crash!
- Sorted return, filterable by length or value.
- Working on prettier GUI.

  
Installation:

- Clone the repository
- Install the required dependencies. Pipfile, since I know you use pipenv like all God-fearing Python men do. 
- ``pip install customtkinter`` etc. 
- Run the app.py file and please don't laugh.


### Contributing

Working on making it prettier, but CTk looks pretty good out-of-box. Any suggestions, let me know. 

Feel free to contribute.

### License

This project is licensed under the MIT License - see the LICENSE file for details.
