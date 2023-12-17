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

from time import sleep
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
    # print("\nDFS Search starts here")

    stack = util.Stack()
    visited_nodes = set()
    
    # Start node tuple (Location, action, cost)
    start_node = (problem.getStartState(), None, 0)
    # Stack with node + path to that node
    stack.push((start_node, []))

    while not stack.isEmpty():
        current_node, path = stack.pop()
        
        if current_node[0] in visited_nodes:
            continue
        
        visited_nodes.add(current_node[0])

        if problem.isGoalState(current_node[0]):
            return path

        for successor_node in problem.getSuccessors(current_node[0]):
            stack.push((successor_node, path + [successor_node[1]]))                

    print("#### Path not found ####\n\n")
    return False


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # print("BFS Search starts here\n")

    queue = util.Queue()
    visited_nodes = set()
    
    # Start node tuple (Location, action, cost)
    start_node = (problem.getStartState(), None, 0)
    # Queue with node + path to that node
    queue.push((start_node, []))

    while not queue.isEmpty():
        current_node, path = queue.pop()

        if current_node[0] in visited_nodes:
            continue

        visited_nodes.add(current_node[0])
        
        if problem.isGoalState(current_node[0]):
            return path

        for successor_node in problem.getSuccessors(current_node[0]):
            queue.push((successor_node, path + [successor_node[1]]))

    print("#### Path not found ####\n\n")
    return False


def uniformCostSearch(problem):
    # print("UCS Search starts here\n")

    priority_queue = util.PriorityQueue()
    visited_nodes = set()
    start_node = (problem.getStartState(), None, 0)
    priority_queue.push((start_node, []), 0)
    node_cost = {problem.getStartState(): 0}

    while not priority_queue.isEmpty():
        current_node, path = priority_queue.pop()
        
        if current_node[0] in visited_nodes:
            continue
        
        visited_nodes.add(current_node[0])

        if problem.isGoalState(current_node[0]):
            return path

        for successor_state, action, cost in problem.getSuccessors(current_node[0]):
            total_cost = node_cost[current_node[0]] + cost

            if (successor_state not in node_cost) or (total_cost < node_cost[successor_state]):
                node_cost[successor_state] = total_cost
                new_path = path + [action]
                new_node = (successor_state, action, total_cost)
                priority_queue.push((new_node, new_path), total_cost)

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
    # print("aStart Search starts here\n")

    priority_queue = util.PriorityQueue()
    visited_nodes = set()

    start_node = (problem.getStartState(), None, 0)
    priority_queue.push((start_node, []), heuristic(start_node[0], problem))
    node_cost = {problem.getStartState(): 0}

    while not priority_queue.isEmpty():
        current_node, path = priority_queue.pop()
        
        if current_node[0] in visited_nodes:
            continue
        
        visited_nodes.add(current_node[0])

        if problem.isGoalState(current_node[0]):
            return path

        for successor_state, action, cost in problem.getSuccessors(current_node[0]):
            total_cost = node_cost[current_node[0]] + cost

            if (successor_state not in node_cost) or (total_cost < node_cost[successor_state]):
                node_cost[successor_state] = total_cost
                priority = total_cost + heuristic(successor_state, problem)
                priority_queue.push(((successor_state, action, total_cost), path + [action]), priority)

    print("#### Path not found ####\n\n")
    return False


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
