Repo reupload: Completely overhauled app to the point it no longer resembles original version. This one has OCR and auto-fill implemented, but EasyOCR has a lot of trouble with certain letters in this font. It doesn't even detect 'V', it will read '12' as 'IZ' and likes to mistake 'I' for 'T'. If you use this, be aware it's probably faster to manually insert the letters and hit Solve than it is to run the OCR and have it insert and then make any corrections. OCR itself is optional, but the first time you open the OCR window it is going to instantiate EasyOCR, which may take 1-2 seconds. Check output to follow along.


![Don't sue me](/assets/wm.png)

## Wordament Solver App with GUI
Description:

This Wordament Solver app allows users to input a 4x4 board of letters and find valid words from the board based on a provided dictionary. The dictionary is the standard OSPD Scrabble dictionary, commonly found as ``twl06.txt``. This means you will encounter invalid words at times since Wordament has an internal dictionary that is nearly identical, but not quite. If you can get Microsoft to share their dictionary, I thank you in advance.

Features:
- Windows only, specifically Windows 10/11.
- Python 3.10+ required.
- Input a 4x4 board of letters as they appear on the tile.
- Handles all special tiles: double-letters aka. digrams, either/or tiles, prefix and suffix tiles of each type (**- and ***-, or vice versa). Now with proper either/or handling that doesn't crash!
- Sorted return, filterable by length or value.

  
Installation:

- Clone the repository
- Install the required dependencies. Pipfile, since I know you use pipenv like all God-fearing Python men do. 👼
- Sorry, but EasyOCR is going to be a requirement unless you'd like to fix the code and remove the import. It will pull in Torch and several large libraries as dependencies. If the OCR window is never opened, it should never get called so with some clever requirements editing and never hitting the button, you may be able to use this without the EasyOCR library.
- Run the `wordup.py` file and behold the mediocrity! I am working on a self-contained binary executable with auto-py-to-exe, but it needs to shrink a lot before I can host it here.


### Contributing

Working on making it prettier, but CTk looks pretty good out-of-box. Any suggestions, let me know. Any criticism? /dev/null

Feel free to contribute.

### License

This project is licensed under the MIT License - see the LICENSE file for details.
