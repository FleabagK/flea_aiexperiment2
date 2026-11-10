
from src.minimax import (
    TreeNode,
    minimax,
    alpha_beta,
)


def build_tree():
    """构建老师给出的测试博弈树。"""

    # 第一组 MAX 节点
    max1 = TreeNode(
        children=[
            TreeNode(value=3),
            TreeNode(value=5),
        ],
        is_maximizing_player=True,
    )

    max2 = TreeNode(
        children=[
            TreeNode(value=6),
            TreeNode(value=9),
        ],
        is_maximizing_player=True,
    )

    max3 = TreeNode(
        children=[
            TreeNode(value=1),
            TreeNode(value=2),
        ],
        is_maximizing_player=True,
    )

    # 两个 MIN 节点
    min1 = TreeNode(
        children=[max1, max2],
        is_maximizing_player=False,
    )

    min2 = TreeNode(
        children=[
            TreeNode(
                children=[
                    TreeNode(value=6),
                    TreeNode(value=9),
                ],
                is_maximizing_player=True,
            ),
            max3,
        ],
        is_maximizing_player=False,
    )

    # 根节点 MAX
    root = TreeNode(
        children=[min1, min2],
        is_maximizing_player=True,
    )

    return root


def main():
    # 一、Minimax 完整搜索
    root = build_tree()

    minimax_value, minimax_stats = minimax(root)

    print("===== Minimax =====")
    print("最优得分：", minimax_value)
    print("访问节点数：", minimax_stats["visited_nodes"])
    print("评估叶子数：", minimax_stats["evaluated_leaves"])

    # 二、Alpha-Beta，按照从左到右搜索
    root = build_tree()

    ab_value, ab_stats = alpha_beta(root)

    print("\n===== Alpha-Beta（从左到右）=====")
    print("最优得分：", ab_value)
    print("访问节点数：", ab_stats["visited_nodes"])
    print("评估叶子数：", ab_stats["evaluated_leaves"])
    print("剪枝次数：", ab_stats["cutoffs"])
    print("剪去节点数：", ab_stats["pruned_nodes"])

    # 三、Alpha-Beta，反向访问子节点
    root = build_tree()

    reverse_value, reverse_stats = alpha_beta(
        root,
        reverse_children=True,
    )

    print("\n===== Alpha-Beta（从右到左）=====")
    print("最优得分：", reverse_value)
    print("访问节点数：", reverse_stats["visited_nodes"])
    print("评估叶子数：", reverse_stats["evaluated_leaves"])
    print("剪枝次数：", reverse_stats["cutoffs"])
    print("剪去节点数：", reverse_stats["pruned_nodes"])

    # 四、验证结果
    assert minimax_value == 5
    assert ab_value == 5
    assert reverse_value == 5

    assert minimax_stats["visited_nodes"] == 15
    assert minimax_stats["evaluated_leaves"] == 8

    print("\n所有测试通过！")


if __name__ == "__main__":
    main()
