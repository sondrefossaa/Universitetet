from sys import stdin


lines = stdin.readlines()

for line in lines[1:]:
    population, growth_factor, food_prod = map(int, line.split())
    years = 0
    current_food = food_prod
    while True:
        current_food = food_prod
        current_food -= population
        population *= growth_factor
        if current_food < 0:
            break
        years += 1

    print(years)
