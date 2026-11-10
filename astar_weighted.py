
import heapq
from itertools import count


DIRECTIONS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


def astar_weighted_with_stats(start, end, grid, heuristic="improved"):
    """
    加权地形 A*。

    返回：
        cost: 最小总代价，无解时为 -1
        path: 最优路径，无解时为 []
        expanded_nodes: 有效弹出的节点数
    """

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    if rows == 0 or any(len(row) != cols for row in grid):
        raise ValueError("地图必须是非空且行长度一致的二维网格")

    def is_valid(pos):
        r, c = pos
        return (
            0 <= r < rows
            and 0 <= c < cols
            and grid[r][c] != "X"
        )

    def entry_cost(pos):
        """进入一个格子的代价，E 为 0。"""
        r, c = pos
        cell = grid[r][c]

        if cell == "E":
            return 0
        if cell == "S":
            return 0

        return int(cell)

    if not is_valid(start) or not is_valid(end):
        return -1, [], 0

    # 找到普通地形中的最低进入代价
    terrain_costs = [
        int(cell)
        for row in grid
        for cell in row
        if cell not in ("S", "E", "X")
    ]
    min_cost = min(terrain_costs) if terrain_costs else 0

    def h(pos):
        distance = (
            abs(pos[0] - end[0])
            + abs(pos[1] - end[1])
        )

        if heuristic == "zero":
            return 0
        elif heuristic == "improved":
            return max(0, distance - 1) * min_cost
        elif heuristic == "manhattan":
            return distance * min_cost
        else:
            raise ValueError(
                "heuristic 只能是 zero、improved 或 manhattan"
            )

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

        if current in closed:
            continue

        closed.add(current)
        expanded_nodes += 1

        if current == end:
            path = [current]

            while current in parent:
                current = parent[current]
                path.append(current)

            path.reverse()
            return g_score[end], path, expanded_nodes

        r, c = current

        for dr, dc in DIRECTIONS:
            neighbor = (r + dr, c + dc)

            if not is_valid(neighbor) or neighbor in closed:
                continue

            tentative_g = (
                g_score[current] + entry_cost(neighbor)
            )

            if tentative_g < g_score.get(
                neighbor, float("inf")
            ):
                g_score[neighbor] = tentative_g
                parent[neighbor] = current

                f_score = tentative_g + h(neighbor)

                heapq.heappush(
                    open_list,
                    (f_score, next(sequence), neighbor)
                )

    return -1, [], expanded_nodes


def minimum_cost(start, end, grid):
    """题目二要求的标准接口，只返回最小总代价。"""
    cost, _, _ = astar_weighted_with_stats(
        start, end, grid, heuristic="improved"
    )
    return cost
