import sys
import os
import pytest
from unittest.mock import patch
from prefect.testing.utilities import prefect_test_harness

# ensure src module is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from flows import (
    fetch_characters, 
    fetch_locations, 
    fetch_character_by_id, 
    fetch_episodes, 
    list_character_names, 
    list_all_episodes, 
    rick_and_morty_flow
)

# mocking the data
mock_characters = {
    'results': [{'name': 'Rick Sanchez'}, {'name': 'Morty Smith'}]
}

mock_locations = {
    'results': [{'name': 'Earth'}, {'name': 'Gazorpazorp'}]
}

mock_episodes = {
    'results': [{'name': 'Pilot'}, {'name': 'Lawnmower Dog'}]
}

@pytest.fixture
def mock_rick_and_morty():
    with patch('flows.rick_and_morty.get_characters', return_value=mock_characters) as mock_get_characters, \
         patch('flows.rick_and_morty.get_locations', return_value=mock_locations) as mock_get_locations, \
         patch('flows.rick_and_morty.get_episodes', return_value=mock_episodes) as mock_get_episodes:
        yield {
            'get_characters': mock_get_characters,
            'get_locations': mock_get_locations,
            'get_episodes': mock_get_episodes
        }

@pytest.fixture
def mock_time():
    with patch('flows.time.sleep', return_value=None), \
         patch('flows.random.randint', return_value=1):
        yield

def test_fetch_characters(mock_rick_and_morty, mock_time):
    result = fetch_characters()
    assert result == mock_characters

def test_fetch_locations(mock_rick_and_morty):
    result = fetch_locations()
    assert result == mock_locations

def test_fetch_character_by_id(mock_rick_and_morty):
    character_id = 1
    mock_character = {'name': 'Rick Sanchez'}
    with patch('flows.rick_and_morty.get_character_by_id', return_value=mock_character):
        result = fetch_character_by_id(character_id)
        assert result == mock_character

def test_fetch_episodes(mock_rick_and_morty):
    result = fetch_episodes()
    assert result == mock_episodes

def test_list_character_names(mock_rick_and_morty, capsys):
    list_character_names(mock_characters)
    captured = capsys.readouterr()
    assert "Rick Sanchez" in captured.out
    assert "Morty Smith" in captured.out

def test_list_all_episodes(mock_rick_and_morty, capsys):
    list_all_episodes(mock_episodes)
    captured = capsys.readouterr()
    assert "Pilot" in captured.out
    assert "Lawnmower Dog" in captured.out

def test_rick_and_morty_flow(mock_rick_and_morty, mock_time, capsys):
    with prefect_test_harness():
        rick_and_morty_flow()
    captured = capsys.readouterr()
    assert "Quantidade de personagens encontrados 👥: 2" in captured.out
    assert "Localizações encontradas 🗺️: 2" in captured.out
    assert "Listando todos os personagens: " in captured.out
    assert "Rick Sanchez" in captured.out
    assert "Morty Smith" in captured.out
    assert "Listando todos os episódios: " in captured.out
    assert "Pilot" in captured.out
    assert "Lawnmower Dog" in captured.out
