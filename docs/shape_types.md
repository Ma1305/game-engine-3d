# Shape Types (`shape_types.py`)

This module defines all built-in shape types. Each type follows the same pattern: a `change_to_*` function that initializes per-shape attributes, a `draw_*` function that renders the shape, and optionally a `move_*` function. Types are registered globally via `graphics.add_type()`.

Every draw function receives the `Shape` instance as `self` and accesses the parent scene via `self.game_graphics`, the camera via `self.game_graphics.camera`, and the render surface via `self.game_graphics.screen.screen`.

---

## Square

**Type name:** `"square"`

### Initialization

```python
change_to_square(shape, color, rect, real=False)
```

| Parameter | Type           | Description                                                                      |
|-----------|----------------|----------------------------------------------------------------------------------|
| `color`   | `tuple(r,g,b)` | Fill color                                                                       |
| `rect`    | `tuple`        | If `real`: `(x, y, w, h)`. If 3D: `(x, y, w, h, z)` where z is the depth value |
| `real`    | `bool`         | If `True`, drawn in screen space. If `False`, projected through the camera       |

### Rendering

In 3D mode, the square's `(x, y, z)` position is projected via `camera.vr_to_real()`, and its width/height are scaled by `original_at / depth` to simulate perspective. Squares behind the camera or entirely off-screen are culled.

### Movement

`move_square` translates by `(dx, dy)` in the square's coordinate space.

---

## Line

**Type name:** `"line"`

### Initialization

```python
change_to_line(shape, start_point, end_point, color, width=1, real=False)
```

| Parameter     | Type          | Description                                                 |
|---------------|---------------|-------------------------------------------------------------|
| `start_point` | `tuple`       | `(x, y)` if real, `(x, y, z)` if 3D                        |
| `end_point`   | `tuple`       | `(x, y)` if real, `(x, y, z)` if 3D                        |
| `color`       | `tuple(r,g,b)` | Stroke color                                                |
| `width`       | `int`         | Line thickness in pixels (scaled by perspective in 3D mode) |
| `real`        | `bool`        | Screen-space vs. world-space flag                            |

### Rendering

In 3D mode, both endpoints are projected through the camera. If one endpoint is behind the camera, the draw function clips the line by calculating the intersection point at `z = camera.z + 1` using linear interpolation along the x, y, and z axes. This prevents lines from disappearing abruptly when partially behind the camera. Line width is also scaled by perspective.

---

## Circle

**Type name:** `"circle"`

### Initialization

```python
change_to_circle(shape, center, radius, color, real=False)
```

| Parameter | Type           | Description                          |
|-----------|----------------|--------------------------------------|
| `center`  | `tuple`        | `(x, y)` if real, `(x, y, z)` if 3D |
| `radius`  | `float`        | Circle radius in world units         |
| `color`   | `tuple(r,g,b)` | Fill color                           |
| `real`    | `bool`         | Screen-space vs. world-space flag    |

### Rendering

In 3D mode, the center is projected and the radius is scaled by the camera's zoom factor. The circle type is defined but uses `camera.zoom` which is currently only present on the JavaScript `Camera` class -- the Python `Camera` does not have a `zoom` attribute, so this type will raise an `AttributeError` if used in 3D mode.

---

## Polygon

**Type name:** `"polygon"`

### Initialization

```python
change_to_polygon(shape, color, points, outline=False, real=False)
```

| Parameter | Type             | Description                                                 |
|-----------|------------------|-------------------------------------------------------------|
| `color`   | `tuple(r,g,b)`   | Fill color                                                  |
| `points`  | `list of tuples` | Vertex list. `(x, y)` if real, `(x, y, z)` if 3D           |
| `outline`  | `bool`           | If `True`, draws a gray outline on top of the filled polygon |
| `real`    | `bool`           | Screen-space vs. world-space flag                            |

### Rendering

The polygon draw function is the most complex renderer in the engine. It performs:

1. **Projection** -- All vertices are projected via `camera.vr_to_real()`.
2. **Bounding box cull** -- If all projected vertices fall entirely outside the screen, the polygon is skipped.
3. **Behind-camera clipping** -- For vertices behind the camera, the function finds the intersection at `z = camera.z + 1` by interpolating toward the nearest visible neighbor vertex.
4. **Screen-edge clipping** -- Vertices that project outside screen bounds are clamped to screen edges, with neighbor-based interpolation to preserve polygon shape at the borders.
5. **Fill + optional outline** -- If at least 3 valid vertices remain, `pygame.draw.polygon` fills the shape, optionally followed by a gray outline stroke.

### Movement

`move_polygon` translates all vertices by `(dx, dy, dz)`.

---

## Cube

**Type name:** `"cube"`

### Initialization

```python
change_to_cube(shape, color, position, dimensions)
```

| Parameter    | Type          | Description                                          |
|--------------|---------------|------------------------------------------------------|
| `color`      | `tuple(r,g,b)` | Fill color for all faces                             |
| `position`   | `tuple(x,y,z)` | Back-top-left corner of the cube in world space      |
| `dimensions` | `tuple(w,h,d)` | Width (x), height (y), depth (z) of the cube        |

### Construction

A cube is composed of 6 polygon `Shape` instances -- one for each face (back, top, right, left, bottom, front). Each face is constructed as a quad with 4 vertices computed from `position` and `dimensions`, then initialized via `change_to_polygon` with `outline=True`.

The individual face shapes are stored on the parent shape as:
- `shape.back`, `shape.top`, `shape.right`, `shape.left`, `shape.bottom`, `shape.front`
- `shape.polygons` -- list of all 6 faces

### Rendering

`draw_cube` iterates `self.polygons` and calls `.draw()` on each face. Currently draws all faces regardless of visibility (no back-face culling).

---

## Line Formula

**Type name:** `"line formula"`

### Initialization

```python
change_to_line_formula(shape, color, start_x, end_x, y_formula, z_formula, accuracy, width=1)
```

| Parameter   | Type   | Description                                                |
|-------------|--------|------------------------------------------------------------|
| `color`     | `tuple` | Stroke color                                              |
| `start_x`  | `int`  | Starting X value for the parametric sweep                  |
| `end_x`    | `int`  | Ending X value for the parametric sweep                    |
| `y_formula` | `str`  | Python math expression for Y as a function of `x`          |
| `z_formula` | `str`  | Python math expression for Z as a function of `x`          |
| `accuracy`  | `int`  | Step size between sample points (smaller = smoother curve) |
| `width`    | `int`  | Line thickness                                             |

### Construction

The formula strings are compiled using Python's `parser.expr().compile()` and evaluated with `eval()`. For each step from `start_x` to `end_x`, a line segment `Shape` is created connecting consecutive sample points, forming a polyline approximation of the parametric curve.

### Example

```python
change_to_line_formula(shape, (255, 200, 100), -600, 600,
                       "20*sin(0.5*x)+0.01*(x**2)", "0.01*(x**2)", 1, width=5)
```

This generates a 3D curve where Y follows a damped sine wave and Z follows a parabola.

---

## Terrain

**Type name:** `"terrain"`

### Initialization

```python
change_to_terrain(shape, color, position, width, length, y_formula, accuracy)
```

| Parameter   | Type          | Description                                               |
|-------------|---------------|-----------------------------------------------------------|
| `color`     | `tuple(r,g,b)` | Base terrain color                                       |
| `position`  | `tuple(x,y,z)` | World-space origin of the terrain grid                   |
| `width`     | `int`         | Terrain extent along the X axis                           |
| `length`    | `int`         | Terrain extent along the Z axis                           |
| `y_formula` | `str`         | Python math expression for height Y as a function of `x` and `z` |
| `accuracy`  | `int`         | Grid cell size (smaller = more detail, more polygons)     |

### Construction

The terrain is a heightfield mesh. For each grid cell `(x, z)`, four corner heights are evaluated from `y_formula`, and a quad polygon is created. A depth-based shading factor `(length - z) / (length - accuracy)` is applied to the base color, giving a simple distance fog effect where farther quads are darker.

### Rendering

`draw_terrain` draws polygons in reverse order (back to front), implementing a basic painter's algorithm for correct depth ordering.

### Example

```python
change_to_terrain(shape, (0, 200, 0), (-400, 100, 0), 200, 200,
                  "math.sqrt(-(((x-100)**2+(z-100)**2)-10000))", 5)
```

This generates a green dome-shaped terrain surface (the top half of a sphere equation).
