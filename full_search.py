from map_maker import create_cities, create_map, NO_ROAD, describe_map

START_CITY = 0


def dfs(table):
    count = len(table)

    best_route = None

    # best cost starts with infinity so it can always be cheaper as we replace it
    best_cost = NO_ROAD

    # waiting list starts at city 0 and with zero cost
    waiting_list = [([START_CITY], 0)]

    # Check if the waiting list is not empty and create next routes
    while len(waiting_list) > 0:
        # remove the last element since DFS is LIFO
        route, cost = waiting_list.pop()

        # to get where the salesman is currently standing in a route we point to the last element of the list
        here = route[-1]

        if len(route) == count:
            if table[here][START_CITY] != NO_ROAD:
                total_cost = cost + table[here][START_CITY]
                # print("complete trip:", route +
                #       [START_CITY], round(total_cost, 3))
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


def bfs(table):
    count = len(table)

    best_route = None

    # best cost starts with infinity so it can always be cheaper as we replace it
    best_cost = NO_ROAD

    # waiting list starts at city 0 and with zero cost
    waiting_list = [([START_CITY], 0)]

    # Check if the waiting list is not empty and create next routes
    while len(waiting_list) > 0:
        # remove the first element since BFS is FIFO
        route, cost = waiting_list.pop(0)

        here = route[-1]

        if len(route) == count:
            if table[here][START_CITY] != NO_ROAD:
                total_cost = cost + table[here][START_CITY]
                # print("complete trip:", route +
                #       [START_CITY], round(total_cost, 3))
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


# for testing this file to see if dfs and bfs are returning the right thing
def main():
    cities = create_cities(12, 42)
    table = create_map(cities, True, True, 42)
    # describe_map(cities, table)
    print("bfs;", bfs(table))
    print("dfs", dfs(table))


if __name__ == "__main__":
    main()
