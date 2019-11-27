# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 15:18:01 2019

@author: kondr
"""
#funkcje czekajace na implementacje
def neighbours(node):
    return set_of_node_neghbours
    
def reconstruct_path(came_from, currnt_node):
    if came_from is set:
        path = reconstruct_path(came_from)
            return path

def reconstruct_path(cameFrom, current)
    total_path = {currentNode}
    while currentNode in cameFrom.Keys:
        current := cameFrom[current]
        total_path.prepend(current)
    return total_path  
      
def lowest_f:
    #wierzcholek z najmniejszym f_score
    
def f_score(node):
    return g_score(node) + heuristic_estimation 
    
def g_score(node):
    #dlugosc krawedzi od startu do current_node
    
def heuristic_value(node):
    #
    
def A_star(start, end):
    visited = set(start)
    cameFrom = {}                   #wierzcholki odwiedzone
    not_visited = neighbours(start)       #sasiady odwiedzonych
    g_score = 0                              #odleglosc od startu
    
    
    while not_visited not empty:
        x = lowest_f(not_visited)
        if x = end:
            return reconstruct_path(came_from, end)
        not_visited.discard(x)  
        visited.add(x)
        
        for y in neighbours(x):
            if y in visited:
                continue
            anticipated_g = g_score(x) + dist_between(x, y)
            anticipated_isbetter = false
            if y not in not_visited:
                visited.add(y)
                h_score = heuristic_estimation(y, end)
                anticipated_isbetter = true
            if anticipated_g < g_score(y):
                anticipated_isbetter = true
            if anticipated_isbetter:
                
                