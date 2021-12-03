import json
import os
import argparse
import networkx as nx

def main():
    args = get_args()
    output_file = args.output
    input_file = args.input
    
    with open (input_file) as f:
        dict = json.load(f)
    
    G = nx.Graph()
    construct_Graph(G,dict)

    stat_dict = compute_stats(G)
    
    dir = os.path.dirname(output_file)
    if not (os.path.exists(dir)) and not (dir == ''):
        os.makedirs(dir)
    with open(output_file,'w') as f:
        json.dump(stat_dict,f,indent = 2)


def compute_stats(G):
     
    dict = {
                "most_connected_by_num" : [],
                "most_connected_by_weight" : [],
                "most_central_by_betweenness" : [],
            }
    
    dict["most_connected_by_num"].extend(most_connected_by_num(G))
    dict["most_connected_by_weight"].extend(most_connected_by_weight(G))
    dict["most_central_by_betweenness"].extend(most_central_by_betweenness(G))
    return dict

def most_connected_by_num(G):
    char_degree_dict = {}
    for node in G.nodes():
        char_degree_dict[node] = G.degree(node)
    
    char_degree_dict_sorted = {k: v for k, v in sorted(char_degree_dict.items(), key=lambda item: item[1],reverse= True)}
    char_list = list(char_degree_dict_sorted.keys())[:3]
    return char_list

def most_connected_by_weight(G):
    char_weight_dict = {}
    for n1,n2 in G.edges():
        if n1 not in char_weight_dict.keys():
            char_weight_dict[n1] = G[n1][n2]['weight']
        else:
            char_weight_dict[n1] += G[n1][n2]['weight']

        if n2 not in char_weight_dict.keys():
            char_weight_dict[n2] = G[n1][n2]['weight']
        else:
            char_weight_dict[n2] += G[n1][n2]['weight']

    char_weight_dict_sorted = {k: v for k, v in sorted(char_weight_dict.items(), key=lambda item: item[1],reverse= True)}
    char_list = list(char_weight_dict_sorted.keys())[:3]
    return char_list

def most_central_by_betweenness(G):
    betweenness_dict = nx.algorithms.centrality.betweenness_centrality(G)
    betweenness_dict_sorted = {k: v for k, v in sorted(betweenness_dict.items(), key=lambda item: item[1],reverse= True)}
    char_list = list(betweenness_dict_sorted.keys())[:3]
    return char_list


def construct_Graph(G,dict):
    for char,net in dict.items():
        for other_char,weight in net.items():
            if weight == 0 or other_char == char:
                continue
            if G.has_edge(char,other_char):
                 continue
            #     G[char][other_char]['weight'] += weight
            else:
                G.add_edge(char,other_char, weight = weight)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o','--output')
    parser.add_argument('-i','--input')
    return parser.parse_args()

if __name__ == "__main__":
    main()