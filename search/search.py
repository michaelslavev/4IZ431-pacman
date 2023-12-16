# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    print("\nDFS Search starts here")

    stack = util.Stack()
    visited_nodes = set()
    path = []
    # Start node tuple (Location, action, cost)
    start_node = (problem.getStartState(), 'Stop', 0)
    # Store nodes as keys with parent node as value 
    memory_map = {start_node : None}
    stack.push(start_node)

    while not stack.isEmpty():
        current_node = stack.pop()
        current_state = current_node[0]

        if current_state not in visited_nodes:            
            visited_nodes.add(current_state)

            # Goal found, create path
            if problem.isGoalState(current_state):
                # traversing from finish node to start node
                while memory_map[current_node] is not None:
                    path.append(current_node[1])
                    current_node = memory_map[current_node]
                return path[::-1]

            # find next succesor node
            for successor_node in problem.getSuccessors(current_state):
                if successor_node[0] not in visited_nodes:
                    memory_map[successor_node] = current_node
                    stack.push(successor_node)

    print("#### Path not found ####\n\n")
    return False
    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    print("BFS Search starts here\n")

    queue = util.Queue()
    visited_nodes = set()
    path = []
    # Start node tuple (Location, action, cost)
    start_node = (problem.getStartState(), 'Stop', 0)
    # Store nodes as keys with parent node as value 
    memory_map = {start_node : None}
    queue.push(start_node)

    while not queue.isEmpty():
        current_node = queue.pop()
        current_state = current_node[0]

        if current_state not in visited_nodes:
            visited_nodes.add(current_state)

            # Goal found, create path
            if problem.isGoalState(current_state):
                # traversing from finish node to start node
                while memory_map[current_node] is not None:
                    path.append(current_node[1])
                    current_node = memory_map[current_node]                    
                return path[::-1]

            # find next succesor node
            for successor_node in problem.getSuccessors(current_state):
                if successor_node[0] not in visited_nodes:
                    memory_map[successor_node] = current_node
                    queue.push(successor_node)

    print("#### Path not found ####\n\n")
    return False


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    print("UCS Search starts here\n")

    priority_queue = util.PriorityQueue()
    visited_nodes = set()
    path = []
    # Start node tuple - Location, action, cost
    start_node = (problem.getStartState(), 'Stop', 0)
    # Store nodes as keys with parent node as value 
    memory_map = {start_node : None}
    priority_queue.push(start_node, 0)
    node_cost = {problem.getStartState() : 0}

    while not priority_queue.isEmpty():
        current_node = priority_queue.pop()
        current_state = current_node[0]
        
        if current_state not in visited_nodes:
            visited_nodes.add(current_state)

            # Goal found, create path
            if problem.isGoalState(current_state):
                # traversing from finish node to start node
                while memory_map[current_node] is not None:
                    path.append(current_node[1])
                    current_node = memory_map[current_node]
                return path[::-1]

            # find next succesor node
            for successor in problem.getSuccessors(current_state):
                if successor[0] not in visited_nodes:
                    memory_map[successor] = current_node
                    node_cost[successor[0]] = successor[2] + node_cost[current_node[0]]
                    priority_queue.push(successor, node_cost[successor[0]])

    print("#### Path not found ####\n\n")
    return False


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    print("aStart Search starts here\n")

    priority_queue = util.PriorityQueue()
    visited_nodes = set()
    path = []
    # Start node tuple - Location, action, cost
    start_node = (problem.getStartState(), 'Stop', 0)
    # Store nodes as keys with parent node as value 
    memory_map = {start_node : None}
    priority_queue.push(start_node, heuristic(start_node[0],problem))
    node_cost = {problem.getStartState() : 0}

    while not priority_queue.isEmpty():
        current_node = priority_queue.pop()
        current_state = current_node[0]
        
        if current_state not in visited_nodes:
            visited_nodes.add(current_state)

            # Goal found, create path
            if problem.isGoalState(current_state):
                # traversing from finish node to start node
                while memory_map[current_node] is not None:
                    path.append(current_node[1])
                    current_node = memory_map[current_node]
                return path[::-1]

            # find next succesor node
            for successor in problem.getSuccessors(current_state):
                if successor[0] not in visited_nodes:
                    memory_map[successor] = current_node
                    node_cost[successor[0]] = successor[2] + node_cost[current_node[0]]
                    priority = node_cost[successor[0]] + heuristic(successor[0], problem)
                    priority_queue.push(successor, priority)
    
    print("#### Path not found ####\n\n")
    return False


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
