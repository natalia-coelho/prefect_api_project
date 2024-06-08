from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
import requests

@task(retries=3, retry_delay_seconds=10, timeout_seconds=5)
def fetch_characters():
    response = requests.get('https://rickandmortyapi.com/api/character')
    response.raise_for_status()
    return response.json()

@task(retries=3, retry_delay_seconds=10, timeout_seconds=5)
def fetch_locations():
    response = requests.get('https://rickandmortyapi.com/api/location')
    response.raise_for_status()
    return response.json()

@flow
def rick_and_morty_flow():
    characters = fetch_characters()
    locations = fetch_locations()
    print(f"Personagens encontrados: {len(characters['results'])}")
    print(f"Localizações encontradas: {len(locations['results'])}")
    
if __name__ == "__main__":
    rick_and_morty_flow()