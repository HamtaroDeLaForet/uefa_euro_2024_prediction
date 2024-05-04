import pandas as pd
from string import ascii_uppercase as alphabet
import pickle

all_tables = pd.read_html('https://en.wikipedia.org/wiki/UEFA_Euro_2024')

dict_table = {}

for letter, i in zip(alphabet, range(18,60,7)):
    df = all_tables[i]
    df.rename(columns={df.columns[1]: 'Team'}, inplace=True)
    df.pop('Qualification')
    dict_table[f'Group {letter}'] = df

with open('dict_table', 'wb')  as output:
    pickle.dump(dict_table, output)