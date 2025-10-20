"""
Configuration pytest pour tous les tests
"""
import pytest
import json
import os
import tempfile
import sys
from unittest.mock import patch

# Ajouter le répertoire parent au path pour importer server
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import server


@pytest.fixture
def app():
    """Fixture pour créer l'application Flask pour les tests"""
    server.app.config['TESTING'] = True
    server.app.config['SECRET_KEY'] = 'test_secret_key'
    return server.app


@pytest.fixture
def client(app):
    """Fixture pour créer un client de test Flask"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Fixture pour créer un runner de commandes Flask"""
    return app.test_cli_runner()


@pytest.fixture
def clubs_test_data():
    """Fixture pour les données de test des clubs"""
    fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'clubs_test.json')
    with open(fixture_path, 'r', encoding='utf-8') as f:
        return json.load(f)['clubs']


@pytest.fixture
def competitions_test_data():
    """Fixture pour les données de test des compétitions"""
    fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'competitions_test.json')
    with open(fixture_path, 'r', encoding='utf-8') as f:
        return json.load(f)['competitions']


@pytest.fixture
def bookings_test_data():
    """Fixture pour les données de test des réservations"""
    fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'bookings_test.json')
    with open(fixture_path, 'r', encoding='utf-8') as f:
        return json.load(f)['bookings']


@pytest.fixture
def mock_data_files(clubs_test_data, competitions_test_data, bookings_test_data):
    """Fixture pour mocker les fichiers de données avec des données de test"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Créer des fichiers temporaires avec les données de test
        clubs_file = os.path.join(temp_dir, 'clubs.json')
        competitions_file = os.path.join(temp_dir, 'competitions.json')
        bookings_file = os.path.join(temp_dir, 'bookings.json')
        
        with open(clubs_file, 'w', encoding='utf-8') as f:
            json.dump({'clubs': clubs_test_data}, f)
        
        with open(competitions_file, 'w', encoding='utf-8') as f:
            json.dump({'competitions': competitions_test_data}, f)
        
        with open(bookings_file, 'w', encoding='utf-8') as f:
            json.dump({'bookings': bookings_test_data}, f)
        
        # Patcher les fonctions de chargement pour utiliser nos fichiers de test
        with patch('server.loadClubs') as mock_load_clubs, \
             patch('server.loadCompetitions') as mock_load_competitions, \
             patch('server.loadBookings') as mock_load_bookings:
            
            mock_load_clubs.return_value = clubs_test_data
            mock_load_competitions.return_value = competitions_test_data
            mock_load_bookings.return_value = bookings_test_data
            
            yield {
                'clubs': clubs_test_data,
                'competitions': competitions_test_data,
                'bookings': bookings_test_data,
                'temp_dir': temp_dir
            }


@pytest.fixture(autouse=True)
def reset_server_data():
    """Fixture pour réinitialiser les données du serveur après chaque test"""
    yield
    # Recharger les données originales après chaque test
    server.competitions = server.loadCompetitions()
    server.clubs = server.loadClubs()
    server.bookings = server.loadBookings()
