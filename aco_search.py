import random
from map_maker import create_cities, create_map, NO_ROAD

START_CITY = 0

# ACO settings
ANTS = 10           # number of ants used per round
ROUNDS = 100        # number of rounds
FADE = 0.8          # each round, every road keeps this much of their smell
ADD = 100           # each ant adds ADD / (its trip cost) to every road it used
ALPHA = 1           # how much the ants trust the smell
BETA = 1            # how much the ants trust short roads
SEED = 42           # makes the ants' random choices repeatable


def lottery(cities, scores, rdm):
    # pick a city at random; cities with a bigger score get more chances

    # find the sum of all scores
    total = 0
    for score in scores:
        total += score

    # calculate the chance of each city to be picked using their score
    chances = []
    for score in scores:
        chances.append(score / total)

    # generate a random number between 0 and 1
    ticket = rdm.random()

    # find where the random number falls within each cities' chance
    border = 0
    for index in range(len(cities)):
        border += chances[index]
        if ticket < border:
            return cities[index]

    return cities[-1]


def build_trip(table, smell, rdm):
    # let one ant build a full trip, choosing the next city by lottery

    count = len(table)
    route = [START_CITY]
    cost = 0

    while len(route) < count:
        here = route[-1]
        cities = []
        scores = []

        # calculate the score = smell x (1:distance) of next city
        for next_city in range(count):
            if next_city not in route:
                if table[here][next_city] != NO_ROAD:
                    smell_part = smell[here][next_city] ** ALPHA
                    distance_part = (1 / table[here][next_city]) ** BETA
                    cities.append(next_city)
                    scores.append(smell_part * distance_part)

        if len(cities) == 0:
            return None, NO_ROAD

        chossen = lottery(cities, scores, rdm)
        route.append(chossen)
        cost += table[here][chossen]

    if table[route[-1]][START_CITY] == NO_ROAD:
        return None, NO_ROAD

    cost += table[route[-1]][START_CITY]
    route.append(START_CITY)

    return route, cost


def aco(table, deadline=None):
    count = len(table)
    rdm = random.Random(SEED)

    smell = []
    for i in range(count):
        row = []
        for j in range(count):
            row.append(1.0)
        smell.append(row)

    best_route = None
    best_cost = NO_ROAD

    for round_number in range(ROUNDS):
        trips = []

        # let all ants build their trips and record which one has the best cost
        for ant in range(ANTS):
            route, cost = build_trip(table, smell, rdm)
            if route is not None:
                trips.append((route, cost))
                if cost < best_cost:
                    best_cost = cost
                    best_route = route

        # fade the smell
        for i in range(count):
            for j in range(count):
                smell[i][j] = smell[i][j] * FADE

        # add to smell for each ant that took that route
        for route, cost in trips:
            amount = ADD / cost

            for i in range(len(route) - 1):
                from_city = route[i]
                to_city = route[i + 1]
                smell[from_city][to_city] += amount

    return best_route, best_cost


# testing for just this file
def main():
    cities = create_cities(12, 42)
    table = create_map(cities, True, True, 42)
    print("aco:", aco(table))


if __name__ == "__main__":
    main()
