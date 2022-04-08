red_chosen = []
blue_chosen = []
with open('test.csv', "r") as f:
    red = f.readline()
    red_ar = red.split(',')
    blue = f.readline()
    blue_ar = blue.split(',')
    for i in range(0, 6):
        red_chosen.append(int(red_ar[i]))
        blue_chosen.append(int(blue_ar[i]))

print(red_chosen)
print(blue_chosen)
