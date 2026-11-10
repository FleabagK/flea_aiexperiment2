
class TreeNode:
    """博弈树节点。"""

    def __init__(
        self,
        value=None,
        children=None,
        is_maximizing_player=None
    ):
        self.value = value
        self.children = children if children is not None else []
        self.is_maximizing_player = is_maximizing_player


def count_subtree_nodes(node):
    """统计一棵子树包含的全部节点数。"""
    return 1 + sum(
        count_subtree_nodes(child)
        for child in node.children
    )


def minimax(node, reverse_children=False):
    """
    标准 Minimax 算法。

    返回：
        best_value: 最优得分
        stats: 搜索统计信息
    """

    stats = {
        "visited_nodes": 0,
        "evaluated_leaves": 0,
    }

    def search(current):
        stats["visited_nodes"] += 1

        # 叶子节点直接返回评价值
        if not current.children:
            stats["evaluated_leaves"] += 1
            return current.value

        children = current.children

        if reverse_children:
            children = list(reversed(children))

        if current.is_maximizing_player:
            best_value = float("-inf")

            for child in children:
                best_value = max(
                    best_value,
                    search(child)
                )

            return best_value

        else:
            best_value = float("inf")

            for child in children:
                best_value = min(
                    best_value,
                    search(child)
                )

            return best_value

    best_value = search(node)
    return best_value, stats


def alpha_beta(
    node,
    reverse_children=False
):
    """
    Alpha-Beta 剪枝算法。

    返回：
        best_value: 最优得分
        stats: 搜索统计信息
    """

    stats = {
        "visited_nodes": 0,
        "evaluated_leaves": 0,
        "pruned_nodes": 0,
        "cutoffs": 0,
    }

    def search(current, alpha, beta):
        stats["visited_nodes"] += 1

        # 到达叶子节点
        if not current.children:
            stats["evaluated_leaves"] += 1
            return current.value

        children = current.children

        if reverse_children:
            children = list(reversed(children))

        if current.is_maximizing_player:
            best_value = float("-inf")

            for i, child in enumerate(children):
                value = search(child, alpha, beta)

                best_value = max(best_value, value)
                alpha = max(alpha, best_value)

                # Alpha-Beta 剪枝条件
                if alpha >= beta:
                    stats["cutoffs"] += 1

                    # 统计尚未访问的整棵子树
                    for remaining in children[i + 1:]:
                        stats["pruned_nodes"] += (
                            count_subtree_nodes(remaining)
                        )

                    break

            return best_value

        else:
            best_value = float("inf")

            for i, child in enumerate(children):
                value = search(child, alpha, beta)

                best_value = min(best_value, value)
                beta = min(beta, best_value)

                # Alpha-Beta 剪枝条件
                if alpha >= beta:
                    stats["cutoffs"] += 1

                    for remaining in children[i + 1:]:
                        stats["pruned_nodes"] += (
                            count_subtree_nodes(remaining)
                        )

                    break

            return best_value

    best_value = search(
        node,
        float("-inf"),
        float("inf")
    )

    return best_value, stats
