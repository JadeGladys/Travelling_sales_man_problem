from map_maker import create_cities, create_map, NO_ROAD, describe_map
import heapq

START_CITY = 0


def nearest_neighbor(table):
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

        # once next best city is none algorithm ends
        # this happenes if one of the roads is removed since the while loops stops at the last city
        # this wouldn't affect returning back to the start
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


def dijkstra(table):
    # find a roundtrip by always picking the cheapest road in the waiting list
    count = len(table)
    waiting_list = [([START_CITY], 0)]

    while len(waiting_list) > 0:
        # take out the cheapest route
        route, cost = heapq.heappop(waiting_list)
        print("Took out:", route, cost)

        here = route[-1]

        # since even full trips are returned to the waiting list we add 1 the number of cities
        if len(route) == count + 1:
            return route, cost

        # if all cities have been visited add the return cost and add route to waiting list
        if len(route) == count:
            if table[here][START_CITY] != NO_ROAD:
                full_route = route + [START_CITY]
                full_cost = cost + table[here][START_CITY]
                waiting_list.append((full_route, full_cost))
            continue

        for next_city in range(count):
            if next_city not in route:
                if table[here][next_city] != NO_ROAD:
                    new_route = route + [next_city]
                    new_cost = cost + table[here][next_city]
                    waiting_list.append((new_route, new_cost))

    return None, NO_ROAD


# for testing this file to see if dfs and bfs are returning the right thing
def main():
    cities = create_cities(6, 42)
    table = create_map(cities, True, True, 42)
    describe_map(cities, table)
    # print(nearest_neighbor(table))
    print(dijkstra(table))


if __name__ == "__main__":
    main()
