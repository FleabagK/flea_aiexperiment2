
from src.treasure_game import (
    build_distance_matrix,
    alpha_beta_game
)


def run_order_experiment():
    matrix = build_distance_matrix()

    for H in [2, 4]:
        print(f"\n========== H={H} ==========")

        # 默认顺序：T1 -> T2 -> T3 -> T4
        target_normal, value_normal, stats_normal = (
            alpha_beta_game(matrix, H, reverse_order=False)
        )

        # 反向顺序：T4 -> T3 -> T2 -> T1
        target_reverse, value_reverse, stats_reverse = (
            alpha_beta_game(matrix, H, reverse_order=True)
        )

        print("\n默认顺序：T1 -> T2 -> T3 -> T4")
        print("最优首步：", target_normal)
        print("收益差：", value_normal)
        print("访问节点：", stats_normal["visited_nodes"])
        print("评估叶子：", stats_normal["evaluated_leaves"])
        print("剪枝次数：", stats_normal["cutoffs"])
        print("剪去节点：", stats_normal["pruned_nodes"])

        print("\n反向顺序：T4 -> T3 -> T2 -> T1")
        print("最优首步：", target_reverse)
        print("收益差：", value_reverse)
        print("访问节点：", stats_reverse["visited_nodes"])
        print("评估叶子：", stats_reverse["evaluated_leaves"])
        print("剪枝次数：", stats_reverse["cutoffs"])
        print("剪去节点：", stats_reverse["pruned_nodes"])

        assert value_normal == value_reverse
        assert target_normal == target_reverse

        print("\n两种访问顺序的决策结果一致！")


if __name__ == "__main__":
    run_order_experiment()
