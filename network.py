# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import os

def constructNetwork(article_obj, articles, step, dir):
    # Networkを宣言
    article_network = nx.Graph()
    # Networkに対象記事のノードを追加
    article_network.add_node(article_obj.name, No = article_obj.no)
    # Networkの各要素を再帰的に構築
    article_network = constructElement(article_obj, articles, article_network, step)
    '''
    calcDegreeCentrality(article_network, article_obj.name)
    calcClosenessCentrality(article_network, article_obj.name)
    calcBetweennessCentrality(article_network, article_obj.name)
    '''
    # Networkの可視化
    printNetwork(article_network, article_obj.name, dir)
    # 各Network特徴量のDATAFRAMEを作成
    series = pd.Series([article_obj.name,
                        calcDegreeCentrality(article_network, article_obj.name),
                        calcClosenessCentrality(article_network, article_obj.name),
                        calcBetweennessCentrality(article_network, article_obj.name),
                        calcDensity(article_network),
                        calcCluster(article_network)],
                       index = ['NAME', 'DEGREE', 'CLOSENESS', 'BETWEENNESS', 'DENSITY', 'CLUSTER'])
    return series

# 関連記事ネットワークの構築(再帰)
def constructElement(article_obj, articles, network, step):
    step = step - 1
    new_node = []
    if step >= 0:
        for i, e in enumerate(article_obj.adjacencyVec):
            if e == 0 or i == article_obj.no:
                continue
            if network.has_node(articles[i].name) and network.has_edge(article_obj.name, articles[i].name):
                continue
            elif not network.has_node(articles[i].name):
                network.add_node(articles[i].name, No = i)
                new_node.append(articles[i].name)
            network.add_edge(article_obj.name, articles[i].name, weight = article_obj.similarityVec[i])
    if step >= 1 and len(new_node) != 0:
        for node in new_node:
            network = constructElement(articles[network.node[node]['No']], articles, network, step)
    return network

# 次数中心性
def calcDegreeCentrality(network, node):
    '''
    # 次数中心性の正規化
    try:
        degree_centrality = nx.degree_centrality(network) # nodeの次数 / node数 - 1 正規化される
        print('Degree Centrality : ' + str(degree_centrality[node]))
    except:
        print('The degree centrality can not be calculated.')
    '''
    return nx.degree(network)[node]

# 近接中心性
def calcClosenessCentrality(network, node):
    '''
    closeness_centrality = nx.closeness_centrality(network)
    print('Closeness Centrality : ' + str(closeness_centrality[node]))
    '''
    return nx.closeness_centrality(network)[node]

# 媒介中心性
def calcBetweennessCentrality(network, node):
    '''
    betweenness_centrality = nx.betweenness_centrality(network)
    print('Betweenness Centrality : ' + str(betweenness_centrality[node]))
    '''
    return nx.betweenness_centrality(network)[node]

# ネットワーク密度
def calcDensity(network):
    # density = nx.density(network)
    # print('Density : ' + str(density))
    return nx.density(network)

# クラスター係数
def calcCluster(network):
    return nx.average_clustering(network)

#ネットワークの可視化
def printNetwork(network, node, dir):
    plt.figure(figsize = (15, 15))
    pos = nx.spring_layout(network)
    edge_width = [30 ** d['weight'] for (u, v, d) in network.edges(data = True)]

    nx.draw_networkx_nodes(network, pos, node_color = 'black', node_size = 2700)
    nx.draw_networkx_nodes(network, pos, node_color='w', node_size = 2650)
    nx.draw_networkx_nodes(network, pos, node_color = 'r', node_size = 2650, nodelist = [node])
    nx.draw_networkx_labels(network, pos, fontsize = 1, font_color = 'black')
    nx.draw_networkx_edges(network, pos, edge_color = 'C', alpha = 1, width = edge_width)

    if not os.path.exists(dir):
        os.mkdir(dir)

    plt.axis('off')
    plt.savefig(dir + node.split('.')[0] + '.png')
    plt.show()
