#!/usr/bin/env python

import argparse
import json
import requests
import time

def log(message, condition):
    if condition:
        print(message)
    
def load_config_data():
    with open('config.json', 'r') as file:
        return json.load(file)

def get_headers(api_key):
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

def find_api_key(users, user_id):
    for user in users:
        if user_id == user['ownerId']:
            return user['apiKey']

def get_album(url, headers, album_name):
    response = requests.get(f'{url}/api/albums', headers=headers)
    data = response.json()
    for item in data:
        if item['albumName'] == album_name:
            return item
        
def get_assets(url, headers, album_id):
    response = requests.get(f'{url}/api/albums/{album_id}', headers=headers)
    data = response.json()
    return data['assets']

def find_album_among_users(url, users, album_name):
    for user in users:
        headers = get_headers(user['apiKey'])
        album = get_album(url, headers, album_name)
        if album and album['id'] != "None":
            return album

def remove_asset_from_album(url, headers, album_id, asset_id, verbose):
    data = { "ids": [asset_id] } 
    response = requests.delete(f'{url}/api/albums/{album_id}/assets', headers=headers, json=data)
    return response.ok

def in_multiple_albums(url, headers, asset):
    response = requests.get(f'{url}/api/albums?assetId={asset['id']}', headers=headers)
    if response.ok and len(response.json()) > 1:
        return True

def is_album_cover(asset):
    filename = asset["originalFileName"]
    matches = ["(album cover)", "(album_cover)"]
    if any(match.lower() in filename.lower() for match in matches):
        return True
