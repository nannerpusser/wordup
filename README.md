# Wordament Solver App with GUI
Description:

This Wordament Solver app allows users to input a 4x4 board of letters and find valid words from the board based on a provided dictionary. The dictionary is the standard SOWPODS Scrabble list, commonly found as ``twl06.txt`` I believe. App's a skeleton right now without being fleshed out and properly fully implemented. I added some quick instructions inside the code as a comment if it was necessary for anyone. Will be adding a proper instruction widget in the UI, but it's all pretty straightfoward and the Wordament rules are as simple as it gets. Added Help Menu class, GUI components.

Features:
- Cross-platform (Built on Linux, runs on Windows 11. No DPI awareness on linux and no Mac in my realm so can't test it there even if I wanted to.
- Input a 4x4 board of letters as they appear on the tile.
- Handles all digrams, double-letters, either/or tiles, prefix and suffix tiles of each type (**- and ***-, or vice versa). 
- Sorted return based on length, filterable and displayed in row/col form within a ttk TreeView widget.
- Absolutely no tile scoring because that was Hard Mode and it's the weekend. Working on that.
- Length is a good indicator of score anyway, just like your mom told me.
  
Installation:

- Clone the repository
- Install the required dependencies. Pipfile, since I know you use pipenv like all God-fearing Python men do. 
``pip install customtkinter`` etc. 
- Run the ws.py file and please don't laugh.


### Contributing

Working on making it prettier, but CTk looks pretty good out-of-box. I did throw in a custom Messagebox widget for customtkinter and am pleased with how it looks. Trying out various return methods with available widgets, TreeView is not built into CTk.

Feel free to contribute.

### License

This project is licensed under the MIT License - see the LICENSE file for details.
