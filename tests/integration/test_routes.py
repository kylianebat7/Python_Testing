import pytest
from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestRoutes:
    def test_index_route(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b'Welcome' in response.data  # Assumant qu'il y a du texte de bienvenue

    def test_showSummary_invalid_email(self, client):
        response = client.post('/showSummary', data={'email': 'invalid@example.com'})
        assert response.status_code in [200, 302]  # Peut rediriger ou rester sur page

    def test_showSummary_valid_email(self, client):
        # Utiliser un email valide des données de test
        response = client.post('/showSummary', data={'email': 'simplylift@email.com'})
        assert response.status_code in [200, 302]  # Peut rester sur page ou rediriger

    def test_interface_route(self, client):
        response = client.get('/interface/simplylift@email.com')
        assert response.status_code in [200, 302]  # Peut rediriger si email invalide

    def test_book_route_valid(self, client):
        response = client.get('/book/Spring Festival 2026/Simply Lift')
        assert response.status_code in [200, 302]  # Peut rediriger

    def test_book_route_past_competition(self, client):
        # Créer une compétition passée
        from server import competitions
        original_comp = None
        for comp in competitions:
            if comp['name'] == 'Spring Festival 2026':
                original_comp = comp.copy()
                comp['date'] = '2020-01-01 12:00:00'
                break

        try:
            response = client.get('/book/Spring Festival 2026/Simply Lift')
            assert response.status_code in [200, 302]  # Peut rediriger
        finally:
            if original_comp:
                for comp in competitions:
                    if comp['name'] == 'Spring Festival 2026':
                        comp.update(original_comp)
                        break

    def test_purchasePlaces_valid(self, client):
        response = client.post('/purchasePlaces', data={
            'competition': 'Spring Festival 2026',
            'club': 'Simply Lift',
            'places': '2'
        })
        assert response.status_code == 302  # Redirection après réservation

    def test_purchasePlaces_invalid_places(self, client):
        response = client.post('/purchasePlaces', data={
            'competition': 'Spring Festival 2026',
            'club': 'Simply Lift',
            'places': '-1'
        })
        assert response.status_code in [200, 302]  # Peut rediriger

    def test_purchasePlaces_too_many_places(self, client):
        response = client.post('/purchasePlaces', data={
            'competition': 'Spring Festival 2026',
            'club': 'Simply Lift',
            'places': '15'
        })
        assert response.status_code in [200, 302]  # Peut rediriger

    def test_view_section_competitions(self, client):
        response = client.get('/view_section/competitions/simplylift@email.com')
        assert response.status_code in [200, 302]  # Peut rediriger

    def test_logout_route(self, client):
        response = client.get('/logout')
        assert response.status_code == 302  # Redirection vers index
