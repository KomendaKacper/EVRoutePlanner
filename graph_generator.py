import random
from src.graph import Graph
from src.charging_station import ChargingStation

def generate_graph(output_file="generated_graph.py", num_nodes=100, num_edges=1000, num_stations=30):
    """
    Generuje graf i zapisuje go do pliku w formacie używanym w aplikacji.

    :param output_file: Nazwa pliku do zapisania grafu.
    :param num_nodes: Liczba węzłów w grafie.
    :param num_edges: Liczba krawędzi w grafie.
    :param num_stations: Liczba stacji ładowania w grafie.
    """
    nodes = [f"N{i}" for i in range(num_nodes)] 
    graph = Graph()
    distances = {}
    stations = {}

    for i in range(num_nodes):
        start = nodes[i]
        end = nodes[(i + 1) % num_nodes]  # Łączenie wierzchołków w cyklu
        distance = random.randint(10, 100)
        difficulty = round(random.uniform(1.0, 2.0), 2)
        graph.add_edge(start, end, distance, difficulty=difficulty)
        graph.add_edge(end, start, distance, difficulty=difficulty)
        distances[(start, end)] = distance
        distances[(end, start)] = distance

    # Dodawanie pozostałych krawędzi
    while len(distances) < num_edges:
        start = random.choice(nodes)
        end = random.choice(nodes)
        if start != end and (start, end) not in distances:
            distance = random.randint(10, 100)
            difficulty = round(random.uniform(1.0, 2.0), 2)
            graph.add_edge(start, end, distance, difficulty=difficulty)
            graph.add_edge(end, start, distance, difficulty=difficulty)
            distances[(start, end)] = distance
            distances[(end, start)] = distance

    for node in nodes:
        if node not in graph.edges or not graph.edges[node]:
            potential_target = random.choice([n for n in nodes if n != node])
            distance = random.randint(10, 100)
            difficulty = round(random.uniform(1.0, 2.0), 2)
            graph.add_edge(node, potential_target, distance, difficulty=difficulty)
            graph.add_edge(potential_target, node, distance, difficulty=difficulty)
            distances[(node, potential_target)] = distance
            distances[(potential_target, node)] = distance

    for _ in range(num_stations):
        station_node = random.choice(nodes)
        if station_node not in stations:
            price_per_kwh = round(random.uniform(0.4, 0.8), 2)  # Cena za kWh
            queue_time = round(random.uniform(0.1, 0.5), 2)  # Czas oczekiwania w godzinach
            max_power = random.randint(30, 100)  # Maksymalna moc ładowania w kW
            stations[station_node] = ChargingStation(
                id=station_node,
                x=random.randint(0, 100),
                y=random.randint(0, 100),
                price_per_kwh=price_per_kwh,
                queue_time=queue_time,
                max_power=max_power,
            )

    with open(output_file, "w") as f:
        f.write("from src.graph import Graph\n")
        f.write("from src.charging_station import ChargingStation\n\n")
        f.write("# Wygenerowany graf\n")
        f.write("graph = Graph()\n")
        for node1, edges in graph.edges.items():
            for node2, edge_data in edges.items():
                f.write(f'graph.add_edge("{node1}", "{node2}", {edge_data["distance"]}, '
                        f'difficulty={edge_data["difficulty"]})\n')
        f.write("\n")
        f.write("# Węzły grafu\n")
        f.write(f'nodes = {nodes}\n\n')
        f.write("# Odległości między wierzchołkami\n")
        f.write(f'distances = {distances}\n\n')
        f.write("# Wygenerowane stacje ładowania\n")
        f.write("stations = {\n")
        for station, data in stations.items():
            f.write(f'    "{station}": ChargingStation("{station}", {data.x}, {data.y}, '
                    f'price_per_kwh={data.price_per_kwh}, queue_time={data.queue_time}, '
                    f'max_power={data.max_power}),\n')
        f.write("}\n")

    print(f"Graf został wygenerowany i zapisany do pliku {output_file}.")

if __name__ == "__main__":
    generate_graph()
