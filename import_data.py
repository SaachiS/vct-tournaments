import pandas as pd
from app import app, db
from models import Tournament, Team, Venue, TournamentTeam, TournamentVenue
from datetime import datetime
import os

def parse_date(date_str):
    """Convert date string to datetime object"""
    if pd.isna(date_str) or date_str == '':
        return None
    try:
        return datetime.strptime(str(date_str), '%Y-%m-%d').date()
    except:
        try:
            return datetime.strptime(str(date_str), '%m/%d/%Y').date()
        except:
            print(f"Could not parse date: {date_str}")
            return None
        
def parse_prize_pool(prize_str):
    """Convert prize pool string to integer"""
    if pd.isna(prize_str) or prize_str == '':
        return None
    try:
        # Remove dollar signs, commas, and other currency symbols
        cleaned = str(prize_str).replace('$', '').replace(',', '').replace(' ', '')
        return int(cleaned) if cleaned else None
    except:
        print(f"Could not parse prize pool: {prize_str}")
        return None

def import_data():
    """Import all CSV files into the database"""
    
    with app.app_context():
        # Create tables
        db.drop_all()
        db.create_all()
        
        # Clear existing data
        print("Clearing existing data...")
        TournamentVenue.query.delete()
        TournamentTeam.query.delete()
        Tournament.query.delete()
        Team.query.delete()
        Venue.query.delete()
        db.session.commit()
        
        # Import Venues
        print("Importing venues...")
        venues_df = pd.read_csv('data/venues.csv')
        for _, row in venues_df.iterrows():
            venue = Venue(
                venue_id=row['venue_id'],
                venue_name=row['venue_name'],
                city=row['city'],
                country=row['country'],
                latitude=row['latitude'] if pd.notna(row['latitude']) else None,
                longitude=row['longitude'] if pd.notna(row['longitude']) else None,
            )
            db.session.add(venue)
        
        # Import Teams
        print("Importing teams...")
        teams_df = pd.read_csv('data/teams.csv')
        for _, row in teams_df.iterrows():
            team = Team(
                team_id=row['team_id'],
                team_name=row['team_name'],
                region=row['region'] if pd.notna(row['region']) else None,
            )
            db.session.add(team)
        
        # Import Tournaments
        print("Importing tournaments...")
        tournaments_df = pd.read_csv('data/tournaments.csv', keep_default_na=False)
        for _, row in tournaments_df.iterrows():
            tournament = Tournament(
                tournament_id=row['tournament_id'],
                tournament_name=row['tournament_name'],
                start_date=parse_date(row['start_date']),
                end_date=parse_date(row['end_date']),
                prize_pool=parse_prize_pool(row['prize_pool']) if pd.notna(row['prize_pool']) else None,
                winner_id=row['winner_id'] if pd.notna(row['winner_id']) else None,
                runner_up_id=row['runner_up_id'] if pd.notna(row['runner_up_id']) else None,
                tournament_region=row['tournament_region']
            )
            db.session.add(tournament)
        
        # Import Tournament-Team relationships
        print("Importing tournament-team relationships...")
        tournament_teams_df = pd.read_csv('data/tournament_teams.csv')
        for _, row in tournament_teams_df.iterrows():
            tournament_team = TournamentTeam(
                tournament_id=row['tournament_id'],
                team_id=row['team_id'],
                placement=row['placement'] if pd.notna(row['placement']) else None
            )
            db.session.add(tournament_team)
        
        # Import Tournament-Venue relationships
        print("Importing tournament-venue relationships...")
        tournament_venues_df = pd.read_csv('data/tournament_venues.csv')
        for _, row in tournament_venues_df.iterrows():
            tournament_venue = TournamentVenue(
                tournament_id=row['tournament_id'],
                venue_id=row['venue_id'],
                stage_type=row['stage_type'] if pd.notna(row['stage_type']) else None
            )
            db.session.add(tournament_venue)
        
        # Commit all changes
        db.session.commit()
        print("Data import completed successfully!")
        
        # Print summary
        print(f"Imported:")
        print(f"- {Tournament.query.count()} tournaments")
        print(f"- {Team.query.count()} teams")
        print(f"- {Venue.query.count()} venues")
        print(f"- {TournamentTeam.query.count()} tournament-team relationships")
        print(f"- {TournamentVenue.query.count()} tournament-venue relationships")

if __name__ == '__main__':
    import_data()