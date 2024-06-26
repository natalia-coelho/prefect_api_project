from asyncio import sleep
from random import randrange
import random
from requests import Timeout
from prefect import flow, task, get_run_logger
from sqlalchemy import engine_from_config
import time
import rick_and_morty
import logging

logging.basicConfig(level=logging.INFO)

@task(log_prints=True, retries=5, retry_delay_seconds=5, timeout_seconds=5)
def fetch_characters():
    time.sleep(random.randint(1, 100)) # simulating random timeouts 
    return rick_and_morty.get_characters()
    
@task(retries=5, retry_delay_seconds=10, timeout_seconds=5)
def fetch_locations():
    return rick_and_morty.get_locations()
    
@task(retries=5, retry_delay_seconds=10, timeout_seconds=5)
def fetch_character_by_id(character_id):
    return rick_and_morty.get_character_by_id(character_id)
    
@task(retries=5, retry_delay_seconds=10, timeout_seconds=5)
def fetch_episodes():
    return rick_and_morty.get_episodes()

@task(log_prints=True)
def list_character_names(characters):
    for character in characters['results']:
        print(f"{character['name']}")
        
@task(log_prints=True)
def list_all_episodes(episodes):
    for episode in episodes['results']:
        print(f"{episode['name']}")
        
@flow(timeout_seconds=1)
def rick_and_morty_flow():
    characters = fetch_characters()
    locations = fetch_locations()
    episodes = fetch_episodes()
    print(f"Quantidade de personagens encontrados 👥: {len(characters['results'])}")
    print(f"Localizações encontradas 🗺️: {len(locations['results'])}")
    print("Listando todos os personagens: ")
    list_character_names(characters)
    
    print("Listando todos os episódios: ")
    list_all_episodes(episodes)
    
    