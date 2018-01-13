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
       # newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #basic score form action
        score = successorGameState.getScore()
        #check if win
        if successorGameState.isWin() :   
            return 100000
        #add food score tp basic score
        #check distance to nearest food
        foodList = newFood.asList()
        nearestFood =  min([util.manhattanDistance(newPos, food) for food in foodList])
        foodScore = 0
        if nearestFood == 0:
            foodScore += 1.0 #because for every food it eaten, pacman got one point
        else:
            score += 1.0/nearestFood
            
        #add ghost score to basic score
        #2 ghosts, red and blue
        nearestGhost = 10000; #default disdance to a ghost
        ghostScore = 10
        for ghostState in newGhostStates: 
           # if ghostState.scaredTimer == 0: #when ghost is dangerous
               ghostPos = ghostState.getPosition()
               distanceToGhost = util.manhattanDistance(newPos, ghostPos)
               if nearestGhost > distanceToGhost:
                  nearestGhost = distanceToGhost
        if nearestGhost<1:       #collide distance in pacman.py is 0.7
                                 #if about to be eaten - Ghost in scared Time doesn't count as ghost here anyway
             return -10000 #been eaten, minus 500 in pacman.py
        ghostScore = -nearestGhost #nearer, more dangerous
           
        #add penalty for not moving
        if action == Directions.STOP:
            score -= 1 #for in pacman.py been punished by mere existing
        
        #add capsule score, for with capsule, ghost's scaredTimer been reset
        #and when scredTimer>0, score+200
        capsuleList = currentGameState.getCapsules()

        if newPos in capsuleList: #if has capsule, do not seek out for capsule though
           score += 200
               
        #because simply add foodScore and subtract ghostScore did not work well
        #using ratio of foodScore/ghostScore as additional score
        #for as question 5 shows, weights of food/ghost score alone does not matter much
        #what matters is the ratio of these weights
        #therefore using food/ghost
        #when food nearer, adds more
        #ghost nearer,subtracts more
        #a functional linear function (although evaluate gameState instead of action) can be found in question 5's solution
        return score + foodScore/ghostScore

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

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

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
        #must be first, because minValue will call this function
        #in a layer, whenever it's pacman's turn to evaluation gameState
        #it will pick best scored situation
  


        #hence max
        def maxValue(gameState, depth, numghosts):
            #if pacman can definitely win/lose
            #or if reached depth of game-theory-gameState tree
            #exit for this recurssive function
            #evaluate the gameState
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
               return self.evaluationFunction(gameState)
            score = -(float("inf")) #system min int, "inf" == infinite
            
            #pacman's turn to move
            pacActions = gameState.getLegalActions(0)
            for action in pacActions:
                successorGameState = gameState.generateSuccessor(0, action) # for pacman moves
            
            #after pacman, ghost moves
            #ghost 1, agent[1] about to move
            #pacman assumes worst to the extent of commiting suicide
            #thus, pacman takes worst situation - min-scored-gameState as ghosts' choice
            #from all worst, pacman chooses a best - based on predicted gameState in depth-Future
            #minValue(GameState, currentDepth, agentIndex, total ghost number)
                score=max(score, minValue(successorGameState, depth, 1, ghostNum)) 
            return score
        
        #in a layer, whenever it is ghost's turn to move
        #for pacman, who would rather commit suicide, always expects the worst from ghosts
        #therefore pacman thinks it would pick the least scored gameState for ghosts to it
        #hence min
        def minValue(gameState, depth, agentIndex, ghstNum):
            #if pacman can definitely win/lose
            #or if reached depth of game-theory-gameState tree
            #exit for this recurssive function
            #evaluate the gameState
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
               return self.evaluationFunction(gameState)
            score = float("inf") #system max int
            
            #ghosts' turn to move
            ghostActions = gameState.getLegalActions(agentIndex)
            if agentIndex != ghostNum: #if this isn't the last ghost
               for action in ghostActions:
                   successorGameState = gameState.generateSuccessor(agentIndex, action)
                   #next move whould still be ghost's, hence minValue
                   #pass turn to next ghost
                   score = min(score, minValue(successorGameState, depth, agentIndex+1, ghostNum))
            else: #if this is last ghost, next would be pacman's turn
                for action in ghostActions:
                    successorGameState = gameState.generateSuccessor(agentIndex, action)
                    #to next layer
                    #pacman's turn, hence maxValue
                    score = min(score, maxValue(successorGameState, depth+1, ghostNum))
            return score
        
        #root of game-theory gameState tree
        depth=0
        #pacman's turn to move
        pacActions = gameState.getLegalActions(0) #pacman's always agent 0
        ghostNum = gameState.getNumAgents()-1 #agent 0 is pacman
        scoreGS = -(float("inf")) #score of gameState, system min int
        
        for action in pacActions:
            prevScore = scoreGS
            successorGameState = gameState.generateSuccessor(0, action) # for pacman moves
            
            #after pacman, ghost move
            #ghost 1, agent[1] about to move
            #pacman assumes worst to the extent of commiting suicide
            #thus, pacman takes worst situation - min-scored-gameState as ghosts' choice
            #from all worst, pacman chooses a best - based on predicted gameState in depth-Future
            #minValue(GameState, currentDepth, agentIndex, total ghost number)
            scoreGS=max(scoreGS, minValue(successorGameState, depth, 1, ghostNum)) 
            
            if scoreGS > prevScore:
                bestAction = action
                
        return bestAction
        

        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxValue(gameState, depth, numghosts, alpha, beta):
              #if pacman can definitely win/lose
            #or if reached depth of game-theory-gameState tree
            #exit for this recurssive function
            #evaluate the gameState
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
               return self.evaluationFunction(gameState)
            score = -(float("inf")) #system min int
            
            #pacman's turn to move
            pacActions = gameState.getLegalActions(0)
            for action in pacActions:
                successorGameState = gameState.generateSuccessor(0, action) # for pacman moves
            
            #after pacman, ghost moves
            #ghost 1, agent[1] about to move
            #pacman assumes worst to the extent of commiting suicide
            #thus, pacman takes worst situation - min-scored-gameState as ghosts' choice
            #from all worst, pacman chooses a best - based on predicted gameState in depth-Future
            #minValue(GameState, currentDepth, agentIndex, total ghost number)
                score=max(score, minValue(successorGameState, depth, 1, ghostNum, alpha, beta))
                if score > beta: #whatever ghosts come up, pacman can out best them
                    return score#prune, return this score to outer layer, for this situation garantee a win for pacman
                alpha = max(alpha, score)#pacman can at least win when gameState is this score,so possiblly reset alpha
            return score
        
        #in a layer, whenever it is ghost's turn to move
        #for pacman, who would rather commit suicide, always expects the worst from ghosts
        #therefore pacman thinks it would pick the least scored gameState for ghosts to it
        #hence min
        def minValue(gameState, depth, agentIndex, ghstNum, alpha, beta):
            #if pacman can definitely win/lose
            #or if reached depth of game-theory-gameState tree
            #exit for this recurssive function
            #evaluate the gameState
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
               return self.evaluationFunction(gameState)
            score = float("inf") #system max int
            
            #ghosts' turn to move
            ghostActions = gameState.getLegalActions(agentIndex)
            if agentIndex != ghostNum: #if this isn't the last ghost
               for action in ghostActions:
                   successorGameState = gameState.generateSuccessor(agentIndex, action)
                   #next move whould still be ghost's, hence minValue
                   #pass turn to next ghost
                   score = min(score, minValue(successorGameState, depth, agentIndex+1, ghostNum, alpha, beta))
                   if score < alpha: #if the future/situation worse than pacman do handle
                       return score#prune, for pacman garantee to lose, no need to expand this node further, it's dead
                   #if score >= alpha, pacman can outrun ghost still
                   #game continues
                   beta = min(beta, score)# ghost can only do this worse, though,so possiblly reset beta
            else: #if this is last ghost, next would be pacman's turn
                for action in ghostActions:
                    successorGameState = gameState.generateSuccessor(agentIndex, action)
                    #to next layer
                    #pacman's turn, hence maxValue
                    score = min(score, maxValue(successorGameState, depth+1, ghostNum, alpha, beta))
                    if score < alpha: #if the future/situation worse than pacman do handle
                       return score#prune, for pacman garantee to lose, no need to expand this node further, it's dead
                   #if score >= alpha, pacman can outrun ghost still
                   #game continues
                    beta = min(beta, score)# ghost can only do this worse, though,so possiblly reset beta
            return score
        
        #root of game-theory gameState tree
        #both alpha and beta make pacman and ghost seem invincible at beginning
        #as game continues, their best actions will reset their limmits
        alpha = -(float("inf")) # bottom line of pacman, the worst situ it can handle
        beta = float("inf") # up limit of ghosts, the best/worst they can do
        #as long as score>= alpha, pacman might live, no garantee win for ghost
        #as long as score<=beta, ghost might win, no garantee win for pacman
        #as long as no future predetermined, game goes on
        depth=0
        bestAction = Directions.STOP
        #pacman's turn to move
        pacActions = gameState.getLegalActions(0) #pacman's always agent 0
        ghostNum = gameState.getNumAgents()-1 #agent 0 is pacman
        scoreGS = -(float("inf")) #score of gameState, system min int
        
        for action in pacActions:
            prevScore = scoreGS
            successorGameState = gameState.generateSuccessor(0, action) # for pacman moves
            
            #after pacman, ghost move
            #ghost 1, agent[1] about to move
            #pacman assumes worst to the extent of commiting suicide
            #thus, pacman takes worst situation - min-scored-gameState as ghosts' choice
            #from all worst, pacman chooses a best - based on predicted gameState in depth-Future
            #minValue(GameState, currentDepth, agentIndex, total ghost number)
            scoreGS=max(scoreGS, minValue(successorGameState, depth, 1, ghostNum, alpha, beta)) 
            
            if scoreGS > prevScore:
                bestAction = action
            if scoreGS > beta: #whatever ghosts come up, pacman can out best them
                return bestAction #prune, return this score to outer layer, for this situation garantee a win for pacman
             #if scoreGS<=beta
            #ghosts' worst might win, game should continue
            #for pacman wnats a better way with higher possibility to win
            alpha = max(alpha, scoreGS)#pacman can at least win when gameState is this score,so possiblly reset alpha
                
        return bestAction

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

        def maxValue(gameState, depth, numghosts):
              #if pacman can definitely win/lose
            #or if reached depth of game-theory-gameState tree
            #exit for this recurssive function
            #evaluate the gameState
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
               return self.evaluationFunction(gameState)
            score = -(float("inf")) #system min int
            
            #pacman's turn to move
            pacActions = gameState.getLegalActions(0)
            for action in pacActions:
                successorGameState = gameState.generateSuccessor(0, action) # for pacman moves
            
            #after pacman, ghost moves
            #ghost 1, agent[1] about to move
            #pacman assumes worst to the extent of commiting suicide
            #thus, pacman takes worst situation - min-scored-gameState as ghosts' choice
            #from all worst, pacman chooses a best - based on predicted gameState in depth-Future
            #minValue(GameState, currentDepth, agentIndex, total ghost number)
                score=max(score, expectValue(successorGameState, depth, 1, ghostNum)) 
            return score
        
        #in a layer, whenever it is ghost's turn to move
        #for pacman, who would rather commit suicide, always expects the worst from ghosts
        #therefore pacman thinks it would pick the least scored gameState for ghosts to it
        #hence min
                #ghost moves at random choice
        #no telling which direction they will pick
        #could be worst, would be anything
        #however, I do not write code to manipulate ghosts' behavior
        #only pacman's rection to this random behavior
        #therfore, average a score of all ghost's possible behaviors' score
        def expectValue(gameState, depth, agentIndex, ghstNum):
            #if pacman can definitely win/lose
            #or if reached depth of game-theory-gameState tree
            #exit for this recurssive function
            #evaluate the gameState
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
               return self.evaluationFunction(gameState)
            score = float("inf") #system max int
            scoreAllActions = float(0)
            
            #ghosts' turn to move
            ghostActions = gameState.getLegalActions(agentIndex)
            actionNum = len(ghostActions)
            if agentIndex != ghostNum: #if this isn't the last ghost
               for action in ghostActions:
                   successorGameState = gameState.generateSuccessor(agentIndex, action)
                   #next move whould still be ghost's, hence minValue
                   #pass turn to next ghost
                   score = expectValue(successorGameState, depth, agentIndex+1, ghostNum)
                   scoreAllActions = scoreAllActions+score
            else: #if this is last ghost, next would be pacman's turn
                for action in ghostActions:
                    successorGameState = gameState.generateSuccessor(agentIndex, action)
                    #to next layer
                    #pacman's turn, hence maxValue
                    score = maxValue(successorGameState, depth+1, ghostNum)
                    scoreAllActions = scoreAllActions+score
            return scoreAllActions/actionNum #average score of all possible actions
        
        #root of game-theory gameState tree
        depth=0
        #pacman's turn to move
        pacActions = gameState.getLegalActions(0) #pacman's always agent 0
        ghostNum = gameState.getNumAgents()-1 #agent 0 is pacman
        scoreGS = -(float("inf")) # score of gameState, system min int
        
        for action in pacActions:
            prevScore = scoreGS
            successorGameState = gameState.generateSuccessor(0, action) # for pacman moves
            
            #after pacman, ghost move
            #ghost 1, agent[1] about to move
            #pacman assumes worst to the extent of commiting suicide
            #thus, pacman takes worst situation - min-scored-gameState as ghosts' choice
            #from all worst, pacman chooses a best - based on predicted gameState in depth-Future
            #minValue(GameState, currentDepth, agentIndex, total ghost number)
            scoreGS=max(scoreGS, expectValue(successorGameState, depth, 1, ghostNum)) 
            
            if scoreGS > prevScore:
                bestAction = action
                
        return bestAction

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin():
       return float("inf")
    if currentGameState.isLose():
       return - float("inf")
    #baseline score
    score = scoreEvaluationFunction(currentGameState)
    #features: food, ghost, capsule
    #foodDist to nearestFood
    foodList=currentGameState.getFood().asList()
    pacPos=currentGameState.getPacmanPosition()
   
    nearestF=1000
    nearestF=min([util.manhattanDistance(pacPos, food) for food in foodList])
   
    #ghostDist to nearestGhost
    ghostStates = currentGameState.getGhostStates()
   
    nearestG=1000
    nearestG=min([util.manhattanDistance(pacPos, ghostState.getPosition()) for ghostState in ghostStates])
   
    #capsuleDist to nearestCap
    capList = currentGameState.getCapsules()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    
    #weight on ghost depends on ghost's mode : scared or not
    #if ghost is white
    if sum(scaredTimes)!=0:
        #one of the two reasons this evaluation can be over 1100
        ghostScore = 1/(nearestG+1)*15 #if ghost's not scaring, hunt it
    #if ghost can eat    
    else:   
        #only care about ghost when it is within 3
        #one of the other reasons this evaluation could be over 1100
       ghostScore = min(nearestG,3) * 2
       #if ghost is upon pacman, run for life if it still can
       if nearestG == 0:
          return - float("inf") 
      
    #the weight on this feature auctually doesn't matter much
    foodScore = nearestF
    
    #if still food/cap out there uneaten, punish
    #so pacman be encouraged to eat food and capsule
    #weight on food left cannot be too hight, otherwise pacman crashes
    #weight on capsule can be higher, but doesn't really matter much
    punish = 4*len(foodList) + 4*len(capList)

    #final score
    score = score + ghostScore - foodScore-punish
    
   
    return score 
       
      
   

# Abbreviation
better = betterEvaluationFunction

