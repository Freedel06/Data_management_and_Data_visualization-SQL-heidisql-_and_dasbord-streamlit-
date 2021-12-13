import streamlit as st
import pandas as pd 
import numpy as np 
import sqlite3

header=st.beta_container()
dataset=st.beta_container()
table=st.beta_container()
query=st.beta_container()


with header:
    st.title("Programmation for big data: SQL and Streamlit")
    st.text("Made by Freedel ZINSOU-PLY and Ahaloudine Assani")
    st.title("European'soccer data analysis")
    st.text('In this projet we look into the data analysis of Europeen soccer data')
    
    
with dataset:
  
    st.header('Introduction')
    st.text('The database has download from Kaggle')
    st.text('this database contains seven table and each')
    st.text('table contain different type of information about')
    st.text('the characteristic of the players and theirs team.')
    st.text('In this short project we have made several SQL queries to get a deep insight of this database.')
    st.text ('Then, the results of these queries have been presented in a streamlit dashboard')
    
    database=r'C:\Users\33758\Desktop\Cours APE\database.sqlite'
    conn=sqlite3.connect(database)
    
    
    
with table:
    st.header('The table of our database')
    tables = pd.read_sql("""SELECT *
                        FROM sqlite_master
                        WHERE type='table';""", conn)
    st.write(tables)
    
    
with query:
    st.header('The different result of our query')
    st.text('Here we use a several SQL query like Join , select CASE, select When')
    st.text('First query:  What are the different leagues we have and what countries are they playing in?')
    league_country= pd.read_sql("""select country.id,
                                league.name as leagues_name,
                                country.name as leagues_country
                                from league 
                                join country on country.id=league.id
                                group by country.name""", conn)
    st.write(league_country)
    
    
    st.text('In our database we got information about different team in each match')
    st.text('The team are classifier as Away team and home team')
    
    st.text('Second query: Away team information')
    away=pd.read_sql(""" select 
                         season,
                         date,
                         league.name as league,
                         team.team_long_name as away_team,
                         away_team_api_id,
                         home_team_api_id,
                         home_team_goal,
                         match_api_id
                        from match
                        join league on league.id=match.league_id
                        join team on team.team_api_id=match.away_team_api_id
                        """, conn)
    st.write(away.head())
    
    st.text('Third query: Home team information')
    
    home=pd.read_sql("""select 
                        season,
                        date,
                        league.name as league,
                        team.team_long_name as home_team,
                        home_team_api_id,
                        away_team_api_id,
                        match_api_id
                        from match
                        join league on league.id=match.league_id
                        join team on team.team_api_id=match.home_team_api_id
                           """, conn)
    st.write(home.head())
    
    st.text('Now the gonna see diffirent information match between the two team such as:')
    st.text('season,date,teams, numbers of goal,match_result,and the winner')
    st.text('fourth query: information about match')
    jer=pd.read_sql("""select
                    home.league as league_name,
                    home.season as season,
                    date(home.date) as date,
                    home.home_team,
                    away.away_team,
                    home.home_team_goal,
                    away.away_team_goal,
                   CASE 
                       when home.home_team_goal = away.away_team_goal then 'match_null'
                       when home.home_team_goal > away.away_team_goal then 'home_win'
                       when home.home_team_goal < away.away_team_goal then 'visitor_win'
                   end as match_result,
                   Case 
                        when home.home_team_goal = away.away_team_goal then 'nobody'
                        when home.home_team_goal > away.away_team_goal then home.home_team
                        when home.home_team_goal < away.away_team_goal then away.away_team
                   end as winner
                  from (select 
                  league.name as league,
                  season,
                  date,
                  team.team_long_name as home_team,
                  home_team_api_id,
                  away_team_api_id,
                  home_team_goal,
                  stage,
                  match_api_id
                 from match
                 join league on league.id=match.league_id
                 join team on team.team_api_id=match.home_team_api_id) home
                 join ( select 
                 team.team_long_name as away_team,
                 league.name,
                 away_team_goal,
                 away_team_api_id,
                 home_team_api_id,
                 match_api_id
                 from match
                 join league on league.id=match.league_id
                 join team on team.team_api_id=match.away_team_api_id) away on away.match_api_id=home.match_api_id""",conn)
    st.write(jer.head())
    
    st.write("Now we gonna talk about player")
    st.write("we gonna see some player characteristic such as:")
    st.write(" name , birthday, height, overal rating,potential, peferred foot")
    st.write("attacking work rate, defense work rate ,attacking_work_rate,defensive_work_rate")
    st.write("Fith query : information about players")
    player=pd.read_sql(""" Select p.player_name,
                       date(birthday), 
                       p.height, 
                       p.weight, 
                       attr.overall_rating,
                       attr.preferred_foot,
                       attr.attacking_work_rate,
                       attr.defensive_work_rate,attr.penalties
                       from player  p 
                       join Player_Attributes attr on attr.id=p.id;""",conn)
    st.write(player)