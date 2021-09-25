# MLBScheduler

This program was written by myself, David Heintz

The purpose of this program is to randomly generate a full season schedule for all 30 MLB teams playing 162 games which follows the rules for the generation of a real MLB schedule. This program also attempts to use a machine learning algorithm to minimze overall travel distance for all teams

Current: The program randomly determines the league matchups since each team plays 6 games against 2 teams and 7 games against 3 in each other division in the same league. It also randomly determines interleague matchups based on which divisions are meant to play each other that year.

Next: Using these determined matchup coordinates stores in the teams dataframe, the program can generate 3 30x30 matrices storing the number of games, series, and home/away that each team must play against each other team
