# Mathematics (`mathematics.py`)

This module provides math utility functions used by the camera projection system and shape rendering. It wraps Python's standard `math` module and adds geometry helpers specific to the engine's 3D-to-2D pipeline.

---

## Functions

### `lcm(a, b)`

Computes the least common multiple of two integers.

```python
lcm(a, b) -> int
```

Uses the identity `lcm(a, b) = |a * b| / gcd(a, b)` via `math.gcd`.

---

### `rotate_point(point2d, rotation, rotation_center=(0, 0))`

Rotates a 2D point around a given center by a specified angle in degrees.

```python
rotate_point(point2d, rotation, rotation_center=(0, 0)) -> (x, y)
```

| Parameter         | Type          | Description                             |
|-------------------|---------------|-----------------------------------------|
| `point2d`         | `tuple(x, y)` | The point to rotate                    |
| `rotation`        | `float`       | Rotation angle in degrees               |
| `rotation_center` | `tuple(x, y)` | Center of rotation (default: origin)   |

This is the core rotation function used by `Camera.vr_to_real()`. The camera applies it three times per point -- once for each axis of rotation (pitch, yaw, roll) -- by rotating pairs of coordinate components:

1. **Pitch (x_rotation):** Rotates `(z, y)` around the camera's `(z, y)`.
2. **Yaw (y_rotation):** Rotates `(z, x)` around the camera's `(z, x)`.
3. **Roll (z_rotation):** Rotates `(x, y)` around the camera's `(x, y)`.

The implementation uses the standard 2D rotation matrix:

```
x' = (x - cx) * cos(θ) - (y - cy) * sin(θ) + cx
y' = (x - cx) * sin(θ) + (y - cy) * cos(θ) + cy
```

where `(cx, cy)` is the rotation center and `θ` is the angle converted from degrees to radians.

---

### `calculate_parallel_distant(center, point, angle)`

Calculates the perpendicular distance from a point to a line passing through a center at a given angle.

```python
calculate_parallel_distant(center, point, angle) -> float
```

| Parameter | Type          | Description                                  |
|-----------|---------------|----------------------------------------------|
| `center`  | `tuple(x, y)` | A point on the reference line               |
| `point`   | `tuple(x, y)` | The point to measure distance from          |
| `angle`   | `float`       | Angle of the reference line in degrees       |

This function is designed for alternative depth calculation approaches. It computes the shortest distance from `point` to a line that passes through `center` at the given `angle`. Special cases for 0 and 90 degrees are handled explicitly to avoid division by zero.

The function works by:
1. Computing the slope from the angle: `slope = tan(angle)`.
2. Finding the y-intercept of a perpendicular line through the center.
3. Finding the y-intercept of a line with the given slope through the point.
4. Solving the system to find the closest point on the reference line.
5. Returning the Euclidean distance between the original point and the closest point.

This function is currently not used in the active code paths (the relevant calls in `Camera` are commented out), but it would enable more accurate depth calculation for rotated cameras where simple `point.z - camera.z` is insufficient.
