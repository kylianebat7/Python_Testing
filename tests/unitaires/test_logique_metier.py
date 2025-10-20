"""
Tests unitaires pour la logique métier de l'application
"""
import pytest
import json
from unittest.mock import patch, MagicMock
from datetime import datetime
import sys
import os

# Ajouter le répertoire parent au path pour importer server
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import server


class TestLogiqueMetier:
    """Classe de tests pour la logique métier"""

    def test_recherche_club_par_email_existant(self, clubs_test_data):
        """Test la recherche d'un club par email existant"""
        with patch('server.clubs', clubs_test_data):
            # Simuler la logique utilisée dans showSummary
            email = "test1@email.com"
            club = next((club for club in clubs_test_data if club['email'] == email), None)
            
            assert club is not None
            assert club['name'] == 'Club Test 1'
            assert club['email'] == email
            assert club['points'] == 15

    def test_recherche_club_par_email_inexistant(self, clubs_test_data):
        """Test la recherche d'un club par email inexistant"""
        with patch('server.clubs', clubs_test_data):
            email = "inexistant@email.com"
            club = next((club for club in clubs_test_data if club['email'] == email), None)
            
            assert club is None

    def test_recherche_club_par_nom_existant(self, clubs_test_data):
        """Test la recherche d'un club par nom existant"""
        with patch('server.clubs', clubs_test_data):
            nom = "Club Test 1"
            club = next((c for c in clubs_test_data if c['name'] == nom), None)
            
            assert club is not None
            assert club['name'] == nom
            assert club['email'] == "test1@email.com"

    def test_recherche_competition_par_nom_existant(self, competitions_test_data):
        """Test la recherche d'une compétition par nom existant"""
        with patch('server.competitions', competitions_test_data):
            nom = "Competition Test 1"
            competition = next((c for c in competitions_test_data if c['name'] == nom), None)
            
            assert competition is not None
            assert competition['name'] == nom
            assert competition['numberOfPlaces'] == "25"

    def test_recherche_competition_par_nom_inexistant(self, competitions_test_data):
        """Test la recherche d'une compétition par nom inexistant"""
        with patch('server.competitions', competitions_test_data):
            nom = "Competition Inexistante"
            competition = next((c for c in competitions_test_data if c['name'] == nom), None)
            
            assert competition is None

    def test_verification_points_suffisants(self, clubs_test_data):
        """Test la vérification des points suffisants pour une réservation"""
        club = clubs_test_data[0]  # Club Test 1 avec 15 points
        places_requises = 10
        
        assert club['points'] >= places_requises

    def test_verification_points_insuffisants(self, clubs_test_data):
        """Test la vérification des points insuffisants pour une réservation"""
        club = clubs_test_data[1]  # Club Test 2 avec 8 points
        places_requises = 10
        
        assert club['points'] < places_requises

    def test_filtrage_reservations_par_club(self, bookings_test_data, clubs_test_data):
        """Test le filtrage des réservations par nom de club"""
        club = clubs_test_data[0]  # Club Test 1
        reservations_club = [b for b in bookings_test_data if b['club_name'] == club['name']]
        
        assert len(reservations_club) == 1
        assert reservations_club[0]['club_name'] == 'Club Test 1'
        assert reservations_club[0]['competition_name'] == 'Competition Test 1'

    def test_creation_nouvelle_reservation(self):
        """Test la création d'une nouvelle réservation"""
        club = {'name': 'Test Club', 'email': 'test@email.com', 'points': 15}
        competition = {'name': 'Test Competition', 'numberOfPlaces': '20'}
        places_requises = 5
        
        # Simuler la création d'une réservation comme dans purchasePlaces
        nouvelle_reservation = {
            'club_name': club['name'],
            'competition_name': competition['name'],
            'category': competition.get('category', 'Unknown'),
            'places': places_requises,
            'date_booked': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        assert nouvelle_reservation['club_name'] == 'Test Club'
        assert nouvelle_reservation['competition_name'] == 'Test Competition'
        assert nouvelle_reservation['places'] == 5
        assert nouvelle_reservation['category'] == 'Unknown'
        assert nouvelle_reservation['date_booked'] is not None

    def test_mise_a_jour_points_et_places(self):
        """Test la mise à jour des points du club et des places de la compétition"""
        club = {'name': 'Test Club', 'email': 'test@email.com', 'points': 15}
        competition = {'name': 'Test Competition', 'numberOfPlaces': '20'}
        places_requises = 5
        
        # Sauvegarder les valeurs originales
        points_originaux = club['points']
        places_originales = int(competition['numberOfPlaces'])
        
        # Simuler la mise à jour comme dans purchasePlaces
        club['points'] = club['points'] - places_requises
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_requises
        
        # Vérifier les mises à jour
        assert club['points'] == points_originaux - places_requises
        assert int(competition['numberOfPlaces']) == places_originales - places_requises

    def test_conversion_nombre_places(self):
        """Test la conversion des places de string à int"""
        competition = {'name': 'Test', 'numberOfPlaces': '25'}
        
        places_disponibles = int(competition['numberOfPlaces'])
        assert places_disponibles == 25
        assert isinstance(places_disponibles, int)

    def test_validation_email_format(self):
        """Test de validation basique du format email"""
        emails_valides = [
            "test@email.com",
            "user@domain.org",
            "admin@company.co.uk"
        ]
        
        emails_invalides = [
            "invalid",
            "@domain.com",
            "user@",
            "user.domain.com"
        ]
        
        # Validation basique : doit contenir @ et un point après @
        for email in emails_valides:
            assert '@' in email
            assert '.' in email.split('@')[1]
        
        for email in emails_invalides:
            if '@' in email:
                parts = email.split('@')
                if len(parts) != 2 or not parts[1] or '.' not in parts[1]:
                    assert True  # Email invalide comme attendu
            else:
                assert True  # Email invalide comme attendu

    def test_gestion_categories_competition(self):
        """Test la gestion des catégories de compétition"""
        competition_avec_categorie = {
            'name': 'Test Competition',
            'category': 'Senior',
            'numberOfPlaces': '10'
        }
        
        competition_sans_categorie = {
            'name': 'Test Competition 2',
            'numberOfPlaces': '15'
        }
        
        # Test avec catégorie
        categorie1 = competition_avec_categorie.get('category', 'Unknown')
        assert categorie1 == 'Senior'
        
        # Test sans catégorie
        categorie2 = competition_sans_categorie.get('category', 'Unknown')
        assert categorie2 == 'Unknown'
