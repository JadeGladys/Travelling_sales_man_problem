import time
from map_maker import create_cities, create_map, NO_ROAD

START_CITY = 0


def dfs(table, deadline=None):
    count = len(table)

    best_route = None
    best_cost = NO_ROAD
    waiting_list = [([START_CITY], 0)]

    while len(waiting_list) > 0:
        # check whether the algorithm has not exceeded the time limit
        if deadline is not None and time.perf_counter() > deadline:
            return None, None

        # remove the last element since DFS is LIFO
        route, cost = waiting_list.pop()

        here = route[-1]

        if len(route) == count:
            if table[here][START_CITY] != NO_ROAD:
                total_cost = cost + table[here][START_CITY]
                if total_cost < best_cost:
                    best_cost = total_cost
                    best_route = route + [START_CITY]
            continue

        for next_city in range(count):
            if next_city not in route:
                if table[here][next_city] != NO_ROAD:
                    new_route = route + [next_city]
                    new_cost = cost + table[here][next_city]
                    waiting_list.append((new_route, new_cost))

    return best_route, best_cost


def bfs(table, deadline=None):
    count = len(table)

    best_route = None
    best_cost = NO_ROAD
    waiting_list = [([START_CITY], 0)]

    while len(waiting_list) > 0:
        # check whether the algorithm has not exceeded the time limit
        if deadline is not None and time.perf_counter() > deadline:
            return None, None

        # remove the first element since BFS is FIFO
        route, cost = waiting_list.pop(0)

        here = route[-1]

        if len(route) == count:
            if table[here][START_CITY] != NO_ROAD:
                total_cost = cost + table[here][START_CITY]
                if total_cost < best_cost:
                    best_cost = total_cost
                    best_route = route + [START_CITY]
            continue

        for next_city in range(count):
            if next_city not in route:
                if table[here][next_city] != NO_ROAD:
                    new_route = route + [next_city]
                    new_cost = cost + table[here][next_city]
                    waiting_list.append((new_route, new_cost))

    return best_route, best_cost


# testing for just this file
def main():
    cities = create_cities(6, 42)
    table = create_map(cities, True, True, 42)
    print("dfs:", dfs(table))
    print("bfs:", bfs(table))


if __name__ == "__main__":
    main()
