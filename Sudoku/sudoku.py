import numpy as np
import copy
import heapq


def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.
    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.
    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    class Sudoku_Node:
        def __init__(self, sudoku):
            self.state = np.asarray(sudoku, float)
            self.n = len(self.state)
            self.next = None
            self.head = None
            self.goal = False

        def isgoal(self, ndSudokugrid):
            unit_dict = {}
            unit_dict[0] = copy.deepcopy(ndSudokugrid[:3, :3])
            unit_dict[1] = copy.deepcopy(ndSudokugrid[:3, 3:6])
            unit_dict[2] = copy.deepcopy(ndSudokugrid[:3, 6:9])
            unit_dict[3] = copy.deepcopy(ndSudokugrid[3:6, :3])
            unit_dict[4] = copy.deepcopy(ndSudokugrid[3:6, 3:6])
            unit_dict[5] = copy.deepcopy(ndSudokugrid[3:6, 6:9])
            unit_dict[6] = copy.deepcopy(ndSudokugrid[6:9, :3])
            unit_dict[7] = copy.deepcopy(ndSudokugrid[6:9, 3:6])
            unit_dict[8] = copy.deepcopy(ndSudokugrid[6:9, 6:9])

            # Checks Units, Rows, and Then Columns and Returns Boolean False
            # Logic: Subtracting Two Sets Will Produce the Emppty Set. This Only Occurs When All of the
            # Value In the Domain [1-9] is Equal To All of the Values In The Row/Column/Unit, Which Should Have
            # Values [1-9] in Their Domain
            domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for i in range(9):
                if set(domain) - set(unit_dict[i].flatten()) != set():
                    return False
                elif set(domain) - set(ndSudokugrid[i]) != set():
                    return False
                elif set(domain) - set(ndSudokugrid[:, i]) != set():
                    return False
            self.goal = True
            return True

        def priority_var_array(self):
            """
                We want to chose the Variable (an empty cell in the Sudoku Grid) Which is:
                    i) Least Constrained (the smallest subset of the Domain the Variable Can Take
                The priority_variable_array function will return a priority queue with the grid position of the
                least constrained variable first
            """
            state_cpy = copy.deepcopy(self.state)
            # All of the possible Values A Cell Can Take
            initial_domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]

            least_constrained_list = []
            for i in range(self.n):
                for j in range(self.n):
                    if state_cpy[i][j] == 0:
                        row = copy.deepcopy(state_cpy[i])
                        column = copy.deepcopy(state_cpy[:, j])
                        # Domain Check the Unit 3x3 the element belongs to
                        unit = self.threebythree_domain_check(i, j)
                        unit = unit.flatten()

                        # Total contains all of the numbers in the element row, column and 3by3 Unit.
                        total = np.concatenate((row, column, unit))
                        # print(f"total {total}")

                        # The domain is worked out by the complement of everything in the initial domain set
                        # excluding the numbers in the element row, column and 3by3 Unit
                        domain = list(set(initial_domain) - set(total))
                        least_constrained_list.append((len(domain), domain, [i, j]))
                        # print(f"set difference is {domain}, with row {row} and collum {column}, and co-ordinate ({i},{j}), variable_list {least_constrained_list}")



            heapq.heapify(least_constrained_list)
            #print(least_constrained_list)
            # print(domain)

            if least_constrained_list == []:
                return False
            else:
                least_constrained_list = least_constrained_list.pop(0)
                print(least_constrained_list)

                coordinate = (least_constrained_list[2][0], least_constrained_list[2][1])
                domain = least_constrained_list[1]
                return domain, coordinate

        def threebythree_domain_check(self, i, j):
            #  ___________
            # | A | B | C |
            # | D | E | F |
            # | G | H | I |
            #  -----------

            # Square A
            global array
            if i <= 2 and j <= 2:
                array = self.state[:3, :3]
            # Square B
            if i <= 2 and j > 2 and j < 6:
                array = self.state[:3, 3:6]
            # Square C
            if i <= 2 and j > 5 and j < 9:
                array = self.state[:3, 6:9]
            # Square D
            if i > 2 and i < 6 and j <= 2:
                array = self.state[3:6, :3]
            # Square E
            if i > 2 and i < 6 and j > 2 and j < 6:
                array = self.state[3:6, 3:6]
            # Square F
            if i > 2 and i < 6 and j > 5 and j < 9:
                array = self.state[3:6, 6:9]
            # Square G
            if i >= 6 and i < 9 and j <= 3:
                array = self.state[6:9, :3]
            # Square H
            if i >= 6 and i < 9 and j > 2 and j < 6:
                array = self.state[6:9, 3:6]
            # Square I
            if i >= 6 and i < 9 and j > 5 and j < 9:
                array = self.state[6:9, 6:9]
            return array

    # include a goal checker in the function definition, so that it ends when the goal state is reached.
    def recursive_backtracking(sudoku):
        node = Sudoku_Node(sudoku)
        initial_state = node.state
        if node.isgoal(initial_state):
            # Return Solved Sudoku
            return initial_state

        if not node.priority_var_array():
            return

        l_constrained_domain, l_constrained_coord = node.priority_var_array()
        # If the returned domain array is empty, then there is an empty space on the Grid with no option between
        # 1-9 to insert
        if l_constrained_domain == []:
            #  We Back Track To The Previous Stack Level And Branch
            return

        for possible_value in l_constrained_domain:
            i = l_constrained_coord[0]
            j = l_constrained_coord[1]
            copy_sudoku = copy.deepcopy(initial_state)
            copy_sudoku[i][j] = float(possible_value)
            x = recursive_backtracking(copy_sudoku)

            if x is not None:
                return x

    solution = recursive_backtracking(sudoku)
    if solution is None:
        return np.full((9,9),float(-1))
    else:
        return solution


if __name__ == '__main__':
    sudoku = np.load("data/hard_puzzle.npy")
    sudoku1 = np.load("data/hard_puzzle.npy")
    # Load solutions for demonstration
    solutions = np.load("data/hard_solution.npy")

    # Print the first 9x9 sudoku...
    # print("First sudoku:")
    # print(sudoku[0], "\n")
    a = 11
    print(sudoku_solver(sudoku[a]))
    print()
    print(solutions[a])
