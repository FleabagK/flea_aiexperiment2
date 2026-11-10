
from src.treasure_game import (
    build_distance_matrix,
    minimax_game,
    alpha_beta_game,
)


def main():

    # 一、测试距离矩阵
    matrix = build_distance_matrix()

    assert matrix["A"]["B"] == 12
    assert matrix["A"]["T2"] == 4
    assert matrix["T3"]["B"] == 4
    assert matrix["T4"]["T1"] == 12

    print("===== 距离矩阵测试 =====")
    print("距离矩阵计算正确！")

    # 二、测试 H=2
    target, value, stats = minimax_game(matrix, 2)

    assert target == "T2"
    assert value == -1

    target_ab, value_ab, stats_ab = alpha_beta_game(matrix, 2)

    assert target_ab == "T2"
    assert value_ab == -1

    print("\n===== H=2 测试 =====")
    print("Minimax：", target, value)
    print("Alpha-Beta：", target_ab, value_ab)
    print("Minimax 访问节点：", stats["visited_nodes"])
    print("Alpha-Beta 访问节点：", stats_ab["visited_nodes"])

    # 三、测试 H=4
    target, value, stats = minimax_game(matrix, 4)

    assert target == "T3"
    assert value == 3

    target_ab, value_ab, stats_ab = alpha_beta_game(matrix, 4)

    assert target_ab == "T3"
    assert value_ab == 3

    print("\n===== H=4 测试 =====")
    print("Minimax：", target, value)
    print("Alpha-Beta：", target_ab, value_ab)
    print("Minimax 访问节点：", stats["visited_nodes"])
    print("Alpha-Beta 访问节点：", stats_ab["visited_nodes"])
    print("Alpha-Beta 剪枝次数：", stats_ab["cutoffs"])

    print("\n题目四所有测试通过！")


if __name__ == "__main__":
    main()
