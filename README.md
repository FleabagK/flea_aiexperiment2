# flea_aiexperiment2
26fallAI — Experiment 2: SearchAlgorithms
# 实验二：搜索算法（Search Algorithms）

## 1. 项目简介

本项目为《当代人工智能》课程实验二，主要实现并比较经典搜索与博弈树搜索算法，包含以下四个部分：

1. **迷宫寻路**：使用 A* 算法寻找起点到终点的最短路径，并比较曼哈顿距离启发函数与零启发函数的搜索效率。
2. **加权地形寻路**：在不同地形具有不同进入代价的地图中，使用改进的 A* 启发函数寻找总代价最小的路径。
3. **Minimax 与 Alpha-Beta 剪枝**：在给定博弈树上实现 Minimax 和 Alpha-Beta 算法，比较不同节点访问顺序下的搜索开销。
4. **综合宝藏分配博弈**：结合 A* 路径代价、Minimax 和 Alpha-Beta 剪枝，模拟双方轮流选择宝藏的博弈过程，并比较不同搜索深度与访问顺序的影响。

## 2. 项目结构

```text
SearchAlgorithms/
├── src/
│   ├── __init__.py
│   ├── astar_maze.py          # 题目一：迷宫 A* 搜索
│   ├── astar_weighted.py      # 题目二：加权地形 A* 搜索
│   ├── minimax.py             # 题目三：Minimax 与 Alpha-Beta
│   └── treasure_game.py       # 题目四：综合宝藏分配博弈
│
├── tests/
│   ├── __init__.py
│   ├── test_maze.py           # 题目一测试
│   ├── test_weighted.py       # 题目二测试
│   ├── test_minimax.py        # 题目三测试
│   └── test_treasure.py       # 题目四测试
│
├── experiments/
│   └── treasure_order_experiment.py  # 综合题节点访问顺序对照实验
│
├── results/
│   ├── data/                  # 实验数据
│   └── figures/               # 实验图表
│
├── report/                    # 实验报告
│
├── README.md
└── requirements.txt
```

## 3. 环境要求

- Python 3.14.6
- 无需安装第三方 Python 库，算法实现与测试均使用 Python 标准库。

## 4. 运行方式

请在项目根目录下打开终端，执行以下命令。

### 4.1 运行各题测试

```bash
python -m tests.test_maze
python -m tests.test_weighted
python -m tests.test_minimax
python -m tests.test_treasure
```

### 4.2 运行综合题访问顺序对照实验

```bash
python -m experiments.treasure_order_experiment
```

## 5. 核心算法

| 题目 | 算法 | 主要功能 |
|---|---|---|
| 题目一 | A* Search | 无权迷宫最短路径搜索 |
| 题目二 | Weighted A* Search | 加权地形最小代价路径搜索 |
| 题目三 | Minimax、Alpha-Beta Pruning | 博弈树最优决策与剪枝 |
| 题目四 | A*、Minimax、Alpha-Beta Pruning | 综合路径代价与双人宝藏分配博弈 |

## 6. 测试说明

项目通过四组测试文件验证算法的基本功能、边界情况及实验结果，包括：

- 迷宫最短路径与无解情况；
- 加权地图最小总代价与无解情况；
- Minimax 和 Alpha-Beta 的决策结果及节点访问统计；
- 综合博弈在不同搜索深度下的最优首步、收益差和剪枝效果。

具体实验数据、算法分析及对照实验结果见 `report/` 目录中的实验报告。
