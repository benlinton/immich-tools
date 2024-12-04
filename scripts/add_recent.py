#!/usr/bin/env python

# Run:
#   pip install requests
#   python3 add_recent.py -h

import argparse
import json
import requests
import time
from _common import log, load_config_data, get_headers, find_api_key, get_album, get_assets, find_album_among_users, remove_asset_from_album, in_multiple_albums, is_album_cover

def load_arguments():
    parser = argparse.ArgumentParser(
        description="Add recently uploaded assets to target album (e.g. Review Later)."
    )
    parser.add_argument(
        'album_name', type=str, 
        help="name of the target album"
    )
    parser.add_argument(
        'created_after_date', type=str, 
        help="fetch assets uploaded after date (i.e. 2024-04-28 or 2024-04-28T10:03:52.000Z)"
    )
    parser.add_argument(
        '--verbose', 
        action='store_true', 
        help="enable verbose mode"
    )
    return parser.parse_args()

def get_assets_created_after(url, headers, date, verbose):
    data = {
        "createdAfter": date,
        "isNotInAlbum": True
    }   
    response = requests.post(f'{url}/api/search/metadata', headers=headers, json=data) 
    if response.ok:
        return response.json()['assets']['items']

def add_assets_to_album(url, headers, album_id, asset_ids, verbose):
    data = { "ids": asset_ids }
    response = requests.put(f'{url}/api/albums/{album_id}/assets', headers=headers, json=data) 
    return response.ok

def main():
    # Parse args and load config data from file
    args = load_arguments()
    config = load_config_data()

    # Initialize script options
    url = config['url']
    users = config['users']
    album_name = args.album_name
    created_after_date = args.created_after_date
    verbose = args.verbose

    # Iterate through users to find the album
    album = find_album_among_users(url, users, album_name)
    if album:
        log(f'Album found: {album['id']}', verbose)
    elif not album:
        log('Album not found.', True)
        return False

    # Initialize progress
    total = 0
    more_assets = True
    api_key = find_api_key(users, album['ownerId'])
    headers = get_headers(api_key)

    # Fetch assets in batches of 250
    while more_assets:
        assets = get_assets_created_after(url, headers, created_after_date, verbose)
        batch_count = len(assets)
        
        if batch_count < 250:
            more_assets = False

        # Display inline progress
        total += batch_count
        print(f"Updating: {batch_count} of {total}", end='\r')

        # Add assets to the album
        asset_ids = [item['id'] for item in assets]
        log(f'Adding asset ids to album: {asset_ids}', verbose)
        add_assets_to_album(url, headers, album['id'], asset_ids, verbose)
            
    # Script is complete
    log("\nDone!", True)  


if __name__ == "__main__":
    main()