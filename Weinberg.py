# -*- coding: utf-8 -*-


# This method is based on the algorithm presented by Louis Weinberg in his
# paper "A Simple and Efficient Algorithm for Determining Isomorphism of
# Planar Triply Connected Graphs" from 1965, available at
# ieeexplore.ieee.org/document/1082573
# It is in polynomial time and applies to planar triply-connected graphs.
#
# A graph must be modelised by an array for which each index corresponds to a
# node. The values in the i-th array (corresponding to the i-th node) are the
# indices of the nodes that are linked by a vertex to the i-th node. This way
# each branch is modelised 2 times, one time in each direction, as is needed for
# the algorithm.
# For instance, K2 would be [ [1] , [0] ]
# In the same way, K3 would be [ [1,2] , [0,2] , [0,1] ] and a "square" graph
# (4 nodes and 4 vertices forming a square) would be
# [ [1,3] , [0,2] , [1,3] , [0,2] ]


def getNodesValence(graphs):
    """
    Outputs a 2-dimensions array containing, for each graph, a list of
    the numbers of nodes having the valence (ie, number of branches)
    corresponding to the index in the list.
    For example, if there are 3 nodes with valence equal to 5 in the graph of
    the i-th graph, then the output at coordinates (i,5) will be 3.
    For K3, the output is [0,0,3] because all 3 nodes have valence 2.
    Note that it applies to a set of graphs and therefore outputs a set of
    valence vectors.
    """
    nodesValence = []
    for graph in graphs:
        val = [0]*(len(graph)+1) # Could be reduced to occupy less memory
        for node in graph:
            val[ len(node) ] += 1
        nodesValence.append(val)
    return nodesValence

def choseNextBranch(branchesVisited,node,previousBranch,reverseOrder):
    """
    Returns the next branch that has not already been used in this direction,
    at node 'node' and coming from branch 'previousBranch'.
    The default order is clockwise but if 'reverseOrder' is True, the order is
    counter-clockwise.
    """
    started = False
    for k in range( 2*len(branchesVisited[node]) + 1 ):
        if reverseOrder:
            k = -k
        b = k % len(branchesVisited[node])
        if started and (not branchesVisited[node][b]):
            return b
        if b == previousBranch:
            started = True

def generateCodeVector(graph,r,b,reverseOrder=False):
    """
    Given a graph, a node of index r and a branch of index b on this
    node, this function follows Weinberg's algorithm to generate the eulerian
    path and return the code vector of the graph 'graph' for starting
    branch b on node r.
    Variable 'reverseOrder' indicates whether the order is default or not
    (clockwise or counterclockwise).
    """
    # Vector indicating for each node if the path already passed by it
    # Starting node r is already visited at the beginning
    nodesVisited = [False]*len(graph)
    nodesVisited[r] = True
    # Vector indicating for each branch if the path already passed by it
    branchesVisited = [ [False]*len(node) for node in graph]
    # Initialise path
    path = [r]

    initialNode = r; branch = b; terminalNode = graph[r][b];
    # Inside the loop, we mark the current branch (between initialNode and
    # terminalNode) as visited, as well as terminalNode if it isn't already,
    # we add terminalNode to path, and update the value of initialNode,
    # terminalNode and branch.
    while(True): # Could be changed to the length of the eulerian path for more security

        reverseBranch = graph[terminalNode].index(initialNode)

        branchesVisited[initialNode][branch] = True
        path.append(terminalNode)

        if nodesVisited[terminalNode] == False: #new node: go to next branch
            nodesVisited[terminalNode] = True

            branch = choseNextBranch(branchesVisited,terminalNode,reverseBranch,reverseOrder)
            if branch == None:
                print("Error: no available branch on a new node")
                break
            initialNode = terminalNode
            terminalNode = graph[terminalNode][branch]

        else: #old node

            if branchesVisited[terminalNode][reverseBranch] == False: #new branch: make a U-turn
                branchesVisited[terminalNode][reverseBranch] = True
                path.append(initialNode)
                branch = choseNextBranch(branchesVisited,initialNode,branch,reverseOrder)
                if branch == None:
                    print("Error: no available branch while coming from a new branch\n")
                    break
                terminalNode = graph[initialNode][branch]

            else: #old branch: go to next available branch
                branch = choseNextBranch(branchesVisited,terminalNode,reverseBranch,reverseOrder)
                if branch == None:
                    break
                initialNode = terminalNode
                terminalNode = graph[terminalNode][branch]
    else:
        print("Error: no break instruction reached in the loop")
    correspondance = []
    vector = []
    for n in path:
        if not( n in correspondance ):
            correspondance.append(n)
            vector.append( len(correspondance)-1 )
        else:
            vector.append( correspondance.index(n) )
    return vector

def generateCodeMatrix(graph):
    """
    Generates the full code matrix (list of code vectors) from a given graph
    'graph' given as a parameter
    """
    codeMat = []
    for r in range(len(graph)):
        for b in range(len( graph[r][0] )):
            codeMat.append( generateCodeVector(graph,r,b) )
            codeMat.append( generateCodeVector(graph,r,b,True) )
    # To do: sort the vectors
    return codeMat

def graphBranchFromLabel(graph,n):
    """
    Returns indices of the node and branch corresponding to label n in the graph
    (with oriented branches, hence the variable reverseOrder).
    Returns r = -1 if n > number of branches.
    This is a way to define an order in the code vectors for a given graph, with
    the position of the starting branch of the eulerian path for this vector. It
    allows to store a label (an int n) to indicate which vectors have already
    been generated. It is only needed when comparing two graphs, so that we
    don't always need to generate all the vectors of a graph.
    """
    r = 0; b = -1; reverseOrder = False
    for c in range(n+1):
        b += 1
        if len(graph[r]) <= b:
            b = 0; r += 1
        if len(graph) <= r:
            if reverseOrder == False:
                b = 0; r = 0; reverseOrder = True
            else:
                return -1,-1,False
    return r,b,reverseOrder

def checkIdenticalExistingVectors( newgraphs, vectors, v ):
    """
    Checks if there exists a vector from 'vectors' corresponding to one of the
    graphs from 'newgraphs', that is equal to v (ie, checks if a vector equal to
    v has already been generated). If such vector exists, it returns True, and
    else it returns None
    """
    for i in newgraphs:
        for j in vectors[i]:
            if j == v:
                return True

def checkIdenticalNewVectors( graphs, newgraphs, vectors, v ):
    """
    Checks if there exists a vector not yet generated, corresponding to one of
    the graphs from 'newgraphs', that is equal to v (ie, generates code vectors
    of the newgraphs and checks if they are equal to v). If such vector exists,
    it returns True, and else it returns None.
    In any case, the vectors generated are stored in 'vectors'.
    """
    for i in newgraphs:
        while True:
            # Get the next vector for graph i
            r,b,reverseOrder = graphBranchFromLabel( graphs[i],len(vectors[i]) )
            if r == -1: # If we already checked all vectors of graph i
                break
            newVect = generateCodeVector(graphs[i],r,b,reverseOrder)
            # Add it to vectors
            vectors[i].append(newVect)
            # Check if it is equal to v
            if newVect == v:
                return True

def eliminateDoubles( graphs ):
    """
    Applies the Weinberg algorithm to reduce the size of graphs by eliminating
    a graph when 2 of them are isomorphic.
    """
    # generate the vector of nodes valence and the vector of meshes shapes
    nodesValence = getNodesValence(graphs)
    #meshesShapes = getMeshesShapes(graphs)
    # To do: we still need to find an efficient way to get meshes shapes
    # as is suggested in Weinberg's paper

    newgraphs = [0] # contains INDICES (from graphs) of the graphs that will be kept after the execution of the function
    vectors = [ [] for k in range(len(graphs)) ] # list of the lists of vectors of all graphs

    # for each graph k, we check if it is isomorphic to a previous graph i
    for k in range( 1 , len(graphs) ):

        for i in newgraphs:
            # check if valences are equal
            if nodesValence[k] != nodesValence[i]:
                newgraphs.append(k)
                break

        else: # if valences are identical, check existing vectors compared to v
            v = generateCodeVector(graphs[k],0,0)
            if checkIdenticalExistingVectors(newgraphs, vectors, v):
                break

            # if no already generated vectors match with v, add vectors to previously registered graphs
            if checkIdenticalNewVectors(graphs, newgraphs, vectors, v):
                break
            else:
                newgraphs.append(k)
                vectors[k] = [v]

    # Conversion from indices to actual graphs
    graphsReturned = []
    for i in newgraphs:
        graphsReturned.append(graphs[i])

    return graphsReturned # return graphs with only indices from newgraphs

graphs = [[ [1,2] , [0,2] , [0,1] ],[ [1,2] , [0,2] , [0,1] ]]
print(eliminateDoubles(graphs))





















