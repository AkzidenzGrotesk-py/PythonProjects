# PythonProjects/consoleengine/
*A ConsoleEngine designed after javidx9's, but no tutorial was followed, I just added some rasterizers and functionality. Very much unfinished.*

## ConsoleEngine.py
- *FORMAT* : get your ANSI sequences here, actually, don't. This breaks the engine.
- *PIXEL_TYPE* : get your 4 pixel shades here --> PIXEL_SOLID, PIXEL_THREEQUARTERS, PIXEL_HALF, PIXEL_QUARTER
- *ConsoleEngine* : Main console engine class.

### *ConsoleEngine* class
- `OnUserCreate(func)` : used to decorate for setup.
- `OnUserUpdate(func)` : used to decorate for every frame, all deltatime, frame clearing and updating is handled by this function.
- `Pixel(pos, char, place, rawc, fsp)` : places or checks a pixel. 
  - **pos** as (x, y), **char** as string, **place** as bool, **rawc** not used, **fsp** as bool
  - **pos** location to check/place a pixel 
  - **char** character to place, you can use PIXEL_TYPEs
  - **place** condition whether to check for a pixel or whether to place a pixel
  - **fsp** force single pixel, if enabled overflow characters will not automatically be places in neighbouring cells. This is mostly useful for coloured pixels used with FORMAT.
- `RootArray(plan)` : this function replaces the screen array with your own custom one (must be done every frame)
  - **plan** as 2D array
- `DrawRawLine(pos1, pos2, char, rawc)` : draws a line between **pos1** and **pos2** with **char** that is 1 px wide
  - **pos1/pos2** as (x, y), **char** as string (PIXEL_TYPEs accepted)
- `DrawLine(pos1, pos2, char, thickness, rawc)` : draws a line between **pos1** and **pos2** with **char** that is **thickness** px wide
  - **pos1/pos2** as (x, y), **char** as string (PIXEL_TYPEs accepted), **thickness** as integer
- `DrawBox(pos, size, char, fill, thickness, rawc, rawf)` : draws a box at **pos** that is **size** with border **thickness** with **char** and filled with **fill**
  - **pos1/pos2** as (x, y), **char** as string (PIXEL_TYPEs accepted), **thickness** as integer
