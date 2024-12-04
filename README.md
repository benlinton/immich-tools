# Immich Tools

These tools help resolve limitations of Immich while managing multiple users with partner mode.  They allow you to trash, archive, and review recent uploads by utilizing shared albums and then running these scripts via `cron`.


## Setup

Copy the example config and edit it.

    cp config.json.example script/config.json

Install the `requests` library.

    pip install requests


## Run the commands

    cd scripts

Auto-archive all assets in a shared album (e.g. `Archive Later`).

    python archive.py -h

Trash all assets in a shared album (e.g. `Trash Later`).

    python trash.py -h

Add recently uploaded photos to an album for review (e.g. `Review Later` album).

    python3 add_recent.py -h