## Overview

Springboard requires an open ended capstone project with the subject of my choosing. I have selected processing [lichess](https://lichess.org/) game data because the data is large, complex, and chess is a passion of mine. 


## Data Source

Lichess stores [monthly standard game files](https://database.lichess.org/), zipped, in a pgn format, ranging from 15 MB to 27 GB. Each record contains game level data, like who was black and who was white, and move level data like the move, AI evaluation, and time left on the clock. The data set can be anywhere between 10 GB to 500 GB depending on the scope I select. At a glance the data appears relatively challenging to parse; however, many others have successfully used this dataset before (e.g. [popularity and win rate of chess openings](https://github.com/Paul566/chessOpeningStats)), so I can learn from them, and cite them as inspiration for the work I do.


## My Idea

I would like to analyze the games for brilliant moves, defined as approximatly +2 on your eval, meaning the engine didn’t see it. I may choose to increase or decrease this eval depending on how many results I find. More detailed ideas include:
- Find players who made the most brilliant moves
- An example game (may reference the agadmator’s video as another example)
- Brilliant moves by elo
- % of moves that are brilliant by elo
- Find the most brilliant move I’ve ever made
- Find the game with the most brilliant moves


## My Goals

1. Successfully create a pipeline for 25-500 GB of data
2. If possible update the pipeline dynamically, monthly with new data
3. Visualize and analyze the data to extract meaningful and potentially surprising insights 


## What DE Skills are Highlighted?

- Cleaning messy data
- Working with large datasets
- Building pipelines, ideally dynamic ones
- Extracting insights from data


## Output

The final output should be at least record the set of brilliant moves for the entire dataset, but may extend to creating a games and moves table. The visualization and analysis will likely be done in Python using a Jupyter notebook or markdown.