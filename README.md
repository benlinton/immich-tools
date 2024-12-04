# Immich Tools

These tools help resolve limitations of Immich when **partner mode** is enabled (for multiple users).

- `archive.py` - users can archive each other's photos
- `trash.py` - users can trash each other's photos
- `add_recent.py` - capture recently uploaded photos for easy review

Simply create **shared albums** and then run these scripts manually or via `cron` (recommended).


## Setup

Copy the example config and edit it.

    cp config.json.example scripts/config.json

Install the `requests` library.

    pip install requests


## Run the commands

Auto-archive all assets in a shared album (e.g. `Archive Later`).

    python3 ./scripts/archive.py --help

Trash all assets in a shared album (e.g. `Trash Later`).

    python3 ./scripts/trash.py --help

Add recently uploaded photos to an album for review (e.g. `Review Later` album).

    python3 ./scripts/add_recent.py --help


## Beautify with cover photos

Upload the provided [cover photos](images/) to Immich for each album.

The scripts will not touch any files that contain `(Album_Cover)` in their filename.