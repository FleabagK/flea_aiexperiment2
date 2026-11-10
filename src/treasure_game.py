
import heapq


# =========================
# 一、地图与特殊位置
# =========================

GRID = [
    ["A", "1", "1", "X", "2", "1", "T1"],
    ["1", "X", "6", "X", "1", "X", "1"],
    ["1", "1", "T2", "1", "1", "1", "1"],
    ["X", "1", "X", "8", "X", "1", "X"],
    ["1", "1", "1", "1", "T3", "1", "1"],
    ["1", "X", "9", "X", "1", "X", "1"],
    ["T4", "1", "1", "X", "1", "1", "B"],
]

POSITIONS = {
    "A": (0, 0),
    "B": (6, 6),
    "T1": (0, 6),
    "T2": (2, 2),
    "T3": (4, 4),
    "T4": (6, 0),
}

TREASURE_VALUES = {
    "T1": 9,
    "T2": 6,
    "T3": 7,
    "T4": 7,
}

NODES = ["A", "B", "T1", "T2", "T3", "T4"]


# =========================
# 二、进入格子的移动代价
# =========================

def entry_cost(cell):
    """返回进入指定格子的代价。"""

    if cell == "X":
        return None

    if cell in ["A", "B", "T1", "T2", "T3", "T4"]:
        return 1

    return int(cell)


# =========================
# 三、A* 启发函数
# =========================

def heuristic(pos, end):
    """曼哈顿距离，最低每步代价为 1。"""

    return (
        abs(pos[0] - end[0])
        + abs(pos[1] - end[1])
    )


# =========================
# 四、A* 最短路径搜索
# =========================

def astar_cost(start, end):
    """
    使用 A* 计算两个位置之间的最小移动代价。

    start、end：特殊位置名称，如 "A"、"T1"
    返回：最小移动代价；无路径时返回 -1
    """

    start_pos = POSITIONS[start]
    end_pos = POSITIONS[end]

    rows = len(GRID)
    cols = len(GRID[0])

    # 优先队列：(f, g, position)
    open_heap = [
        (heuristic(start_pos, end_pos), 0, start_pos)
    ]

    g_score = {start_pos: 0}
    closed = set()

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
    ]

    while open_heap:

        f, current_cost, current = heapq.heappop(open_heap)

        if current in closed:
            continue

        if current_cost != g_score[current]:
            continue

        if current == end_pos:
            return current_cost

        closed.add(current)

        for dr, dc in directions:

            nr = current[0] + dr
            nc = current[1] + dc

            if not (0 <= nr < rows and 0 <= nc < cols):
                continue

            next_pos = (nr, nc)
            cost = entry_cost(GRID[nr][nc])

            if cost is None:
                continue

            new_cost = current_cost + cost

            if new_cost < g_score.get(next_pos, float("inf")):

                g_score[next_pos] = new_cost

                new_f = (
                    new_cost
                    + heuristic(next_pos, end_pos)
                )

                heapq.heappush(
                    open_heap,
                    (new_f, new_cost, next_pos)
                )

    return -1


# =========================
# 五、构建两两距离矩阵
# =========================

def build_distance_matrix():
    """计算六个特殊位置之间的有向最小移动代价矩阵。"""

    matrix = {}

    for source in NODES:

        matrix[source] = {}

        for target in NODES:

            if source == target:
                matrix[source][target] = 0
            else:
                matrix[source][target] = astar_cost(
                    source,
                    target
                )

    return matrix


def print_distance_matrix(matrix):
    """以表格形式打印距离矩阵。"""

    print("===== 两两最小移动代价矩阵 =====")

    print("位置".ljust(8), end="")

    for node in NODES:
        print(node.rjust(6), end="")

    print()

    for source in NODES:

        print(source.ljust(8), end="")

        for target in NODES:

            print(
                str(matrix[source][target]).rjust(6),
                end=""
            )

        print()


# =========================
# 六、博弈树节点统计
# =========================

def subtree_node_count(remaining_count, depth):
    """计算一棵子树包含的节点总数。"""

    if depth <= 0 or remaining_count <= 0:
        return 1

    return (
        1
        + remaining_count
        * subtree_node_count(remaining_count - 1, depth - 1)
    )

# =========================
# 七、Minimax 搜索
# =========================

def minimax_game(distance_matrix, H):
    """
    使用 Minimax 计算 A 的最优首步和最终收益差。

    返回：
    best_target：A 的最优首步
    best_value：对应的最优收益差
    stats：搜索统计数据
    """

    stats = {
        "visited_nodes": 1,
        "evaluated_leaves": 0,
    }

    treasures = tuple(TREASURE_VALUES.keys())

    def search(pos_a, pos_b, remaining, score_diff, player, depth):

        stats["visited_nodes"] += 1

        # 搜索终止条件
        if depth == 0 or not remaining:
            stats["evaluated_leaves"] += 1
            return score_diff

        values = []

        for target in remaining:

            new_remaining = tuple(
                t for t in remaining if t != target
            )

            if player == "A":

                gain = (
                    TREASURE_VALUES[target]
                    - distance_matrix[pos_a][target]
                )

                value = search(
                    target,
                    pos_b,
                    new_remaining,
                    score_diff + gain,
                    "B",
                    depth - 1,
                )

            else:

                gain = (
                    TREASURE_VALUES[target]
                    - distance_matrix[pos_b][target]
                )

                value = search(
                    pos_a,
                    target,
                    new_remaining,
                    score_diff - gain,
                    "A",
                    depth - 1,
                )

            values.append(value)

        if player == "A":
            return max(values)

        return min(values)

    # 根节点：A 选择第一件宝藏
    best_target = None
    best_value = float("-inf")

    for target in treasures:

        gain = (
            TREASURE_VALUES[target]
            - distance_matrix["A"][target]
        )

        remaining = tuple(
            t for t in treasures if t != target
        )

        value = search(
            target,
            "B",
            remaining,
            gain,
            "B",
            H - 1,
        )

        if value > best_value:
            best_value = value
            best_target = target

    return best_target, best_value, stats


# =========================
# 八、Alpha-Beta 剪枝搜索
# =========================

def alpha_beta_game(distance_matrix, H, reverse_order=False):
    """
    使用 Alpha-Beta 剪枝计算 A 的最优首步和最终收益差。
    """

    stats = {
        "visited_nodes": 1,
        "evaluated_leaves": 0,
        "cutoffs": 0,
        "pruned_nodes": 0,
    }

    treasures = tuple(TREASURE_VALUES.keys())
    if reverse_order:
        treasures = tuple(reversed(treasures))
    def search(
        pos_a,
        pos_b,
        remaining,
        score_diff,
        player,
        depth,
        alpha,
        beta,
    ):

        stats["visited_nodes"] += 1

        if depth == 0 or not remaining:
            stats["evaluated_leaves"] += 1
            return score_diff

        if player == "A":

            best_value = float("-inf")

            for i, target in enumerate(remaining):

                gain = (
                    TREASURE_VALUES[target]
                    - distance_matrix[pos_a][target]
                )

                new_remaining = tuple(
                    t for t in remaining if t != target
                )

                value = search(
                    target,
                    pos_b,
                    new_remaining,
                    score_diff + gain,
                    "B",
                    depth - 1,
                    alpha,
                    beta,
                )

                best_value = max(best_value, value)
                alpha = max(alpha, best_value)

                if alpha >= beta:

                    stats["cutoffs"] += 1

                    for unvisited in remaining[i + 1:]:
                        stats["pruned_nodes"] += (
                            subtree_node_count(
                                len(remaining) - 1,
                                depth - 1,
                            )
                        )

                    break

            return best_value

        else:

            best_value = float("inf")

            for i, target in enumerate(remaining):

                gain = (
                    TREASURE_VALUES[target]
                    - distance_matrix[pos_b][target]
                )

                new_remaining = tuple(
                    t for t in remaining if t != target
                )

                value = search(
                    pos_a,
                    target,
                    new_remaining,
                    score_diff - gain,
                    "A",
                    depth - 1,
                    alpha,
                    beta,
                )

                best_value = min(best_value, value)
                beta = min(beta, best_value)

                if alpha >= beta:

                    stats["cutoffs"] += 1

                    for unvisited in remaining[i + 1:]:
                        stats["pruned_nodes"] += (
                            subtree_node_count(
                                len(remaining) - 1,
                                depth - 1,
                            )
                        )

                    break

            return best_value

    # 根节点：A 选择第一件宝藏
    best_target = None
    best_value = float("-inf")
    alpha = float("-inf")
    beta = float("inf")

    for target in treasures:

        gain = (
            TREASURE_VALUES[target]
            - distance_matrix["A"][target]
        )

        remaining = tuple(
            t for t in treasures if t != target
        )

        value = search(
            target,
            "B",
            remaining,
            gain,
            "B",
            H - 1,
            alpha,
            beta,
        )

        if value > best_value:
            best_value = value
            best_target = target

        alpha = max(alpha, best_value)

    return best_target, best_value, stats


# =========================
# 九、运行综合实验
# =========================

def run_game_experiments(distance_matrix):

    for H in [2, 4]:

        print(f"\n========== 搜索深度 H={H} ==========")

        # Minimax
        target, value, stats = minimax_game(
            distance_matrix,
            H,
        )

        print("\n--- Minimax ---")
        print("A 的最优首步：", target)
        print("最优收益差：", value)
        print("访问节点数：", stats["visited_nodes"])
        print("评估叶子数：", stats["evaluated_leaves"])

        # Alpha-Beta
        target_ab, value_ab, stats_ab = alpha_beta_game(
            distance_matrix,
            H,
        )

        print("\n--- Alpha-Beta ---")
        print("A 的最优首步：", target_ab)
        print("最优收益差：", value_ab)
        print("访问节点数：", stats_ab["visited_nodes"])
        print("评估叶子数：", stats_ab["evaluated_leaves"])
        print("剪枝次数：", stats_ab["cutoffs"])
        print("剪去节点数：", stats_ab["pruned_nodes"])

        # 检查两个算法的决策结果
        assert target == target_ab
        assert value == value_ab

        print("\nMinimax 与 Alpha-Beta 结果一致！")

if __name__ == "__main__":

    distance_matrix = build_distance_matrix()

    print_distance_matrix(distance_matrix)

    run_game_experiments(distance_matrix)