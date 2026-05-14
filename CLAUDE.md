# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common commands

```powershell
make up       # build image and start container
make down     # stop and remove container
make restart  # restart without rebuilding
make build    # build image only
make logs     # tail container logs
make shell    # open sh inside running container
```

Or directly with Docker Compose:

```powershell
docker compose up -d --build
docker compose down
docker compose logs -f
```

The app runs on **http://localhost:8080**. Credentials: `mahler` / `mahler`.

## Architecture

Single-page Flask app served via gunicorn in Docker.

- **`app/app.py`** — entire backend. Reads `app/data/voices.csv` once at startup into `TRACK_DATA`, serialises it as JSON into the Jinja2 template, and serves MP3 files from `app/mp3/` via `send_from_directory`. Auth is a Flask session cookie set on POST `/login`.
- **`app/templates/index.html`** — all UI logic lives here. Track data is embedded as a `const ALL_TRACKS` JSON array; filtering, rendering, playback, and localStorage persistence are all vanilla JS in a single `<script>` block at the bottom.
- **`app/templates/login.html`** — standalone login page, no JS.
- **`mp3/`** (project root) — bind-mounted read-only into `/app/mp3/` inside the container. Adding or removing MP3 files here takes effect immediately without a rebuild.
- **`app/data/voices.csv`** — the data source (columns: Voice, Choir, Voice type, Part, Section, MP3 filename). Changing it requires a rebuild since it is baked into the image.

## Key behaviours to know

- `TRACK_DATA` is loaded at import time; a gunicorn worker restart is needed to pick up CSV changes.
- All filtering is client-side — the server renders one page with the full dataset embedded.
- Filter state and playback speed are persisted in `localStorage` under keys `mahler_filters` and `mahler_speed`.
- The `<audio>` player is sticky at the top; clicking a ▶ Play button sets `player.src` and calls `player.play()`.
- Part I rows are styled `.part-i` (blue tint), Part II rows `.part-ii` (purple tint), active row `.playing` (amber, `!important`).
