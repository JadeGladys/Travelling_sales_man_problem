import heapq
import time
from map_maker import create_cities, create_map, NO_ROAD

START_CITY = 0


def nearest_neighbor(table, deadline=None):
    # Build one trip by always taking the cheapest road to an unvisited city

    count = len(table)
    route = [START_CITY]
    cost = 0

    while len(route) < count:
        here = route[-1]

        next_best_city = None
        best_cost = NO_ROAD

        for next_city in range(count):
            if next_city not in route:
                if table[here][next_city] != NO_ROAD:
                    if table[here][next_city] < best_cost:
                        best_cost = table[here][next_city]
                        next_best_city = next_city

        # if the loop doesn't return the next city,a trip can't be completed and alogorithm stops
        if next_best_city is None:
            return None, NO_ROAD

        cost += best_cost
        route.append(next_best_city)

    # check if the final city has an existing road back to the start
    last_city = route[-1]
    if table[last_city][START_CITY] == NO_ROAD:
        return None, NO_ROAD

    # if the road exists add the final cost and return it
    cost += table[last_city][START_CITY]
    route.append(START_CITY)
    return route, cost


def dijkstra(table, deadline=None):
    # find a roundtrip by always picking the cheapest route in the waiting list
    count = len(table)
    waiting_list = [(0, [START_CITY])]

    while len(waiting_list) > 0:
        # check whether the algorithm has not exceeded the time limit
        if deadline is not None and time.perf_counter() > deadline:
            return None, None

        # take out the cheapest route
        cost, route = heapq.heappop(waiting_list)

        here = route[-1]

        # since even full trips are returned to the waiting list we add 1 the number of cities
        if len(route) == count + 1:
            return route, cost

        # if all cities have been visited add the return cost and add route to waiting list
        if len(route) == count:
            if table[here][START_CITY] != NO_ROAD:
                full_route = route + [START_CITY]
                full_cost = cost + table[here][START_CITY]
                heapq.heappush(waiting_list, (full_cost, full_route))
            continue

        for next_city in range(count):
            if next_city not in route:
                if table[here][next_city] != NO_ROAD:
                    new_route = route + [next_city]
                    new_cost = cost + table[here][next_city]
                    heapq.heappush(waiting_list, (new_cost, new_route))

    return None, NO_ROAD


# testing for just this file
def main():
    cities = create_cities(6, 42)
    table = create_map(cities, True, True, 42)
    print("Nearest Neighbor:", nearest_neighbor(table))
    print("Dijkstra:", dijkstra(table))


if __name__ == "__main__":
    main()
