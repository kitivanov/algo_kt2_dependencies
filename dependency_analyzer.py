from collections import deque


class DependencyAnalyzer:
    def __init__(self, graph):
        self.graph = graph
        self.cache_dfs = {}  # кэширование для DFS

    def find_dependencies_bfs(self, start):
        levels = []
        visited = set([start])
        queue = deque([start])

        while queue:
            level_size = len(queue)
            level = []

            for _ in range(level_size):
                node = queue.popleft()
                for nei in self.graph.graph[node]:
                    if nei not in visited:
                        visited.add(nei)
                        queue.append(nei)
                        level.append(nei)

            if level:
                levels.append(level)

        return levels

    def find_dependencies_dfs(self, start):
        if start in self.cache_dfs:
            return self.cache_dfs[start]

        visited = set()

        def dfs(node):
            for nei in self.graph.graph[node]:
                if nei not in visited:
                    visited.add(nei)
                    dfs(nei)

        dfs(start)
        self.cache_dfs[start] = visited
        return visited
