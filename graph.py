class Graph:
    def __init__(self, numberOfVertices = 0, adjacencyMatrix = None):
        self.numberOfVertices = numberOfVertices
        if adjacencyMatrix == None:
            adjacencyMatrix = list(list() for i in range(self.numberOfVertices + 1))
        self.graph = adjacencyMatrix
        self.numberOfEdge = 0
        self.connectedComponent = []
        self.numberOfComponents = 0
        self.eulerianPaths = []
        self.numberOfEulerianPaths = 0
    def hasEdge(self, u, v):
        return v in self.graph[u] and u in self.graph[v]
    def addEdge(self, u, v):
        if not self.hasEdge(u, v):
            self.numberOfEdge += 1
            self.graph[u].append(v)
            self.graph[v].append(u)
    def removeEdge(self, u, v):
        if self.hasEdge(u, v):
            tmp = self.graph[u].index(v)
            self.graph[u].pop(tmp)
            tmp = self.graph[v].index(u)
            self.graph[v].pop(tmp)
    def dfsCount(self, start, visited = None):
        if visited == None:
            visited = [False] * (self.numberOfVertices + 1)
        count = 1
        visited[start] = True
        for i in self.graph[start]:
            if not visited[i]:
                count = count + self.dfsCount(i, visited)
        return count
    def isEdgeValid(self, u, v):
        if len(self.graph[u]) == 1:
            return True
        else:
            count1 = self.dfsCount(u)
            self.removeEdge(u, v)
            count2 = self.dfsCount(u)
            self.addEdge(u, v)
            return False if count1 > count2 else True
    def findComponents(self):
        adjacencyDictionary = {}
        for index, item in enumerate(self.graph[1:]):
            adjacencyDictionary[index + 1] = set(item)
        visit = [False for i in range(self.numberOfVertices + 1)]
        for i in range(1, self.numberOfVertices + 1):
            if not visit[i]:
                temp = self.__dfs(adjacencyDictionary, i, visit)
                self.connectedComponent.append(temp)
                if len(temp) > 0:
                    self.numberOfComponents += 1
    def __dfs(self, graph, start, visit, visited = None):
        if visited is None:
            visited = set()
        visited.add(start)
        visit[start] = True
        for n in graph[start] - visited:
            self.__dfs(graph, n, visit, visited)
        return visited
    def __eulerHelper(self, u, temp):
        for v in self.graph[u]:
            if self.isEdgeValid(u, v):
                t = True
                #print("%d,%d" % (u, v))
                temp.append([u, v])
                self.removeEdge(u, v)
                self.__eulerHelper(v, temp)
    def eulerTour(self):
        u = 1
        for i in range(2, self.numberOfVertices + 1):
            if len(self.graph[i]) % 2 != 0 :
                u = i
                break
        temp = list()
        self.__eulerHelper(u, temp)
        if len(temp) > 0:
            self.eulerianPaths.insert(self.numberOfEulerianPaths, temp)
            self.numberOfEulerianPaths += 1
# Alternative approach: "I could not do this part"
inputFile = open("GraphData.txt") # output file sould be "Graph/GraphDataOut.txt"
rawData = inputFile.readlines()
inputFile.close()
data = []
numberOfNode = 0
for i in rawData:
    data.append(map(int, i.rstrip("\r\n").lstrip("(").rstrip(")").split(",")))
    a0 = data[-1][0]
    a1 = data[-1][1]
    if numberOfNode < a0:
        numberOfNode = a0
    if numberOfNode < a1:
        numberOfNode = a1
g = Graph(numberOfNode)
for i in data:
    g.addEdge(i[0], i[1])
outputFile = open("GraphDataOut.txt", "w")
outputFile.write("The number of vertices in the graph is %d.\r\n" % g.numberOfVertices)
outputFile.write("The number of edges in the graph is %d.\r\n" % g.numberOfEdge)
outputFile.write("Below is the adjacency list for this graph with the vertices sorted.\r\n")
for i in range(1, g.numberOfVertices + 1):
    if len(g.graph[i]) == 0:
        outputFile.write("%d,\r\n" % i)
        continue
    g.graph[i].sort()
    outputFile.write("%d," % i)
    outputFile.write(",".join(map(str, g.graph[i])).rstrip(","))
    outputFile.write("\r\n")
g.findComponents()
outputFile.write("The number of connected components of this graph is %d.\r\n" % \
                 g.numberOfComponents)
hold = 0
while True:
    g.eulerTour()
    if g.numberOfEulerianPaths > hold:
        hold = g.numberOfEulerianPaths
    else:
        break
outputFile.write("The number of connected components of the graph that have an Euler\
path is %d.\r\n" % g.numberOfEulerianPaths)
eulerianCircuit = [False] * g.numberOfEulerianPaths
numberOfEulerianCircuit = 0
for index, term in enumerate(g.eulerianPaths):
    outputFile.write("The following %d lines list the edges \
for the Eulerian path for Component %d.\r\n" % (len(term), index))
    if term[0][0] == term[-1][-1]:
        eulerianCircuit[index] = True
        numberOfEulerianCircuit += 1
    for j in term:
        outputFile.write(",".join(map(str,j)))
        outputFile.write("\r\n")
outputFile.write("The number of connected components of the graph that have an Euler \
circuit is %d.\r\n" % numberOfEulerianCircuit)
for index, term in enumerate(g.eulerianPaths):
    if not eulerianCircuit[index]:
        continue
    outputFile.write("The following %d lines list \
        the edges for the Eulerian path for Component %d.\r\n" % (len(term), index))
    for j in term:
        outputFile.write(",".join(map(str,j)))
        outputFile.write("\r\n")
outputFile.close()
