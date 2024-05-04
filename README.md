# UEFA Euro 2024 Predictor

Predictor for UEFA Euro 2024 football tournament matches using Python and the Poisson Distribution.

## Overview

This project is a predictor for the UEFA Euro 2024 football tournament matches. It utilizes historical match data, team strength calculations, and Poisson distribution to predict the outcomes of matches. The prediction process includes group stage matches, knockout stage matches, and ultimately predicts the winner of the tournament.

## Requirements

- Python 3.x
- pandas
- pickle
- scipy
- seaborn
- matplotlib

## Usage

1. Clone the repository to your local machine:

```
git clone https://github.com/HamtaroDeLaForet/UEFA-Euro-2024-Predictor.git
```

2. Navigate to the project directory:

```
cd UEFA-Euro-2024-Predictor
```

3. Ensure all required dependencies are installed:

```
pip install -r requirements.txt
```

4. Run the predictor script:

```
python predictor.py
```

5. View the predicted outcomes for the UEFA Euro 2024 matches.

## Features

- Prediction of group stage matches.
- Prediction of knockout stage matches (round of 16, quarterfinals, semifinals, and final).
- Calculation of overall winner of the UEFA Euro 2024 tournament.
- Visualization of tournament summary in a heatmap format.

## Files

- `predictor.py`: Main Python script containing the predictor logic.
- `clean_uefa_euros_matches.csv`: Cleaned historical match data for UEFA Euro tournaments.
- `clean_uefa_euro_fixture.csv`: Cleaned fixture data for UEFA Euro 2024 tournament matches.
- `dict_table`: Pickle file containing dictionary data for teams and groups.
- `requirements.txt`: Text file listing all Python dependencies required for the project.

## Credits

This project was developed by Mateo Fauquembergue . It is based on the concepts of football match prediction using historical data and statistical methods.
