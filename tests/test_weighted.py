
from src.astar_weighted import (
    minimum_cost,
    astar_weighted_with_stats,
)


def main():
    start = (0, 0)
    end = (4, 4)

    grid = [
        ["S", 1, 1, 8, 1],
        [1, 8, 3, 1, 1],
        [1, 8, 1, 8, 1],
        [1, 1, 1, 8, 1],
        [8, 8, 1, 1, "E"],
    ]

    # 测试标准接口
    result = minimum_cost(start, end, grid)
    print("最小总代价：", result)

    # 查看最优路径和搜索节点数
    cost, path, improved_nodes = astar_weighted_with_stats(
        start, end, grid, heuristic="improved"
    )

    print("最优路径：", path)
    print("路径代价：", cost)
    print("改进启发函数搜索节点数：", improved_nodes)

    # 对照实验：h(n) = 0
    _, _, zero_nodes = astar_weighted_with_stats(
        start, end, grid, heuristic="zero"
    )

    print("\n搜索节点数对比：")
    print("改进启发函数：", improved_nodes)
    print("h(n) = 0：", zero_nodes)

    # 无解测试
    blocked_grid = [
        ["S", "X", 1],
        ["X", "X", "X"],
        [1, 1, "E"],
    ]

    no_path = minimum_cost(
        (0, 0), (2, 2), blocked_grid
    )

    print("\n无解测试：", no_path)

    assert result == 7
    assert cost == 7
    assert path[0] == start
    assert path[-1] == end
    assert no_path == -1

    print("\n所有测试通过！")


if __name__ == "__main__":
    main()
