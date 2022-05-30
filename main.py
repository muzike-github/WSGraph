# 产生递归分支，返回可行社区和最小权重边
import networkx as nx
import core.function as fc


# 递归函数
def Recursion(C, R, H, h, score):
    fun = fc.Fun(G)
    # 如果C满足个数且最小权重更大
    if len(C) == h and fun.cohesiveScore(C) > score:
        # 更新H和最小权重
        H.clear()
        H = C[:]
        score = fun.cohesiveScore(C)
        print("更新社区:", H, "凝聚分数为", score)
    # 如果C的节点数小于h并且候选集R不为空
    if len(C) < h and len(R) != 0:
        for v in R:
            CAndV = list(set(C).union({v}))
            RExcludeV = list(set(R).difference({v}))
            H, score = Recursion(CAndV, RExcludeV, H, h, score)
            H, score = Recursion(C, RExcludeV, H, h, score)
    return H, score


# 主算法
def WBS(G, q, h):
    fun = fc.Fun(G)
    H = fun.WSHeuristic(q, h)  # 调用WSHeuristic算法计算一个可行社区H
    HGraph = nx.subgraph(G, H)
    scoreLower = fun.cohesiveScore(H)  # 计算初始社区的内聚分数,是为最优社区的下界
    scoreUpper = 2  # 上界为最理想情况,社区每个点达到最大值，最小权值也达到最大值
    print("scoreLower:", scoreLower, "scoreUpper:", scoreUpper)
    # 开始递归
    R = list(G.nodes)
    R.remove(q)
    # 将初始可行社区H作为递归参数，
    if scoreLower < scoreUpper:
        H, score = Recursion([q], R, H, h, scoreLower)  # 初始最优社区就是SCheu算出的可行社区H
    return H


# if __name__ == '__main__':
#     # 测试用例
#     GTest = [(0, 1, 10), (0, 2, 10), (0, 3, 5), (0, 4, 6), (0, 5, 5),
#              (1, 4, 7), (2, 3, 6), (2, 5, 6), (2, 7, 9), (3, 4, 8),
#              (4, 5, 7), (4, 6, 6), (4, 9, 9),
#              (5, 6, 7), (5, 7, 7), (5, 8, 6), (6, 7, 8), (6, 8, 6), (7, 8, 10), (8, 9, 4)]
#     G = nx.Graph()
#     G.add_weighted_edges_from(GTest)
#     fc.paint(GTest, [])
#     result = WBS(G, 0, 5)
#     print("最优社区为：", result)
#     fc.paint(GTest, result)
#     print()
if __name__ == '__main__':
    # 测试用例
    GTest = [(0, 1, 2), (0, 2, 10), (0, 3, 5), (0, 4, 6), (0, 5, 5),
             (1, 4, 7), (2, 3, 6), (2, 5, 6), (2, 7, 9), (3, 4, 8),
             (4, 5, 7), (4, 6, 6), (4, 9, 9),
             (5, 6, 7), (5, 7, 7), (5, 8, 6), (6, 7, 8), (6, 8, 6), (7, 8, 10), (8, 9, 4)]
    G = nx.Graph()
    G.add_weighted_edges_from(GTest)
    fun = fc.Fun(G)
    print("最小度", fc.minDegree(G))
    print("最大度", fc.maxDegree(G))
    print("最小权重", fun.minWeight(G))
    print("最大权重", fun.maxWeight(G))
    print("凝聚分数", fun.cohesiveScore(G.nodes()))
    print("权重连接分数",sorted(fun.ConnectScoreWeight([3,4,5,6]).items(),key=lambda x:x[1]))
    H=fun.WSHeuristic(0,5)
    fc.paint(GTest,H)
