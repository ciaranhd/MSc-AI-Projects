
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------									
									Nature of the Problem
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

The Dice Game is a Reinforcement Learning problem, in which I will write an Agent which choses Actions to maximise long term rewards. 

The Probability/Transformation Functions for any given action is known in advance, therefore it is an example of a “Complete” Markov Decision Process ("MDP"). 

The Dice Game is an MDP as the decision on what action is next is dependent ONLY on the current state (current dice).

The objective of the programme is to take any state (possible throw of dice), and return a “deterministic” action, which ranges from holding/sticking,
to throwing any combination of Dice available, in order to maximise the total points from a game.

“Value Iteration” using the “Bellman Equation” is the mechanism by which I will attempt to chose between actions in order to maximise the the total expected return from a State.

Before proceeding, lets unpack some of the terms referred to above, and where appropriate describe them with reference to the Dice Game.




-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
									What is the Agent?
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Abstract Definition: A learner whose actions are dependent on the environment which provides rewards. 

The learner in this problem is the player who must decide amongst multiple actions at any given state to maximise long term rewards.




-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
									Maximising Rewards?
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

In Reinforcement Learning, the rewards flowing from an action at a given State are decided exogenously by higher powers outside the Agent’s control (Andrew).

The Dice Game Rewards are predefined as the sum of the digits on the upward facing dice thrown, with the caveat that duplicate dice are flipped prior to summation of their upward facing digits.




-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
					Will The Long Term Rewards Of an Infinite Game Be Infinite Also At All States? 
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

The Dice Game is an example of a “Continuing Task” problem, as is it does not have a terminal state. We can use the principle of discounting so that the cumulative reward for a State reaches a limit point 
(avoiding the infinity conundrum). This is true for any discount factor between 0 and 1, which can be proven using the Infinite Geometric Series principle.

The value of the discount factor is in my opinion a question of preference to risk and the future. However, we can make some logical deductions on what value the discount factor cannot take. For example, 
a discount factor of 0 would mean the Agent is Myopic and completely ignores rewards in the future. 

The essence of the question is to maximise the long-term score; therefore a Myopic agent would be incongruent to this objective, leading us to weight the future quite heavily instead, and thereby the discount 
factor should be closer to 1. It cannot be 1 however, as the Value Iteration would no longer converge (if no terminal state exists).

The concept of discounting in order to involve infinite rewards leads us to reframing the Agent’s objective to maximising the long term DISCOUNTED rewards given a state. 

Now that we have defined some of the main elements of the problem, the main question is how we ensure that an Agent choses Actions which are able to maximise the long-term 
discounted reward for a given State. As already alluded to, the tool is a process called Value Iteration using the Bellman’s Equation.




-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
									What is Value Iteration?
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

It is a process which returns the State/Action Pair for a given state with the highest Value.

A less abstract explanation:
If I roll (1,1,1), I have 8 possible actions. Obviously, the State-Action Pair of Holding is the best choice, and therefore it should be the highest Value State-Action amongst the 8 possible actions.




-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
									Bellman’s Equation
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

This is simply a mathematical expression that the “Value of a state is equal to the discounted “Value” of the expected next states, plus the rewards expected along the way” (Sutton, R.S. & Barto AG. Reinforcement Learning: An Introduction, MIT Press, p.97) 

We use this to assign Values to State-Action Pairs.

Notice the recursive properties of the equation as the value of a state today, is dependent on the values tomorrow, which are in turn deduced by calling the same equation.

The Bellman’s equation can be solved for Continuous Problems:
	In the Continuous case for the dice game, we use the Bellman’s equation “Iteratively” by way of “Dynamic Programming”. 
	We assume that we are at the terminal state (at the very end of the Tree), which would result in the Value Vectors being 0 Vector, for there is no next stage (there is no tomorrow) and therefore no values. 
	The output of the Bellman’s equation is continuously fed back as an input until it reaches a limit (i.e., the change in the Argmax Value Vector goes to 0). 
	All Actions in the Dice Game will be solved iteratively apart from Holding and ending the game.

“Holding” is an example with a closed Form Solution. We are in effect looping back on ourselves.
VS = T(r + VS'), where VS = VS' (from holding), could be solved instantly. Therefore  VS = Reward/ (1-Discount Factor). All other state-actions would take time to "build" to their convergent values, hence comparing is left to the very end when finalising the Polcy.




-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
										Policy
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

The Value Function returns a NUMBER. If I were to ask what the best action is… and you were to reply “7”, this might be a valid answer if the question is 5 + 2, but it is utterly meaningless in the context of what I should throw next in a Dice Game.
After convergence, we can distil the best Action at a given state by choosing the state-action (for that state) with the highest Value, and saving that Action in a Dictionary which we can access by hashing the State we are at. 
In my Code I have stored this in the Policy Dictionary





-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
										Code 
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class MyAgent(DiceGameAgent):
    def __init__(self, game):
        # this calls the superclass constructor (does self.game = game)
        global copy_values
        super().__init__(game)
        self.values_iteration_dictionary = None

        class probability_reward_functions:
            """ This Class Recognises That Every State Has Different Optimum Actions Associated With It.
                The Code Will Create A "Node" for Every State, Saving The Reward Vectors For Each State
                Action Pair From That State. Later In The Code, The Memory Location (A "Pointer") Will
                Be Saved In A Dictionary, Thereby Allowing Us To "Hash" By State to Retrieve Data and
                Methods For That State"""
		The basic outline of the code can be illustrated below:

	                                                                                                     ########################
                                                             			<------------------  	 /   self.state = (1,1,1)      \
               #Dictionary#                                  		      /  			/    self.get_next_states()     |
(1,1,1) : |___(Node/Pointer)__| <--------     Class: probability_reward_functions                       |    self.actions               |
(1,1,2) : |___________________|                           						|    Def: Reward Functions      |
(1,1,3) : |___________________|                          			        		|    Def: Probability Function  |---->------->-------------
     .                                                   			        		|                               |			  |	
     .                                                    				 		\_______________________________/			  |
(6,6,6) : |___________________|   																  |
																				  |	
																				  |
													  							  |
            def __init__(self, state, game):								 							  |
                # Modifying The Game Will Mean The Hold Action Will Vary. 3 Dice --> (0,1,2)            							  |
                # 2 Dice --> (0,1). Therefore We Must Dynamically Update The Hold Action               								  |
		no_dice = game._dice                                                                  								  |
                self.hold_action = tuple([_ for _ in range(no_dice)])				     								  |
																				  |
                # The Number Of Actions In A Modified Game Changes Dependent On The Number Of Dice. 								  |
                # It Is Worth Keeping Track Of The Number Of Actions For Iterating Through Them									  |
                
		self.actions = game.actions															  |
                self.no_actions = len(self.actions)														  |
																				  |
                # Import Crucial Data From The "game" Class in "dice_game.py"											  |
                
		self.state = state																  |
                self.game = game																  |
                self.state_score_dict = game.final_scores													  |
                self.actions = game.actions															  |
                self.penalty = game._penalty															  |
																				  |
                # ------------------------------------------------------------------------------------------------------------------#				  |
                			### TRANSFORMATION/PROBABILITY FUNCTIONS ###										  |
                # There Are Distinct Probability Functions And Reward Functions For A Given Action At A State/							  |
                # Create A Default Dictionaries Which Will Allow Us To Retrieve The Prob and Reward Functions/							  |
                # For A Given State																  |
																				  |
																				  |
                self.probability_dictionary = defaultdict(lambda: 0)  <--- The initialised empty dictionaries are explained below				  |
                self.reward_dictionary = defaultdict(lambda: 0)	      												  |
                self.state_action_dictionary = defaultdict(lambda: 0)												  |
            																			  |
		The For Loop (below) will will produce 3 Main Dictionaries											  |
			1) The State-Action Dictionary (self.state_action_dictionary): Which will tell us the States which arise from taking an action		  |
			2) The Reward Dictionary (self.reward_dictionary): This will tell us the reward vector from taking an action				  |
			3) The Transformation Function (self.probability_dictionary): This will give us a probability vector for a given action			  |
																				  |	
		 for i in range(self.no_actions):														  |
                    temp = []																	  | 
                    action_states = []															          |
                    next_states, _, _, probabilities = self.game.get_next_states(self.actions[i], self.state)							  |
                    for state in next_states:															  |
                        if self.actions[i] != self.hold_action:												          |
                            state_reward = self.state_score_dict[state]												 /
                            temp.append(state_reward)														/
                            action_states.append(state)													       /
                        else:																      /
                            state_reward = self.state_score_dict[self.state]										     /
                            temp.append(state_reward)													    /
                            action_states.append(state)													   /
																			  /
                    self.state_action_dictionary[self.actions[i]] = action_states									 /
                    self.reward_dictionary[self.actions[i]] = temp										        /
                    self.probability_dictionary[self.actions[i]] = np.array(probabilities)							       /
																		      /
            # ------------------------------------------------------------------------------------------------------------------#		     /
	    The Methods below were created for convenience, so that I could call them in the main program. I felt it made things		    /
	    easier to follow.															   /
																		  /
            # Method To Find All the Reward Values For A Specific ACTION									 /
            def call_reward_dictionary(self):													/
                return self.reward_dictionary            										       /
																	      /		
            # Method To Find All the PROBABILITY Values For A Specific ACTION								     /
            def call_probability_dictionary(self):											    /
                return self.probability_dictionary											   /
																          /
            def state_action_pairs(self):												 /
                return self.state_action_dictionary											/
																       /																
       																      /
	|															     /
																    /
	# ------------------------------------------------------------------------------------------------------------------#      /
        					### NODE DICTIONARY ###								  /
        # As Previously Stated At The Beginning Of The "probability_reward_functions" Class, We Will Save  			 /
        # A Node In Memory For Each State, So That We Can Effeciently Retrieve It From A Dictionary (O(1)), To Prevent			/
        # Needless Node Creation And Memory Use As We Continually Iterate Until Convergence.				       /
        node_dictionary = defaultdict(lambda: 0)							<--------<------------/
        for state in self.game.states:
            node_state = probability_reward_functions(state, game)
            node_dictionary[state] = node_state
        # ------------------------------------------------------------------------------------------------------------------#

        # Initialise the Values Dictionary to Take 0. We Assume The Value For S' is 0. Explained in the Intro Narrative.
        value_array = []
        values_dictionary = defaultdict(lambda: 0)
        self.values_dictionary_temp = defaultdict(lambda: 0)
        for state in self.game.states:
            values_dictionary[state] = 0
            value_array.append(0)

            					### VALUE ITERATION ALGORITHM ###
        # ------------------------------------------------------------------------------------------------------------------#
        delta = 1
	For dynamic games with 5 dice or more, I have reduced the theta and convergence factor in order to reduce the run time.
        if self.game._dice > 4:
            theta = 1 - (self.game._dice*0.05)
            convergence_factor = 0.001
        else:
            theta = 0.88   ----------> Theta is 0.88 for the default tests.
            convergence_factor = 0.00000000001
        i = 0
        while delta > convergence_factor:
            # The Iteration We Will Use The Zero Vector For Values. Afer This We Will Use The Output From The Function (Recursively), Until We Reach Convergence.
            if i == 0:
                values_dictionary = defaultdict(lambda: 0)
                i = i + 1
                for state in self.game.states:
                    values_dictionary[state] = 0
                    copy_values = values_dictionary.copy()
            else:
                copy_values = values_dictionary.copy()

            for state in self.game.states:
                # Hash The Node Dictionary To Retrieve Data Such As Reward Function + Transformation Function + State Action Pairs For That State.
                
		node_state = node_dictionary[state]           ---------> Find the State Node 
                rewards = node_state.call_reward_dictionary()  -----------> Call the reward dictionary for that state. 
                probabilities = node_state.call_probability_dictionary() -----> Call the Probability Dictionary for the state
                state_action_pair = node_state.state_action_pairs()      -------> Different States Arise from Actions on a specific State. State Action Pair retrieves a Dictionary which we can use to find states from an action
                penalty = node_state.penalty

                # We Wil Iterate Through ALl Actions For Their Values, Saving Them To "temp_value_states"/ after Which We Will Find The Highest Value, And Save It For That State Action Pair.
                temp_value_states = []
                for action in self.game.actions:
                    possible_states = state_action_pair[action]
                    if possible_states == 0:
                        break
                    value_array1 = []
                    for states in list(possible_states):
                        if states == None:
                            value_array1.append(values_dictionary[state])
                        else:
                            value_array1.append(values_dictionary[states])
                    reward = np.array(rewards[action])
                    probability = np.array(probabilities[action])

                    value_state = np.dot(probability, ((reward - penalty) + (theta * np.array(value_array1))))  ---------------> VALUE ITERATION FORMULA		      (0,1,2) Contains the Maximum Value (hypothetical example)
                    temp_value_states.append((value_state))															 /
																						/                
		highest_action_value = max(temp_value_states) -------------> The State-Action Pair which returns the highest Value for the State: [():12, (0,):44, ... (0,1,2): 1000)
                copy_values[state] = highest_action_value

            # Test For Convergence --> We Keep iterating until the Value Vector Changes (delta) get extremely close to Zero.
            total1 = 0
            total2 = 0
            for state in self.game.states:
                total1 = total1 + values_dictionary[state]
                total2 = total2 + copy_values[state]
            delta = total2 - total1
            values_dictionary = copy_values.copy()
 
						Visual Illustration of Updating the Value Vector Iteratively
 ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


VK(1,1,1) = MAX{											-                  -								
		action_1(Hold) – (Reward) 											    
																                       
		action_2(R,R,R) – probability(1,1,1)* ([ reward(1,1,1) – 1 ]+ VK’(1,1,1) )+					                           
				       probability(1,1,2)* ( [reward(1,1,2) – 1] + VK’(1,1,2) +					                        
				       probability(1,1,3) * ([reward(1,1,3) – 1] + VK’(1,1,3)) +				                          
				       probability(1,1,4) * ([reward(1,1,4) – 1] + VK’(1,1,4)) +                                    
								.							            
								.						.		    
				       probability(6,6,6) * ([reward(6,6,6) – 1] + VK(6,6,6)              
					all states visited by R,R,R (all possible state)
					
		
		
		action_3(H,H,R) - probability(1,1,1)* ([ reward(1,1,1) – 1 ]+ VK(1,1,1) )+
				       probability(1,1,2)* ( [reward(1,1,2) – 1] + VK(1,1,2) +
				       probability(1,1,3) * ([reward(1,1,3) – 1] + VK(1,1,3)) +
				       probability(1,1,4) * ([reward(1,1,4) – 1] + VK(1,1,4)) +
				       probability(1,1,5) * ([reward(1,1,5) – 1] + VK(1,1,5)) +
				       probability(1,1,6) * ([reward(1,1,6) – 1] + VK(1,1,6))		



	
		All 8 Actions!}


                                    				### FINAL POLICY DICTIONARY ###
 ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # Final Iteration to create Policy Dictionary
         	We now need to compare the best action produced with the value of Holding. The Value Iteration (above) has given each state a Value which depends on 
		the discounted rewards we can expect from that State. 
		This is to be compared with the Value of sticking today. The State Action Value of Holding has a Closed Solution which is equal to R/(1-discount rate)

        values_iteration_dictionary = defaultdict(lambda: 0)
        for state in self.game.states:
            node_state = node_dictionary[state]
            rewards = node_state.call_reward_dictionary()
            probabilities = node_state.call_probability_dictionary()
            state_action_pair = node_state.state_action_pairs()
            penalty = node_state.penalty

            best_action_value = 0
            best_state_action = None
            for action in self.game.actions:
                possible_states = state_action_pair[action]
                if possible_states == 0:
                    break
                value_array = []
                for states in list(possible_states):
                    if states == None:
                        value_array.append(values_dictionary[state])
                    else:
                        value_array.append(values_dictionary[states])
                reward = np.array(rewards[action])
                probability = np.array(probabilities[action])

                value_state = np.dot(probability, ((reward - penalty) + (theta * np.array(value_array))))
                if value_state >= best_action_value:
                    best_action_value = value_state
                    best_state_action = action

            # Reward For Sticking/Holding
            reward_sticking = self.game.final_scores[state]
            value_sticking = reward_sticking / (1 - theta)
            if best_action_value >= value_sticking:
                values_iteration_dictionary[state] = best_state_action
            else:
                # Hold If It's Value Is Higher Than All Actions Computed Iteratively
                values_iteration_dictionary[state] = node_state.hold_action
        
	# Final Policy Dictionary For All States
        self.policy_dictionary = values_iteration_dictionary
        
        
    def play(self, state):
        """The Policy Dictionary Is Saved In The Previous Section Under "values_iteration_dictionary" """
    
        call_dictionary = self.policy_dictionary
        return call_dictionary[state]




* Much of the research was carried out using (Sutton, R.S. & Barto AG. Reinforcement Learning: An Introduction, MIT Press)







                                                           

