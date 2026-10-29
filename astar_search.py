import heapq
import time
from map_maker import create_cities, create_map, NO_ROAD

START_CITY = 0


def cheapest_road(table):
    # find the cheapest road
    count = len(table)

    cheapest = NO_ROAD

    for i in range(count):
        for j in range(count):
            if table[i][j] != NO_ROAD:
                if table[i][j] < cheapest:
                    cheapest = table[i][j]
    return cheapest


def average_road(table):
    # find the average cost of all roads
    count = len(table)
    total = 0
    roads = 0

    for i in range(count):
        for j in range(count):
            if table[i][j] != NO_ROAD:
                total += table[i][j]
                roads += 1
    return total / roads


def guess(count, route, guess_per_road):
    # guess the cost to finish the route
    roads_left = count - len(route) + 1
    return roads_left * guess_per_road


def a_star(table, guess_per_road, deadline=None):
    count = len(table)
    start_score = 0 + guess(count, [START_CITY], guess_per_road)
    waiting_list = [(start_score, 0, [START_CITY])]

    while len(waiting_list) > 0:
        # check whether the algorithm has not exceeded the time limit
        if deadline is not None and time.perf_counter() > deadline:
            return None, None

        # take out the route with the lowest score
        _, cost, route = heapq.heappop(waiting_list)

        here = route[-1]

        if len(route) == count + 1:
            return route, cost

        if len(route) == count:
            if table[here][START_CITY] != NO_ROAD:
                full_route = route + [START_CITY]
                full_cost = cost + table[here][START_CITY]
                full_score = full_cost + \
                    guess(count, full_route, guess_per_road)
                heapq.heappush(
                    waiting_list, (full_score, full_cost, full_route))
            continue

        for next_city in range(count):
            if next_city not in route:
                if table[here][next_city] != NO_ROAD:
                    new_route = route + [next_city]
                    new_cost = cost + table[here][next_city]
                    new_score = new_cost + \
                        guess(count, new_route, guess_per_road)
                    heapq.heappush(
                        waiting_list, (new_score, new_cost, new_route))

    return None, NO_ROAD


def a_star_admissible(table, deadline=None):
    return a_star(table, cheapest_road(table), deadline)


def a_star_inadmissible(table, deadline=None):
    return a_star(table, average_road(table), deadline)


# testing for just this file
def main():
    cities = create_cities(6, 42)
    table = create_map(cities, True, True, 42)
    print("a_star admissible:", a_star_admissible(table))
    print("a_star inadmissible:", a_star_inadmissible(table))


if __name__ == "__main__":
    main()
