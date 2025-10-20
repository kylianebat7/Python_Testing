# Documentation des Tests GUDLFT

## 📁 Structure des Tests

```
tests/
├── __init__.py
├── conftest.py                 # Configuration globale pytest
├── README_TESTS.md            # Cette documentation
├── run_all_tests.py           # Script pour lancer tous les tests
├── fixtures/                  # Données de test
│   ├── clubs_test.json
│   ├── competitions_test.json
│   └── bookings_test.json
├── unitaires/                 # Tests unitaires
│   ├── __init__.py
│   ├── test_chargement_donnees.py
│   └── test_logique_metier.py
├── integration/               # Tests d'intégration
│   ├── __init__.py
│   └── test_routes_flask.py
└── fonctionnels/             # Tests fonctionnels
    ├── __init__.py
    └── test_workflows_complets.py
```

## 🧪 Types de Tests

### Tests Unitaires
Les tests unitaires se concentrent sur des fonctions individuelles :
- **test_chargement_donnees.py** : Tests des fonctions `loadClubs()`, `loadCompetitions()`, `loadBookings()`, `saveBookings()`
- **test_logique_metier.py** : Tests de la logique métier (recherche, validation, calculs)

### Tests d'Intégration  
Les tests d'intégration vérifient l'interaction entre les composants :
- **test_routes_flask.py** : Tests des routes Flask et de leurs interactions

### Tests Fonctionnels
Les tests fonctionnels valident les workflows complets de l'utilisateur :
- **test_workflows_complets.py** : Tests end-to-end des parcours utilisateur

## 🚀 Lancer les Tests

### Méthode 1 : Script Python personnalisé

```bash
# Tous les tests
python tests/run_all_tests.py

# Tests unitaires seulement
python tests/run_all_tests.py --type unitaires

# Tests d'intégration seulement  
python tests/run_all_tests.py --type integration

# Tests fonctionnels seulement
python tests/run_all_tests.py --type fonctionnels

# Avec couverture de code
python tests/run_all_tests.py --coverage

# Mode verbeux
python tests/run_all_tests.py --verbose

# Installer les dépendances et lancer les tests
python tests/run_all_tests.py --install-deps
```

### Méthode 2 : Makefile

```bash
# Installer les dépendances
make install

# Tous les tests
make test

# Tests unitaires
make test-unit

# Tests d'intégration
make test-integration  

# Tests fonctionnels
make test-functional

# Avec couverture
make test-coverage

# Lancer l'application
make run

# Nettoyer les fichiers temporaires
make clean
```

### Méthode 3 : Pytest direct

```bash
# Tous les tests
pytest tests/

# Tests unitaires
pytest tests/unitaires/

# Tests d'intégration
pytest tests/integration/

# Tests fonctionnels
pytest tests/fonctionnels/

# Mode verbeux avec couleurs
pytest tests/ -v --color=yes

# Avec couverture
pytest tests/ --cov=server --cov-report=html
```

## 📊 Rapport de Couverture

Les tests avec couverture génèrent un rapport HTML :
```bash
python tests/run_all_tests.py --coverage
# Ouvrir htmlcov/index.html dans un navigateur
```

## 🔧 Dépendances de Test

Les tests nécessitent les packages suivants :
- `pytest>=7.0.0`
- `pytest-cov>=4.0.0` 
- `pytest-flask>=1.2.0`

Installation automatique :
```bash
python tests/run_all_tests.py --install-deps
```

## 📝 Données de Test (Fixtures)

Les fixtures fournissent des données de test cohérentes :

### Clubs de test
```json
{
  "clubs": [
    {"name": "Club Test 1", "email": "test1@email.com", "points": 15},
    {"name": "Club Test 2", "email": "test2@email.com", "points": 8},
    {"name": "Club Test 3", "email": "test3@email.com", "points": 20}
  ]
}
```

### Compétitions de test
```json
{
  "competitions": [
    {"name": "Compétition Test 1", "date": "2026-08-15 14:00:00", "numberOfPlaces": "25"},
    {"name": "Compétition Test 2", "date": "2026-12-20 10:30:00", "numberOfPlaces": "10"},
    {"name": "Compétition Passée", "date": "2024-01-15 12:00:00", "numberOfPlaces": "0"}
  ]
}
```

## 🎯 Cas de Tests Couverts

### Tests Unitaires
- ✅ Chargement réussi des données
- ✅ Gestion des fichiers inexistants
- ✅ Gestion des JSON invalides
- ✅ Recherche par email/nom
- ✅ Validation des points
- ✅ Logique de réservation

### Tests d'Intégration
- ✅ Routes Flask (GET/POST)
- ✅ Validation des formulaires
- ✅ Gestion des erreurs HTTP
- ✅ Redirections
- ✅ Sessions et contexte

### Tests Fonctionnels
- ✅ Workflow de connexion complet
- ✅ Workflow de réservation complet
- ✅ Navigation entre sections
- ✅ Gestion des échecs
- ✅ Réservations multiples
- ✅ Historique des réservations

## 🐛 Debugging

Pour déboguer les tests :

```bash
# Arrêter au premier échec
pytest tests/ -x

# Mode verbeux avec sorties print
pytest tests/ -v -s

# Lancer un test spécifique
pytest tests/unitaires/test_chargement_donnees.py::TestChargementDonnees::test_loadClubs_succes

# Mode débogage avec pdb
pytest tests/ --pdb
```

## 📈 Métriques de Tests

Les tests visent :
- **Couverture** : >90% du code métier
- **Performance** : Tests rapides (<5 secondes total)
- **Fiabilité** : Tests déterministes et reproductibles
- **Maintenabilité** : Tests clairs et bien documentés

## 🔄 Intégration Continue

Pour intégrer ces tests dans un pipeline CI/CD :

```yaml
# Exemple GitHub Actions
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    pip install pytest pytest-cov pytest-flask

- name: Run tests
  run: |
    python tests/run_all_tests.py --coverage
```
