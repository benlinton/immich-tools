#!/usr/bin/env python

# Run:
#   pip install requests
#   python3 archive.py -h

import argparse
import json
import requests
import time
from _common import log, load_config_data, get_headers, find_api_key, get_album, get_assets, find_album_among_users, remove_asset_from_album, in_multiple_albums, is_album_cover

def load_arguments():
    parser = argparse.ArgumentParser(
         description="Archive assets found in a target album (e.g. Archive Later)."
    )
    parser.add_argument(
        'album_name', type=str, 
        help="Name of the target album."
    )
    parser.add_argument(
        '--cleanup', 
        action='store_true', 
        help="Remove assets from album after archiving."
    )
    parser.add_argument(
        '--verbose', 
        action='store_true', 
        help="Enable verbose mode."
    )
    return parser.parse_args()

def archive_asset(url, headers, asset, verbose):
    data = { 'isArchived': 'true' }
    response = requests.put(f'{url}/api/assets/{asset['id']}', headers=headers, json=data) 
    return response.ok

def main():
    # Parse args and load config data from file
    args = load_arguments()
    config = load_config_data()

    # Initialize script options
    url = config['url']
    users = config['users']
    album_name = args.album_name
    allow_single_album = False
    cleanup = args.cleanup
    keep_album_cover = True
    verbose = args.verbose

    # Iterate through users to find the album
    album = find_album_among_users(url, users, album_name)
    if album:
        log(f'Album found: {album['id']}', verbose)
    elif not album:
        log('Album not found.', True)
        return False

    # Fetch assets for a given album
    api_key = find_api_key(users, album['ownerId'])
    headers = get_headers(api_key)
    assets = get_assets(url, headers, album['id'])
    asset_count = len(assets)
    log(f'Album assets found: {asset_count}', verbose)

    # Loop through and update each asset
    progress = 0
    for asset in assets:

        # Display inline progress
        progress += 1
        print(f"Updating: {progress} of {asset_count}", end='\r')

        # Api key and header for asset
        api_key = find_api_key(users, asset['ownerId'])
        headers = get_headers(api_key)

        # Skip unless asset is in multiple albums (more than archive album)
        if not in_multiple_albums(url, headers, asset) and not allow_single_album:
            log(f'Skipping asset: {asset['id']} - add to another album first', True)
            continue

        # Archive the asset using the correct api key
        if asset['isArchived'] == True:
            log(f'Asset already archived: {asset['id']}', verbose)
        else:
            log(f'Archiving asset: {asset['id']}', verbose)
            archive_asset(url, headers, asset, verbose)  

        # Remove asset from album after archiving it
        if cleanup: 
            if keep_album_cover and is_album_cover(asset):
                log(f'Skipping album cover: {asset['id']}', verbose)
            else: 
                log(f'Removing asset from album: {asset['id']}', verbose)
                remove_asset_from_album(url, headers, album['id'], asset['id'], verbose)
            
    # Script is complete
    log("\nDone!", True)  


if __name__ == "__main__":
    main()