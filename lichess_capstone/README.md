## Overview

For my open-ended capstone, I have selected to process 106 million [lichess](https://lichess.org/) games and derive insights on forced checkmates. The parsed data contains over 14 million games with evaluations and over 900 milllion rows of move level data.


## Data Source

Lichess stores [monthly standard game files](https://database.lichess.org/), zipped, in a pgn format. Each record contains game level data, like who was black and who was white, and move level data like the move, AI evaluation, and time left on the clock. I have processed 106 million games using monthly batch processing for January 2013 to October 2016. I gained inspiration from [the following example](https://github.com/Paul566/chessOpeningStats)) to efficiently parse the pgn data.


## Architecture

I use the requests library to download each month of zipped pgn data. The data is then unzipped, cleaned and written to a csv file. I load the csv file to a pandas dataframe, which is loaded into two final postgres tables: moves and games. I elected to make my scaled pipeline locally in postgres because it was substantially faster than writing to Azure using the methods in their official documentation, and speed and scale were the primary challenges of this project. However, I wrote a small pipeline to Azure for proof of concept. The postgres data is finally used with Matplotlib to generate visualizations for key insights on forced checkmates. 

![architecture](https://github.com/rivergrove/springboard/blob/master/lichess_capstone/deployment_architecture/architecture.png)


## Insights 

Using lichess games from January 2013 to October 2016, I explored interesting patterns in forced checkmates. Only 28% of games end in checkmate. Most end in resignation.

![termination_type](https://github.com/rivergrove/springboard/blob/master/lichess_capstone/production/plots/termination_type.png)

35% of games have a forced checkmate in one. This means that many 7% of games have a forced checkmate, but do not end in checkmate, and instead end in resignation or time forfeit.

![forced_checkmate_in_one](https://github.com/rivergrove/springboard/blob/master/lichess_capstone/production/plots/pct_checkmate_in_one_games.png)

Of the moves with forced checkmate in one, 29% of the time the player misses the forced checkmate on that turn. I use the alias [rivergrove](https://lichess.org/@/rivergrove) on lichess.org. Of my games, I miss forced checkmate in one 20% of the time.

![pct_checkmate_in_one_found](https://github.com/rivergrove/springboard/blob/master/lichess_capstone/production/plots/pct_checkmate_in_one_found.png)
![my_pct_checkmate_in_one_found](https://github.com/rivergrove/springboard/blob/master/lichess_capstone/production/plots/my_pct_checkmate_in_one_found.png)

When cut by game type, there is a trend that games types with more time yield better checkmate in one found percentages. The exception to this rule is the correspondence game type, which has the most time, but sports one of the worst checkmate in one percentages. My hypothesis for this is that players are more likely to resign in a correspondence game rather than play until the bitter end. If I have additional time, I can check this hypothesis by running the data with resigntations included.

![pct_checkmate_in_one_found_pct_by_game_type](https://github.com/rivergrove/springboard/blob/master/lichess_capstone/production/plots/pct_checkmate_in_one_found_pct_by_game_type.png)
