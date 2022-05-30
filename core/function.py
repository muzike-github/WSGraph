import networkx as nx
import matplotlib.pyplot as plt


# 求图G的最小度
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


# 用于画图的函数
def paint(GList, H):
    # 添加加权边
    G = nx.Graph()
    G.add_weighted_edges_from(GList)
    if len(H) != 0:
        G = G.subgraph(H)
    # 生成节点位置序列（）
    pos = nx.circular_layout(G)
    # 重新获取权重序列
    weights = nx.get_edge_attributes(G, "weight")
    # 画节点图
    nx.draw_networkx(G, pos, with_labels=True)
    # 画权重图
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weights)
    plt.show()





class Fun:
    def __init__(self, G):
        self.G = G

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

    # 带权重的连接分数(计算候选集R中各个节点的分数)
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

    # 求出社区的凝聚力分数
    # score=w+d
    def cohesiveScore(self, H):
        degreeScore = minDegree(nx.subgraph(self.G, H)) / maxDegree(nx.subgraph(self.G, H))
        weightScore = self.minWeight(nx.subgraph(self.G, H)) / self.maxWeight(nx.subgraph(self.G, H))
        score = degreeScore + weightScore
        score = round(score, 2)  # 保留两位小数
        return score

    # 利用权重分数计算初始社区（Q：查询节点集合，h:目标社区的节点数量）
    def WSHeuristic(self, q, h):
        print("===========权重分数启发式算法开始=============")
        # print("查询节点", q, "的度为：", self.G.degree(q))
        H = [q] # 初始为查询节点
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
        print("初始可行解的顶点数为：", len(H))
        print("初始可行解的最小度为：", minDegree(nx.subgraph(self.G, H)))
        print("初始可行解的最小权重为：", self.minWeight(nx.subgraph(self.G, H)))
        print("初始可行解的凝聚分数为", self.cohesiveScore(H))
        print("启发式算法结束")
        return H


