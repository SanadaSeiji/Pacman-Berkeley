# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        #means you can use values[state]
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"      
        i = 0
        #"it ponders its MDP model to arrive at a complete policy
        #before ever interacting with a real environment."
        #that's why in init() we iterate 100 times to hope the best value converged
        #however, which demands to know all the probabilities of all possible sequenes
        #which in real world is impossible to know
        for i in range(self.iterations):
            #because self.values are going to have the new v k+1
            #use vk store the last time's iteration's values
            vk = self.values.copy() #Attention! to copy a list, must use copy()
                                    #otherwise cannot pass autograder!!! 
                                    
            states=self.mdp.getStates()
            for s in states:
                if self.mdp.isTerminal(s):#since imported and write slef.mdp=mdp, must use self???
                                          #otherwise cannot pass autograder
                    self.values[s] = 0 #v0 = 0
                else:
                    #vk=1 = max-a Q(s,a)
                    actions = self.mdp.getPossibleActions(s)
                    QvalueList = []
                    for a in actions:
                        #HOWEVER
                        #cannot just use v k+1 =self.getQvalue(s,a)
                        #-> self.values[s] = max(self.getQvalue(s,a) for a in actions)
                        #because here need to use v k 's value
                        #but q value use self.values, which is the new, current values, it has no memory of vk
                        #unless to change arguments in computeQValue() and getQ() completely and give vk to it...
                        #which is too complicated
                        #easier to just write the redundent code here
                        transitions = self.mdp.getTransitionStatesAndProbs(s, a)
                        vkplus1 = sum((t[1]*(self.mdp.getReward(s, a, t[0]) + self.discount * vk[t[0]])) for t in transitions)
                        """
                        for t in transitions:
                            vkplus1 += t[1]*(self.mdp.getReward(s, a, t[0]) + self.discount * vk[t[0]])
                        """
                        QvalueList.append(vkplus1)
                    self.values[s] = max(QvalueList)
              
    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        s=state
        a=action
        transitions = self.mdp.getTransitionStatesAndProbs(s,a) 
        # for every t in transition
        # according to mdp.py
        # t[0] = nextState, t[1] = probability to land in that state
        #HOWEVER, "from the value function stored in self.values", how could this be correct?
        #"init"'s audiograder disagree!

        v = sum((t[1]*(self.mdp.getReward(s, a, t[0]) + self.discount * self.values[t[0]])) for t in transitions)
        """
        v=0
        for t in transitions:
            v+=t[1]*( self.mdp.getReward(s,a,t[0])+self.discount*self.values[t[0]])
        """
        return v

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        s=state
        #if v0
        #no best actions, for no action at all
        if self.mdp.isTerminal(s):
            return None
        #otherwise
        actions=self.mdp.getPossibleActions(s)
        #what if the initial value iteration has not got a converged result?
        #means it is still possible for more than one action makes max value here
        #or, two or more actions lead to same value
        #to break tie, here record the value they got too
        policy = None #default action
        vFixedPolicy = -float('inf')
        vBaseline = self.values[s]
        for a in actions:
            vFixedPolicy=self.getQValue(s,a)
            if  vFixedPolicy >= vBaseline:
                policy = a # this way, the last action which got a highest value, is the bestAction
                vBaseline = vFixedPolicy
        return policy        
                

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
