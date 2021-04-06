# PythonProjects/pygame/3d/
**Requires pygame.**
*A decently horrible implementation of javidx9's 3d engine tutorial in Python. With relatively low objects this runs at pretty good FPS, but try loading anything of size and it will run at like 2-8 FPS*

- **engine.py** - Main engine file, pretty well commented.
- **pygao.py** - Utility functions (vec3d, mat4x4 class)
- **/assets/** - Place all .obj models here
- **/assets/config.json** - Config file, see below.

### Config
- **title** : sets window title (use %fps% for FPS display)
- **icon** : path from _engine.py_ to icon image
- **size** : window size as *[width, height]*
- **modelData** : \*all must be filled in for every file (except *preloadedb*).
  - **file** : path from _engine.py_ to .obj file
  - **offsets** : where to place the .obj file in space as *[x, y, z]*
  - **rotations** : applicable rotations as *[x, y, z]*
  - **preloadedb** : *[x, y, z]* coordinates of blocks
- **floor** : where to place floor as *[x-corner-diagonal, y-height, x-corner-diagonal]*
- **wireFrame** : *true/false* to render wireframes for triangles
- **wireFrameColour** : *[r, g, b]* for wireframe colour
- **constantFPS** : *true/false* constantly update the fps, even if the change is minute.
- **showClipping** : *true/false* to toggle colours for clipped triangles
- **roundFPS** : decimal places to round FPS to.
- **controls** : controls for character, *i don't think some of the controls are bound properly...*
  - **quit** : quit game
  - **up/down/left/right/forward/backwards** : directional controls
  - **sprint** : double-speed when held
  - **lrsensitivity** : sensitivity for turning left-right
  - **udsensitivity** : sensitivity for turning up-down
