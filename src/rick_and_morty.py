import requests

API_BASE_URL = "https://rickandmortyapi.com/api"

def get_characters():
    response = requests.get(f'{API_BASE_URL}/character')
    response.raise_for_status()
    return response.json()
    
def get_locations():
    response = requests.get(f'{API_BASE_URL}/location')
    response.raise_for_status()
    return response.json()

def get_episodes():
    response = requests.get(f'{API_BASE_URL}/episode')
    response.raise_for_status()
    return response.json()

def get_character_by_id(character_id):
    response = requests.get(f'{API_BASE_URL}/character/{character_id}')
    response.raise_for_status()
    return response.json()