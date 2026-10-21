import random

NO_ROAD = float('inf')


def create_cities(n, seed):
    # create n random cities with x,y,z coordinates
    rdm = random.Random(seed)
    cities = []
    for i in range(n):
        x = rdm.uniform(-100, 100)
        y = rdm.uniform(-100, 100)
        z = rdm.uniform(0, 50)
        cities.append((x, y, z))
    return cities


def cities_dist(a, b):
    # measure the distance between two cities using their x,y,z coordinates
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    dz = b[2] - a[2]
    return (dx**2 + dy**2 + dz**2) ** 0.5


def create_map(cities, symmetric, all_roads, seed):
    # building the price table with no value yet
    count = len(cities)
    rdm = random.Random(seed)
    table = []

    for i in range(count):
        row = []
        for j in range(count):
            row.append(NO_ROAD)
        table.append(row)

    # add the price which is equal to the distance between two cities
    for i in range(count-1):
        for j in range(i+1, count):
            # first check: all roads or 80% of the roads
            if not all_roads:
                if rdm.random() < 0.2:
                    continue
            distance = cities_dist(cities[i], cities[j])
            # second check: symmentrical or asymmetrical
            if symmetric:
                table[i][j] = distance
                table[j][i] = distance
            else:
                height_i = cities[i][2]
                height_j = cities[j][2]
                if height_j > height_i:
                    table[i][j] = distance + (distance * 0.1)
                    table[j][i] = distance - (distance * 0.1)
                elif height_j < height_i:
                    table[i][j] = distance - (distance * 0.1)
                    table[j][i] = distance + (distance * 0.1)
                else:
                    table[i][j] = distance
                    table[j][i] = distance
    return table


def describe_map(cities, table):
    # Print road that are removed, and print uphill or downhill prices.
    count = len(table)
    removed = 0
    for i in range(count-1):
        for j in range(i + 1, count):
            if table[i][j] == NO_ROAD:
                print("road", i, "-", j, "and", j, "-", i, ": REMOVED")
                removed = removed + 1
            else:
                height_i = cities[i][2]
                height_j = cities[j][2]
                if height_j > height_i:
                    i_to_j = "uphill"
                    j_to_i = "downhill"
                elif height_j < height_i:
                    i_to_j = "downhill"
                    j_to_i = "uphill"
                else:
                    i_to_j = "flat"
                    j_to_i = "flat"
                print(i, "->", j, i_to_j, round(table[i][j], 1),
                      "   and   ", j, "->", i, j_to_i, round(table[j][i], 1))
    print("removed roads:", removed)


def main():
    cities = create_cities(5, 42)
    table = create_map(cities, True, False, 42)
    # test to see if cities are created randomly but the seed helps recreate it
    print(create_cities(5, 12))

    # test the distance calculator
    print(cities_dist((0, 0, 0), (3, 4, 12)))
    print(cities_dist((3, 4, 12), (0, 0, 0)))
    print(cities_dist((0, 0, 0), (3, 4, 0)))

# test if the table is being create
    cities = create_cities(20, 42)
    table = create_map(cities, True, False, 42)
    roads = 0
    for row in table:
        for price in row:
            print(round(price, 1), end="  ")
        print()
    for i in range(len(table)):
        for j in range(i+1, len(table)):
            if table[i][j] != NO_ROAD:
                roads = roads + 1
    print("roads:", roads, "out of", len(table) * (len(table) - 1) // 2)


# these are ran only this file
if __name__ == "__main__":
    main()
