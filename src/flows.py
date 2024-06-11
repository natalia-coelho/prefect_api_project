from sre_constants import FAILURE
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
import requests
import logging

from sqlalchemy import engine_from_config

logging.basicConfig(level=logging.INFO)

@task(retries=3, retry_delay_seconds=10, timeout_seconds=0.1)
def fetch_characters():
    try: 
        response = requests.get('https://rickandmortyapi.com/api/character', timeout=0.1)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print ("Ocorreu um timeout ao buscar os personagens.")
        raise 
    except requests.exceptions.RequestException as e:
        ("Ocorreu um erro ao buscar os personagens: {e}")
        raise 

@task(retries=3, retry_delay_seconds=10, timeout_seconds=5)
def get_characters():
    response = requests.get('https://rickandmortyapi.com/api/character')
    characters = response.json()['results']
    return [character['name'] for character in characters]

@task(retries=3, retry_delay_seconds=10, timeout_seconds=5)
def fetch_locations():
    try:
        response = requests.get('https://rickandmortyapi.com/api/location', timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        logging.error("Timeout ao buscar as localizações.")
        raise engine_from_config("Timeout ao buscar as localizações.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao buscar as localizações: {e}")
        raise FAILURE(f"Erro ao buscar as localizações: {e}")

@flow
def rick_and_morty_flow():
    characters = fetch_characters()
    locations = fetch_locations()
    names = get_characters()
    logging.info(f"Quantidade de personagens encontrados: {len(characters['results'])}")
    logging.info(f"Localizações encontradas: {len(locations['results'])}")
    
if __name__ == "__main__":
    rick_and_morty_flow()