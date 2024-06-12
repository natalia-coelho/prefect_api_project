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

@flow
def rick_and_morty_flow():
    characters = fetch_characters()
    locations = fetch_locations()
    character = fetch_character_by_id(1)
    print(f"Quantidade de personagens encontrados 👥: {len(characters['results'])}")
    print(f"Localizações encontradas 🗺️: {len(locations['results'])}")
    print(f"Nome do personagem com ID 1: {character['name']}")