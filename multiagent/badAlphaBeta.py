class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def maxValue(self, node, depth, alpha, beta):
        """
        Return score and node
        """
        v = (float('-inf'), node)
        legalMoves = node.gameState.getLegalActions(node.agentIndex)
        for legal in legalMoves:
            successor = node.gameState.generateSuccessor(node.agentIndex, legal)
            successorNode = Node(successor, node.nextAgentIndex(), legal, node)
            successorV = self.alphaBeta(successorNode, depth-1, alpha, beta)
            #max
            if (successorV[0] > v[0]):
                v = successorV
            if v[0] > beta:
                return v
            alpha = max(alpha, v[0])
        return v

    def minValue(self, node, depth, alpha, beta):
        """
        Return score and node
        """
        v = (float('inf'), node)
        legalMoves = node.gameState.getLegalActions(node.agentIndex)
        for legal in legalMoves:
            successor = node.gameState.generateSuccessor(node.agentIndex, legal)
            successorNode = Node(successor, node.nextAgentIndex(), legal, node)
            successorV = self.alphaBeta(successorNode, depth-1, alpha, beta)
            #min
            if (successorV[0] < v[0]):
                v = successorV
            if v[0] < alpha:
                return v
            beta = min(beta, v[0])
        return v


    def alphaBeta(self, node, depth, alpha, beta):
        if depth == 0 or node.gameState.isWin() or node.gameState.isLose():
            return self.evaluationFunction(node.gameState), node
        if node.agentIndex == 0:
            return self.maxValue(node, depth, alpha, beta)
        else:
            return self.minValue(node, depth, alpha, beta)

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        root = Node(gameState, 0, Directions.STOP)
        #return self.alphaBetaPruning(root, self.depth*gameState.getNumAgents(), float('-inf'), float('inf'))[1].action
        return self.alphaBeta(root, self.depth*gameState.getNumAgents(), float('-inf'), float('inf'))[1].action
