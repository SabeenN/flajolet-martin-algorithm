from random import *
import operator
import numpy as np
import time
import matplotlib.pyplot as plt

"""
This implementation is based on Flajolet-Martin algorithm as described in the paper "TRIÈST: Counting Local and Global
Triangles in Fully-Dynamic Streams with Fixed Memory Size" by De Stefani, Lorenzo & Epasto, Alessandro & Riondato, Matteo & Upfal, Eli. (2016).
The datasets are from http://konect.uni-koblenz.de/networks/facebook-wosn-links and http://konect.uni-koblenz.de/networks/maayan-faa

This implementation counts the number of triangles in a graph processed on stream with limited size
"""

#Set hyperparameters
files = ["out.facebook-wosn-links","out.maayan-faa"] #from:
impr = False #set False to run the BASE algorithm, True to run the improved version
nr_samples = 1 #nr of times to run the algorithm
file = files[0]
Ms = [500,600,700,800,900,1000,1500,2000,2500,3000] #nr of triangles on stream
#-----


start_time = time.time()
ops = {'+': operator.add, '-': operator.sub}
def read_stream():
    stream=[]
    with open(file,'r') as f:
        f.readline()
        lines = f.readlines()
        for line in lines:
            stream.append(tuple(line.strip().split(" ")[0:2]))
    return stream

def get_neighbours(u,v):
    return sample_neighbours[u], sample_neighbours[v]

def update_counters(op,edge):
    u = edge[0]
    v = edge[1]
    Nu=set()
    Nv=set()
    try:
        Nu, Nv = get_neighbours(u, v)
    except:
        pass
    Nuv = Nu.intersection(Nv)
    n=1
    if impr:
        n = max(1, ((t-1)*(t-2))/(M*(M-1)))
    for c in list(Nuv):
        counters['global'] = max(0, ops[op](counters['global'], n)) #T = T +/- 1
        if c not in counters:
            counters[c] = n
        else:
            counters[c] = max(0, ops[op](counters[c], n))  # T = T +/- 1
        if u not in counters:
            counters[u] = n
        else:
            counters[u] = max(0, ops[op](counters[u], n))  # T = T +/- 1
        if v not in counters:
            counters[v] = n
        else:
            counters[v] = max(0, ops[op](counters[v], n))  # T = T +/- 1

def sample_edge(t):
    if t <= M:
        return True
    elif np.random.binomial(1, M/t) == 1:
        idx = randint(0, M-1)
        popped_edge = list(S.keys())[idx]
        try:
            sample_neighbours[popped_edge[0]].remove(popped_edge[1])
            sample_neighbours[popped_edge[1]].remove(popped_edge[0])
        except:
            pass
        S.pop(popped_edge)
        if not impr:
            update_counters('-', popped_edge)
        return True
    return False

sum_counters=[]
stream = read_stream()
results_Ms=[]
for M in Ms:
    sum_counters = []
    for avg in range(0,nr_samples):
        t = 0
        S = {}
        sample_neighbours = {}
        counters = {'global': 0}
        for edge in stream:
            if len(set(edge)) > 1 and (edge not in S) and (tuple([edge[1], edge[0]]) not in S):
                t += 1
                if impr:
                    update_counters('+', edge)
                if sample_edge(t):
                    S[edge] = 0
                    if edge[0] not in sample_neighbours:
                        sample_neighbours[edge[0]] = set([edge[1]])
                    else:
                        sample_neighbours[edge[0]].add(edge[1])
                    if edge[1] not in sample_neighbours:
                        sample_neighbours[edge[1]] = set([edge[0]])
                    else:
                        sample_neighbours[edge[1]].add(edge[0])
                if not impr:
                    update_counters('+', edge)
        epsilon = 1
        if not impr:
            epsilon = max(1,(t*(t-1)*(t-2)) / (M*(M-1)*(M-2)))
        sum_counters.append(int(counters['global']*epsilon))
    results_Ms.append(int(sum(sum_counters)/len(sum_counters)))

print("---Processing file", file, "took time %s seconds ---" % round((time.time() - start_time),3))
#print("Estimation of triangles for M=817035:", results_Ms[0])
