# Micr0DesmosDrawer

A tool for converting an image to a collectiong of lines and curves which are outputed to be used in Desmos

## How To Use
- Click to add a point
- Hold `X` to connect to the previous point via a Linear Connection
- Tap `C` to start a (3 Point) curve
- Tap `V` to start a (2 Point) ellipse
- Hold `Shift` to snap the cursor to the nearest point
- Press `P` to print current equations to the terminal 
- Tap `Z` to delete the nearest point and all of it's connections

## Installation
1. Download and extract this repo
2. Make sure to have `Numpy` and `Pygame` installed from pip (if not just run `pip3.X install numpy pygame`)
3. To run: Run the `Micr0Desmos.py` file with the latest Python 3.X
4. To add an image as a background, add the path to the image as a command line argument: `Micr0Desmos.py /path/to/image.png`

## Example Images
Example of all possible tools combined.<img width="1319" alt="Screen Shot 2022-04-19 at 10 10 26 AM" src="https://user-images.githubusercontent.com/26364458/164026084-dd6f8bf8-b864-414d-a1c8-a8090b24acf8.png">


Example of what can be done if tracing a background image.<img width="661" alt="Screen Shot 2022-04-15 at 9 52 15 AM" src="https://user-images.githubusercontent.com/26364458/164026127-fc491e67-c265-4eae-83e8-181eb2330fd5.png">
