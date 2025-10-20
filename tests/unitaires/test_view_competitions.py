import pytest
import json
import os
from unittest.mock import patch
from view_competitions import display_competitions


class TestDisplayCompetitions:
    def test_display_competitions_with_valid_file(self, capsys):
        # Utiliser les données existantes
        display_competitions()
        captured = capsys.readouterr()
        assert "LISTE DES COMPETITIONS GUDLFT" in captured.out
        assert "Nombre total de compétitions" in captured.out

    def test_display_competitions_handles_missing_file(self, capsys):
        # Renommer temporairement le fichier
        original_exists = os.path.exists('competitions.json')
        if original_exists:
            os.rename('competitions.json', 'competitions_backup.json')
        try:
            display_competitions()
            captured = capsys.readouterr()
            assert "Fichier competitions.json introuvable!" in captured.out
        finally:
            if original_exists:
                os.rename('competitions_backup.json', 'competitions.json')

    def test_display_competitions_handles_invalid_json(self, capsys):
        # Créer un fichier JSON invalide
        with open('competitions.json', 'w') as f:
            f.write('invalid json')
        try:
            display_competitions()
            captured = capsys.readouterr()
            assert "Erreur dans le JSON" in captured.out
        finally:
            # Restaurer le fichier original
            with open('competitions.json', 'w') as f:
                json.dump({'competitions': []}, f)
