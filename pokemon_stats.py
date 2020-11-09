# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 10:57:17 2020

@author: Nathan
"""

from csv import DictReader
from math import inf, sqrt
# Use linkage to verify results
from scipy.cluster.hierarchy import linkage
import numpy as np


def load_data(filepath):
    toret = []
    with open(filepath) as csvfile:
        reader = DictReader(csvfile)
        i = 0
        for row in reader:
            toadd = row
            del toadd['Legendary']
            del toadd['Generation']
            toret.append(toadd)
            i += 1
            
            if i == 20:
                break
            
    return toret


def calculate_x_y(stats):
    return (int(stats['Attack']) + int(stats['Sp. Atk']) + int(stats['Speed']),
            int(stats['Defense']) + int(stats['Sp. Def']) + int(stats['HP']))


def euclid(point1, point2):
    dist = 0
    for xi, yi in zip(point1, point2):
        dist += (xi - yi) ** 2
    return sqrt(dist)


def cluster_dist(cluster1, cluster2):
    shortest_dist = inf
    for item1 in cluster1:
        for item2 in cluster2:
            dist = euclid(item1, item2)
            if dist < shortest_dist:
                shortest_dist = dist
                
    return shortest_dist


def hac(dataset):
    Z = []
    clusters = []
    for i in range(len(dataset)):
        clusters.append({'id':i, 'data':[dataset[i]]})
    _next_cluster_id = len(clusters)
        
    shortest_dist = inf
    merging = (-1, -1)
    _merging = (-1, -1)
    while len(clusters) > 1:
        for i in range(len(clusters)-1):
            for j in range(i+1, len(clusters)):
                dist = cluster_dist(clusters[i]['data'], clusters[j]['data'])
                
                if dist < shortest_dist:
                    shortest_dist = dist
                    merging = (clusters[i]['id'], clusters[j]['id'])
                    _merging = (i, j)
        
        i = _merging[0]
        j = _merging[1]
        clusters[i]['data'].extend(clusters[j]['data'])
        clusters[i]['id'] = _next_cluster_id
        _next_cluster_id += 1
        del clusters[j]
        
        Z.append([min(merging), max(merging), shortest_dist, len(clusters[i]['data'])])
        
        shortest_dist = inf
        merging = (-1, -1)
        
    return Z