# Core Engine (`graphics.py`)

The core engine module defines the fundamental building blocks of the 3D game engine: scenes, cameras, surfaces, shapes, and types. All rendering, scene management, and object composition flows through the classes in this file.

## GameGraphics

`GameGraphics` is the central scene container. Each instance represents an independent scene with its own shape list, camera, input bindings, and per-frame loopers. The engine supports running multiple `GameGraphics` instances simultaneously, which enables scenarios like running multiple game servers in the same process.

### Constructor

```python
GameGraphics(screen, camera, background_color=(0, 0, 0))
```

| Parameter          | Type           | Description                                    |
|--------------------|----------------|------------------------------------------------|
| `screen`           | `Screen`       | The offscreen surface this scene renders to    |
| `camera`           | `Camera`       | The camera used for 3D-to-2D projection        |
| `background_color` | `tuple(r,g,b)` | RGB background fill color (default: black)     |

### Key Attributes

- `shape_list` -- Ordered list of `Shape` objects drawn each frame in insertion order.
- `on_input_list` -- List of `InputFunc` handlers checked against each Pygame event.
- `looper_list` -- List of `Looper` callbacks executed every frame.
- `center` -- Precomputed screen center `(width/2, height/2)`, used as the projection origin.
- `storage` -- A general-purpose dictionary for attaching arbitrary data to the scene.

### Shape Management

```python
add_shape(shape)           # Append a Shape to the end of the draw list
insert_shape(index, shape) # Insert a Shape at a specific draw-order position
```

Shapes are drawn in list order inside `draw()`, which means shapes added later render on top. Use `insert_shape` to control layering.

### Input and Looper Management

```python
add_input_func(input_func)           # Register an InputFunc handler
insert_input_func(index, input_func) # Insert at a specific priority position
add_looper(looper)                   # Register a per-frame Looper
insert_looper(index, looper)         # Insert at a specific priority position
```

### Lifecycle Control

```python
pause()                  # Remove this scene from the global game_graphics_list (stops updates)
start()                  # Add this scene back to the global game_graphics_list
pause_user_input()       # Disable all input handlers (sets state=False)
unpause_user_input()     # Re-enable all input handlers
pause_loopers()          # Disable all per-frame loopers
unpause_loopers()        # Re-enable all per-frame loopers
restart()                # Clear all shapes and input handlers
```

### Rendering

```python
draw_background()   # Fills the screen surface with background_color
draw()              # Iterates shape_list and calls shape.draw() on each
```

The main game loop calls `draw_background()` then `draw()` each frame for the active scene.

---

## Camera

The `Camera` performs 3D-to-2D perspective projection. It rotates world-space points around the camera's position using 3-axis Euler rotation, then projects them onto the 2D screen using a simple depth-based perspective divide.

### Constructor

```python
Camera(x, y, z, game_graphics, original_at=1, x_rotation=0, y_rotation=0, z_rotation=0)
```

| Parameter      | Type           | Description                                              |
|----------------|----------------|----------------------------------------------------------|
| `x, y, z`      | `float`        | Camera position in world space                           |
| `game_graphics` | `GameGraphics` | Parent scene (used to read screen center)                |
| `original_at`  | `float`        | Focal length / projection distance. Higher = less perspective distortion |
| `x_rotation`   | `float`        | Pitch (rotation around X axis) in degrees                |
| `y_rotation`   | `float`        | Yaw (rotation around Y axis) in degrees                  |
| `z_rotation`   | `float`        | Roll (rotation around Z axis) in degrees                 |

### Projection Pipeline (`vr_to_real`)

The `vr_to_real(point)` method transforms a 3D `(x, y, z)` world point to a 2D `(sx, sy)` screen pixel:

1. **Pitch rotation** -- Rotates the `(z, y)` components around the camera's `(z, y)` center by `-x_rotation` degrees.
2. **Yaw rotation** -- Rotates the `(z, x)` components around the camera's `(z, x)` center by `-y_rotation` degrees.
3. **Roll rotation** -- Rotates the `(x, y)` components around the camera's `(x, y)` center by `-z_rotation` degrees.
4. **Depth calculation** -- `depth = point.z - camera.z`. If depth <= 0 the point is behind the camera and `False` is returned.
5. **Perspective divide** -- `magnify = original_at / depth`. The world-space `(x, y)` are scaled by this factor.
6. **Screen mapping** -- The projected point is offset from the screen center returned by `get_origin()`.

### get_origin

`get_origin(point)` computes the screen-space origin offset for a given world point, applying the same depth-based perspective scaling to the camera's own position. This shifts the vanishing point based on camera panning.

### Movement

```python
move((dx, dy))   # Translates the camera by (dx, dy) in screen-aligned axes
```

The Z axis (depth) is typically modified directly (e.g., `camera.z -= 10` for zoom).

---

## Screen

A thin wrapper around `pygame.Surface` that represents an offscreen render target.

```python
Screen(width, height)
```

The `.screen` attribute holds the actual `pygame.Surface`. All draw calls in shape types write to this surface.

---

## Shape

`Shape` is the runtime instance of a drawable object. It binds a `GameGraphics` scene to a `Type` definition and delegates drawing, movement, and collision to the type's function pointers.

### Constructor

```python
Shape(game_graphics, shape_type)
```

The constructor copies the type's `draw`, `move`, `collider`, and `loop_function` references onto the shape instance.

### Methods

```python
draw()              # Calls self.draw_func(self) -- the Type's draw function
move(movement)      # Calls self.move_func(self, movement) if defined
collide(point)      # Calls self.collide_func(self, point) if defined
loop_functions()    # Runs all per-shape loop functions
```

Per-shape attributes (color, position, vertices, etc.) are set after construction by calling the appropriate `change_to_*` function from `shape_types.py`. These functions dynamically attach attributes to the shape instance.

---

## Type

`Type` defines a category of shape by providing function pointers for drawing, movement, and collision.

```python
Type(name, draw, move=None, collider=None, loop_function=None)
```

| Parameter       | Type       | Description                              |
|-----------------|------------|------------------------------------------|
| `name`          | `str`      | Human-readable type name                 |
| `draw`          | `function` | `draw(shape)` -- renders the shape       |
| `move`          | `function` | `move(shape, movement)` -- translates it |
| `collider`      | `function` | `collide(shape, point)` -- hit test      |
| `loop_function` | `function` | Called every frame for shapes of this type |

Types are registered globally via `add_type(shape_type)` and stored in the module-level `types` list.

---

## Module-Level State

```python
types = []               # Global registry of all Type instances
game_graphics_list = []  # All active GameGraphics scenes (updated by the game loop)
```

### Utility Functions

```python
add_type(shape_type)                    # Register a Type in the global types list
add_game_graphics(game_graphics_obj)    # Add a GameGraphics to the active scene list
game_graphics_copy(game_graphics, new_screen)  # Deep-copy a scene onto a new Screen
```

`game_graphics_copy` performs a `copy.deepcopy` of the entire scene, temporarily detaching the surface (which cannot be deep-copied), then reattaching a new screen. This is useful for duplicating scenes across multiple server instances.
