import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime

# Set page title
st.title('Basketball Analytics Dashboard')

# Connect to the database
@st.cache_resource
def get_connection():
    return sqlite3.connect('basketball.db')

# Load data
def load_data():
    conn = get_connection()
    teams_df = pd.read_sql_query("SELECT * FROM team", conn)
    games_df = pd.read_sql_query("SELECT * FROM game", conn)
    
    # Calculate win percentage
    teams_df['win_pct'] = teams_df['wins'] / (teams_df['wins'] + teams_df['losses'])
    teams_df['win_pct'] = teams_df['win_pct'].round(3)
    
    # Convert date column to datetime
    games_df['date'] = pd.to_datetime(games_df['date'])
    
    return teams_df, games_df

teams_df, games_df = load_data()

# Sidebar
st.sidebar.title('Navigation')
page = st.sidebar.radio('Select a page', ['Team Statistics', 'Game Analysis', 'League Leaders'])

if page == 'Team Statistics':
    st.header('Team Statistics')
    
    # Team Rankings
    st.subheader('Current Standings')
    standings = teams_df.sort_values('win_pct', ascending=False).reset_index(drop=True)
    standings.index = standings.index + 1  # Start ranking from 1
    st.dataframe(standings[['name', 'wins', 'losses', 'win_pct']])
    
    # Win-Loss Distribution
    st.subheader('Win-Loss Distribution')
    fig = px.bar(teams_df, x='name', y=['wins', 'losses'], 
                 title='Team Win-Loss Records',
                 barmode='group')
    st.plotly_chart(fig)

elif page == 'Game Analysis':
    st.header('Game Analysis')
    
    # Recent Games
    st.subheader('Recent Games')
    recent_games = games_df[games_df['date'] < datetime.now()].sort_values('date', ascending=False)
    
    for _, game in recent_games.head().iterrows():
        st.write(f"{game['date'].strftime('%Y-%m-%d')}: {game['home_team']} {game['score_home']} - {game['score_away']} {game['away_team']}")
    
    # Upcoming Games
    st.subheader('Upcoming Games')
    upcoming_games = games_df[games_df['date'] >= datetime.now()].sort_values('date')
    
    for _, game in upcoming_games.head().iterrows():
        st.write(f"{game['date'].strftime('%Y-%m-%d')}: {game['home_team']} vs {game['away_team']}")
    
    # Home vs Away Performance
    if len(recent_games) > 0:
        st.subheader('Home vs Away Performance')
        home_avg = recent_games['score_home'].mean()
        away_avg = recent_games['score_away'].mean()
        
        performance_df = pd.DataFrame({
            'Location': ['Home', 'Away'],
            'Average Score': [home_avg, away_avg]
        })
        
        fig = px.bar(performance_df, x='Location', y='Average Score',
                     title='Average Scoring by Home/Away Teams')
        st.plotly_chart(fig)

else:  # League Leaders
    st.header('League Leaders')
    
    # Top 5 teams by win percentage
    st.subheader('Top Teams by Win Percentage')
    top_teams = teams_df.nlargest(5, 'win_pct')[['name', 'win_pct']]
    fig = px.bar(top_teams, x='name', y='win_pct',
                 title='Top 5 Teams - Win Percentage',
                 labels={'win_pct': 'Win Percentage', 'name': 'Team'})
    st.plotly_chart(fig)
    
    # Most points scored (home games)
    st.subheader('Highest Scoring Teams (Home Games)')
    home_scoring = games_df.groupby('home_team')['score_home'].mean().sort_values(ascending=False)
    st.write(home_scoring.head())
