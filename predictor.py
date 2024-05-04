import pandas as pd
import pickle
from scipy.stats import poisson

df_dict_table = pd.read_csv('euro_2024_teams_and_groups.csv')
df_historical_data = pd.read_csv('clean_uefa_euros_matches.csv')
df_fixture = pd.read_csv('clean_uefa_euro_fixture.csv')
dict_table = df_dict_table.to_dict(orient="records")

df_home = df_historical_data[['HomeTeam', 'HomeGoals', 'AwayGoals']]
df_away = df_historical_data[['AwayTeam', 'HomeGoals', 'AwayGoals']]

df_home = df_home.rename(columns={'HomeTeam':'Team', 'HomeGoals': 'GoalsScored', 'AwayGoals': 'GoalsConceded'})
df_away = df_away.rename(columns={'AwayTeam':'Team', 'HomeGoals': 'GoalsConceded', 'AwayGoals': 'GoalsScored'})

df_team_strength = pd.concat([df_home, df_away], ignore_index=True).groupby(['Team']).mean()
df_team_strength



def predict_points(home, away):
    if home in df_team_strength.index and away in df_team_strength.index:
        # goals_scored * goals_conceded
        lamb_home = df_team_strength.at[home,'GoalsScored'] * df_team_strength.at[away,'GoalsConceded']
        lamb_away = df_team_strength.at[away,'GoalsScored'] * df_team_strength.at[home,'GoalsConceded']
        prob_home, prob_away, prob_draw = 0, 0, 0
        for x in range(0,11): #number of goals home team
            for y in range(0, 11): #number of goals away team
                p = poisson.pmf(x, lamb_home) * poisson.pmf(y, lamb_away)
                if x == y:
                    prob_draw += p
                elif x > y:
                    prob_home += p
                else:
                    prob_away += p
        
        points_home = 3 * prob_home + prob_draw
        points_away = 3 * prob_away + prob_draw
        return (points_home, points_away)
    else:
        return (0, 0)
    
df_fixture_group_36 = df_fixture[:36].copy()
df_fixture_knockout = df_fixture[36:44].copy()
df_fixture_quarter = df_fixture[44:48].copy()
df_fixture_semi = df_fixture[48:50].copy()
df_fixture_final = df_fixture[50:].copy()

def process_group_data(dict_table, df_fixture_group_36):
    group_dataframes = {}

    for group_data in dict_table:
        group = group_data['Group']
        df_group = pd.DataFrame([group_data], index=[0])  # Créer un DataFrame avec un seul dictionnaire

        teams_in_group = df_group['Team'].values
        df_fixture_group_6 = df_fixture_group_36[df_fixture_group_36['home'].isin(teams_in_group)]

        for index, row in df_fixture_group_6.iterrows():
            home, away = row['home'], row['away']
            points_home, points_away = predict_points(home, away)
            df_group.loc[df_group['Team'] == home, 'Pts'] += points_home
            df_group.loc[df_group['Team'] == away, 'Pts'] += points_away

        df_group = df_group.sort_values('Pts', ascending=False).reset_index(drop=True)
        df_group = df_group[['Team', 'Pts']]
        df_group = df_group.round(0)

        group_dataframes[group] = df_group

    return group_dataframes

# Exemple d'utilisation :
group_dataframes = process_group_data(dict_table, df_fixture_group_36)