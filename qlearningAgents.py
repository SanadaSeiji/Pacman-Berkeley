# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    #try manually test it on grid first please...
    #before autograder kick your arse...
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        #similar like in valueIterationAgent
        #using the dict provided in util
        #would be in form: qValues[(state, action)]
        #init Q-values
        self.qValues = util.Counter()


    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        #similar like in valueIterationAgents
        #its getValue func
        #if not in q dict yet, add that to the dict
        #so that later you can deal with unseen action
        if (state, action) not in self.qValues:
          self.qValues[(state, action)] = 0.0
        q=self.qValues[(state,action)]
        
        return q

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        #state given
        #thus, goal: computer qV got from different action
        
        actions = self.getLegalActions(state)
        #if terminal state /no legal actions:
        if len(actions) == 0:
            return 0.0
        else: #otherwise return a q's value, the max q value in every possible actions
        #assuming that
        #q's value should already be in the self.qValues' dict
            return max(self.getQValue(state, a) for a in actions)

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        #like in above, computeValueFromQValue
        #state given, goal: get an action, who leads to max q
        actions = self.getLegalActions(state)
        #if terminal state /no legal actions:
        if len(actions) == 0:
            return 0.0
        else:
            highestQV = 0.0 #for unseen actions
            bestAction = None #see valueIterationAgents, computeActionFromValues()
                              #...or the last line from this one's instruction
            for a in actions:
                qV=self.getQValue(state, a)
                if qV>=highestQV or bestAction == None:
                    highestQV = qV
                    bestAction = a

                    
            return bestAction
        
    def getAction(self, state):
        #worked from crawler too
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None #this is the action you might return!!!
        "*** YOUR CODE HERE ***"
        if len(legalActions) == 0:
            return action #now still None
        else:
        #epsilon greedy
        #epsilon chances, random action
        #1-epsilon chance, best policy action
            #in random case/ exploration mode
            #flipCoin return true if r=random.random < epsilon
            if util.flipCoin(self.epsilon):
               #choose a random q
               action=random.choice(legalActions)
            else: #otherwise r>=epsilon, magority case
            #choose best action given a state
            #the function written above
                action = self.computeActionFromQValues(state)#don't forget "self"!!!
            return action
        

        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf ????
        """
        "*** YOUR CODE HERE ***"
        #the resson to write this core function in the end
        #because you need to call functions like
        #getQValue...
        
        #unlike valueIteration, agent offline solving MDP
        #here you are online, means no i in range self.iteration, agent will learn in enviroment
        # "it will be called on your behalf"
        #not really sure how this is going to work...
        #just follow the tiny gridworld example on slides, do the same process...
        #according to slides
        #q(s,a) <- (1-alpha)*q(s,a) + alpha * sample
        #q(s,a) <- (1-alpha)*q(s,a) + alpha * (R + discount * max q(nestS, nextA) )
        # no f(u, n) epsilon chance of random action should be able to take care of this aspect
        #given s, a, nextS, R, have self alpha and discount
        #nextA got from legalAction(nextS)
        #update the qValue dict
        
        #similar to valueIteration, for safe, no direct update half ways
        #although judging from result, does not really matter

        #oldQVs = self.qValues.copy() <-- don't do this
        #copy a dict waste too much time
        #algo correct, but won't pass autograder
        #which would raise you a time out exception and make you lose one point
        #have to check if no legalAction, like instructed above
        if len(self.getLegalActions(nextState)) == 0:
            #terminal state
            # max q future =0
            sample = reward
        else: # don't forget discount!!!!
            sample = reward + self.discount * (max( self.getQValue(nextState, a) for a in self.getLegalActions(nextState)))
        #any now update
        #only change record qV[(state, action)] !!! no iteration here...
       # self.qValues[(state,action)] = (1-self.alpha)* oldQVs[(state,action)] + self.alpha*sample
        self.qValues[(state,action)] = (1-self.alpha)* self.getQValue(state, action) + self.alpha*sample

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)

class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())() # "feat" here is "feature"
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        # see in featureExtractors.py
        # features are like:  features["#-of-ghosts-1-step-away"] = a value
        # getFeatures return features vector
        
        featVec = self.featExtractor.getFeatures(state, action)
        weights=self.getWeights()
        #if never has this state , see getQValue for  q learning grid agent and crawler
        q=0.0
        # q = weight vector dot feature vector, means sum of every w * every v
        # w=weights[f]
        # f's value = featVec[f]
        q= sum( featVec[f] * weights[f] for f in featVec)
        return q


    def update(self, state, action, nextState, reward):
        """
           !!! Should update your weights based on transition!!!!
        """
        "*** YOUR CODE HERE ***"
        # not care about q value, update weight
        # according to (not slides but) q8 on berkely's website:
        # w m <- w m + alpha * difference*f m (s,a)
        #difference = [r + gamma * max(Q(nextS, nextA)] - Q(s, a)
        # as in getQValue
        # search w based on f
        #HOWEVER!!!
        # according to instruction here above
        # "based on transition !!"
        #means: difference = [r + gamma * computeValueFromValues(nextState)] - Q(s,a)
        
        featVec = self.featExtractor.getFeatures(state, action)
        # max(self.getQValue(nextState, a) for a in slef.getLegalAction(nextState)) 
        # can help pacman win all the game
        # but unable to pass autograder 's last test 
        # iteration 3, "EXIT" value's slightly different...
        # if use max though, don't forget to check if len(legalAction) == 0
        
        #"base on transition"
        difference = reward + self.discount * self.computeValueFromQValues(nextState)-self.getQValue(state,action) 
        
        for f in featVec:       
            self.weights[f] += self.alpha * difference * featVec[f]  
        
       
    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
