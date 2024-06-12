from sre_constants import FAILURE
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
import requests
import logging

from sqlalchemy import engine_from_config

logging.basicConfig(level=logging.ERROR)

API_BASE_URL = "https://rickandmortyapi.com/api"

@task(retries=3, retry_delay_seconds=10, timeout_seconds=0.1)
def fetch_characters():
    try: 
        response = requests.get(f'{API_BASE_URL}/character', timeout=0.1)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print ("Ocorreu um timeout ao buscar os personagens.")
        raise 
    except requests.exceptions.RequestException as e:
        ("Ocorreu um erro ao buscar os personagens: {e}")
        raise 

@task(retries=3, retry_delay_seconds=10, timeout_seconds=5)
def fetch_locations():
    try:
        response = requests.get(f'{API_BASE_URL}/location', timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        logging.error("Timeout ao buscar as localizações.")
        raise engine_from_config("Timeout ao buscar as localizações.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao buscar as localizações: {e}")
        raise FAILURE(f"Erro ao buscar as localizações: {e}")
    
@task(retries=3, retry_delay_seconds=10, timeout_seconds=5)
def get_character_by_id(character_id):
    try:
        response = requests.get(f'{API_BASE_URL}/character/{character_id}')
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.Timeout:
        logging.error("Timeout ao buscar o personagem.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao buscar o personagem: {e}")
        raise FAILURE(f"Erro ao buscar o personagem: {e}")

@flow
def rick_and_morty_flow():
    characters = fetch_characters()
    locations = fetch_locations()
    character = get_character_by_id(1)
    print(f"Quantidade de personagens encontrados 👥: {len(characters['results'])}")
    print(f"Localizações encontradas 🗺️: {len(locations['results'])}")
    print(f"Nome do personagem com ID 1: {character['name']}")
    
if __name__ == "__main__":
    rick_and_morty_flow()