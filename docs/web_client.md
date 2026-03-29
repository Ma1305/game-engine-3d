# Web Client (`static/game_tools/shapes.js`)

The web client module provides JavaScript classes for rendering shapes on an HTML5 Canvas, mirroring a subset of the Python engine's shape and camera API. It is intended for use by browser clients connecting to the Flask + Socket.IO server.

---

## Camera

The JavaScript `Camera` operates in 2D with a zoom factor, unlike the Python `Camera` which performs full 3D Euler rotation and perspective projection.

### Constructor

```javascript
new Camera(canvas, ctx, x, y, zoom)
```

| Parameter | Type                       | Description                         |
|-----------|----------------------------|-------------------------------------|
| `canvas`  | `HTMLCanvasElement`        | The target canvas element           |
| `ctx`     | `CanvasRenderingContext2D` | The 2D rendering context            |
| `x`       | `number`                   | Camera X position in world space    |
| `y`       | `number`                   | Camera Y position in world space    |
| `zoom`    | `number`                   | Zoom/scale factor                   |

### Methods

**`vr_to_real(point)`** -- Converts a virtual `[x, y]` position to screen coordinates by applying zoom scaling and camera offset from the canvas center.

**`get_origin()`** -- Returns the screen-space position of the world origin `(0, 0)` based on the current camera position and zoom level.

**`move(move)`** -- Translates the camera by `[dx, dy]`.

### Projection Math

```
origin = [canvas.width/2 + zoom * (-camera.x), canvas.height/2 - zoom * (-camera.y)]
screen_point = [origin.x + zoom * point.x, origin.y - zoom * point.y]
```

The Y axis is flipped (subtracted) to convert from math-style Y-up coordinates to canvas Y-down coordinates.

---

## Square

### Constructor

```javascript
new Square(ctx, x, y, w, h, color)
```

### Modes
- **Real mode** (default): Draws at pixel coordinates using `ctx.fillRect`.
- **Virtual mode** (after `make_virtual(camera)`): Transforms position and size through the camera before drawing.

---

## Line

### Constructor

```javascript
new Line(ctx, startPoint, endPoint, color)
```

### Modes
- **Real mode**: Draws a line between pixel coordinates.
- **Virtual mode**: Transforms both endpoints through the camera.

---

## Circle

### Constructor

```javascript
new Circle(ctx, x, y, radius, color)
```

### Modes
- **Real mode**: Draws a filled circle at pixel coordinates.
- **Virtual mode**: Transforms center and scales radius by camera zoom.

---

## CircleOutline

### Constructor

```javascript
new CircleOutline(ctx, x, y, radius, color)
```

Identical to `Circle` but uses `ctx.stroke()` instead of `ctx.fill()` for an unfilled outline.

---

## Shared Pattern

All shape classes follow the same interface:

| Method              | Description                                   |
|---------------------|-----------------------------------------------|
| `draw()`            | Renders the shape to the canvas               |
| `move([dx, dy])`    | Translates the shape by a delta               |
| `make_virtual(cam)` | Switches to camera-projected rendering        |

Each shape has a `real` flag (default `true`). Calling `make_virtual(camera)` sets `real = false` and stores a camera reference, causing `draw()` to project coordinates through the camera before rendering.

---

## Utility Functions

### `rgbToColor(color)`

Converts an RGB array `[r, g, b]` to a CSS color string `"rgb(r, g, b)"` for use with canvas fill/stroke styles.

---

## Differences from Python API

| Feature                 | Python                                  | JavaScript                          |
|-------------------------|-----------------------------------------|-------------------------------------|
| Coordinate system       | 3D `(x, y, z)` with perspective divide  | 2D `[x, y]` with zoom scaling      |
| Camera rotation         | 3-axis Euler rotation (pitch/yaw/roll)  | No rotation support                 |
| Depth / perspective     | `original_at / depth` projection        | Uniform `zoom` multiplier           |
| Polygon support         | Full polygon with clipping              | Not implemented in JS               |
| Cube / Terrain / Formula | Supported                              | Not implemented in JS               |
| Behind-camera clipping  | Line/polygon clipping at z=camera.z+1   | Not applicable (2D only)            |
