from typing import Dict, List, Tuple

import networkx
from matplotlib import pyplot

CITIES = {
    "EUA": (
        "Albuquerque",
        "Atlanta",
        "Boston",
        "Chicago",
        "Cleveland",
        "Denver",
        "Miami",
        "Minneapolis",
        "New York",
        "Philadelphia",
        "Phoenix",
        "Tulsa",
    ),
    "Brasil": (
        "Curitiba",
        "Foz",
        "Londrina",
        "Maringa",
        "Pinhais",
        "Ponta Grossa",
        "Sao Paulo",
    ),
}


CITY_RELATIONS = {
    "Internacional": (
        ("Chicago", "Pinhais"),
        ("Curitiba", "Atlanta"),
        ("Curitiba", "Chicago"),
        ("Curitiba", "Miami"),
        ("Curitiba", "New York"),
        ("Maringa", "Albuquerque"),
        ("Maringa", "Cleveland"),
        ("Minneapolis", "Foz"),
        ("Phoenix", "Maringa"),
        ("Ponta Grossa", "Cleveland"),
        ("Sao Paulo", "Boston"),
        ("Sao Paulo", "Chicago"),
        ("Sao Paulo", "Minneapolis"),
        ("Tulsa", "Maringa"),
        ("Tulsa", "New York"),
    ),
    "Nacional": (
        ("Albuquerque", "Atlanta"),
        ("Chicago", "New York"),
        ("Curitiba", "Sao Paulo"),
        ("Londrina", "Foz"),
        ("Miami", "Denver"),
        ("Miami", "New York"),
        ("Miami", "Philadelphia"),
        ("New York", "Cleveland"),
        ("New York", "Minneapolis"),
        ("Philadelphia", "Atlanta"),
        ("Phoenix", "Cleveland"),
        ("Pinhais", "Londrina"),
        ("Ponta Grossa", "Foz"),
        ("Ponta Grossa", "Londrina"),
        ("Sao Paulo", "Foz"),
        ("Sao Paulo", "Londrina"),
        ("Sao Paulo", "Ponta Grossa"),
    ),
}


def build_graph(cities: Dict, relations: Dict) -> networkx.Graph:
    g = networkx.Graph()
    for country, list_cities in cities.items():
        g.add_nodes_from(list_cities, country=country)
    for fligth_type, source_dest in relations.items():
        if fligth_type == "Internacional":
            g.add_edges_from(source_dest, cost=5)
        elif fligth_type == "Nacional":
            g.add_edges_from(source_dest, cost=1)
        else:
            raise Exception("Flight is not national or international!")

    return g


def draw_graph(graph: networkx.Graph) -> None:
    pyplot.figure()
    pos = networkx.spring_layout(graph, k=2, scale=2)
    networkx.draw(graph, pos, with_labels=True, font_weight="bold")

    pos_attrs = {}
    for node, coords in pos.items():
        pos_attrs[node] = (coords[0], coords[1] + 0.10)

    node_attrs = {}
    for node, attr in networkx.get_node_attributes(graph, "country").items():
        node_attrs[node] = f"Country: {attr}"

    networkx.draw_networkx_labels(graph, pos_attrs, labels=node_attrs)

    pyplot.show()


def calculate_clustering_coefficient(graph: networkx.Graph, city: str = None) -> float:
    if city:
        return networkx.clustering(graph)[city]
    return networkx.average_clustering(graph)


def calculate_max_length(
    graph: networkx.Graph, relations: Dict
) -> Tuple[int, List[str]]:
    paths = []
    for _, values in relations.items():
        for source, destine in values:
            paths = [path for path in networkx.all_simple_paths(graph, source, destine)]
    max_length = max(paths, key=len)
    return len(max_length), list(max_length)


if __name__ == "__main__":
    graph = build_graph(CITIES, CITY_RELATIONS)
    print("1: Desenho do grafo: ")
    draw_graph(graph)
    max_length, path = calculate_max_length(graph, CITY_RELATIONS)
    print(
        f"2.a: Número máximo de saltos é {max_length} | Caminho feito: {' -> '.join(path)}"
    )
    print(
        f"2.b: Coeficiente de clusterização de Curitiba: {calculate_clustering_coefficient(graph, 'Curitiba')} | "
        f"Coeficiente de clusterização da rede: {calculate_clustering_coefficient(graph)}"
    )
    # Descomente para gerar o GML
    # networkx.write_gml(graph, "city_relations.gml")
