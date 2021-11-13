### Insights from data exploration

I changed the fundamental question set I am trying to answer. Before I was looking for questions around brilliant moves, defined as the computer eval increased in a player's favor by 2 or more after making a move. However, after looking at [an example game](https://lichess.org/0Hn3NKvX) I found that in these moments the players were not always making brilliant moves, the engine was just ajusting to the depth. The new question set I am trying to answer is about forced checkmates. Possible questions include:
- Percent of checkmate in 1 that are found
- Percent of checkamte in 1 that are found by elo
- Games where a player lost after checkmate in one. Highest elo example. 
- Game with player with the highest elo who missed a checkmate in 1
- My percent of checkmates in 1 that are found
- Players with the most games and a perfect checkmate in 1 pct
- Could try percent of checkmate in n that are found by elo, but this would be tricky.

From 10000 games, the percent of checkmate in one completed is 66%. Intuitively, players with better elos spot checkmates in one at a higher rate. 

### How I plan to store the data for optimal query speed and compression of storage files

The final output will be a games table with games attributes like id, white username, black username, white elo, black elo, etc, and a moves table with the move, game id, move number, eval, etc. The games without an evaluation will be discarded. 

Based on the information I have learned in the course, I am unsure of the ideal format to create the pipeline. I think the best way would be to write each row directly to the cloud database as I ingest it, but I may need an intermediate file. For this analysis I loaded the data into a dictionary and then used pd.DataFrame(dictionary) to create a pandas dataframe. However, this step only worked for about 10,000 rows of data, and was prohibitively slow for 100s of thousands of records. I will ask my mentor whether making a pandas dataframe is necessary, or if I can bypass this step and write data directly to the database. If I need to make a pandas dataframe, I will need to work with my mentor to improve performance. However, all other steps in the code process 10s of thousands of rows in a second or two, so the mapping the dictionary to a dataframe is the only step I am currently concerned about. I used %lprun -f function function() to spot bottlenecks in the code. I can use multithreading or multiprocessing to speed up the process if needed. 