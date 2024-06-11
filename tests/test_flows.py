from unittest.mock import patch
from flows import rick_and_morty_flow

def test_rick_and_morty_flow():
    with patch('src.flows.fetch_characters') as mock_fetch_characters, \
        patch('src.flows.fetch_locations') as mock_fetch_locations:
            
            mock_fetch_characters.return_value = {'results': [1, 2, 3]}
            mock_fetch_locations.return_value = {'results': [1, 2]}
            
            rick_and_morty_flow()
            
            mock_fetch_characters.assert_called_once()
            mock_fetch_locations.assert_called_once()