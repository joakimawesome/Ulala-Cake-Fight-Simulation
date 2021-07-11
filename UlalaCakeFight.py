import time
from datetime import timedelta, datetime
import numpy as np
import pandas as pd
from tables import People



# returns time remaining for event.
def countdown():
    endDate = datetime(2021, 7, 24, 22) # Cake Fight event deadline
    timeTotal = endDate - datetime.now()
    return timeTotal.total_seconds()



# ranks up a character, changing the stats the same way as in the game.
def rankup(person, bg_dict=None):
    if bg_dict == None:
        bg_dict = People
    for role in bg_dict:
        for p in role:
            if p == person:
                consume = role[str(person)]["ratio"][0]
                output = role[str(person)]["ratio"][1]
                role[str(person)]["rank"] += 1
                role[str(person)]["consume"] += consume
                role[str(person)]["output"] += output



# reverses a rankup a character for personal use.
def rankdown(person, bg_dict=None):
    if bg_dict == None:
        bg_dict = People
    for role in bg_dict:
        for p in role:
            if p == person:
                consume = role[str(person)]["ratio"][0]
                output = role[str(person)]["ratio"][1]
                role[str(person)]["rank"] -= 1
                role[str(person)]["consume"] -= consume
                role[str(person)]["output"] -= output



# Set the ranks to bakers or gifters.
# Input integers
def ranks(bg_dict=None):
    if bg_dict == None:
        bg_dict = People
    for role in bg_dict:
        for person in role:
            role[str(person)]["rank"] = 0
            role[str(person)]["consume"] = 0
            role[str(person)]["output"] = 0
            print(person)
            x = int(input("rank: "))
            for _ in range(x):
                rankup(person, bg_dict=bg_dict) # Function in Cell 3
    return bg_dict



# Returns total wheat produced by the end of the event from remaining time.
def harvest(wheatOutput, wheatTotal, wheatStored=0):
    remaining = countdown()    
    wheatTotal += wheatStored
    while remaining > 0:
        wheatTotal += int(wheatOutput)
        remaining -= 10
    return wheatTotal



# Consumes the total wheat to return total cake produced.
def bake(baker, wheatTotal, cakeTotal, bg_dict, cakeStored=0):
    remaining = countdown()
    Bakers = bg_dict[0]
    consume = Bakers[str(baker)]["consume"]
    output = Bakers[str(baker)]["output"]           
    while remaining > 0 and wheatTotal >= 0:
        wheatTotal -= consume
        cakeTotal += output
        remaining -= 10
    return cakeTotal   



# Consumes the total cake to return total gifts produced.
def gift(gifter, cakeTotal, giftTotal, bg_dict, giftsStored=0):
    remaining = countdown()
    Gifters = bg_dict[1]
    consume = Gifters[str(gifter)]["consume"]
    output = Gifters[str(gifter)]["output"]
    while remaining > 0 and cakeTotal >= 0:
        cakeTotal -= consume
        giftTotal += output
        remaining -= 10
    return giftTotal



# RUN THIS FUNCTION
def run_sim(wheatOutput, wheatStored=0, cakeStored=0, giftsStored=0):
    # This is why I should've used a class
    bg_dict = None
    bg_dict = ranks()
    Bakers = bg_dict[0]
    Gifters = bg_dict[1]
    wheatTotal = 0 
    cakeTotal = 0
    giftTotal = 0
    bakerName = []
    gifterName = []
    giftsProjected = []

    for baker in Bakers:
        for gifter in Gifters:
            wheatTotal = harvest(wheatOutput, wheatTotal, wheatStored=wheatStored) # changes wheatTotal
            cakeTotal = bake(baker, wheatTotal, cakeTotal, bg_dict, cakeStored=cakeStored) # changes cakeTotal
            giftTotal = gift(gifter, cakeTotal, giftTotal, bg_dict, giftsStored=giftsStored) # finalizes giftTotal
            bakerName.append(baker)
            gifterName.append(gifter)            
            giftsProjected.append(giftTotal)
            wheatTotal = 0
            cakeTotal = 0
            giftTotal = 0       

    array = [bakerName, gifterName]
    index = pd.MultiIndex.from_arrays(array, names=("Baker", "Gifter"))
    df = pd.DataFrame(giftsProjected, index=index, columns=["Projected Gifts"])
    pd.set_option('display.max_rows', None)
    return df



run_sim(input("Wheat Output: ")).sort_values('Projected Gifts', ascending=False) # e.g., 2 4 2 2 3 3 3 3 2 3 3 3 2 2 3 3; each integer inputed individually


# ON SECOND THOUGHT, I SHOULD'VE USED A CLASS FOR THIS ENTIRE CODE. (might update later)