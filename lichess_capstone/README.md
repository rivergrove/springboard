## Overview

Springboard requires an open ended capstone project with the subject of my choosing. I have selected processing [lichess](https://lichess.org/) game data because the data is large, complex, and chess is a passion of mine. 


## Data Source

Lichess stores [monthly standard game files](https://database.lichess.org/), zipped, in a pgn format, ranging from 15 MB to 27 GB. Each record contains game level data, like who was black and who was white, and move level data like the move, AI evaluation, and time left on the clock. I am aiming for a scope of 100M+ games by running from January 2013 to October 2016. At a glance the data appears relatively challenging to parse; however, many others have successfully used this dataset before (e.g. [popularity and win rate of chess openings](https://github.com/Paul566/chessOpeningStats)), so I can learn from them, and cite them as inspiration for the work I do. I will process the data via batch processing on a monthly time scale.


## My Idea

I would like to analyze the games that contain one or more forced checkmate(s) in one move. More detailed ideas include:
- Percent of checkmate in 1 that are found
- Percent of checkmate in 1 that are found by elo
- Games where a player lost after checkmate in one. Highest elo example. 
- Game with player with the highest elo who missed a checkmate in 1
- My percent of checkmates in 1 that are found
- Players with the most games and a perfect checkmate in 1 pct
- Could try percent of checkmate in n that are found by elo, but this would be tricky.


## My Goals

1. Successfully create a pipeline for 100M+ games
2. Include unit testing, logging, and OOP best practices
4. Visualize and analyze the data to extract meaningful and potentially surprising insights 


## What DE Skills are Highlighted?

- Cleaning messy data
- Working with large datasets
- Building pipelines, ideally dynamic ones
- Extracting insights from data


## Output

The final output should at least record the game and move attributes for all games with at least one forced checkmate and evaluations. The visualization and analysis will likely be done in Python using a Jupyter notebook or markdown.
