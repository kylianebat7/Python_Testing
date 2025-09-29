import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime

def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs

def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        # Filtrer les compétitions à venir (date > heure actuelle)
        current_date = datetime.now()  # Utilise l'heure actuelle au lieu d'une date fixe
        return [comp for comp in listOfCompetitions if datetime.strptime(comp['date'], "%Y-%m-%d %H:%M:%S") > current_date]

app = Flask(__name__)
app.secret_key = 'something_special'

# Charger les données au démarrage
competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form['email']
    club = next((club for club in clubs if club['email'] == email), None)
    if club:
        return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs)
    else:
        flash("Invalid email, please try again.")
        return render_template('index.html')

@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = next((c for c in clubs if c['name'] == club), None)
    foundCompetition = next((c for c in competitions if c['name'] == competition), None)
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs)

@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs if c['name'] == request.form['club']), None)
    if not competition or not club:
        flash("Invalid competition or club.")
        return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs)

    placesRequired = int(request.form['places'])
    competitionPlaces = int(competition['numberOfPlaces'])
    clubPoints = int(club['points'])

    # Vérifications selon Phase 1
    if placesRequired > 12:
        flash("You cannot book more than 12 places at a time.")
    elif placesRequired > competitionPlaces:
        flash("Not enough places available for this competition.")
    elif placesRequired > clubPoints:
        flash("You do not have enough points for this booking.")
    else:
        competition['numberOfPlaces'] = str(competitionPlaces - placesRequired)
        club['points'] = str(clubPoints - placesRequired)
        flash('Great-booking complete! {} places booked.'.format(placesRequired))
        # Sauvegarde des changements dans les fichiers JSON
        with open('clubs.json', 'w') as c:
            json.dump({'clubs': clubs}, c)
        with open('competitions.json', 'w') as comps:
            json.dump({'competitions': competitions}, comps)

    return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs)

# TODO: Add route for points display (Phase 2)
@app.route('/points')
def displayPoints():
    return render_template('points.html', clubs=clubs)  # À implémenter avec un template points.html

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)