#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Usage : 
- Input feature file, class file, edge list
- Output Json file with key = id and value = type
- Change file name if you need
'''
import numpy as np
import json


file_features = '../../elliptic_bitcoin_dataset/elliptic_txs_features.csv'
file_edge = '../../elliptic_bitcoin_dataset/elliptic_txs_edgelist.csv'
file_class = '../../elliptic_bitcoin_dataset/elliptic_txs_classes.csv'
json_file = '../../elliptic_bitcoin_dataset/class.json'
graph_file = '../../elliptic_bitcoin_dataset/graph.json'
output_csv = "../../elliptic_bitcoin_dataset/full_data.csv"



def read_features_file():
    with open(file_features) as f:
        FH = np.genfromtxt(f, delimiter=',', dtype='str')
    return FH


def read_edge_file():
    with open(file_edge) as f:
        FH = np.loadtxt(f, delimiter=',', skiprows=1, dtype='str')
    return FH


def read_file_class():
    with open(file_class) as f:
        FH = np.genfromtxt(f, delimiter=',', dtype='str')
    return FH


def output_json(arr):
    dict1 = {arr[i][0] : arr[i][1] for i in range(len(arr))}
    with open(json_file, 'w') as fp:
        json.dump(dict1, fp)
    return dict1


if __name__ == "__main__":
    results_features = read_features_file()
    results_class = read_file_class()
    results_edge = read_edge_file()
    results_class = results_class[1::]
    results_id = results_class[:, :-1]
    r = results_class[:,0]
    dict1 = output_json(results_class)
    dict2 = {}
    for i in r:
        dict2[f'{i}'] = {'in':[], 'out':[]}
    for i in range(len(results_edge)):
        dict2[results_edge[i][0]]['out'].append(results_edge[i][1])
        dict2[results_edge[i][1]]['in'].append(results_edge[i][0])
    with open(graph_file, 'w') as fp:
        json.dump(dict2, fp)
        

    
