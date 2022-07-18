import networkx as nx
import matplotlib.pyplot as plt


# 求图G的最小度(G为图)
def minDegree(G):
    degrees = []
    for i in G:
        degrees.append(G.degree(i))
    return min(degrees)


# 求图G的最大度数
def maxDegree(G):
    degrees = []
    for i in G:
        degrees.append(G.degree(i))
    return max(degrees)


# 缩减规则2中的n公式
def rule2Lemma(K, D):
    if 1 <= D <= 2 or K == 1:
        n = K + D
    else:
        n = K + D + 1 + ((int)(D / 3)) * (K - 2)
    return n


# 用于画图的函数
def paint(GList, H, str):
    # 添加加权边
    G = nx.Graph()
    G.add_weighted_edges_from(GList)
    if len(H) != 0:
        G = G.subgraph(H)
    # 生成节点位置序列（）
    pos = nx.spring_layout(G)
    # 重新获取权重序列
    weights = nx.get_edge_attributes(G, "weight")
    # 画节点图
    nx.draw_networkx(G, pos, with_labels=True)
    # 画权重图
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weights)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title(str)
    plt.show()


class Fun:
    def __init__(self, G):
        self.G = G
        self.weightMax = self.maxWeight(G)
        self.degreeMax = maxDegree(G)

    # 求图G的最小权重（）
    def minWeight(self, G):
        weights = []
        for i in G:
            weight = 0
            for j in nx.neighbors(G, i):  # 遍历节点的所有邻居
                weight += self.G.get_edge_data(i, j)['weight']
            weights.append(weight)
        return min(weights)

    # 求图G的最大权重（）
    def maxWeight(self, G):
        weights = []
        for i in G:
            weight = 0
            for j in nx.neighbors(G, i):  # 遍历节点的所有邻居
                weight += self.G.get_edge_data(i, j)['weight']
            weights.append(weight)
        return max(weights)

    # 根据度数和权重将其归1并转化为分数
    def getScore(self, degree, weight):
        degreeScore = degree / self.degreeMax
        weightScore = weight / self.weightMax
        return degreeScore + weightScore

    # 求出给定社区的凝聚力分数
    def cohesiveScore(self, H):
        graph = nx.subgraph(self.G, H)
        degree = minDegree(graph)
        weight = self.minWeight(graph)
        score = self.getScore(degree, weight)
        score = round(score, 4)  # 保留两位小数
        return score

    # 带权重的连接分数,用于启发式算法计算初始可行社区
    def ConnectScoreWeight(self, C):
        copyC = C.copy()  # 用copyC 代替C的所有操作,否则求完连接分数后C会改变
        scoreDict = {}  # 字典保存R中每个节点的连接分数
        R = []  # todo: 候选集，此处可以优化
        for v in C:  # 候选集应该是C中所有节点的所有邻居
            for i in nx.neighbors(self.G, v):
                if i not in C:
                    R.append(i)
        for v in R:
            graphC = nx.subgraph(self.G, copyC)  # 得到图C
            copyC.append(v)
            graphCAndV = nx.subgraph(self.G, copyC)  # 得到节点集C∪{v}的在G中的子图
            score = 0
            # 此处判断v是否在C∪{v}中是否有邻居，没有邻居，分数为0
            if len(list(nx.neighbors(graphCAndV, v))) != 0:
                # 有邻居但邻居在C中度为0，则设置score为0
                for i in nx.neighbors(graphCAndV, v):  # 得到v(v∈R)在C∪{v}所有的邻居节点
                    tempWeight = self.G.get_edge_data(v, i)['weight']
                    if graphC.degree(i) != 0:
                        score += (1 / graphC.degree(i)) * int(tempWeight)
                        score = round(score, 2)
                    else:
                        score = 0
            # 如果v没有邻居，则直接分数为0
            else:
                score = 0
            scoreDict[v] = score  # 将对应节点的连接分数存储
            copyC.remove(v)  # 节点v测试完毕，移除
        scoreMaxNode = max(scoreDict, key=scoreDict.get)
        return scoreDict

    # 利用权重分数计算初始社区（Q：查询节点集合，h:目标社区的节点数量）
    def WSHeuristic(self, q, h):
        print("===========权重分数启发式算法开始=============")
        # print("查询节点", q, "的度为：", self.G.degree(q))
        H = [q]  # 初始为查询节点
        if len(H) == 1:  # 如果只有一个节点，选取相邻权重最大的点
            weight = 0
            for i in nx.neighbors(self.G, H[0]):
                tempWeight = int(self.G.get_edge_data(i, H[0])['weight'])
                if tempWeight > weight:
                    weight = tempWeight
                    node = i
            H.append(node)
        print("第二个节点是", H)
        while len(H) < h:
            # 找出G\H中连接分数最大的节点V*
            soreDict = self.ConnectScoreWeight(H)
            scoreMaxNode = max(soreDict, key=soreDict.get)
            H.append(scoreMaxNode)  # S=S∪{V*}
        if len(H) == 0:
            H = [q]
        print("权重分数启发式算法得到的可行社区为:", H)
        print("初始可行解的最小度为：", minDegree(nx.subgraph(self.G, H)))
        print("初始可行解的最小权重为：", self.minWeight(nx.subgraph(self.G, H)))
        print("初始可行解的凝聚分数为", self.cohesiveScore(H))
        print("启发式算法结束")
        return H

    # 先把与C中每个节点都不相连的顶点从R中删除
    def reduce0(self, C, R):
        for v in C:
            for u in R:
                if not self.G.has_edge(u, v):
                    R.remove(u)

    # 缩减规则1(基于社区大小h的缩减)
    # todo 感觉可以优化
    def reduce1(self, C, R, h):
        # print("调用缩减规则1")
        RCopy = R.copy()
        CAndR = list(set(C).union(set(R)))
        CAndRGraph = nx.subgraph(self.G, CAndR)
        for v in RCopy:
            for u in C:
                # 这里需要判断删减后的图是否还连通
                # 如果不连通直接删除v
                if not nx.has_path(CAndRGraph, u, v):
                    R.remove(v)
                    break
                else:
                    if len(nx.shortest_path(self.G, u, v)) >= h - 1:
                        R.remove(v)
                        # print("根据reduce1移除节点", v)
                        break
        # print("调用缩减规则2结束")

    def reduceBydiameter(self, C, R, h, k1):
        # print("调用缩减规则2")
        CAndR = list(set(C).union(set(R)))
        CAndRGraph = nx.subgraph(self.G, CAndR)
        # D = nx.diameter(CAndRGraph)  # C∪R子图的直径
        for v in R:
            for u in C:
                # 这里需要判断删减后的图是否还连通
                # 如果不连通直接删除v
                if not nx.has_path(CAndRGraph, u, v):
                    R.remove(v)
                    break
                else:
                    # 根据两点之间的最短线路来求两点之间的距离
                    dist = len(nx.shortest_path(CAndRGraph, u, v)) - 1
                    # print(u,":",v,"之间的距离为",dist)
                    if rule2Lemma(k1 + 1, dist) > h:
                        R.remove(v)
                        # print("根据reduce2移除节点", v)
                        break
        # print("调用缩减规则2结束")
        return R

    # 缩减规则2(计算节点的上限值)
    def reduce2(self, C, R, h, minScore):
        RCopy = R.copy()  # 利用copy数组循环，去改变R
        for i in RCopy:
            CAndRGraph = nx.subgraph(self.G, list(set(C).union(set(R))))  # 图C∪R
            CAndIGraph = nx.subgraph(self.G, list(set(C).union({i})))  # 图C∪{i}
            degreeInC = nx.degree(CAndIGraph, i)  # 节点i在C∪{i}中的度数
            # h - len(C) - 1表示该节点最多可能再和h - len(C) - 1个节点相连
            maxNodeCount = h - len(C) - 1
            # 节点i的
            IDegreeUpper = min(nx.degree(CAndRGraph, i), nx.degree(CAndIGraph, i) + maxNodeCount)
            weight = 0
            weightsI = []
            for j in nx.neighbors(self.G, i):  # 遍历i的所有边，按照权重顺序排列
                # 与C中节点连接的边一定是要加上
                if j in C:
                    weight += self.G.get_edge_data(i, j)['weight']
                # 否则将边存储
                else:
                    weightsI.append(self.G.get_edge_data(i, j)['weight'])
            # 如果节点i的边数大于maxNodeCount，则再选择较大的几条边作为理想情况计算权重
            if maxNodeCount < len(weightsI):
                sorted(weightsI, reverse=True)
                for t in range(0, maxNodeCount):
                    weight += weightsI[t]
            # 　根据节点可能连接的最多节点和最大权重边计算节点的最大理想分数
            score = self.getScore(IDegreeUpper, weight)
            # print(i, "最大分数", degreeScore + weightScore)
            if score < minScore:
                # print("移除", i)
                R.remove(i)
        return R

    # 基于上界修剪
    # 基于部分解C的分数上界
    def scoreUpperbound(self, C, R, h):
        degreeList = []
        weightList = []
        CAndR = list(set(C).union(set(R)))
        CAndRGraph = nx.subgraph(self.G, CAndR)
        CGraph = nx.subgraph(self.G, C)
        lengthC = len(CGraph.nodes)
        for u in C:
            # 计算u的可能最大度数
            degreeList.append(min(CAndRGraph.degree(u), CGraph.degree(u) + h - lengthC))
            # 计算u在C∪R中的可能最大权重
            weightInCAndR = 0
            weightInC = 0
            for i in nx.neighbors(CAndRGraph, u):
                weightInCAndR += self.G.get_edge_data(i, u)['weight']
            for j in nx.neighbors(CGraph, u):
                weightInC += self.G.get_edge_data(j, u)['weight']
            weightList.append(min(weightInCAndR, weightInC + (h - lengthC) * self.weightMax))
            # todo 这里乘以的数值是不是可以换成当前已经修剪的图中的最大权重值
        upperDegree = min(degreeList)
        upperWeight = min(weightList)
        return self.getScore(upperDegree, upperWeight)
