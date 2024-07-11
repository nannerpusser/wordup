# Wordament Solver App with GUI
Description:

This Wordament Solver app allows users to input a 4x4 board of letters and find valid words from the board based on a provided dictionary. The dictionary is the standard SOWPODS Scrabble list, commonly found as ``twl06.txt``. 

Features:
- Cross-platform (Linux and Windows). No DPI awareness on linux and depending on your WM, complete disregard for window size constraints. 
- Input a 4x4 board of letters as they appear on the tile.
- Handles all special tiles: double-letters, either/or tiles, prefix and suffix tiles of each type (**- and ***-, or vice versa). 
- Sorted return based on length, filterable and displayed in row/col form.
- Working on adding approx. scoring.
- Length is a good indicator of score anyway, just like your mom told me.
  
Installation:

- Clone the repository
- Install the required dependencies. Pipfile, since I know you use pipenv like all God-fearing Python men do. 
``pip install customtkinter`` etc. 
- Run the ws.py file and please don't laugh.


### Contributing

Working on making it prettier, but CTk looks pretty good out-of-box. Any suggestions, let me know. 

Feel free to contribute.

### License

This project is licensed under the MIT License - see the LICENSE file for details.
