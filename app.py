from flask import Flask, render_template, request, jsonify
from models import db, Tournament, Team, Venue, TournamentTeam, TournamentVenue
import os

app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "tournaments.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

@app.route('/')
def index():
    """Home page showing recent tournaments"""
    tournaments = Tournament.query.order_by(Tournament.start_date.desc()).limit(10).all()
    return render_template('index.html', tournaments=tournaments)

@app.route('/tournament/<int:tournament_id>')
def tournament_detail(tournament_id):
    """Individual tournament detail page"""
    tournament = Tournament.query.get_or_404(tournament_id)
    
    # Get teams for this tournament
    teams = db.session.query(Team, TournamentTeam).join(
        TournamentTeam, Team.team_id == TournamentTeam.team_id
    ).filter(TournamentTeam.tournament_id == tournament_id).all()
    
    # Get venues for this tournament
    venues = db.session.query(Venue, TournamentVenue).join(
        TournamentVenue, Venue.venue_id == TournamentVenue.venue_id
    ).filter(TournamentVenue.tournament_id == tournament_id).all()

    # Winner and Runner Ups for this tournament
    winner_team = tournament.winner_team if tournament.winner_id else None
    runner_up_team = tournament.runner_up_team if tournament.runner_up_id else None

    return render_template('tournament_detail.html', 
                         tournament=tournament, teams=teams, venues=venues)

@app.route('/teams')
def teams():
    """All teams page"""
    teams = Team.query.order_by(Team.team_name).all()
    return render_template('teams.html', teams=teams)

@app.route('/venues')
def venues():
    """All venues page"""
    venues = Venue.query.order_by(Venue.venue_name).all()
    return render_template('venues.html', venues=venues)

@app.route('/map')
def map_view():
    """Interactive map showing tournament locations"""
    return render_template('map.html')

@app.route('/api/tournaments')
def api_tournaments():
    """API endpoint for map data"""
    tournaments = Tournament.query.all()
    data = []
    
    for tournament in tournaments:
        # Get teams for this tournament
        teams = db.session.query(Team.team_name).join(
            TournamentTeam, Team.team_id == TournamentTeam.team_id
        ).filter(TournamentTeam.tournament_id == tournament.tournament_id).all()
        
        team_names = [team.team_name for team in teams]
        
        for tv in tournament.tournament_venues:
            venue = tv.venue
            if venue.latitude and venue.longitude:
                data.append({
                    'tournament_id': tournament.tournament_id,
                    'tournament_name': tournament.tournament_name,
                    'venue_name': venue.venue_name,
                    'city': venue.city,
                    'country': venue.country,
                    'latitude': venue.latitude,
                    'longitude': venue.longitude,
                    'capacity': getattr(venue, 'capacity', 0),  # Add if exists
                    'start_date': tournament.start_date.isoformat() if tournament.start_date else None,
                    'prize_pool': tournament.prize_pool or 0,
                    'tournament_region': tournament.tournament_region, 
                    'format': getattr(tournament, 'format', 'Unknown'), 
                    'region': getattr(tournament, 'region', 'Unknown'),
                    'teams': team_names
                })
    
    return jsonify(data)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)