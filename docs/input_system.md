# Input System (`user_input.py`)

The input system provides two types of callbacks that bridge Pygame events to game logic: event-driven `InputFunc` handlers and per-frame `Looper` callbacks.

---

## InputFunc

`InputFunc` binds a specific Pygame event type to a callback function. Each frame, the game loop passes every Pygame event to each active `GameGraphics`, which checks all registered `InputFunc` handlers against the event.

### Constructor

```python
InputFunc(name, input_type, func, state=True, pass_event=False)
```

| Parameter    | Type       | Description                                                |
|--------------|------------|------------------------------------------------------------|
| `name`       | `str`      | Human-readable identifier for this handler                 |
| `input_type` | `int`      | Pygame event type to match (e.g., `pygame.KEYDOWN`, `pygame.MOUSEBUTTONDOWN`) |
| `func`       | `callable` | The callback to invoke when a matching event occurs        |
| `state`      | `bool`     | Whether this handler is active (default: `True`)           |
| `pass_event` | `bool`     | If `True`, the Pygame event object is passed as an argument to `func` |

### Behavior

When `check(event)` is called:
1. If `event.type` matches `self.input_type`, the callback fires.
2. If `pass_event` is `True`, the callback receives the event as `func(event)`.
3. If `pass_event` is `False`, the callback is called with no arguments as `func()`.

The `state` flag allows handlers to be toggled on and off without removing them from the list. `GameGraphics.pause_user_input()` and `unpause_user_input()` bulk-toggle all handlers.

### Usage Examples

From the demo scene in `main.py`:

**Mouse click without event data:**

```python
def move_screen_with_mouse1():
    first_mouse_pos = pygame.mouse.get_pos()
    original_cam_pos = (camera.x, camera.y)

input_func = ui.InputFunc("move screen with mouse 1", pygame.MOUSEBUTTONDOWN, move_screen_with_mouse1)
game_graphics.add_input_func(input_func)
```

**Scroll wheel with event data:**

```python
def zoom(event):
    if event.button == 4:
        camera.z -= 10    # scroll up = zoom in
    elif event.button == 5:
        camera.z += 10    # scroll down = zoom out

zoom_func = ui.InputFunc("zoom", pygame.MOUSEBUTTONDOWN, zoom, pass_event=True)
game_graphics.add_input_func(zoom_func)
```

---

## Looper

`Looper` wraps a function that runs every frame. It is the engine's equivalent of an update/tick callback.

### Constructor

```python
Looper(name, func, state=True)
```

| Parameter | Type       | Description                                      |
|-----------|------------|--------------------------------------------------|
| `name`    | `str`      | Human-readable identifier                        |
| `func`    | `callable` | No-argument function called every frame          |
| `state`   | `bool`     | Whether this looper is active (default: `True`)  |

### Behavior

When `run()` is called (once per frame by `GameGraphics.run_loopers()`), `self.func()` executes if `self.state` is `True`.

Loopers are the primary mechanism for continuous behavior like keyboard polling, animation updates, and physics steps.

### Usage Example

```python
def move_screen():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        camera.move((speed, 0))
    if keys[pygame.K_LEFT]:
        camera.move((-speed, 0))

move_looper = ui.Looper("move screen", move_screen)
game_graphics.add_looper(move_looper)
```

---

## Registration and Lifecycle

Input handlers and loopers are registered on a `GameGraphics` instance:

```python
game_graphics.add_input_func(input_func)
game_graphics.add_looper(looper)
```

They can also be inserted at specific positions for priority ordering:

```python
game_graphics.insert_input_func(0, high_priority_handler)
game_graphics.insert_looper(0, early_update_looper)
```

Lifecycle control is available at the individual level (`handler.state = False`) or in bulk via `GameGraphics`:

```python
game_graphics.pause_user_input()    # Disables all InputFunc handlers
game_graphics.unpause_user_input()  # Re-enables all InputFunc handlers
game_graphics.pause_loopers()       # Disables all Loopers
game_graphics.unpause_loopers()     # Re-enables all Loopers
```
