## Overview

Springboard requires an open ended capstone project with the subject of my choosing. I have selected processing [lichess](https://lichess.org/) game data because the data is large, complex, and chess is a passion of mine. 


## Data Source

Lichess stores [monthly standard game files](https://database.lichess.org/), zipped, in a pgn format, ranging from 15 MB to 27 GB. Each record contains game level data, like who was black and who was white, and move level data like the move, AI evaluation, and time left on the clock. The data set can be anywhere between 10 GB to 500 GB depending on the scope I select. At a glance the data appears relatively challenging to parse; however, many others have successfully used this dataset before (e.g. [popularity and win rate of chess openings](https://github.com/Paul566/chessOpeningStats)), so I can learn from them, and cite them as inspiration for the work I do. I will process the data via batch processing on a monthly time scale.


## My Idea

I would like to analyze the games that contain one or more forced checkmate(s) in one move. I originally wanted to search for 'brilliant' moves, however this was not very interesting given the data. More detailed ideas include:
- Percent of checkmate in 1 that are found
- Percent of checkmate in 1 that are found by elo
- Games where a player lost after checkmate in one. Highest elo example. 
- Game with player with the highest elo who missed a checkmate in 1
- My percent of checkmates in 1 that are found
- Players with the most games and a perfect checkmate in 1 pct
- Could try percent of checkmate in n that are found by elo, but this would be tricky.


## My Goals

1. Successfully create a pipeline for 25-500 GB of data
2. If possible update the pipeline dynamically, monthly with new data
3. Initially work with a small file, but eventually host the data on the cloud
4. Visualize and analyze the data to extract meaningful and potentially surprising insights 


## What DE Skills are Highlighted?

- Cleaning messy data
- Working with large datasets
- Building pipelines, ideally dynamic ones
- Extracting insights from data
- Cloud data storage


## Output

The final output should be at least record the game and move attributes for all games with at least one forced checkmate and evaluations for the entire dataset. The visualization and analysis will likely be done in Python using a Jupyter notebook or markdown.
