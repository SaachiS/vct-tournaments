from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tournament(db.Model):
    __tablename__ = 'tournaments'
    
    tournament_id = db.Column(db.Integer, primary_key=True)
    tournament_name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    prize_pool = db.Column(db.Integer)
    winner_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=True)
    runner_up_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=True)
    tournament_region = db.Column(db.String(255), nullable=False)
    
    # Relationships
    tournament_teams = db.relationship('TournamentTeam', backref='tournament', lazy=True)
    tournament_venues = db.relationship('TournamentVenue', backref='tournament', lazy=True)
    winner_team = db.relationship('Team', foreign_keys=[winner_id], backref='tournaments_won')
    runner_up_team = db.relationship('Team', foreign_keys=[runner_up_id], backref='tournaments_runner_up')
    
    def __repr__(self):
        return f'<Tournament {self.tournament_name}>'

class Team(db.Model):
    __tablename__ = 'teams'
    
    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(255), nullable=False)
    region = db.Column(db.String(100))
    
    # Relationships
    tournament_teams = db.relationship('TournamentTeam', backref='team', lazy=True)
    
    def __repr__(self):
        return f'<Team {self.team_name}>'

class Venue(db.Model):
    __tablename__ = 'venues'
    
    venue_id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Relationships
    tournament_venues = db.relationship('TournamentVenue', backref='venue', lazy=True)
    
    def __repr__(self):
        return f'<Venue {self.venue_name}>'

class TournamentTeam(db.Model):
    __tablename__ = 'tournament_teams'
    
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.tournament_id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)
    placement = db.Column(db.String(20))
    
    def __repr__(self):
        return f'<TournamentTeam {self.tournament_id}-{self.team_id}>'

class TournamentVenue(db.Model):
    __tablename__ = 'tournament_venues'
    
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.tournament_id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.venue_id'), nullable=False)
    stage_type = db.Column(db.String(50))
    
    def __repr__(self):
        return f'<TournamentVenue {self.tournament_id}-{self.venue_id}>'