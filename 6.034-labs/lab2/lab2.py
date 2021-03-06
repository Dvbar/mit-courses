# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False 

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True 

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    raise NotImplementedError

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    raise NotImplementedError


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    queue = [[start]]
    while len(queue) > 0 and queue[0][-1] != goal:
        current_path = queue.pop(0)
        current_node = current_path[-1]
        connected = graph.get_connected_nodes(current_node)
        new_paths = {}
        for connected_node in connected:
            distance_to_goal = graph.get_heuristic(connected_node, goal)
            if connected_node not in current_path:
                add_to_dictlist(new_paths, distance_to_goal, current_path + [connected_node])
        paths_for_front = []
        for path_distance in sorted(new_paths):
            paths_for_front.extend(new_paths[path_distance])
        queue = paths_for_front + queue
    if len(queue) > 0:
        return queue[0]
    else:
        return [] 

def add_to_dictlist(dictionary, key, value):
    if key in dictionary:
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    queue = { graph.get_heuristic(start, goal): [[start]]}
    made_progress = True
    while len(queue) > 0 and made_progress:
        top_k_distances = sorted(queue)[:beam_width]
        k = 0
        current_paths = []
        for distance in top_k_distances:
            for path in queue[distance]:
                if k < beam_width:
                    current_paths.append(path)
                    k += 1
                else:
                    break
                    break
        made_progress = False
        queue = {}
        for path in current_paths:
            current_node = path[-1]
            for node in graph.get_connected_nodes(current_node):
                if node == goal:
                    return path + [node]
                if node not in path:
                    made_progress = True
                    add_to_dictlist(queue, graph.get_heuristic(node, goal), path + [node])
    return []
     
## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    length = 0
    for i in xrange(len(node_names)-1):
        node1 = node_names[i]
        node2 = node_names[i+1]
        length += graph.get_edge(node1, node2).length
    return length 

def branch_and_bound(graph, start, goal):
    paths = [(0, [start])]
    while len(paths) > 0:
        current_path = paths.pop(0)[1]
        current_node = current_path[-1]
        for node in graph.get_connected_nodes(current_node):
            if node not in current_path:
                new_path = current_path + [node]
                if node == goal:
                    return new_path
                paths.append((path_length(graph, new_path), new_path))
        paths.sort(key=lambda tup: tup[0])
    return []
    
def a_star(graph, start, goal):
    import heapq
    queue = []
    heapq.heapify(queue)
    heapq.heappush(queue, (graph.get_heuristic(start, goal), [start]))
    extended_set = {start: graph.get_heuristic(start, goal)}
    while len(queue) > 0:
        current_path = heapq.heappop(queue)[1]
        current_node = current_path[-1]
        if current_node == goal:
             return current_path
        for node in graph.get_connected_nodes(current_node):
            if node not in current_path:
                new_path = current_path + [node]
                new_path_length = path_length(graph, new_path) + graph.get_heuristic(node, goal)
                if node in extended_set:
                    if new_path_length < extended_set[node]:
                        for i in xrange(len(queue)):
                            if queue[i][1][-1] == node:
                                queue[i] = (new_path_length, new_path)
                else:
                    extended_set[node] = new_path_length
                    heapq.heappush(queue, (new_path_length, new_path))
        queue.sort(key=lambda tup: tup[0])
    return []

def dijkstras(graph, start):
    queue = [(0, start)]
    distances = {start: 0}
    parents = {start: None}
    finished_set = {}
    while len(queue) > 0:
        tup = queue.pop(0)
        current_node = tup[1]
        original_distance = tup[0]
        finished_set[current_node] = True
        for node in graph.get_connected_nodes(current_node):
           if node not in finished_set:
               new_distance = original_distance + graph.get_edge(current_node, node).length
               if node in distances:
                   if new_distance < distances[node]:
                       distances[node] = new_distance
                       parents[node] = current_node
                       queue.append((new_distance, node))
               else:
                   distances[node] = new_distance
                   parents[node] = current_node
                   queue.append((new_distance, node))
        queue.sort(key=lambda tup: tup[0])
    return (distances, parents)

## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    distances, parents = dijkstras(graph, goal)
    for node in graph.nodes:
        if distances[node] < graph.get_heuristic(node, goal):
            return False
    return True

def is_consistent(graph, goal):
    for edge in graph.edges:
        if edge.length < abs(graph.get_heuristic(edge.node1, goal) - graph.get_heuristic(edge.node2, goal)):
            return False
    return True

HOW_MANY_HOURS_THIS_PSET_TOOK = '2.25'
WHAT_I_FOUND_INTERESTING = 'Implementing A* was really cool. I liked doing a lot of the implementation for the algorithms.'
WHAT_I_FOUND_BORING = 'I thought this was really interesting, so I didnt find anything very boring.'
