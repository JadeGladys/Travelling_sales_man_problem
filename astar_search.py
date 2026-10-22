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


def find_lowest_score(waiting_list):
    lowest_score = NO_ROAD
    lowest_position = 0

    for index_position in range(len(waiting_list)):
        _, _, score = waiting_list[index_position]
        if score < lowest_score:
            lowest_score = score
            lowest_position = index_position
    return waiting_list.pop(lowest_position)


def a_star(table, guess_per_road):
    count = len(table)
    start_score = 0 + guess(count, [START_CITY], guess_per_road)
    waiting_list = [([START_CITY], 0, start_score)]

    while len(waiting_list) > 0:
        # take out the route with the lowest score
        route, cost, _ = find_lowest_score(waiting_list)
        # print("Took out:", route, cost)

        here = route[-1]

        if len(route) == count + 1:
            return route, cost

        if len(route) == count:
            if table[here][START_CITY] != NO_ROAD:
                full_route = route + [START_CITY]
                full_cost = cost + table[here][START_CITY]
                full_score = full_cost + \
                    guess(count, full_route, guess_per_road)
                waiting_list.append((full_route, full_cost, full_score))
            continue

        for next_city in range(count):
            if next_city not in route:
                if table[here][next_city] != NO_ROAD:
                    new_route = route + [next_city]
                    new_cost = cost + table[here][next_city]
                    new_score = new_cost + \
                        guess(count, new_route, guess_per_road)
                    waiting_list.append((new_route, new_cost, new_score))

    return None, NO_ROAD


def a_star_admissible(table):
    return a_star(table, cheapest_road(table))


def a_star_inadmissible(table):
    return a_star(table, average_road(table))


def main():
    cities = create_cities(6, 42)
    table = create_map(cities, True, True, 42)
    print("a_star admissible:", a_star_admissible(table))
    print("a_star inadmissible:", a_star_inadmissible(table))


if __name__ == "__main__":
    main()
