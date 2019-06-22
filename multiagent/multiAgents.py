# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

DirectionsPos = {
    "North": (0,1),
    "South": (0,-1),
    "East": (1,0),
    "West": (-1,0)
}

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]


    def willCollide(self, pacmanState, ghostState):
        """
        Returns True if it estimates pacman and the ghost will collide
        """
        pacmanX, pacmanY = pacmanState.getPosition()
        ghostX, ghostY = ghostState.getPosition()
        SAFEDISTANCE = 2
        #Represent the differences in positions, square around pacman
        perpendicular = {(1,1),(-1,-1),(1,-1),(-1,1)}
        if (pacmanX-ghostX, pacmanY-ghostY) in perpendicular:
            #will collide in a perpendicular way
            if Directions.LEFT[pacmanState.getDirection()] == ghostState.getDirection():
                return True
            elif Directions.RIGHT[pacmanState.getDirection()] == ghostState.getDirection():
                return True
        #Checks the distance horizontally and vertically
        elif pacmanX == ghostX and abs(pacmanY-ghostY) <= SAFEDISTANCE:
            return True
        elif pacmanY == ghostY and abs(pacmanX-ghostX) <= SAFEDISTANCE:
            return True

        return False


    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        new_score = 0
        #The closest to the new position can be the one on the new position so we eat it
        closest_dot = min(currentGameState.getFood().asList(), key=lambda x: util.manhattanDistance(newPos, x))
        #The further it is from the closest dot, the more the score is penalized
        new_score -= util.manhattanDistance(newPos, closest_dot)
        for ghostState in newGhostStates:
            if self.willCollide(successorGameState.getPacmanState(), ghostState):
                new_score -= 50
        return new_score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


# class Node:
#     def __init__(self, gameState, agentIndex, action, parent=None):
#         self.gameState = gameState
#         self.depth = 1
#         self.parent = parent
#         #index of the agent who has to take action
#         self.agentIndex = agentIndex
#         #action that brought us here
#         self.action = action
#         if parent:
#             #if the agent index is lower than its parent, it means we reached a new depth
#             self.depth = parent.depth+1 if agentIndex < parent.agentIndex else parent.depth
#
#     def nextAgentIndex(self):
#         return (self.agentIndex+1) % self.gameState.getNumAgents()
class Node:
    def __init__(self, gameState, agentIndex, action, parent=None):
        self.gameState = gameState
        self.depth = 0
        self.parent = parent
        #index of the agent who has to take action
        self.agentIndex = agentIndex
        #action that brought us here
        self.action = action
        self.children = []
        if parent:
            #if the agent index is lower than its parent, it means we reached a new depth
            self.depth = parent.depth+1 if agentIndex < parent.agentIndex else parent.depth

    def nextAgentIndex(self):
        return (self.agentIndex+1) % self.gameState.getNumAgents()

    def generateChildren(self):
        legalMoves = self.gameState.getLegalActions(self.agentIndex)
        successors = [self.gameState.generateSuccessor(self.agentIndex, legal) for legal in legalMoves]
        self.children = [Node(successors[i], self.nextAgentIndex(), legalMoves[i], self) for i in range(len(successors))]


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    def minimax(self, state, depth, agentIndex):
        if depth == 0 or state.isLose() or state.isWin():
            return self.evaluationFunction(state), Directions.STOP
        legalMoves = state.getLegalActions(agentIndex)
        #maximizing agent
        if agentIndex == 0:
            successors = [state.generateSuccessor(agentIndex, legal) for legal in legalMoves]
            nextAgent = (agentIndex+1) % state.getNumAgents()
            scores = [self.minimax(successor, depth-1, nextAgent)[0] for successor in successors]
            return max(scores), legalMoves[scores.index(max(scores))]
        #minimizing agent
        else:
            successors = [state.generateSuccessor(agentIndex, legal) for legal in legalMoves]
            nextAgent = (agentIndex+1) % state.getNumAgents()
            scores = [self.minimax(successor, depth-1, nextAgent)[0] for successor in successors]
            return min(scores), legalMoves[scores.index(min(scores))]


    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        return self.minimax(gameState, self.depth*gameState.getNumAgents(), 0)[1]






class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
