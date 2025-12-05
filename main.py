from graph import DependencyGraph, visualize_graph
from dependency_analyzer import DependencyAnalyzer

GRAPH_FILE_NAME = 'result_graph'


def read_dependencies(file_path):
    """
    Читает файл зависимостей в формате:
    A -> B, C
    B -> D
    C -> D, E
    D ->
    E -> B
    и возвращает объект DependencyGraph
    """
    graph_obj = DependencyGraph()

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # пропускаем пустые строки и комментарии

            # Разделяем по "->"
            if "->" in line:
                comp, deps = line.split("->")
                comp = comp.strip()
                deps = [d.strip() for d in deps.split(",") if d.strip()]
            else:
                comp = line.strip()
                deps = []

            graph_obj.add_component(comp)
            for dep in deps:
                graph_obj.add_dependency(comp, dep)

    return graph_obj


def pipeline(graph_obj, analyzer_obj):

    print("\n=== ТОПОЛОГИЧЕСКАЯ СОРТИРОВКА ===")
    topo = graph_obj.get_topological_order()
    if topo:
        print("Топологический порядок:", topo)
    else:
        print('[ERROR] - !!! Обнаружен цикл !!!')
        return

    print("\n=== BFS ===")
    bfs = analyzer_obj.find_dependencies_bfs("A")
    print("BFS для A:", bfs)

    print("\n=== DFS ===")
    dfs = analyzer_obj.find_dependencies_dfs("A")
    print("DFS для A:", dfs)

    print("\n=== КРИТИЧЕСКИЙ ПУТЬ ===")
    cp, length = graph_obj.get_critical_path()
    print("Критический путь:", cp)
    print("Длина пути:", length)

    print("\n=== ВИЗУАЛИЗАЦИЯ ГРАФА ===")
    visualize_graph(graph, file_name=GRAPH_FILE_NAME)
    print("Граф сохранён как dependencies_graph.png")

    print("\n", "*"*30, "Выполнение завершено", "*"*30)


if __name__ == "__main__":

    print("\n", "=>"*15, "ПРИМЕР БЕЗ ЦИКЛА", "<="*15)
    graph = read_dependencies("dependencies.txt")
    analyzer = DependencyAnalyzer(graph)
    pipeline(graph, analyzer)

    print("\n"*3, "=>"*15, "ПРИМЕР С ЦИКЛОМ", "<="*15)
    cyclic_graph = read_dependencies("dependencies_cyclic.txt")
    analyzer = DependencyAnalyzer(cyclic_graph)
    pipeline(graph, analyzer)
