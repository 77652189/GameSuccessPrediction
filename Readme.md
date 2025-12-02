## Game Success Prediction


Question:Can we predict if a game will be successful on Steam based on its features?

Binary classification - predict "Success" (1) or "Not Success" (0)

## What counts as "success"?

I defined a successful game as:
- Has good reviews (positive ratio ≥ 85%) AND
- Has enough players (either 1000+ recommendations OR 50,000+ owners)


## Data Sources

I used two Kaggle datasets:

### Steam Games Dataset：

Information of more than 110,000 games published on Steam.
https://www.kaggle.com/datasets/fronkongames/steam-games-dataset?resource=download

### Top games on Twitch 2016 - 2023:

Monthly top 200 games on the platform
https://www.kaggle.com/datasets/rankirsh/evolution-of-top-games-on-twitch?select=Twitch_game_data.csv

I merged these two datasets by game name to get a richer feature set.

## important tip: don't upload big file(more than 100mb) to github, it will boom your project. download the data and add it in you own computer