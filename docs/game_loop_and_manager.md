# Game Loop and Manager

## Manager (`manager.py`)

The `GameLoop` class is a singleton that holds global engine state. A single instance, `game_loop`, is created at module load and imported by other modules.

### GameLoop Attributes

| Attribute               | Type                | Description                                      |
|-------------------------|---------------------|--------------------------------------------------|
| `fps`                   | `int`               | Target frames per second (default: 40)           |
| `clock`                 | `pygame.time.Clock` | Pygame clock, set by the main loop at startup    |
| `screen`                | `pygame.Surface`    | The main display surface (the OS window)         |
| `screen_width`          | `int`               | Width of the display window in pixels             |
| `screen_height`         | `int`               | Height of the display window in pixels            |
| `main_game_graphics`    | `GameGraphics`      | The primary scene rendered to the display         |
| `events`                | `list`              | Current frame's Pygame event queue                |
| `server`                | `Sever` or `None`   | Optional network server reference                 |
| `server_user_input`     | `list`              | Input handlers registered at the server level     |
| `server_loopers`        | `list`              | Per-frame loopers registered at the server level  |

### Key Methods

```python
make_screen(width, height)
```
Creates the Pygame display window by calling `pygame.display.set_mode((width, height))`. Stores the surface and dimensions on the singleton.

```python
set_main_game_graphics(game_graphics)
```
Designates which `GameGraphics` scene is blitted to the OS display window each frame. Only one scene is rendered to the display at a time, but multiple scenes can still run their logic in the background.

```python
turn_to_server(server)
```
Attaches a network server to the game loop, enabling server-level input and looper dispatch. When `self.server` is set, the main loop will also process `server_user_input` and `server_loopers` each frame.

```python
on_input(event)
```
Dispatches a single Pygame event to all handlers in `server_user_input`.

```python
run_server_loopers()
```
Runs all per-frame callbacks in `server_loopers`.

---

## Game Loop (`game_loop.py`)

The main loop is the engine's entry point and heartbeat. It executes the following sequence every frame:

### Frame Lifecycle

```
1. RENDER
   ├── main_game_graphics.draw_background()    # Fill screen with background color
   ├── main_game_graphics.draw()               # Draw all shapes in the scene
   ├── screen.blit(...)                         # Copy offscreen surface to display
   └── pygame.display.update()                  # Flip the display buffer

2. INPUT DISPATCH
   ├── pygame.event.get()                       # Collect all pending OS events
   └── for each GameGraphics in game_graphics_list:
       ├── game_graphics.on_input(event)        # Fire matching InputFunc handlers
       └── Check for pygame.QUIT → exit

3. PER-FRAME LOOPERS
   └── for each GameGraphics in game_graphics_list:
       └── game_graphics.run_loopers()          # Run all Looper callbacks

4. SERVER DISPATCH (if server is active)
   ├── manager.game_loop.on_input(event)        # Server-level input handlers
   └── manager.game_loop.run_loopers()          # Server-level loopers

5. CLOCK TICK
   └── clock.tick(fps)                          # Cap frame rate to target FPS
```

### Initialization Sequence

Before the loop begins, `from main_folder import main` executes at import time. This runs the demo scene setup in `main.py`, which:

1. Creates a `Screen(1000, 700)` and a `GameGraphics` scene.
2. Creates a `Camera` positioned at `(-150, 200, -400)` with `original_at=400`.
3. Instantiates shapes (polygon, terrain) and adds them to the scene.
4. Registers keyboard and mouse input handlers.
5. Calls `manager.game_loop.make_screen(1000, 700)` to open the Pygame window.
6. Calls `manager.game_loop.set_main_game_graphics(game_graphics)` to designate the active scene.

After all of this executes, the `while True` loop in `game_loop.py` takes over.

### Multiple Scenes

The architecture supports multiple `GameGraphics` in `game_graphics_list`. All of them receive input events and run their loopers every frame, but only `main_game_graphics` is rendered to the display. This enables background scenes (e.g., for server-side game instances) that process logic without being drawn to the user's screen.

### Error Handling

The event polling is wrapped in a `try/except pygame.error` block to gracefully handle cases where Pygame's display has been closed or the event system is in an invalid state.
