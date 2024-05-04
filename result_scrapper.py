import pandas as pd
from bs4 import BeautifulSoup
import requests

def  get_matches(year):
    url = f"https://en.wikipedia.org/wiki/UEFA_Euro_{year}"
    response = requests.get(url)
    content = response.text
    soup = BeautifulSoup(content, 'lxml')
    matches = soup.find_all('div', class_='footballbox')
    home = []
    score = []
    away = []
    for match in matches:
        home.append(match.find('th',class_="fhome").get_text())
        score.append(match.find("th",class_="fscore").get_text())
        away.append(match.find('th',class_="faway").get_text())
    dict_football = {'home': home, 'score': score, 'away': away}
    df_football = pd.DataFrame(dict_football)
    df_football['year'] = year
    return df_football

euros = [1960,1964,1968,1972,1976,1980,1984,1988,1992,1996,2000,2004,2008,2012,2016,2020]
uefa =  [get_matches(year) for year in euros]
df_uefa = pd.concat(uefa, ignore_index=True)
df_uefa.to_csv("uefa_euros_historical_data.csv", index=False)

df_fixture = get_matches(2024)
df_fixture.to_csv('uefa_euro_fixture.csv', index=False)