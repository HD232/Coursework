from pydantic import BaseModel
from typing import Dict

class ShortestPathResult(BaseModel):
    distances: Dict[str, Dict[str, float]]
    next_nodes: Dict[str, Dict[str, str]]
    message: str = ""

def floyd_warshall(graph: Dict[str, Dict[str, float]]) -> ShortestPathResult:
    nodes = list(graph.keys())
    dist = {u: {v: float('inf') for v in nodes} for u in nodes}
    next_node = {u: {v: None for v in nodes} for u in nodes}

    for u in graph:
        dist[u][u] = 0.0
        for v, weight in graph[u].items():
            dist[u][v] = weight
            next_node[u][v] = v

    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]

    return ShortestPathResult(distances=dist, next_nodes=next_node)