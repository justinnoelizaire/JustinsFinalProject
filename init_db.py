from app import app, db, Team, Game, Player
from datetime import datetime, timedelta

with app.app_context():
    # Clear existing data
    db.drop_all()
    db.create_all()

    # Add teams with realistic records
    teams_data = [
        ("Boston Celtics", 64, 18),
        ("Milwaukee Bucks", 49, 33),
        ("New York Knicks", 50, 32),
        ("Cleveland Cavaliers", 48, 34),
        ("Orlando Magic", 47, 35),
        ("Miami Heat", 46, 36),
        ("Philadelphia 76ers", 47, 35),
        ("Indiana Pacers", 47, 35),
        ("Denver Nuggets", 57, 25),
        ("Minnesota Timberwolves", 56, 26),
        ("Oklahoma City Thunder", 57, 25),
        ("Los Angeles Clippers", 51, 31),
        ("Phoenix Suns", 49, 33),
        ("New Orleans Pelicans", 49, 33),
        ("Los Angeles Lakers", 47, 35),
        ("Golden State Warriors", 46, 36)
    ]

    # Add teams to database and store references
    teams_dict = {}
    for name, wins, losses in teams_data:
        team = Team(name=name, wins=wins, losses=losses)
        db.session.add(team)
        db.session.flush()  # This will assign the ID to the team
        teams_dict[name] = team

    # Add players with realistic statistics
    players_data = [
        # Celtics
        ("Jayson Tatum", "Boston Celtics", "SF", 27.6, 8.6, 4.8, 1.0, 0.7, 47.1, 35.3),
        ("Jaylen Brown", "Boston Celtics", "SG", 23.1, 5.6, 3.7, 1.2, 0.3, 49.2, 35.7),
        
        # Bucks
        ("Giannis Antetokounmpo", "Milwaukee Bucks", "PF", 30.4, 11.5, 6.5, 1.2, 1.0, 61.1, 27.5),
        ("Damian Lillard", "Milwaukee Bucks", "PG", 24.7, 4.4, 7.0, 1.0, 0.2, 42.1, 35.4),
        
        # Knicks
        ("Jalen Brunson", "New York Knicks", "PG", 28.7, 3.6, 6.7, 0.9, 0.2, 47.9, 40.1),
        ("OG Anunoby", "New York Knicks", "SF", 14.6, 4.4, 2.3, 1.3, 0.7, 49.8, 37.9),
        
        # Lakers
        ("LeBron James", "Los Angeles Lakers", "SF", 25.4, 7.2, 8.1, 1.2, 0.5, 54.0, 38.7),
        ("Anthony Davis", "Los Angeles Lakers", "PF", 24.7, 12.6, 3.5, 1.2, 2.3, 55.6, 27.3),
        
        # Warriors
        ("Stephen Curry", "Golden State Warriors", "PG", 26.8, 4.2, 4.9, 0.8, 0.2, 45.3, 40.1),
        ("Klay Thompson", "Golden State Warriors", "SG", 17.9, 3.3, 2.4, 0.7, 0.2, 43.2, 38.7),
        
        # Nuggets
        ("Nikola Jokic", "Denver Nuggets", "C", 26.1, 12.3, 9.0, 1.3, 0.9, 58.3, 35.9),
        ("Jamal Murray", "Denver Nuggets", "PG", 21.2, 4.0, 6.5, 1.0, 0.3, 48.1, 42.5),
        
        # Suns
        ("Devin Booker", "Phoenix Suns", "SG", 27.1, 4.5, 6.9, 1.0, 0.3, 49.8, 36.4),
        ("Kevin Durant", "Phoenix Suns", "SF", 28.3, 6.7, 5.1, 0.7, 1.2, 52.7, 41.2),
        
        # Thunder
        ("Shai Gilgeous-Alexander", "Oklahoma City Thunder", "PG", 30.1, 5.5, 6.2, 2.0, 0.8, 54.0, 32.1),
        ("Chet Holmgren", "Oklahoma City Thunder", "C", 16.6, 7.9, 2.5, 0.8, 2.3, 53.4, 37.2),
        
        # Timberwolves
        ("Anthony Edwards", "Minnesota Timberwolves", "SG", 26.0, 5.6, 5.1, 1.3, 0.6, 46.2, 35.3),
        ("Karl-Anthony Towns", "Minnesota Timberwolves", "C", 22.1, 8.4, 3.0, 0.8, 0.6, 50.7, 42.3)
    ]

    # Add players to database
    for name, team_name, position, ppg, rpg, apg, spg, bpg, fgp, tpp in players_data:
        player = Player(
            name=name,
            team_id=teams_dict[team_name].id,
            position=position,
            points_per_game=ppg,
            rebounds_per_game=rpg,
            assists_per_game=apg,
            steals_per_game=spg,
            blocks_per_game=bpg,
            field_goal_percentage=fgp,
            three_point_percentage=tpp
        )
        db.session.add(player)

    # Generate games schedule (keeping the existing game generation code)
    start_date = datetime.now()
    teams = [team[0] for team in teams_data]
    games_data = []

    # Create some past games with scores
    for i in range(10):
        game_date = start_date - timedelta(days=i+1)
        home_idx = i % len(teams)
        away_idx = (i + 1) % len(teams)
        
        home_score = 100 + (i % 20)
        away_score = 95 + ((i + 5) % 25)
        
        games_data.append({
            'home_team': teams[home_idx],
            'away_team': teams[away_idx],
            'date': game_date,
            'score_home': home_score,
            'score_away': away_score
        })

    # Create upcoming games without scores
    for i in range(10):
        game_date = start_date + timedelta(days=i+1)
        home_idx = (i + 5) % len(teams)
        away_idx = (i + 6) % len(teams)
        
        games_data.append({
            'home_team': teams[home_idx],
            'away_team': teams[away_idx],
            'date': game_date,
            'score_home': None,
            'score_away': None
        })

    # Add games to database
    for game_data in games_data:
        game = Game(**game_data)
        db.session.add(game)

    # Commit all changes
    db.session.commit()

    print("Database initialized with teams, players, and games data!")
