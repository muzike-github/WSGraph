# 产生递归分支，返回可行社区和最小权重边
import networkx as nx
import core.function as fc
import core.fileHandle as fh
import time


# 递归函数
def Recursion(C, R, H, h, score):
    # fun = fc.Fun(G)
    # fun.reduce0(C,R)
    #fun.reduce1(C, R, h)
    fun.reduce2(C, R, h, score)
    # print("缩减后R：",R)
    # 如果C满足个数且最小权重更大
    if len(C) == h and fun.cohesiveScore(C) > score:
        # 更新H和最小权重
        H.clear()
        H = C[:]
        score = fun.cohesiveScore(C)
        print("更新社区:", "凝聚分数为", score)
    # 如果C的节点数小于h并且候选集R不为空
    Upperbound = fun.scoreUpperbound(C, R, h)
    # print("C的分数上界：",Upperbound,"score:",score)
    if len(C) < h and len(R) != 0 and Upperbound > score:
        # 从候选集R中选一个节点生成两个分支
        v = R[0]
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
    # GTest = [(0, 1, 2), (0, 2, 10), (0, 3, 5), (0, 4, 6), (0, 5, 5),
    #          (1, 4, 7), (2, 3, 6), (2, 5, 6), (2, 7, 9), (3, 4, 8),
    #          (4, 5, 7), (4, 6, 6), (4, 9, 9),
    #          (5, 6, 7), (5, 7, 7), (5, 8, 6), (6, 7, 8), (6, 8, 6), (7, 8, 10), (8, 9, 4)]

    startTime = time.time()
    count = 0
    GTest = fh.csvResolve("dataset/bitcoinData.csv")
    G = nx.Graph()
    G.add_weighted_edges_from(GTest)
    fun = fc.Fun(G)
    # 开始测试
    # 设置要求的社区规模
    size = 6
    # fc.paint(GTest,[])
    print("母图的最大度数", fun.degreeMax)
    print("母图的最大权重", fun.weightMax)
    print("数据的节点数量",len(G.nodes))
    print("数据的边数量",len(G.edges))
    H = fun.WSHeuristic(1, size)
    scoreH = fun.cohesiveScore(H)
    print("启发式算法社区", H, "凝聚分数", scoreH)
    # fc.paint(GTest, H,"WS启发式算法")
    result = WBS(G, 1, size)
    scoreResult = fun.cohesiveScore(result)
    print("最终结果", result, "凝聚分数", scoreResult)
    print("最终社区的最小度为：", fc.minDegree(nx.subgraph(G, result)))
    print("最终社区的最小权重为：", fun.minWeight(nx.subgraph(G, result)))
    # fc.paint(GTest, result,"WS最终社区")
    endTime = time.time()
    print("搜索完成共耗时：", endTime - startTime)
