import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'something_special'

def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs

def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions

def loadBookings():
    try:
        with open('bookings.json') as b:
            return json.load(b).get('bookings', [])
    except FileNotFoundError:
        return []

def saveBookings(bookings):
    with open('bookings.json', 'w') as b:
        json.dump({'bookings': bookings}, b)

# Permet de rafraîchir la liste des compétitions depuis le fichier JSON
def refresh_competitions():
    global competitions
    competitions = loadCompetitions()
    # Annoter chaque compétition avec un indicateur de date passée
    for comp in competitions:
        try:
            comp_date = datetime.strptime(comp.get('date', ''), '%Y-%m-%d %H:%M:%S')
            comp['isPast'] = comp_date < datetime.now()
        except Exception:
            # En cas de date invalide, considérer comme indisponible
            comp['isPast'] = True

def is_competition_past(competition: dict) -> bool:
    """Retourne True si la compétition est passée (date < maintenant)."""
    try:
        comp_date = datetime.strptime(competition.get('date', ''), '%Y-%m-%d %H:%M:%S')
        return comp_date < datetime.now()
    except Exception:
        return True

# Charger les données au démarrage
competitions = loadCompetitions()
clubs = loadClubs()
bookings = loadBookings()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form['email']
    club = next((club for club in clubs if club['email'] == email), None)
    if club:
        return redirect(url_for('interface', email=email))
    else:
        flash("Invalid email, please try again.")
        return render_template('index.html')

@app.route('/interface/<email>')
def interface(email):
    # S'assurer que les nouvelles compétitions ajoutées au fichier sont visibles
    refresh_competitions()
    club = next((club for club in clubs if club['email'] == email), None)
    if not club:
        flash("Invalid email, please try again.")
        return redirect(url_for('index'))
    user_bookings = [b for b in bookings if b['club_name'] == club['name']]
    return render_template('interface.html', club=club, competitions=competitions, clubs=clubs, bookings=user_bookings)

@app.route('/book/<competition>/<club>')
def book(competition, club):
    # Rafraîchir pour prendre en compte d'éventuelles nouvelles compétitions
    refresh_competitions()
    foundClub = next((c for c in clubs if c['name'] == club), None)
    foundCompetition = next((c for c in competitions if c['name'] == competition), None)
    if foundClub and foundCompetition:
        # Interdire la réservation si la compétition est passée
        if is_competition_past(foundCompetition):
            flash('This competition is closed because the date has passed.')
            return redirect(url_for('interface', email=foundClub['email']))
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return redirect(url_for('interface', email=foundClub['email'] if foundClub else club))

@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs if c['name'] == request.form['club']), None)
    if not competition or not club:
        flash("Invalid competition or club.")
        return redirect(url_for('interface', email=club['email'] if club else ''))
    # Vérifier que la compétition n'est pas passée
    if is_competition_past(competition):
        flash('This competition is closed because the date has passed.')
        return redirect(url_for('interface', email=club['email']))

    # Validation de l'input
    try:
        placesRequired = int(request.form['places'])
    except (TypeError, ValueError):
        flash('Invalid number of places.')
        return redirect(url_for('interface', email=club['email']))

    if placesRequired <= 0:
        flash('Number of places must be greater than 0.')
        return redirect(url_for('interface', email=club['email']))

    # Vérifier le stock disponible
    try:
        available = int(competition['numberOfPlaces'])
    except (TypeError, ValueError):
        available = 0
    if placesRequired > available:
        flash('Not enough places available for this competition.')
        return redirect(url_for('interface', email=club['email']))
    if club['points'] >= placesRequired:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        club['points'] = club['points'] - placesRequired
        # Enregistrer la réservation dans l'historique
        new_booking = {
            'club_name': club['name'],
            'competition_name': competition['name'],
            'category': competition.get('category', 'Unknown'),  # Ajoute une catégorie si disponible
            'places': placesRequired,
            'date_booked': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        bookings.append(new_booking)
        saveBookings(bookings)
        flash('Great-booking complete!')
    else:
        flash('Not enough points to complete the booking.')
    return redirect(url_for('interface', email=club['email']))

@app.route('/view_section/<section>/<email>')
def view_section(section, email):
    # Rafraîchir la liste des compétitions au besoin
    if section == 'competitions':
        refresh_competitions()
    club = next((club for club in clubs if club['email'] == email), None)
    if not club:
        flash("Invalid email, please try again.")
        return redirect(url_for('index'))
    if section == 'competitions':
        return render_template('section_competitions.html', club=club, competitions=competitions)
    elif section == 'points':
        return render_template('section_points.html', club=club)
    elif section == 'clubs_table':
        return render_template('section_clubs_table.html', club=club, clubs=clubs)
    else:
        flash("Section not found.")
        return redirect(url_for('interface', email=email))

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)