# Huy Vu
# Oct/22/2017
from math import *
import heapq
from pq import PQ
from random import randint
import timeit

# Programming Assignment 3
# (5) After doing steps 1 through 4 below (look for relevant comments), return up here.
#    V1 (priority queue) is slightly faster than V2 (binary heap)
#    The density of the graph does affect the running time (performance): denser graph takes longer to find all paths
#    Size of the graph does affect the performance: as example below, G6 has less vertices (but more edges), it still
#    runs faster than G10 (more vertices and less edges)
#    Note, when create G6 Graph, every time it randomly generates the edge, it also check if that edge already exists in
#    the list. That's the reason it seems to run slower at G6, but that's not the path finding algorithm, it the graph 
#    generator. I found a way to generate it more quickly but it's not necessary here
class Vertex(object):

    def __init__(self, vertex):
        self.value = vertex
        self.neighbors = []
        self.visited = False
       
        self.edges = []
        self.distance = inf
        self.pred = self
        
    def addNeighbor(self, neighbor, weight=None):
        if isinstance(neighbor, Vertex):
            if neighbor not in self.neighbors:
                self.neighbors.append(neighbor)
                if weight != None:
                    self.edges.append(self.Edge(weight,neighbor))
        else:
            return False
    
    def printVertex(self):
        print(self.value, "->", end="\t")
        for i in self.neighbors:
            print(i.value, end = "\t")
    
    def __lt__(self, other):
        return self.value<other.value
        
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)
    
    class Edge:
        def __init__(self, weight, neighbor):
            self.weight = weight
            self.neighbor = neighbor
        
        def __repr__(self):
            resultStr = "Neighbor: %s, weight: %s" %(self.neighbor,self.weight)
            return resultStr
        
        #Deprecated - originally for testing
        def __lt__(self, other):
            return self.weight < other.weight
class Graph:
    vertices = []
    stack = []

    def __init__(self,n=10,edges=[],weights=[]):
        self.vertices = [Vertex(x) for x in range(n)]
        if len(weights) > 0:
            for i,e in enumerate(edges):
                self.addEdge(e[0], e[1], weights[i])
        else:
            for e in edges:
                self.addEdge(e[0], e[1])

        
    def addEdge(self,a,b, w=None):
        self.vertices[a].addNeighbor(self.vertices[b],w)
        self.vertices[b].addNeighbor(self.vertices[a],w)
    
    def __repr__(self):
        resultStr = "Graph has %s vertices.\n" %len(self.vertices)
        for i in self.vertices :
            resultStr+="%s -> \t" %i.value
            for j in i.neighbors :
                resultStr+="%s\t"%j.value
            resultStr+="\n"
            
        return resultStr
    
    def printGraphWithWeights(self) :
        resultStr = "Graph has %s vertices.\n" %len(self.vertices)
        for i in self.vertices:
            resultStr+="%s -> \t" %i.value
            for j in range(len(i.neighbors)) :
                resultStr+="%s"%(i.neighbors[j].value)
                resultStr+="(%s)\t"%i.edges[j].weight
            resultStr+="\n"
        print(resultStr)
            
    #to reset every vertices as not visited, solve the bug I've been trying to find for days!
    def resetVisited(self):
        for v in self.vertices:
            v.visited = False;
    
    #DFS using stack             
    def DFS(self):
        stack = []
        for v in self.vertices:
            if v.visited == False:
                v.visited = True
                self.dfsWithStack(stack, v)
        self.resetVisited()        
            
    def dfsWithStack(self, stack, rootVertex):
        stack.append(rootVertex)
        rootVertex.visited = True
        
        while stack:
            actualVertex = stack.pop()
            print("Actual stack", actualVertex.value)
            
            for v in actualVertex.neighbors:
                if v.visited == False:
                    v.visited = True
                    stack.append(v)
    def DFSrecursive(self):
        for v in self.vertices:
            if v.visited == False:
                v.visited = True
                self.dfsWithRecursive(v)
        self.resetVisited()        
       
    def dfsWithRecursive(self, rootVertex):
        rootVertex.visited = True
        print(rootVertex.value)
        
        for v in rootVertex.neighbors:
            if v.visited == False:
                self.dfsWithRecursive(v)
    
    # 2) Implement Dijkstra's Algorithm using a simple list as the "priority queue" as described in paragraph
    def DijkstrasVersion1(self, sourceVertex):
        sourceVertex.distance = 0
        priorityQ = []
        heapq.heappush(priorityQ, sourceVertex)
        
        while priorityQ:
            tempVertex = heapq.heappop(priorityQ)
            heapq.heappush(priorityQ, tempVertex)

            for e in tempVertex.edges:
                v = e.neighbor
                newDistance = tempVertex.distance + e.weight
                
                if newDistance < v.distance:
                    v.distance = newDistance
                    v.pred = tempVertex
                    heapq.heappush(priorityQ, v)
            heapq.heappop(priorityQ)
        
        paths = []
        for v in self.vertices:
            paths.append((v.value, v.distance, v.pred))
        return paths    
    
    # 3) Implement Dijkstra's Algorithm using a binary heap implementation of a PQ as the PQ.           
    def DijkstrasVersion2(self,sourceVertex):
        sourceVertex.distance = 0
        binaryHeap = PQ()
        binaryHeap.add(sourceVertex, sourceVertex.value)
        
        while not binaryHeap.is_empty():
            tempVertex = binaryHeap.peek_min()

#             if tempVertex.visited == False:
            for e in tempVertex.edges:
                v = e.neighbor
                newDistance = tempVertex.distance + e.weight
                
                if newDistance < v.distance:
                    v.distance = newDistance
                    v.pred = tempVertex
                    binaryHeap.add(v, v.value)
#                 tempVertex.visited = True
            binaryHeap.extract_min()
        
        paths = []
        for v in self.vertices:
            paths.append((v.value, v.distance, v.pred))
        return paths
            
            
class Digraph(Graph):
    # adds an edge from a to b
    def addEdge(self,a,b, w = None):
        self.vertices[a].addNeighbor(self.vertices[b], w)
           
    def topologicalSort(self):
        stack = []
        for v in self.vertices:
            if v.visited == False:
                self.topoligicalSortUtils(stack, v)
        self.resetVisited()               
        return stack
    def topoligicalSortUtils(self, stack, rootVertex):
        rootVertex.visited = True
        for v in rootVertex.neighbors:
            if v.visited == False:
                self.topoligicalSortUtils(stack, v)
        stack.insert(0,rootVertex)
    
    def transpose(self):
        g = Digraph(len(self.vertices))
       
        for i in self.vertices:
            for j in i.neighbors:
                g.addEdge(j.value,i.value)
        return g
    
    def stronglyConnectedComponents(self):
        result = []
        g = self.topologicalSort()
        t = self.transpose()
        
        for i in g:
            temp = []
            if t.vertices[i.value].visited == False:
                t.vertices[i.value].visited = True
                temp.append(i)
                self.sccUtils(temp, i, t)
            if len(temp) != 0:
                result.append(temp)
        self.resetVisited()        
        return result
    
    def sccUtils(self, l, rootVertex, t):
        for j in t.vertices[rootVertex.value].neighbors:
                    if j.visited == False:
                        j.visited = True
                        l.append(j)
                        self.sccUtils(l, j, t)
    
   
        
# G = Graph(7, [(0,5),(0,1),(1,3),(5,2),(5,3),(5,4),(3,6)])
# G.DFSrecursive()
# G.DFS()
# H = Digraph(7, [(5,0),(0,1),(1,3),(2,5),(3,5),(5,4),(3,6)])
# print(H)
# print("Topological Sort: \n", H.topologicalSort())
# print("Transpose Graph: \n", H.transpose())
# print("Strongly Connected Component: \n", H.stronglyConnectedComponents())


w = [           1,      2,    6,    5,    10,   4,    3,    1,    4,   3,    3,    2,    8,    4,     9,    3,    6 ]
G3 = Graph(10, [(0,1),(0,2),(1,3),(1,4),(1,7),(2,5),(2,6),(2,8),(3,7),(4,7),(5,8),(6,8),(7,9),(8,9),(0,9),(0,3),(0,6)], w)
G4 = Digraph(10, [(0,1),(0,2),(1,3),(1,4),(1,7),(2,5),(2,6),(2,8),(3,7),(4,7),(5,8),(6,8),(7,9),(8,9),(0,9),(0,3),(0,6)], w)

print("Single shortest path - priority queue - undirected graph: ")
print(G3.DijkstrasVersion1(G3.vertices[0]))

print("Single shortest path - priority queue - directed graph: ")
print(G4.DijkstrasVersion1(G4.vertices[0]))

print("Single shortest path - binary heap - undirected graph: ")
print(G3.DijkstrasVersion1(G3.vertices[0]))

print("Single shortest path - binary heap - directed graph: ")
print(G4.DijkstrasVersion2(G4.vertices[0]))

# (1) Implement this function, which should:
#    -- Generate a random weighted directed graph with v vertices and e different edges.
def generateRandomWeightedDigraph(v,e,minW,maxW) :
    edges = []
    weight = []
    for i in range(e):
        fromVertex = randint(0,v-1)
        toVertext = randint(0,v-1)
        while (fromVertex == toVertext or (fromVertex,toVertext) in edges):
            fromVertex = randint(0,v-1)
            toVertext = randint(0,v-1)
        edges.append((fromVertex, toVertext))
        weight.append(randint(minW,maxW))
        
    return Digraph(v, edges, weight)
     

# (4) Make sure you find steps 2 and 3 later in this module (down in the DiGraph class) then
#     return up here to finish assignment.

G5 = generateRandomWeightedDigraph(16, 240, 1, 10)
print("Graph\tVertices\t\tEdges\tRunning Time v1\t\tRunning Time v2")
print("G5\t16\t\t240", end = "\t")
print(timeit.timeit('G5.DijkstrasVersion1(G5.vertices[0])',setup="from __main__ import G5",number=1000), end = "\t")
print(timeit.timeit('G5.DijkstrasVersion2(G5.vertices[0])',setup="from __main__ import G5",number=1000))
 
G6 = generateRandomWeightedDigraph(64, 4032, 1, 10)
print("G6\t64\t\t4032", end = "\t")
print(timeit.timeit('G6.DijkstrasVersion1(G6.vertices[0])',setup="from __main__ import G6",number=1000), end = "\t")
print(timeit.timeit('G6.DijkstrasVersion2(G6.vertices[0])',setup="from __main__ import G6",number=1000))
 
G7 = generateRandomWeightedDigraph(16, 60, 1, 10)
print("G7\t16\t\t60", end = "\t")
print(timeit.timeit('G7.DijkstrasVersion1(G7.vertices[0])',setup="from __main__ import G7",number=1000), end = "\t")
print(timeit.timeit('G7.DijkstrasVersion2(G7.vertices[0])',setup="from __main__ import G7",number=1000))
 
G8 = generateRandomWeightedDigraph(64, 672, 1, 10)
print("G8\t64\t\t672", end = "\t")
print(timeit.timeit('G8.DijkstrasVersion1(G8.vertices[0])',setup="from __main__ import G8",number=1000), end = "\t")
print(timeit.timeit('G8.DijkstrasVersion2(G8.vertices[0])',setup="from __main__ import G8",number=1000))
 
G9 = generateRandomWeightedDigraph(16, 32, 1, 10)
print("G9\t16\t\t32", end = "\t")
print(timeit.timeit('G9.DijkstrasVersion1(G9.vertices[0])',setup="from __main__ import G9",number=1000), end = "\t")
print(timeit.timeit('G9.DijkstrasVersion2(G9.vertices[0])',setup="from __main__ import G9",number=1000))
 
G10 = generateRandomWeightedDigraph(64, 128, 1, 10)
print("G8\t64\t\t128", end = "\t")
print(timeit.timeit('G10.DijkstrasVersion1(G10.vertices[0])',setup="from __main__ import G10",number=1000), end = "\t")
print(timeit.timeit('G10.DijkstrasVersion2(G10.vertices[0])',setup="from __main__ import G10",number=1000))