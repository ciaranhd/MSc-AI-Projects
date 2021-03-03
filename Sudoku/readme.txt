
------------------------------------------------------------------------------------------------------------------------

					Theoretical Outline And Methodology

------------------------------------------------------------------------------------------------------------------------


					Project Objective

Create an algorithm which takes an unfinished Sudoku Puzzle (as a Numpy Array), and returns either:
	
	1) Unsolvable: Return an array with all elements equal to -1
	2) Solvable: Return an array with solved solution state.

						*
					Nature of the Problem

Sudoku is an example of an NP Complete Problem with 81 grid squares within a 9 by 9 square. There are:
	
	"Variables" - Empty squares of the puzzle which require filling
	
	"Domain" - The “Values” for which a “Variable” can take. This can be any subset of 			        
	           {1,2,3,4,5,6,7,8,9}

The State Space for Sudoku is 9^(variables). The State Space increases exponentially as the number 
of empty grids in the puzzle increases. 
						*
					Choice of Search	

I have ruled out Breadth First Search, as this algorithm has a space complexity of O(b^d), therefore an 
enormous search space could prove problematic due to hardware constraints.

Depth First Search is the immediate candidate, as it performs significantly better with a linear space 
complexity of O(bm).

It is also important that the algorithm is “complete”, i.e. we may visit all possible states in the Search
Space, for it is this property which allows us to conclude that no solution exists once all possible states 
have been exhausted.
						*
				Reducing the State Space

Having chosen the search algorithm, the state space is still too vast to solve the puzzle in a 
reasonable time by Brute Force Strategy alone. I will include the following strategies to reduce the Search 
Space:
	1) Constraint Propagation
	2) Forward Checking
	3) Most Constrained Variable


------------------------------------------------------------------------------------------------------------------------

						Code
The remaining part is a more practical explanation of how the code is designed and it's structure.

------------------------------------------------------------------------------------------------------------------------


						
class Sudoku_Node:
						*
	
	def isgoal(self, ndSudokugrid):

		1) Checks whether the solution is reached. It is implemented by:
			i) Breaking the Sudoku Puzzle into 9, 3by3 “Units”. Each Unit is saved into a 			
 			   Dictionary Data type "unit_dict"

				    #  ___________
				    # | A | B | C |
				    # | D | E | F |
				    # | G | H | I |
				    #  -----------
			
		To check each Unit is valid we flatten each Unit into a 1 dimensional array, 			
		(converting it to a Set for efficiency), and subtracting it from the Starting Domain. 
		
		If all values from 1-9 are in the Unit, then subtracting the Set Values from the Set 		
		Domain should produce an Empty Set, illustrated below:

		set(domain) - set(unit_dict[i].flatten()) != set() ----> Return the Boolean False as it is 									
									/ not a solution

		(1,2,3,4,5,6,7,8,9) - (| A | B | C | D | E | F | G | H | I |) ----> Empty Set if Valid
			

		ii) Row Check: Identical to the above. Simply substract the Set of all values in the 		    
		    row, from the Domain Set which will produce the empty Set if valid

		ii) Column Check: Identical to the above. Simply substract the Set of all values in the 		    
		    column, from the Domain Set which will produce the empty Set if valid

						*
	def priority_var_array(self):
	
		Least_Constrained_List = []
		For each variables in the Sudoku Grid:
			
			row    <---  All filled Variables in it's row
			column <---  All filled Variables in its Column
			
			unit   <---  All filled Variables in the Unit it belongs to. 
				     The Class Method threebythree_domain_check(self, i, j) will return the Unit 
				     the Variable belongs to.
	
			
			(row + unit + column) --> contains all of the elements that the non empty 
			Variable we are inspecting CANNOT take. Producing it in Set form will 				
			remove duplicates

			Domain <--- Set(1,2,3,4,5,6,7,8,9) - Set(row + unit + column). This will 				
			produce the Domain of Values that the variable CAN take.

			Least_Constrained_List.append(Set([Size of Domain, Domain)) --- The Size 			
			of Domain Varaible will appear BEFORE the Domain in a Set, as it allows 			
			us to Order the List by Size of Domain.

		
		HEAPIFY

		When we have a list of all Variable Domains, we want to chose the one with the 		
		fewest Values as it’s Domain (Most Constrained Variable Heurestic).

		I have chosen to import heapq in order to sort the list.

		If Least_Constrained_List is empty ---> Then we know there is no possible solution, as we 
		have a Variable which is unfilled but cannot take a value.

		If the list is Not empty ---> Then we can simply use pop(0) to:
			RETURN the information which points to the least constrained Variable to explore.

							*

	def recursive_backtracking(sudoku):
		This is the heart of the program. It will:

			1) Check if the current sudoku is solved
				Return sudoku grid
			
			2) Calls the priority_var_array() method to retrieve the position of the Most 			     
			   Constrained Variable (mentioned above)

			3) If a the Most Constrained Variable is the empty set, then there is no 			     
			   solution on this pathway and we therefore:
				Return to the previous Stack call to try a different route

			4) Iterate through the "Values" in the Most Constrained Variable, recursively 			    
 			   calling the recursive_backtracking function with the updated states so that 			   
			   we keep diving deeper through the search tree (backtracking where appropriate)


							*
					Final Thoughts/Improvements

There are many other Heuristics such as Naked Doubles and Triples, Least Constrained Value, to name but a few. 
Upon implementing the latter I found that the performance improvements were negligible, if not detrimental
in places.

I reasoned that many of the puzzles in the Easy to Medium Searches where simply "straight through processing", 
i.e. the Most Constrained Variable (in most cases) was a Variable with one Value.

As such, the frequency with which guessing values was required (with the inevitable consequence of backtracking) 
was rarer. In that sense, increasing the complexity of the algorithm, with additional Heurestics, could prove 
detrimental to performance of the simple puzzles, especially if the implementation is not 100% effecient. 





		



			

				

		
	










	
			







