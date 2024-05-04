import pandas as pd
from string import ascii_uppercase as alphabet

# Lire les tables de la page Wikipedia
all_tables = pd.read_html('https://en.wikipedia.org/wiki/UEFA_Euro_2024')

# Initialiser une liste pour stocker les DataFrames de tous les groupes
group_dfs = []

# Parcourir les tables et les stocker dans la liste
for letter, i in zip(alphabet, range(18, 60, 7)):  # A=18, B=25, ...
    df = all_tables[i]
    df.rename(columns={df.columns[1]: 'Team'}, inplace=True)
    df['Group'] = letter  # Ajouter une colonne 'Group' avec la lettre du groupe
    group_dfs.append(df)

# Concaténer les DataFrames de tous les groupes
euro_df = pd.concat(group_dfs, ignore_index=True)

# Enregistrer les données dans un fichier CSV
euro_df.to_csv('euro_2024_teams_and_groups.csv', index=False)
