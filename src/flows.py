from asyncio import sleep
from random import randrange
from sre_constants import FAILURE
from prefect import flow, task
from prefect.tasks import task_input_hash
import rick_and_morty
import requests
import logging
import time

from sqlalchemy import engine_from_config

logging.basicConfig(level=logging.ERROR)

@task(retries=5, retry_delay_seconds=10, timeout_seconds=5)
def fetch_characters():
    try: 
        # sleep(RANDOM_TIMEOUT) #simulating a timeout
        return rick_and_morty.get_characters()
    except requests.exceptions.Timeout:
        print ("Ocorreu um timeout ao buscar os personagens.")
        raise 
    except requests.exceptions.RequestException as e:
        ("Ocorreu um erro ao buscar os personagens: {e}")
        raise 

@task(retries=5, retry_delay_seconds=10, timeout_seconds=5)
def fetch_locations():
    try:
        # sleep(RANDOM_TIMEOUT) #simulating a timeout
        return rick_and_morty.get_locations()
    except requests.exceptions.Timeout:
        logging.error("Timeout ao buscar as localizações.")
        raise engine_from_config("Timeout ao buscar as localizações.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao buscar as localizações: {e}")
        raise FAILURE(f"Erro ao buscar as localizações: {e}")
    
@task(retries=5, retry_delay_seconds=10, timeout_seconds=5)
def fetch_character_by_id(character_id):
    try:
        return rick_and_morty.get_character_by_id(character_id)
    
    except requests.exceptions.Timeout:
        logging.error("Timeout ao buscar o personagem.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao buscar o personagem: {e}")
        raise FAILURE(f"Erro ao buscar o personagem: {e}")

@task(retries=5, retry_delay_seconds=10, timeout_seconds=5)
def fetch_episodes():
        return rick_and_morty.get_episodes()

@flow
def rick_and_morty_flow():
    characters = fetch_characters()
    locations = fetch_locations()
    character = fetch_character_by_id(1)
    print(f"Quantidade de personagens encontrados 👥: {len(characters['results'])}")
    print(f"Localizações encontradas 🗺️: {len(locations['results'])}")
    print(f"Nome do personagem com ID 1: {character['name']}")
    
if __name__ == "__main__":
    rick_and_morty_flow()