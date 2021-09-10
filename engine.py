import numpy as np


# gen_in_league method takes in opt (possible match-up coordinates remaining)
# method returns pair of coordinates to simulate randomly picking 2 of 5 (no equal pairs allowed)
def gen_in_league(opt):
    team_comp = []

    # if last 2 items in array to choose from, pick those 2 and reset choice array
    if len(opt) == 2:
        team_comp.append(opt.pop(0))
        team_comp.append(opt.pop(0))
        opt = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
        np.random.shuffle(opt)

    # if not last 2, choose first, then choose second based on conditions
    else:
        team_comp.append(opt.pop(0))

        # while pair not chosen: if first choice != chosen (pick it), else (pick second choice)
        while len(team_comp) < 2:
            if opt[0] != team_comp[0]:
                team_comp.append(opt.pop(0))
            else:
                team_comp.append(opt.pop(1))

            # if only 2 choices left in array, check they're not equal (if so, switch with item chosen)
            if len(opt) == 2:
                if opt[0] == opt[1]:
                    switch = team_comp.pop(0)
                    team_comp.append(opt.pop(0))
                    opt.append(switch)

    # return team_comp (chosen pair), opt (remaining choice array)
    return team_comp, opt


# gen_out_league method takes in opt (remaining), na (current not allowed), na_array (not allowed remaining)
# method returns two pairs of coordinates: 2 chosen from opt, 2 remaining (not chosen or na)
def gen_out_league(opt, na, na_array):
    team_inter = []
    putback = 0
    removed = []

    # use nums for returning 2 remaining coordinates (not chosen and not na)
    nums = [0, 1, 2, 3, 4]
    nums.pop(na)

    # if last 2 items in array to choose from, pick those 2 then reset choice array and not allowed array
    if len(opt) == 2:

        team_inter.append(opt.pop(0))
        team_inter.append(opt.pop(0))
        na_array = [0, 1, 2, 3, 4]
        opt = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
        np.random.shuffle(opt)

    # if not last two, choose 2 based on conditions that chosen pairs cannot be equal or same as na value
    else:
        i = 0

        # while pair not chosen, check coordinates at incremented i value
        while len(team_inter) < 2:
            if opt[i] != na:  # if not equal to na, can be added
                if len(team_inter) == 0:  # if not item in pair, add first item from choice array
                    team_inter.append(opt.pop(i))
                    i -= 1
                else:
                    if opt[i] != team_inter[0]:  # if already item in pair, check if second would be equal
                        team_inter.append(opt.pop(i))  # if not equal, add second item to make pair
                        i -= 1

                # if pair chosen: check if all future pairings possible
                if len(team_inter) == 2:

                    # if only 2 items left choice array:
                    if len(opt) == 2:
                        if opt[0] == opt[1]:  # if items are same, switch one with chosen pair
                            if team_inter[0] != na_array[0]:  # check if item is na before switch
                                switch = team_inter.pop(0)
                            else:
                                switch = team_inter.pop(1)
                            team_inter.append(opt.pop(0))
                            opt.append(switch)

                        # if either item left in choice array is not allowed for next pair
                        # check conditions and switch with chosen pair item where possible
                        if na_array[0] == opt[0]:
                            if team_inter[0] != opt[1]:
                                switch = team_inter.pop(0)
                            else:
                                switch = team_inter.pop(1)
                            team_inter.append(opt.pop(0))
                            opt.append(switch)
                        if na_array[0] == opt[1]:
                            if team_inter[0] != opt[0]:
                                switch = team_inter.pop(0)
                            else:
                                switch = team_inter.pop(1)
                            team_inter.append(opt.pop(1))
                            opt.append(switch)

                    # if 2 pairs left to create, check if both future pairings possible:
                    if len(opt) == 4:
                        for item in na_array:
                            # if no item in na_array appears > 1 time in choice array, conditions met
                            # if an item appears > 1 time, current pair must be regenerated
                            if opt.count(item) > 1:
                                putback += 1  # allows for reiteration through choices without repeats
                                opt.append(team_inter.pop(1))

            #
            if len(opt) != 0 and len(team_inter) < 2:
                i += 1
                # if all attempts to pair second with first item are used: (no pairs allowed for first item)
                # reset values for choice array and reiterate through (with first item removed)
                if i == len(opt) - putback:
                    i = 0
                    putback = 0
                    removed.append(team_inter.pop(0))

    # after pair chosen, nums becomes pair of coordinates not equal to chosen pair or na
    nums.remove(team_inter[0])  # removing chosen pair items from nums
    nums.remove(team_inter[1])

    for item in removed:
        opt.append(item)  # restore choice array with removed items for next team to choose from
    return team_inter, nums, opt, na_array  # return 2 pairs of coordinates and 2 arrays (choices and na left)
