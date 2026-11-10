
import heapq
from itertools import count


# 四个可移动方向：上、下、左、右
DIRECTIONS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


def manhattan_distance(a, b):
    """计算两个网格坐标之间的曼哈顿距离。"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar_maze_with_stats(start, end, grid, heuristic="manhattan"):
    """
    使用 A* 算法寻找迷宫最短路径。

    参数：
        start: 起点坐标 (row, col)
        end: 终点坐标 (row, col)
        grid: 二维迷宫，X 表示障碍物
        heuristic: "manhattan" 或 "zero"

    返回：
        path: 最短路径坐标列表，无解时返回 []
        expanded_nodes: 搜索过程中有效弹出的节点数
    """

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    if rows == 0 or any(len(row) != cols for row in grid):
        raise ValueError("迷宫必须是非空且行长度一致的二维网格")

    def is_valid(pos):
        r, c = pos
        return (
            0 <= r < rows
            and 0 <= c < cols
            and grid[r][c] != "X"
        )

    if not is_valid(start) or not is_valid(end):
        return [], 0

    if heuristic == "manhattan":
        h = lambda pos: manhattan_distance(pos, end)
    elif heuristic == "zero":
        h = lambda pos: 0
    else:
        raise ValueError("heuristic 只能是 'manhattan' 或 'zero'")

    # 优先队列元素：(f, 序号, 坐标)
    # 序号用于避免坐标在优先级相同时参与比较
    sequence = count()
    open_list = [
        (h(start), next(sequence), start)
    ]

    g_score = {start: 0}
    parent = {}
    closed = set()
    expanded_nodes = 0

    while open_list:
        _, _, current = heapq.heappop(open_list)

        # 跳过已经处理过的节点
        if current in closed:
            continue

        closed.add(current)
        expanded_nodes += 1

        # 到达终点，回溯路径
        if current == end:
            path = [current]

            while current in parent:
                current = parent[current]
                path.append(current)

            path.reverse()
            return path, expanded_nodes

        r, c = current

        for dr, dc in DIRECTIONS:
            neighbor = (r + dr, c + dc)

            if not is_valid(neighbor) or neighbor in closed:
                continue

            tentative_g = g_score[current] + 1

            if tentative_g < g_score.get(neighbor, float("inf")):
                g_score[neighbor] = tentative_g
                parent[neighbor] = current

                f_score = tentative_g + h(neighbor)

                heapq.heappush(
                    open_list,
                    (f_score, next(sequence), neighbor)
                )

    # 搜索结束仍未到达终点
    return [], expanded_nodes


def find_shortest_path(start, end, grid):
    """
    题目一要求的标准接口：
    只返回最短路径，不返回统计信息。
    """
    path, _ = astar_maze_with_stats(
        start, end, grid, heuristic="manhattan"
    )
    return path
