
from src.astar_maze import (
    find_shortest_path,
    astar_maze_with_stats,
)


def main():
    start = (0, 0)
    end = (3, 4)

    grid = [
        ["S", ".", ".", "X", "."],
        [".", "X", ".", ".", "."],
        [".", "X", ".", "X", "."],
        [".", ".", ".", "X", "E"],
        ["X", "X", ".", ".", "."],
    ]

    # 测试标准接口
    path = find_shortest_path(start, end, grid)

    print("曼哈顿距离启发函数：")
    print("最短路径：", path)
    print("路径长度：", len(path) - 1 if path else -1)

    # 对照实验：两种启发函数
    _, manhattan_nodes = astar_maze_with_stats(
        start, end, grid, heuristic="manhattan"
    )

    _, zero_nodes = astar_maze_with_stats(
        start, end, grid, heuristic="zero"
    )

    print("\n搜索节点数对比：")
    print("曼哈顿距离：", manhattan_nodes)
    print("h(n) = 0：", zero_nodes)

    # 测试无解情况
    blocked_grid = [
        ["S", "X", "E"],
        ["X", "X", "X"],
    ]

    no_path = find_shortest_path(
        (0, 0), (0, 2), blocked_grid
    )

    print("\n无解测试：", no_path)

    assert path[0] == start
    assert path[-1] == end
    assert len(path) - 1 == 7
    assert no_path == []

    print("\n所有测试通过！")


if __name__ == "__main__":
    main()
