from collections import defaultdict, deque


class DependencyGraph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.weights = {}

    def add_component(self, name):
        if name not in self.graph:
            self.graph[name] = []

    def add_dependency(self, from_component, to_component, weight=1):
        if from_component not in self.graph:
            self.graph[from_component] = []
        if to_component not in self.graph:
            self.graph[to_component] = []

        self.graph[from_component].append(to_component)
        self.weights[(from_component, to_component)] = weight

    def is_acyclic(self):
        return self.get_topological_order() is not None

    def get_topological_order(self):
        indegree = {node: 0 for node in self.graph}

        for node in self.graph:
            for nei in self.graph[node]:
                indegree[nei] += 1

        queue = deque([n for n in indegree if indegree[n] == 0])
        result = []

        while queue:
            node = queue.popleft()
            result.append(node)

            for nei in self.graph[node]:
                indegree[nei] -= 1
                if indegree[nei] == 0:
                    queue.append(nei)

        if len(result) != len(self.graph):
            return None

        return result

    def get_critical_path(self):
        order = self.get_topological_order()
        if order is None:
            return None, None

        dist = {node: 0 for node in self.graph}
        parent = {node: None for node in self.graph}

        for node in order:
            for nei in self.graph[node]:
                w = self.weights[(node, nei)]
                if dist[node] + w > dist[nei]:
                    dist[nei] = dist[node] + w
                    parent[nei] = node

        end = max(dist, key=lambda x: dist[x])
        max_dist = dist[end]

        path = []
        while end is not None:
            path.append(end)
            end = parent[end]

        path.reverse()
        return path, max_dist


def visualize_graph(graph, file_name="graph"):
    from graphviz import Digraph
    g = Digraph()

    for node in graph.graph:
        g.node(node)
        for nei in graph.graph[node]:
            g.edge(node, nei)

    g.render(file_name, format="png", cleanup=True)
