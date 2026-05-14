# Mahler Symphony No. 8 — Choir Practice Portal

A self-hosted web application that gives every singer in a large-scale choral production a single, organised place to find and listen to their individual practice tracks.

## The problem it solves

Productions of Mahler's Eighth Symphony involve an enormous forces — two full choirs, a boys' choir, eight soloists, and a large orchestra. Each vocal section (soprano, alto, tenor, bass) is further split by choir and by voice type within the choir. This means hundreds of individual practice MP3 files, each relevant only to a specific subset of singers.

Without a dedicated tool, distributing these files is a logistical headache: shared folders become cluttered, email threads get lost, and singers waste time hunting for the one file that applies to them. This portal solves that by putting every file in one place and letting each singer filter down to exactly what they need in seconds.

## What it does

- **Instant filtering** — singers narrow the track list by selecting their Part (I or II), Voice (Soprano, Alto, Tenor, Bass), Choir (choir I, choir II, boys), and Voice Type (e.g. soprano I, alto II). Filters are remembered across visits.
- **Built-in player** — clicking any track loads it directly into a sticky audio player at the top of the page; no downloads required.
- **Playback speed control** — a speed selector (½× to 1½×) lets singers slow a passage down while learning it, with the chosen speed also persisted across sessions.
- **Password protection** — the site is gated behind a shared login so that the practice materials stay within the production.
- **Self-hosted** — runs as a single Docker container on any Windows machine and is exposed to the internet via a Cloudflare tunnel, with no cloud storage or third-party streaming service involved.

## Tech stack

| Layer | Choice |
|---|---|
| Backend | Python / Flask |
| Frontend | Bootstrap 5 + vanilla JavaScript |
| Audio | HTML5 `<audio>` element |
| Container | Docker + docker-compose |
| Reverse proxy | Cloudflare Tunnel |

## Running it

Requires Docker Desktop. Place your MP3 files in the `mp3/` folder at the project root, then:

```sh
make up        # build image and start on port 8080
make logs      # tail live output
make down      # stop
```

Open `http://localhost:8080` and log in with the shared credentials. For internet access, point a Cloudflare Tunnel at `localhost:8080`.

See `CLAUDE.md` for a full description of the code architecture.
