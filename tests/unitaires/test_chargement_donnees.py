"""
Tests unitaires pour les fonctions de chargement des données
"""
import pytest
import json
import os
import tempfile
from unittest.mock import patch, mock_open
import sys

# Ajouter le répertoire parent au path pour importer server
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from server import loadClubs, loadCompetitions, loadBookings, saveBookings


class TestChargementDonnees:
    """Classe de tests pour les fonctions de chargement des données"""

    def test_loadClubs_succes(self, clubs_test_data):
        """Test le chargement réussi des clubs"""
        # Préparer les données JSON simulées
        mock_json_data = {'clubs': clubs_test_data}
        
        with patch('builtins.open', mock_open(read_data=json.dumps(mock_json_data))):
            with patch('json.load', return_value=mock_json_data):
                clubs = loadClubs()
                
                assert len(clubs) == 3
                assert clubs[0]['name'] == 'Club Test 1'
                assert clubs[0]['email'] == 'test1@email.com'
                assert clubs[0]['points'] == 15
                assert clubs[1]['name'] == 'Club Test 2'
                assert clubs[2]['name'] == 'Club Test 3'

    def test_loadClubs_fichier_inexistant(self):
        """Test le comportement quand le fichier clubs.json n'existe pas"""
        with patch('builtins.open', side_effect=FileNotFoundError):
            with pytest.raises(FileNotFoundError):
                loadClubs()

    def test_loadClubs_json_invalide(self):
        """Test le comportement avec un JSON invalide"""
        with patch('builtins.open', mock_open(read_data='invalid json')):
            with patch('json.load', side_effect=json.JSONDecodeError('msg', 'doc', 0)):
                with pytest.raises(json.JSONDecodeError):
                    loadClubs()

    def test_loadCompetitions_succes(self, competitions_test_data):
        """Test le chargement réussi des compétitions"""
        mock_json_data = {'competitions': competitions_test_data}
        
        with patch('builtins.open', mock_open(read_data=json.dumps(mock_json_data))):
            with patch('json.load', return_value=mock_json_data):
                competitions = loadCompetitions()
                
                assert len(competitions) == 3
                assert competitions[0]['name'] == 'Competition Test 1'
                assert competitions[0]['numberOfPlaces'] == '25'
                assert competitions[1]['name'] == 'Competition Test 2'
                assert competitions[2]['name'] == 'Competition Passee'

    def test_loadCompetitions_fichier_inexistant(self):
        """Test le comportement quand le fichier competitions.json n'existe pas"""
        with patch('builtins.open', side_effect=FileNotFoundError):
            with pytest.raises(FileNotFoundError):
                loadCompetitions()

    def test_loadBookings_succes(self, bookings_test_data):
        """Test le chargement réussi des réservations"""
        mock_json_data = {'bookings': bookings_test_data}
        
        with patch('builtins.open', mock_open(read_data=json.dumps(mock_json_data))):
            with patch('json.load', return_value=mock_json_data):
                bookings = loadBookings()
                
                assert len(bookings) == 2
                assert bookings[0]['club_name'] == 'Club Test 1'
                assert bookings[0]['competition_name'] == 'Competition Test 1'
                assert bookings[0]['places'] == 5
                assert bookings[1]['club_name'] == 'Club Test 2'

    def test_loadBookings_fichier_inexistant(self):
        """Test le comportement quand le fichier bookings.json n'existe pas"""
        with patch('builtins.open', side_effect=FileNotFoundError):
            bookings = loadBookings()
            # Doit retourner une liste vide si le fichier n'existe pas
            assert bookings == []

    def test_loadBookings_json_invalide(self):
        """Test le comportement avec un JSON invalide pour les bookings"""
        with patch('builtins.open', mock_open(read_data='invalid json')):
            with patch('json.load', side_effect=json.JSONDecodeError('msg', 'doc', 0)):
                # loadBookings ne gère pas JSONDecodeError, donc l'erreur se propage
                with pytest.raises(json.JSONDecodeError):
                    loadBookings()

    def test_loadBookings_cle_manquante(self):
        """Test le comportement quand la clé 'bookings' est manquante"""
        mock_json_data = {'autre_cle': []}
        
        with patch('builtins.open', mock_open(read_data=json.dumps(mock_json_data))):
            with patch('json.load', return_value=mock_json_data):
                bookings = loadBookings()
                # get() avec valeur par défaut [] doit fonctionner
                assert bookings == []

    def test_saveBookings_succes(self, bookings_test_data):
        """Test la sauvegarde réussie des réservations"""
        with patch('builtins.open', mock_open()) as mock_file:
            with patch('json.dump') as mock_json_dump:
                saveBookings(bookings_test_data)
                
                # Vérifier que le fichier a été ouvert en mode écriture
                mock_file.assert_called_once_with('bookings.json', 'w')
                # Vérifier que json.dump a été appelé avec les bonnes données
                mock_json_dump.assert_called_once_with({'bookings': bookings_test_data}, mock_file.return_value.__enter__.return_value)

    def test_saveBookings_liste_vide(self):
        """Test la sauvegarde d'une liste vide de réservations"""
        with patch('builtins.open', mock_open()) as mock_file:
            with patch('json.dump') as mock_json_dump:
                saveBookings([])
                
                mock_file.assert_called_once_with('bookings.json', 'w')
                mock_json_dump.assert_called_once_with({'bookings': []}, mock_file.return_value.__enter__.return_value)

    def test_saveBookings_erreur_ecriture(self, bookings_test_data):
        """Test le comportement lors d'une erreur d'écriture"""
        with patch('builtins.open', side_effect=PermissionError("Permission denied")):
            with pytest.raises(PermissionError):
                saveBookings(bookings_test_data)
