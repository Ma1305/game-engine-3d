# 3D Game Engine

A custom 3D game engine built from scratch in Python using Pygame. The engine implements software-based 3D rendering through perspective projection, transforming 3D world coordinates into 2D screen space without relying on GPU shaders or OpenGL. It supports multiple primitive shape types, a camera system with full 3D rotation, keyboard/mouse input handling, and an optional multiplayer networking layer via Flask and Socket.IO.

## Features

- **Software 3D Rendering** -- Perspective projection from 3D world space to 2D screen space using a custom camera system with configurable focal length (`original_at`).
- **3D Camera** -- Full 3-axis rotation (pitch, yaw, roll), panning, and zoom-by-depth. Points are rotated around the camera before projection.
- **Primitive Shape Types** -- Square, line, circle, polygon, cube (composed of 6 polygons), line formula (parametric curves), and terrain (heightfield meshes generated from math expressions).
- **Formula-Driven Geometry** -- Terrain and line shapes can be generated from arbitrary math expressions (e.g., `math.sqrt(-(((x-100)**2+(z-100)**2)-10000))`), compiled and evaluated at build time.
- **Scene Graph** -- `GameGraphics` objects act as independent scenes, each holding their own shape list, camera, input bindings, and per-frame loopers. Multiple scenes can run simultaneously.
- **Input System** -- Declarative `InputFunc` (event-driven) and `Looper` (per-frame) callbacks that can be paused, resumed, and swapped at runtime.
- **Networking (WIP)** -- Flask + Socket.IO server skeleton for multiplayer support, with a browser-side JavaScript client that mirrors the Python shape/camera API on an HTML5 Canvas.

## Prerequisites

- Python 3.8+
- pip

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd game-engine-3d
   ```

2. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # macOS / Linux
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Engine

### Desktop (Pygame)

The main entry point is `game/game_loop.py`. It must be run from the `game/` directory so that internal imports resolve correctly:

```bash
cd game
python game_loop.py
```

This launches a 1000x700 Pygame window with the demo scene defined in `game/main_folder/main.py`, which includes a polygon and a terrain surface generated from a sphere equation.

### Controls

| Input             | Action                        |
|-------------------|-------------------------------|
| Arrow keys        | Pan camera (X / Y)            |
| W / S             | Rotate camera around X axis   |
| A / D             | Rotate camera around Y axis   |
| Q / E             | Rotate camera around Z axis   |
| Mouse drag (LMB)  | Pan camera with mouse         |
| Scroll wheel      | Zoom in / out (move along Z)  |

### Web Server (WIP)

The networking module provides a Flask + Socket.IO server. To start it:

```bash
cd game
python -m networking.run_website
```

This serves the web client at `http://localhost:5000` (default Flask port). The web client is a work-in-progress and does not yet have full parity with the desktop renderer.

## Project Structure

```
game-engine-3d/
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
├── docs/                               # Detailed documentation
│   ├── core_engine.md                  # GameGraphics, Camera, Screen, Shape, Type
│   ├── game_loop_and_manager.md        # Main loop and GameLoop manager
│   ├── shape_types.md                  # All built-in shape type definitions
│   ├── mathematics.md                  # Math utilities (rotation, projection helpers)
│   ├── input_system.md                 # InputFunc and Looper system
│   ├── networking.md                   # Flask/SocketIO server and client classes
│   └── web_client.md                   # Browser-side JavaScript shape/camera API
│
└── game/                               # Engine source code
    ├── game_loop.py                    # Main loop: rendering, events, clock
    ├── graphics.py                     # Core types: GameGraphics, Camera, Screen, Shape, Type
    ├── manager.py                      # GameLoop singleton (display, FPS, server hooks)
    ├── mathematics.py                  # 2D rotation, LCM, parallel distance
    ├── shape_types.py                  # Built-in types: square, line, circle, polygon, cube, terrain
    ├── user_input.py                   # InputFunc (event callbacks) and Looper (frame callbacks)
    │
    ├── main_folder/
    │   └── main.py                     # Demo scene setup (shapes, camera, controls)
    │
    └── networking/
        ├── networking.py               # Client and Server wrapper classes
        ├── web_setup.py                # Flask app and SocketIO initialization
        ├── webpages.py                 # HTTP route definitions
        ├── sockets.py                  # WebSocket event handlers (stub)
        ├── run_website.py              # Server entry point
        ├── templates/
        │   ├── layout.html             # Base Jinja2 template
        │   ├── game.html               # Game page (loads Socket.IO CDN)
        │   └── home.html               # Placeholder (empty)
        └── static/
            └── game_tools/
                └── shapes.js           # Browser-side shape and camera classes (Canvas 2D)
```

## Architecture Overview

The engine follows a layered architecture:

1. **Manager** (`manager.py`) -- The `GameLoop` singleton holds global state: the Pygame display surface, FPS setting, active `GameGraphics`, event queue, and optional server hooks.

2. **Core Graphics** (`graphics.py`) -- Defines the scene-level `GameGraphics` container, the `Camera` (3D-to-2D projection), `Screen` (offscreen Pygame surface), and the `Shape`/`Type` pattern for polymorphic rendering.

3. **Shape Types** (`shape_types.py`) -- Registers concrete `Type` instances (square, line, circle, polygon, cube, line_formula, terrain) with their draw, move, and collide functions. Each type operates on per-shape attributes set by a `change_to_*` initializer.

4. **Input** (`user_input.py`) -- `InputFunc` binds a Pygame event type to a callback. `Looper` runs a callback every frame. Both support enable/disable toggling.

5. **Game Loop** (`game_loop.py`) -- The infinite loop that drives everything: clears the screen, draws all shapes via the active `GameGraphics`, dispatches Pygame events to input handlers, runs per-frame loopers, and ticks the clock.

6. **Networking** (`networking/`) -- An optional Flask + Socket.IO layer for serving a web client and exchanging game state over WebSockets. Currently a skeleton with route definitions and connection handling stubs.

## License

This project does not currently include a license file. All rights reserved by the author.
