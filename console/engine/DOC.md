# PythonProjects/consoleengine/
**Requires keyboard, mouse**
*A ConsoleEngine designed after javidx9's, but no tutorial was followed, I just added some rasterizers and functionality. Very much unfinished. Haven't found a way to support OOP yet.*

## Setting Up the Console
To set up a ConsoleEngine game to work, you have to setup some files. *Windows only?*
1. Create file *\[gamename\].bat* in the directory with your python file and add code:
```batch
@echo off
python [pythonfile].py

pause
```
2. Create a shortcut from said .bat file and right-click > Properties
3. Click *Font*, scroll in the Font menu and select *Raster Fonts*. In *Size* select 8x8 (to create square pixels, not oblong ones).
4. Under *Shortcut* click *Change Icon...* at the bottom to change the file and window icon.

## ConsoleEngine.py
- *FORMAT* : get your ANSI sequences here, actually, don't. This breaks the engine.
- *PIXEL_TYPE* : get your 4 pixel shades here --> PIXEL_SOLID, PIXEL_THREEQUARTERS, PIXEL_HALF, PIXEL_QUARTER
- *ConsoleGame* : Main console engine class.

### *ConsoleGame* class
- **Hidden** : hidden functions and variables
  - **root** - 2d array holding screen information
  - **tp1/tp2** - deltatime setup (do not use for deltatime)
  - **fElapsedTime** - deltatime (time of frame)
  - ***__ClearRoot()*** - Clear the root array
  - ***__Bresenham(start, end)*** - Bresenham algorithm for generating lines
  - ***__MidPointCircle(centerpos, radius)*** - Mid-point circle algorithm for circle outlines
  - ***__FillCircleWithEdge(points, char, rawc)*** - Fill a mid-point circle edge
  - ***__CharConvert(char)*** - Converts codes to string (not in use)
  - ***__FillBottomFlatTriangle(v1, v2, v3, char, rawc)*** - Fill flat bottom triangle
  - ***__FillTopFlatTriangle(v1, v2, v3, char, rawc)*** - Fill flat top triangle
  
- `OnUserCreate(func)` : used to decorate for setup. Use this decorator to setup the game. Passes the ConsoleGame to the function it decorates. Options to enable/disable:
  - **title** - _string_ window title, use `%fps%` to display the fps
  - **fpsInTitle** - _bool_ if you do not want to replace `%fps%` with the fps or it is not present, set to False to save a few frames.
  - **geometry** - _tuple_ window size as `(width, height)`
  - **emptychar** - _string_ character to clear the screen with
  - **colorsetting** - _string_ color of the console as two hexadecimals. e.g. `0f`
  - **clear** - _bool_ if the console should be autocleared
  - **active** - _bool_ whether or not to loop
  - **safeSizing** - _int_ padding on bottom and right side to stop scrolling
  - **lettersize** - _tuple_ character size (of monospaced) as `(width, height)`
 
- `OnUserUpdate(func)` : used to decorate for every frame, all deltatime, frame clearing and updating is handled by this function.  Passes the ConsoleGame to the function it decorates. 

- `Pixel(pos, char, place, rawc, fsp)` : places or checks a pixel. 
  - **pos** as (x, y), **char** as string, **place** as bool, **rawc** not used, **fsp** as bool
  - **pos** location to check/place a pixel 
  - **char** character to place, you can use PIXEL_TYPEs
  - **place** condition whether to check for a pixel or whether to place a pixel
  - **fsp** force single pixel, if enabled overflow characters will not automatically be places in neighbouring cells. This is mostly useful for coloured pixels used with FORMAT.
  
- `RootArray(plan)` : this function replaces the screen array with your own custom one (must be done every frame)
  - **plan** as 2D array
  
- `DrawRawLine(pos1, pos2, char, rawc)` : draws a 1px line, use `DrawLine()`
  - **pos1/pos2** as (x, y), **char** as string
  - **pos1/pos2** start/end of line
  - **char** character to place, you can use PIXEL_TYPEs
  
- `DrawLine(pos1, pos2, char, thickness, rawc)` : draws a line
  - **pos1/pos2** as (x, y), **char** as string, **thickness** as integer
  - **pos1/pos2** start/end of line
  - **char** character to place, you can use PIXEL_TYPEs
  - **thickness** thickness of line
  
- `DrawBox(pos, size, char, fill, thickness, rawc, rawf)` : draws a rectangle
  - **pos/size** as (x, y), **char/fill** as string (PIXEL_TYPEs accepted), **thickness** as integer
  - **pos** top-left position of rectangle
  - **size** size `(width, height)` of rectangle
  - **char** character for borders, you can use PIXEL_TYPEs
  - **fill** character for fill, you can use PIXEL_TYPEs, leave as `" "` for no fill
  - **thickness** thickness of border
  
- `DrawTriangle(pos1, pos2, pos3, char, fill, thickness, rawc, rawf` : draws a triangle
  - **pos1/pos2/pos3** as (x, y), **char/fill** as string (PIXEL_TYPEs accepted), **thickness** as integer
  - **pos1/pos2/pos3** vectors of triangle points
  - **char** character for borders, you can use PIXEL_TYPEs
  - **fill** character for fill, you can use PIXEL_TYPEs, leave as `" "` for no fill
  - **thickness** thickness of border
  
- `DrawSprite(pos, chararray)` : draws a sprite
  - **pos** as (x, y), **chararray** as a 2d array
  - **pos** top-left position of sprite
  - **chararray** sprite: of strings (each a pixel): `[["#","#"],["#","#"]]`
  
- `DrawCircle(centerpos, radius, char, fill, rawc, rawf)` : draws a circle
  - **centerpos** as (x, y), **radius** as an integer, **char/fill** as string (PIXEL_TYPEs accepted)
  - **centerpos** center of circle
  - **radius** radius of circle
  - **char** character for borders, you can use PIXEL_TYPEs
  - **fill** character for fill, you can use PIXEL_TYPEs, leave as `" "` for no fill

- `StringToSprite(string, effects)` : get a coloured/formatted version of a string compatible with display
  - **string/effects** as string
  - **string** string to convert with formatting
  - **effects** ANSI escape sequence colours for display (use FORMAT)
  - _Use DrawSprite() with the `chararray` as the returned value from StringToSprite()_

- `Keyboard(key)` : returns True or False for whether or not a key is held. Uses `keyboard.is_pressed()`.

- `GetMousePos(adjusted)` : returns mouse position (divided by font size if **adjusted**)

## Example Program
```python
# Import ConsoleEngine
import ConsoleEngine, time, os

# Quick references for pixel types
l4 = ConsoleEngine.PIXEL_TYPE.PIXEL_SOLID;l3 = ConsoleEngine.PIXEL_TYPE.PIXEL_THREEQUARTERS;l2 = ConsoleEngine.PIXEL_TYPE.PIXEL_HALF;l1 = ConsoleEngine.PIXEL_TYPE.PIXEL_QUARTER

playersprite = [
  ["",l4,l4,""],
  [l4,l2,l1,l4],
  [l4,l1,l2,l4],
  ["",l4,l4,""]
]
master = ConsoleEngine.ConsoleGame()

# Decorate w/ OnUserCreate, this will execute once at the start of the program
@master.OnUserCreate
def setup(self): # !!! *self* is *master*, this is passed by OnUserCreate. 
  self.title = "Player Movement"
  self.geometry = (150, 150)
  self.fpsInTitle = False
  self.playerX = 1 # assign things to the master!
  self.playerY = 1
  
# Decorate w/ OnUserUpdate, this will execute once every frame
@master.OnUserUpdate
def loop(self): # !!! *self* is *master*, this is passed by OnUserUpdate.   
  if self.Keyboard('w'): self.playerY -= 1
  if self.Keyboard('s'): self.playerY += 1
  if self.Keyboard('a'): self.playerX -= 1
  if self.Keyboard('d'): self.playerX += 1
  if self.Keyboard('x'): self.active = False
  
  self.DrawBox((0,0), (self.geometry[0] - 1, self.geometry[1] -1))
  self.DrawSprite((self.playerX, self.playerY), playersprite)
```
