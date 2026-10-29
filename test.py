import time
import csv
import tracemalloc
from map_maker import create_cities, create_map, NO_ROAD
from full_search import dfs, bfs
from greedy_search import nearest_neighbor, dijkstra
from astar_search import a_star_admissible, a_star_inadmissible
from aco_search import aco

SEEDS = [1, 2, 3]
TIME_LIMIT = 60     # seconds; once a run takes longer, skip that algorithm

ALGORITHMS = [
    ("BFS", bfs),
    ("DFS", dfs),
    ("NN", nearest_neighbor),
    ("Dijkstra", dijkstra),
    ("A* admissible", a_star_admissible),
    ("A* inadmissible", a_star_inadmissible),
    ("ACO", aco),
]

SCENARIOS = [
    ("Symmetric, all-roads", True, True),
    ("Symmetric, 80% roads", True, False),
    ("Asymmetric, all-roads", False, True),
    ("Asymmetric, 80% roads", False, False)
]


def measure(algorithm, table):
    # run one algorithm on one map and measure its time and memory
    tracemalloc.start()

    start_time = time.perf_counter()
    deadline = start_time + TIME_LIMIT
    route, cost = algorithm(table, deadline)
    end_time = time.perf_counter()
    _, peak_memory = tracemalloc.get_traced_memory()

    tracemalloc.stop()

    time_used = end_time - start_time
    memory_kb = peak_memory / 1024

    return route, cost, time_used, memory_kb


def main():

    # create a csv file and have python list converted to csv
    with open("results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Scenario", "Cities", "Seed", "Algorithm", "Status",
                         "Best Route", "Best Cost", "Time (s)", "Memory (KB)"])

        for scenario_name, is_symmetric, has_all_roads in SCENARIOS:
            too_slow = []

            for n in range(5, 21):      # number of cities: 5 to 20
                timed_out = []

                for seed in SEEDS:
                    map_seed = seed * 40 + n
                    cities = create_cities(n, map_seed)
                    table = create_map(cities, is_symmetric,
                                       has_all_roads, map_seed)

                    for name, algorithm in ALGORITHMS:
                        if name in too_slow:
                            print(scenario_name, "| cities:",
                                  n, "| Seed:", map_seed, "|", name, "| SKIPPED")
                            writer.writerow(
                                [scenario_name, n, map_seed, name, "Skipped", "", "", "", ""])
                            continue

                        route, cost, time_used, memory_kb = measure(
                            algorithm, table)

                        if cost is None:
                            print(scenario_name, "| cities:", n, "| Seed:", map_seed, "|", name,
                                  "| TIMEOUT after", TIME_LIMIT, "s")
                            writer.writerow([scenario_name, n, map_seed, name, "Timeout", "", "", round(
                                time_used, 6), round(memory_kb, 4)])
                            if name not in timed_out:
                                timed_out.append(name)
                            continue

                        if time_used > TIME_LIMIT:
                            if name not in timed_out:
                                timed_out.append(name)

                        if cost == NO_ROAD:
                            status = "No trip"
                        else:
                            status = "Trip found"

                        print(scenario_name, "| cities:", n, "| Seed:", map_seed, "|", name,
                              "|", status,
                              "| Route:", route,
                              "| cost:", round(cost, 4),
                              "| time:", round(time_used, 6),
                              "| memory:", memory_kb)

                        writer.writerow([scenario_name, n, map_seed, name, status, route,
                                        round(cost, 4),
                                        round(time_used, 6),
                                        (round(memory_kb, 4))])

                too_slow = too_slow + timed_out


if __name__ == "__main__":
    main()
