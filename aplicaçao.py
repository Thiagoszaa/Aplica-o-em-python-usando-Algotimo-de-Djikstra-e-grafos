import heapq
import networkx as nx
import matplotlib.pyplot as plt

def desenhaGrafico(graph, eulerian_path=None, dijkstra_path=None):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(8, 6))

    nx.draw(graph, pos, with_labels=True, node_size=700, node_color='lightblue', font_weight='bold')
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

    if eulerian_path:
        edges_in_path = [(eulerian_path[i], eulerian_path[i+1]) for i in range(len(eulerian_path)-1)]
        nx.draw_networkx_edges(graph, pos, edgelist=edges_in_path, edge_color='red', width=2, label="Eulerian Path")

    if dijkstra_path:
        edges_in_dijkstra = [(dijkstra_path[i], dijkstra_path[i+1]) for i in range(len(dijkstra_path)-1)]
        nx.draw_networkx_edges(graph, pos, edgelist=edges_in_dijkstra, edge_color='green', width=2, label="Dijkstra Path")

    plt.title("Grafo com Caminhos")
    plt.legend()
    plt.show()

# Criar grafo
graph = nx.Graph()
edges = [
    ('A', 'B', 1),
    ('A', 'C', 4),
    ('B', 'C', 2),
    ('B', 'D', 5),
    ('C', 'D', 1)
]
graph.add_weighted_edges_from(edges)

def encontrarCaminhoEuleriano(graph):
    odd_degree_nodes = [node for node, degree in graph.degree() if degree % 2 == 1]
    if len(odd_degree_nodes) not in [0, 2]:
        return None

    start_node = odd_degree_nodes[0] if odd_degree_nodes else list(graph.nodes)[0]
    path = []
    stack = [start_node]

    temp_graph = graph.copy()
    while stack:
        node = stack[-1]
        if temp_graph.degree(node) > 0:
            next_node = list(temp_graph.neighbors(node))[0]
            stack.append(next_node)
            temp_graph.remove_edge(node, next_node)
        else:
            path.append(stack.pop())
    return path[::-1]

def dijkstra(graph, start, end):
    
    distances = {node: float('inf') for node in graph.nodes}
    distances[start] = 0
    predecessors = {}
    priority_queue = [(0, start)]  # (distância, nó)

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == end:
            break

        for neighbor, attrs in graph[current_node].items():
            weight = attrs.get('weight', 1)
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    # Reconstruir o caminho de `start` para `end`
    path = []
    current = end
    while current in predecessors:
        path.insert(0, current)
        current = predecessors[current]
    if path:
        path.insert(0, start)
    return path


eulerian_path = encontrarCaminhoEuleriano(graph)
if eulerian_path:
    print("Caminho Euleriano:", eulerian_path)
else:
    print("Não possui caminho Euleriano")


start_node, end_node = 'A', 'D'
dijkstra_path = dijkstra(graph, start_node, end_node)
if dijkstra_path:
    print(f"Menor caminho entre {start_node} e {end_node} (Dijkstra):", dijkstra_path)
else:
    print(f"Não há caminho entre {start_node} e {end_node}")

# Desenhar grafo com os caminhos
desenhaGrafico(graph, eulerian_path, dijkstra_path)

