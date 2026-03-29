# Networking Module (`networking/`)

The networking module provides a Flask + Socket.IO layer for multiplayer support. It allows the engine to run as a server that web clients connect to via WebSockets. This module is a work-in-progress and is not yet fully integrated with the desktop game loop.

---

## Architecture

```
run_website.py          Entry point -- starts the server
    │
    ├── web_setup.py    Flask app + SocketIO initialization + Server instance
    │
    ├── webpages.py     HTTP route definitions (serves HTML pages)
    │
    └── sockets.py      WebSocket event handlers (connection, messaging)
```

---

## web_setup.py

Creates and configures the Flask application, Socket.IO instance, and server wrapper.

### Components Created

| Variable      | Type                    | Description                                   |
|---------------|-------------------------|-----------------------------------------------|
| `app`         | `flask.Flask`           | The Flask web application                     |
| `web_socket`  | `flask_socketio.SocketIO` | Socket.IO wrapper around the Flask app       |
| `server`      | `networking.Sever`      | Engine server wrapper (manages threads)       |
| `ip`          | `None`                  | Server IP (not yet configured)                |
| `port`        | `None`                  | Server port (not yet configured)              |

The session lifetime is set to 10 hours via `app.permanent_session_lifetime`.

---

## networking.py

Defines the `Client` and `Sever` classes that wrap Socket.IO communication.

### Client

Represents a connected web client.

```python
Client(code, server, game_graphics)
```

| Attribute       | Description                                            |
|-----------------|--------------------------------------------------------|
| `code`          | The Socket.IO session ID (`request.sid`)               |
| `server`        | Reference to the parent `Sever` instance               |
| `game_graphics` | The `GameGraphics` scene assigned to this client       |
| `storage`       | General-purpose dictionary for per-client data         |

**Methods:**
- `send(msg)` -- JSON-serializes `msg` and sends it to this client's room via Socket.IO.

### Sever

Wraps the Flask/Socket.IO server and manages threading.

```python
Sever(ip, port, server, web_socket=None)
```

| Attribute             | Description                                     |
|-----------------------|-------------------------------------------------|
| `ip`                  | Server bind address                             |
| `port`                | Server bind port                                |
| `server`              | The Flask app instance                          |
| `web_socket`          | The SocketIO instance (if using WebSockets)     |
| `list_of_all_clients` | List of all connected `Client` instances        |
| `server_thread`       | The `threading.Thread` running the server       |
| `state`               | Whether the server is currently running         |

**Methods:**
- `run_server()` -- Starts the Flask/Socket.IO server in a background thread. If `web_socket` is provided, it calls `web_socket.run()`; otherwise it calls the Flask app's `.run()` directly. Returns immediately after launching the thread, preventing the server from blocking the game loop.
- `send_all(msg)` -- Broadcasts a JSON message to all connected clients.

### Utility

```python
get_client_by_code(client_list, code)
```
Looks up a `Client` by session ID from a list of clients.

---

## webpages.py

Defines HTTP routes for the web client:

| Route     | Handler | Response                         |
|-----------|---------|----------------------------------|
| `/`       | `home`  | Renders `game.html` template     |
| `/main`   | `home`  | Renders `game.html` template     |
| `/home`   | `home`  | Renders `game.html` template     |

All routes serve the same page, which loads the Socket.IO client library from CDN.

---

## sockets.py

Defines WebSocket event handlers. Currently a stub with two handlers:

### `connect` event
Fires when a new client connects. Creates a `Client` instance with the connecting session's `request.sid`.

### `message` event
Fires when a client sends a message. Parses the incoming JSON and extracts the `command` field. No command handlers are implemented yet.

---

## run_website.py

The server entry point. Imports `webpages` and `sockets` to register routes and event handlers, then calls `server.run_server()` to start the Flask + Socket.IO server in a background thread.

### Running

```bash
cd game
python -m networking.run_website
```

The module-style invocation is required so that `from networking import ...` imports resolve correctly.

---

## Templates

### `layout.html`
Base Jinja2 template with blocks for `title`, `imports`, `content`, and `script`.

### `game.html`
Extends `layout.html`. Sets the title to "Weird Game" and loads the Socket.IO 3.1.3 client library from CDN. The content block is currently empty, awaiting game canvas and client-side logic.

### `home.html`
Empty placeholder template, not currently served by any route.

---

## Static Assets

### `static/game_tools/shapes.js`
Browser-side JavaScript classes that mirror the Python shape API for HTML5 Canvas rendering. See the [Web Client](web_client.md) documentation for details.
