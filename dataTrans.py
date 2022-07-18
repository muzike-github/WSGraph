"""
数据处理
    将有向图或是无向图转换为加权图
"""
import networkx as nx
import csv


# 处理txt文件
def txt_no_weight_trans(filename,output_filename):
    f = open(filename)
    line = f.readline()
    Glist = []
    t = 0
    while line:
        line = line.strip('\n')  # 处理换行
        node = line.split('\t')  # 数据之间以空格隔开
        nodeturple = tuple(node)
        Glist.append(nodeturple)
        line = f.readline()
        # t = t + 1
        # if t > 1000:
        #     break
    f.close()
    # 将结果先处理为图，便于计算邻居
    G = nx.Graph()
    G.add_edges_from(Glist)
    nodes_weight_list = []
    # 对每条边，计算连个节点的公共邻居数 e是一个元组
    for e in Glist:
        nbs1 = list(nx.neighbors(G, e[0]))
        nbs2 = list(nx.neighbors(G, e[1]))
        weight = len(list(set(nbs1).union(nbs2)))
        weight = str(weight)
        nodes_weight_list.append((e[0], e[1], weight))
    # 写入csv文件
    csv_path = 'dataset/wiki-vote.csv'
    csv_file = open(csv_path, 'w', encoding='utf-8', newline='')
    csv_write = csv.writer(csv_file)
    # 　开始写入
    for i in nodes_weight_list:
        print(list(i))
        csv_write.writerow(list(i))

    return nodes_weight_list


def txt_weight_trans(filename, output_filename):
    f = open(filename)
    line = f.readline()
    Glist = []
    t = 0
    while line:
        line = line.strip('\n')  # 处理换行
        node = line.split(' ')  # 数据之间以空格隔开
        node_tuple = tuple(node)
        Glist.append(node_tuple)
        line = f.readline()
        # t = t + 1
        # if t > 1000:
        #     break
    f.close()
    # 写入csv文件
    csv_path = 'dataset/' + output_filename
    csv_file = open(csv_path, 'w', encoding='utf-8', newline='')
    csv_write = csv.writer(csv_file)
    # 　开始写入
    for i in Glist:
        csv_write.writerow(list(i))

    return Glist


# 将无权图处理为加权图
#txt_no_weight_trans("dataset/Wiki-Vote.txt","wiki-vote.csv")
# 将加权图直接处理为csv格式
txt_weight_trans("dataset/emailWeight.txt","emailWeight.csv")
