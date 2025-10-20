"""
Script pour lancer tous les tests de l'application GUDLFT
"""
import os
import sys
import subprocess
import argparse


def run_tests(test_type="all", verbose=False, coverage=False):
    """
    Lance les tests selon le type spécifié
    
    Args:
        test_type (str): Type de tests à lancer ('all', 'unitaires', 'integration', 'fonctionnels')
        verbose (bool): Mode verbeux
        coverage (bool): Générer un rapport de couverture
    """
    
    # Se placer dans le répertoire du projet
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    
    # Commande de base pytest
    cmd = ["python", "-m", "pytest"]
    
    # Ajouter le répertoire de tests selon le type
    if test_type == "unitaires":
        cmd.append("tests/unitaires/")
        print("Lancement des tests unitaires...")
    elif test_type == "integration":
        cmd.append("tests/integration/")
        print("Lancement des tests d'intégration...")
    elif test_type == "fonctionnels":
        cmd.append("tests/fonctionnels/")
        print("Lancement des tests fonctionnels...")
    else:
        cmd.append("tests/")
        print("Lancement de tous les tests...")
    
    # Options pytest
    if verbose:
        cmd.extend(["-v", "-s"])
    
    if coverage:
        cmd.extend(["--cov=server", "--cov-report=html", "--cov-report=term"])
    
    # Ajouter des options pour une meilleure lisibilité
    cmd.extend([
        "--tb=short",  # Traceback plus court
        "--color=yes",  # Couleurs
        "-x"  # Arrêter au premier échec
    ])
    
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except Exception as e:
        print(f"[ERREUR] Erreur lors de l'exécution des tests: {e}")
        return 1


def install_dependencies():
    """Installe les dépendances nécessaires pour les tests"""
    print("Installation des dépendances de test...")
    
    dependencies = [
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
        "pytest-flask>=1.2.0"
    ]
    
    for dep in dependencies:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                         check=True, capture_output=True)
            print(f"[OK] {dep} installé avec succès")
        except subprocess.CalledProcessError as e:
            print(f"[ERREUR] Erreur lors de l'installation de {dep}: {e}")
            return False
    
    return True


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Lanceur de tests pour GUDLFT")
    
    parser.add_argument(
        "--type", "-t",
        choices=["all", "unitaires", "integration", "fonctionnels"],
        default="all",
        help="Type de tests à lancer (défaut: all)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Mode verbeux"
    )
    
    parser.add_argument(
        "--coverage", "-c",
        action="store_true",
        help="Générer un rapport de couverture"
    )
    
    parser.add_argument(
        "--install-deps",
        action="store_true",
        help="Installer les dépendances de test avant de lancer les tests"
    )
    
    args = parser.parse_args()
    
    print("GUDLFT - Lanceur de Tests")
    print("=" * 50)
    
    # Installer les dépendances si demandé
    if args.install_deps:
        if not install_dependencies():
            print("[ERREUR] Échec de l'installation des dépendances")
            return 1
        print()
    
    # Lancer les tests
    return_code = run_tests(args.type, args.verbose, args.coverage)
    
    if return_code == 0:
        print("\n[SUCCES] Tous les tests sont passés avec succès!")
        if args.coverage:
            print("[INFO] Rapport de couverture généré dans htmlcov/index.html")
    else:
        print(f"\n[ECHEC] Certains tests ont échoué (code de retour: {return_code})")
    
    return return_code


if __name__ == "__main__":
    sys.exit(main())
