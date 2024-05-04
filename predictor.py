import pandas as pd
import pickle
from scipy.stats import poisson
import seaborn as sns
import matplotlib.pyplot as plt

# Chargement des données
dict_table = pickle.load(open('./datas/dict_table','rb'))
df_historical_data = pd.read_csv('./datas/clean_uefa_euros_matches.csv')
df_fixture = pd.read_csv('./datas/clean_uefa_euro_fixture.csv')

# Préparation des données
df_home = df_historical_data[['HomeTeam', 'HomeGoals', 'AwayGoals']]
df_away = df_historical_data[['AwayTeam', 'HomeGoals', 'AwayGoals']]

df_home = df_home.rename(columns={'HomeTeam':'Team', 'HomeGoals': 'GoalsScored', 'AwayGoals': 'GoalsConceded'})
df_away = df_away.rename(columns={'AwayTeam':'Team', 'HomeGoals': 'GoalsConceded', 'AwayGoals': 'GoalsScored'})

df_team_strength = pd.concat([df_home, df_away], ignore_index=True).groupby(['Team']).mean()

df_fixture_group_36 = df_fixture[:36].copy()
df_fixture_knockout = df_fixture[36:44].copy()
df_fixture_quarter = df_fixture[44:48].copy()
df_fixture_semi = df_fixture[48:50].copy()
df_fixture_final = df_fixture[50:].copy()

# Fonction pour prédire les points d'un match
def predict_points(home, away):
    if home in df_team_strength.index and away in df_team_strength.index:
        lamb_home = df_team_strength.at[home,'GoalsScored'] * df_team_strength.at[away,'GoalsConceded']
        lamb_away = df_team_strength.at[away,'GoalsScored'] * df_team_strength.at[home,'GoalsConceded']
        prob_home, prob_away, prob_draw = 0, 0, 0
        for x in range(0,11):
            for y in range(0, 11):
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

# Prédiction des points pour chaque match de groupe
for group in dict_table:
    teams_in_group = dict_table[group]['Team'].values
    df_fixture_group_6 = df_fixture_group_36[df_fixture_group_36['home'].isin(teams_in_group)]
    for index, row in df_fixture_group_6.iterrows():
        home, away = row['home'], row['away']
        points_home, points_away = predict_points(home, away)
        dict_table[group].loc[dict_table[group]['Team'] == home, 'Pts'] += points_home
        dict_table[group].loc[dict_table[group]['Team'] == away, 'Pts'] += points_away

    dict_table[group] = dict_table[group].sort_values('Pts', ascending=False).reset_index()
    dict_table[group] = dict_table[group][['Team', 'Pts']]
    dict_table[group] = dict_table[group].round(0)

first_and_second_place_teams = {}

# Ajouter les premiers et deuxièmes de chaque groupe au dictionnaire
for group, group_df in dict_table.items():
    first_place_team = group_df.loc[0, 'Team']
    second_place_team = group_df.loc[1, 'Team']
    first_and_second_place_teams[group] = (first_place_team, second_place_team)

# Sélection des troisièmes de chaque groupe
third_place_teams = {
    'A': dict_table['Group A'].loc[2, 'Team'],
    'B': dict_table['Group B'].loc[2, 'Team'],
    'C': dict_table['Group C'].loc[2, 'Team'],
    'D': dict_table['Group D'].loc[2, 'Team'],
    'E': dict_table['Group E'].loc[2, 'Team'],
    'F': dict_table['Group F'].loc[2, 'Team']
}



# Combinaisons de troisièmes de groupe
third_place_combinations = {
    'D/E/F': ['D', 'E', 'F'],
    'A/D/E/F': ['A', 'D', 'E', 'F'],
    'A/B/C': ['A', 'B', 'C'],
    'A/B/C/D': ['A', 'B', 'C', 'D']
}

# Calcul des points des troisièmes de chaque groupe
points_third_place_teams = {}
for group, team in third_place_teams.items():
    points_third_place_teams[team] = dict_table[f'Group {group}'].loc[2, 'Pts']

# Trier les troisièmes de groupe par points décroissants
sorted_third_place_teams = sorted(points_third_place_teams.items(), key=lambda x: x[1], reverse=True)

teams_already_assigned_to_round_of_16 = []

for group_specified, groups in third_place_combinations.items():
    # Sélectionner les équipes troisièmes pour les groupes spécifiés
    third_place_teams_specified = []
    for group in groups:
        team = third_place_teams.get(group)
        if team and team not in teams_already_assigned_to_round_of_16:
            third_place_teams_specified.append(team)
    # Trouver le meilleur troisième parmi les groupes spécifiés
    best_third_place_team = max(third_place_teams_specified, key=lambda x: points_third_place_teams[x])
    # Retirer l'équipe sélectionnée de la liste des meilleures troisièmes
    del points_third_place_teams[best_third_place_team]
    # Ajouter l'équipe sélectionnée à la liste des équipes déjà affectées aux huitièmes de finale
    teams_already_assigned_to_round_of_16.append(best_third_place_team)
    # Remplacer dans le tableau des huitièmes de finale
    df_fixture_knockout.replace({f'3rd Group {group_specified}': best_third_place_team}, inplace=True)


# Mettre à jour les gagnants et les deuxièmes de chaque groupe dans le tableau des huitièmes de finale



for group in dict_table:
    group_winner = dict_table[group].loc[0, 'Team']
    runners_up = dict_table[group].loc[1, 'Team']
    # Remplacement direct dans le DataFrame df_fixture_knockout
    df_fixture_knockout.loc[df_fixture_knockout['home'] == f'Winner {group}', 'home'] = group_winner
    df_fixture_knockout.loc[df_fixture_knockout['away'] == f'Winner {group}', 'away'] = group_winner
    df_fixture_knockout.loc[df_fixture_knockout['home'] == f'Runner-up {group}', 'home'] = runners_up
    df_fixture_knockout.loc[df_fixture_knockout['away'] == f'Runner-up {group}', 'away'] = runners_up

# Affichage du DataFrame df_fixture_knockout
df_fixture_knockout['winner'] = '?'

def get_winner(df_fixture_updated):
    for index, row in df_fixture_updated.iterrows():
        home, away = row['home'], row['away']
        points_home, points_away = predict_points(home, away)
        if points_home > points_away:
            winner = home
        else:
            winner = away
        df_fixture_updated.loc[index, 'winner'] = winner
    return df_fixture_updated

get_winner(df_fixture_knockout)

def update_table(df_quarters, df_fixture_round_2):
    for index, row in df_quarters.iterrows():
        winner = df_quarters.loc[index, 'winner']
        match = df_quarters.loc[index, 'score']
        # Remplacement des noms dans les quarts de finale
        df_fixture_round_2.loc[df_fixture_round_2['home'] == f'Winner {match}', 'home'] = winner
        df_fixture_round_2.loc[df_fixture_round_2['away'] == f'Winner {match}', 'away'] = winner
    return df_fixture_round_2

knockout_winners = df_fixture_knockout.loc[36:44, 'winner']
quarter = update_table(df_fixture_knockout, df_fixture_quarter)
get_winner(quarter)
quarter_winners = df_fixture_quarter.loc[44:48, 'winner']
semi = update_table(df_fixture_quarter, df_fixture_semi)
get_winner(semi)
semi_winners = df_fixture_semi.loc[48:50, 'winner']
final = update_table(df_fixture_semi, df_fixture_final)
final_match = get_winner(final)
final_winner = df_fixture_final.loc[50, 'winner']

print("Here comes the round of 16. Let's have a look at all the matches:")
print(df_fixture_knockout.loc[36:44, ['home', 'away']])
print("\nThe teams that go through to the round of 16 are:")
print(knockout_winners.to_string(index=False))  # Afficher les équipes sans l'index
print()

print("Here comes the quarter-finals. Let's have a look at all the matches:")
print(df_fixture_quarter.loc[44:48, ['home', 'away']])
print("\nThe teams that go through to the quarter-finals are:")
print(quarter_winners.to_string(index=False))  # Afficher les équipes sans l'index
print()

print("Here comes the semi-finals. Let's have a look at the matches:")
print(df_fixture_semi.loc[48:50, ['home', 'away']])
print("\nThe teams that go through to the semi-finals are:")
print(semi_winners.to_string(index=False))  # Afficher les équipes sans l'index
print()

print("We're finally here, the UEFA Euro 2024 final. Which nation will win?")
print("Here is the final match: {} vs {}".format(final_match['home'].values[0], final_match['away'].values[0]))
print()
print()
print()
print("\n{} are our UEFA Euro 2024 Champions!".format(final_winner))