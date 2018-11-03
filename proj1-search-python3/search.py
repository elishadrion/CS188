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


class Node:
    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state
        self.action = action
        self.depth = 1
        self.cost = cost
        self.parent = parent
        if parent:
            self.depth = parent.depth+1

    def expand_node(self, problem):
        return (Node(x[0], self, x[1], self.cost+x[2]) for x in problem.getSuccessors(self.state))

    def get_solution(self):
        #We go back by using the parent of each node and the action it led us to it
        node, reversed_path = self, []
        while node:
            reversed_path.append(node.action)
            node = node.parent
        reversed_path.pop()
        return list(reversed(reversed_path))

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state


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
    fringe = util.Stack()
    fringe.push(Node(problem.getStartState()))
    explored = set()
    if problem.isGoalState(problem.getStartState()):
        return []
    while not fringe.isEmpty():
        node = fringe.pop()
        explored.add(node.state)
        if problem.isGoalState(node.state):
            print (node.state)
            return node.get_solution()
        for successor in node.expand_node(problem):
            if successor.state not in explored:
                fringe.push(successor)
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    fringe = util.Queue()
    fringe.push(Node(problem.getStartState()))
    explored = set()
    if problem.isGoalState(problem.getStartState()):
        return []
    while not fringe.isEmpty():
        node = fringe.pop()
        explored.add(node.state)
        if problem.isGoalState(node.state):
            return node.get_solution()
        for successor in node.expand_node(problem):
            if successor.state not in explored and successor not in fringe.list:
                fringe.push(successor)
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()
    fringe.push(Node(problem.getStartState()), 0)
    explored = set()
    if problem.isGoalState(problem.getStartState()):
        return []
    while not fringe.isEmpty():
        node = fringe.pop()
        explored.add(node.state)
        if problem.isGoalState(node.state):
            return node.get_solution()
        for successor in node.expand_node(problem):
            if successor.state not in explored and successor not in fringe.heap:
                #the priority is the cost to get to the node
                #the higher the cost, the lower the priority
                fringe.update(successor, successor.cost)
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()
    fringe.push(Node(problem.getStartState()), 0)
    explored = set()
    if problem.isGoalState(problem.getStartState()):
        return []
    while not fringe.isEmpty():
        node = fringe.pop()
        explored.add(node.state)
        if problem.isGoalState(node.state):
            return node.get_solution()
        for successor in node.expand_node(problem):
            if successor.state not in explored and successor not in fringe.heap:
                #priority is heuristic+cost
                fringe.update(successor, successor.cost+heuristic(successor.state, problem))
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
