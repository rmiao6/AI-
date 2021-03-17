#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 07:52:16 2021

@author: miaorunxuan
"""



import psutil
import os
import datetime as dt
import queue
import time
import random
import math
import sys



def Expand_mis(cur_node):

    
    children_mis_tile=[]
    empty_tile=cur_node.index(0)
    for action in actions:
        new_empty_tile=empty_tile+action
        h_num_misplaced=-1
        while (new_empty_tile>=0) & (new_empty_tile<=15):
            list_node=list(cur_node)
            list_node[empty_tile]=list_node[new_empty_tile]
            list_node[new_empty_tile]=0
            child=tuple(list_node)

            for i,j in zip(child, goal_state):
                if i!=j:
                    h_num_misplaced+=1           
            cost_num_of_misplaced_tiles=h_num_misplaced
            child_mis_tiles=(cost_num_of_misplaced_tiles,)+child+(action,)
            children_mis_tile.append(child_mis_tiles)
            
            break
    
    return children_mis_tile


def Expand_man(cur_node):

    
    children_manhattan=[]
    empty_tile=cur_node.index(0)
    for action in actions:
        new_empty_tile=empty_tile+action
        while (new_empty_tile>=0) & (new_empty_tile<=15):
            list_node=list(cur_node)
            list_node[empty_tile]=list_node[new_empty_tile]
            list_node[new_empty_tile]=0
            child=tuple(list_node)
            h_manhattan_distance=sum(abs((val-1)%4 - i%4) + abs((val-1)//4 - i//4)
                                     for i, val in enumerate(child) if val)
            
            cost_manhattan_distance=h_manhattan_distance
            child_manhattan=(cost_manhattan_distance,)+child+(action,)
            children_manhattan.append(child_manhattan)
            break
    
    return children_manhattan


def search_manhattan(path, g, bound):

    expanded_node,move=path[-1]
    path_set=set(expanded_node)
    curren_puzzle=expanded_node[1:17]
    h=sum(abs((val-1)%4 - i%4) + abs((val-1)//4 - i//4)
                                      for i, val in enumerate(curren_puzzle) if val)
    
    f=g+h
    if f>bound:
        return f
    if curren_puzzle==goal_state:
        solving_puzzle=[]
        for i in move:
            if i==1:
                solving_puzzle.append('R')
            elif i==-1:
                solving_puzzle.append('L')
            elif i==4:
                solving_puzzle.append('D')
            elif i==-4:
                solving_puzzle.append('U')

        print('Moves: ',' '.join(solving_puzzle)) 
        print('Number of Node Expanded by manhattan distance: ',len(path))
        return 'FOUND'
    mini= float("inf")
    
    children_manhattan=Expand_man(curren_puzzle)
    children_manhattan.sort(key = lambda children_manhattan: children_manhattan[0]) 
    
    for child_state in children_manhattan:
        child_action=child_state[17]
        child=child_state[1:17]
        updated_node_state=[child_state,move+[child_action]]

                
        if child_state not in path_set :
            
            path.append(updated_node_state) 
            t=search_manhattan(path, g+1, bound)
            if t=='FOUND':
                return 'FOUND'
            
            if t<mini:
                mini=t
            path.pop()
    
    return mini


def search_mis_tiles(path_mis, g_mis, bound):

    expanded_node,move=path_mis[-1]
    path_set_mis=set(expanded_node)
    curren_puzzle=expanded_node[1:17]
    h_mis=-1
    for i,j in zip(curren_puzzle, goal_state):
        if i!=j:
            h_mis+=1  

    
    f_mis=g_mis+h_mis
    if f_mis>bound:
        return f_mis
    if curren_puzzle==goal_state:
        print('Number of Node Expanded by the number of misplaced tiles: ',len(path_mis))

        return 'FOUND'
    mini= float("inf")
    
    children_mis=Expand_mis(curren_puzzle)
    
    children_mis.sort(key = lambda children_mis: children_mis[0]) 
    
    for child_state in children_mis:
        child_action=child_state[17]
        child=child_state[1:17]
        updated_node_state=[child_state,move+[child_action]]

                
        if child_state not in path_set_mis :
            
            path_mis.append(updated_node_state) 
            t=search_mis_tiles(path_mis, g_mis+1, bound)
            if t=='FOUND':
                return 'FOUND'
            
            if t<mini:
                mini=t
            path_mis.pop()
    
    return mini



def ida_star(root):

        
    h_manhattan_distance=sum(abs((val-1)%4 - i%4) + abs((val-1)//4 - i//4)
                                     for i, val in enumerate(root) if val)
    bound=h_manhattan_distance

    h_mis=-1
    for i,j in zip(root, goal_state):
        if i!=j:
            h_mis+=1  
    bound_h_mis=h_mis
    
    
    
    cost=1000
    no_action='None'
    node_state=(cost,)+root+(no_action,)


    node_state_list=[node_state]
    for iters in range(10000):
        move=[]
        node_state_list=[node_state,move]
        print('iterations:',iters)
        path= []
        path.append(node_state_list)
        path_mis=[]
        path_mis.append(node_state_list)

        t=search_manhattan(path, 0, bound)
        t_mis=search_mis_tiles(path_mis, 0, bound_h_mis)
        if t== 'FOUND':
            return goal_state
        if t== float("inf"):
            return 'NOT FOUND'
        bound = t
        
        if t_mis== 'FOUND':
            return goal_state
        if t_mis== float("inf"):
            return 'NOT FOUND'
        bound_h_mis = t_mis
        
process = psutil.Process(os.getpid())
start_memory=process.memory_info().rss / 1024.0
start_time=time.time() 
    







initial_puzzle=[]
initial_puzzle=list(map(int,input().split()))
initial_puzzle=tuple(initial_puzzle)

goal_state=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0)
actions=[-1,1,4,-4]
solved_puzzle=ida_star(initial_puzzle)


end_time=time.time()
end_memory = process.memory_info().rss / 1024.0

print('Time Taken: ',end_time - start_time)
print('Memory Used: ',str(end_memory-start_memory) + " kb")
print('Solved puzzle: ',solved_puzzle)

   

