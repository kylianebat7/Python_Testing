import json
import pytest
import os
import tempfile
from datetime import datetime, timedelta
from server import (
    loadClubs, loadCompetitions, loadBookings, saveBookings, saveClubs, saveCompetitions,
    refresh_competitions, is_competition_past
)


class TestLoadClubs:
    def test_loadClubs_returns_list(self):
        clubs = loadClubs()
        assert isinstance(clubs, list)
        assert len(clubs) > 0
        assert all(isinstance(club, dict) for club in clubs)
        assert all('name' in club and 'email' in club and 'points' in club for club in clubs)


class TestLoadCompetitions:
    def test_loadCompetitions_returns_list(self):
        competitions = loadCompetitions()
        assert isinstance(competitions, list)
        # Note : Peut être vide si competitions.json est vide, donc pas d'assertion sur la longueur


class TestLoadBookings:
    def test_loadBookings_returns_list_when_file_exists(self):
        bookings = loadBookings()
        assert isinstance(bookings, list)

    def test_loadBookings_returns_empty_list_when_file_not_exists(self):
        # Sauvegarder le fichier original
        original_exists = os.path.exists('bookings.json')
        original_content = None
        if original_exists:
            with open('bookings.json', 'r') as f:
                original_content = f.read()
            os.remove('bookings.json')

        try:
            bookings = loadBookings()
            assert bookings == []
        finally:
            # Restaurer le fichier
            if original_content is not None:
                with open('bookings.json', 'w') as f:
                    f.write(original_content)


class TestSaveBookings:
    def test_saveBookings_saves_to_file(self):
        test_bookings = [{'test': 'data'}]
        saveBookings(test_bookings)
        with open('bookings.json', 'r') as f:
            saved_data = json.load(f)
        assert saved_data['bookings'] == test_bookings


class TestSaveClubs:
    def test_saveClubs_saves_to_file(self):
        test_clubs = [{'name': 'Test Club', 'email': 'test@example.com', 'points': 10}]
        saveClubs(test_clubs)
        with open('clubs.json', 'r') as f:
            saved_data = json.load(f)
        assert saved_data['clubs'] == test_clubs


class TestSaveCompetitions:
    def test_saveCompetitions_saves_to_file(self):
        test_competitions = [{'name': 'Test Comp', 'date': '2025-12-31 12:00:00', 'numberOfPlaces': '10'}]
        saveCompetitions(test_competitions)
        with open('competitions.json', 'r') as f:
            saved_data = json.load(f)
        assert saved_data['competitions'] == test_competitions


class TestRefreshCompetitions:
    def test_refresh_competitions_updates_isPast(self):
        # Sauvegarder les données originales
        original_competitions = loadCompetitions()
        original_bookings = loadBookings()
        original_clubs = loadClubs()
        
        if original_competitions:
            # Modifier la première compétition pour avoir une date passée
            modified_comp = original_competitions[0].copy()
            modified_comp['date'] = '2020-01-01 12:00:00'  # Date passée
            saveCompetitions([modified_comp] + original_competitions[1:])

            try:
                refresh_competitions()
                # Vérifier que isPast est ajouté et correct dans la variable globale
                from server import competitions
                updated_comp = next(c for c in competitions if c['name'] == modified_comp['name'])
                assert 'isPast' in updated_comp
                assert updated_comp['isPast'] == True
            finally:
                # Restaurer les données originales
                saveCompetitions(original_competitions)
                saveBookings(original_bookings)
                saveClubs(original_clubs)


class TestIsCompetitionPast:
    def test_is_competition_past_returns_true_for_past_date(self):
        past_competition = {'date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')}
        assert is_competition_past(past_competition) == True

    def test_is_competition_past_returns_false_for_future_date(self):
        future_competition = {'date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')}
        assert is_competition_past(future_competition) == False

    def test_is_competition_past_returns_true_for_invalid_date(self):
        invalid_competition = {'date': 'invalid_date'}
        assert is_competition_past(invalid_competition) == True

    def test_is_competition_past_returns_true_for_empty_date(self):
        empty_competition = {}
        assert is_competition_past(empty_competition) == True
