import pandas as pd  # for use of dataframes
import matplotlib.pyplot as plt  # for plotting location and travel for teams
import numpy as np  # for np array manipulation
import engine  # for use of methods written in engine

teams = pd.read_excel("mlb_teams.xlsx")

# plot city coordinates for all teams (check if resembles united states big cities)
plt.scatter(x=-teams['lng'], y=teams['lat'], s=10)
plt.show()

rot = 0
series = pd.DataFrame()
games = pd.DataFrame()

# undetermined columns in teams to be generated below
teams['in_league'] = ''
teams['out_league'] = ''
teams['home'] = ''
teams['away'] = ''
teams['rival_coord'] = ''

# arrays of indices 0-4 are generated and shuffled for use in determining match-ups
in_l = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
out_l = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
single = [0, 1, 2, 3, 4]
out_ha = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
rivals = [0, 1, 2, 3, 4]  # rivals not shuffled because only used to check w curr_rival

np.random.shuffle(in_l)
np.random.shuffle(out_l)
np.random.shuffle(single)
np.random.shuffle(out_ha)

# loop through teams and determine in and out of league random match-ups if necessary
for index, row in teams.iterrows():

    # for first and second divisions, generate 2 teams for 6 game series (2x6, 3x7)
    # no need to generate for third division because predetermined from first two
    if row['division'] < 3:

        # generate coordinates for 2x6 game series using gen_in_league method
        in_rand = engine.gen_in_league(in_l)
        teams.at[index, 'in_league'] = in_rand[0]  # adjust teams accordingly
        in_l = in_rand[1]  # adjust array in_l for use on next team

    # for first league, generate inter_league match-up randomness
    # no need to generate for league = 1 because predetermined from league = 0
    if row['league'] == 0:

        # for rot = 0 (playing division w rival)
        # generate 1x6 (rival), 2x5, and 2x3 game series
        if rot == 0:

            # determine current rival, remove from rivals array for checking
            curr_rival = (teams.index[teams['rival'] == row['team']] % 5).to_list()[0]
            rivals.remove(curr_rival)
            teams.at[index, 'rival_coord'] = curr_rival

            # generate 2x5 and 2x3 game series using gen_out_league method
            out_rand = engine.gen_out_league(out_l, curr_rival, rivals)

            teams.at[index, 'out_league'] = out_rand[0]  # adjust teams accordingly
            teams.at[index, 'home'] = out_rand[1][0]
            teams.at[index, 'away'] = out_rand[1][1]

            out_l = out_rand[2]  # adjust arrays (out_l, rivals) for use on next team
            rivals = out_rand[3]

        # for rot != 0 (not playing division w rival
        # generate 1x6, 2x3 (home), 2x3 (away) game series
        else:

            # determine team for 1x6 (works same as rival in steps below)
            inter_single = single.pop(0)
            if len(single) == 0:  # if last item, reset single array for next team
                single = [0, 1, 2, 3, 4]
                np.random.shuffle(single)
            teams['out_league'][index] = inter_single

            # generate 2 home and 2 away series using gen_out_league method
            out_rand = engine.gen_out_league(out_ha, inter_single, single)

            teams.at[index, 'home'] = out_rand[0]  # adjust teams accordingly
            teams.at[index, 'away'] = out_rand[1]

            out_ha = out_rand[2]  # adjust arrays (out_l, singles) for use on next team
            single = out_rand[3]

print(teams)
