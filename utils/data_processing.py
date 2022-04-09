import numpy as np
import math
news_index = {0:"Aliens in Area 51", 1:"Cellular Memory", 2:"Moon Landing Hoax", 3:"Loch Ness Monster", 4:"Blonder Hair is disappearing", 5:"Facial Recognition to obtain hotel records"}
news_chosen = [[], [], [], [], [], []]
true_chosen = []
false_chosen = []

with open("./data.txt", "r") as f:
    for i in range(0, 6):
        line = f.readline()
        data = line.rstrip("\n").split(" ")[1].split(",")
        for j in data:
            news_chosen[i].append(j)

print(news_chosen)
