import os
import time
import psutil
import random


class BabyLizard:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def get_row(self):
        return self.row

    def get_column(self):
        return self.column

    def move(self):
        self.row += 1

    # Mengecek Apakah Statenya masi ada konflict
    def is_conflict(self, queen):
        if self.row == queen.get_row() or self.column == queen.get_column():
            return True
        elif abs(self.column - queen.get_column()) == abs(self.row - queen.get_row()):
            return True

        return False


class HillClimbingRandomRestart:
    def __init__(self, n):
        self.n = n
        self.status = False
        self.steps_climbed_after_last_restart = 0
        self.steps_climbed = 0
        self.heuristic = 0
        self.random_restarts = 0

    # Metod Membuat Board Baru
    def generate_board(self):
        start_board = []
        for i in range(self.n):
            start_board.append(BabyLizard(random.randint(0, self.n - 1), i))
        return start_board

    # Metod Mencari Heuristic Dari Suatu State
    def find_heuristic(self, state):
        heuristic = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i].is_conflict(state[j]):
                    heuristic += 1
        return heuristic

    # method to get the next board with lower heuristic
    def next_board(self, present_board):
        next_board = []
        tmp_board = []

        present_heuristic = self.find_heuristic(present_board)
        best_heuristic = present_heuristic

        temp_h = 0

        for i in range(self.n):
            # copy present board as best board and temp board
            next_board.append(
                BabyLizard(present_board[i].get_row(),
                           present_board[i].get_column())
            )
            tmp_board.append(next_board[i])

        # iterate each column
        for i in range(self.n):
            if i > 0:
                tmp_board[i - 1] = BabyLizard(
                    present_board[i - 1].get_row(), present_board[i -
                                                                  1].get_column()
                )

            tmp_board[i] = BabyLizard(0, tmp_board[i].get_column())

            # iterate each row
            for j in range(self.n):
                # get the heuristic
                temp_h = self.find_heuristic(tmp_board)
                # check if temp board better than best board
                if temp_h < best_heuristic:
                    best_heuristic = temp_h
                    # copy the temp board as best board
                    for k in range(self.n):
                        next_board[k] = BabyLizard(
                            tmp_board[k].get_row(), tmp_board[k].get_column()
                        )

                # move the queen
                if tmp_board[i].get_row() != self.n - 1:
                    tmp_board[i].move()

        # check whether the present bord and the best board found have same heuristic
        # then randomly generate new board and assign it to best board
        if best_heuristic == present_heuristic:
            next_board = self.generate_board()
            self.random_restarts += 1
            self.steps_climbed_after_last_restart = 0
            self.heuristic = self.find_heuristic(next_board)
        else:
            self.heuristic = best_heuristic

        self.steps_climbed += 1
        self.steps_climbed_after_last_restart += 1

        return next_board

    # method to print the current state
    def get_state(self, state):
        # creating temporary board from the present board
        # temp_board = np.zeros([self.n, self.n], dtype=int)
        temp_board = [[] for i in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                temp_board[i].append(0)
        # temp_board = temp_board.tolist()

        for i in range(self.n):
            # get the positions of queen from the present board and
            # set those positions as 1 in solution board
            temp_board[state[i].get_row()][state[i].get_column()] = 1

        return temp_board

    def solve(self):
        if self.n == 2 or self.n == 3:
            print(f"No Solution possible for {self.n} queens.")
            return

        # initialize present heuristic
        present_heuristic = 0
        # creating the initial board
        present_board = self.generate_board()
        # creating the initial heuristic
        present_heuristic = self.find_heuristic(present_board)
        # test if the present board is the solution board
        while present_heuristic != 0:
            # get the next board -> printState(presentBoard)
            present_board = self.next_board(present_board)
            present_heuristic = self.heuristic
        # return state from present board
        self.status = True
        return self.get_state(present_board)

    def print_solution_and_status(self):
        print(
            f"Solving {self.n} queen problem with random restart hill climbing")
        # initialize time and memory usage
        start = time.time()
        process = psutil.Process(os.getpid())
        # get the solution
        solution = self.solve()
        print()
        for i in range(self.n):
            for j in range(self.n):
                print(solution[i][j], end=" ")
            print()
        # print complexity
        print("\nStatus\t :", "Complete" if self.status else "Uncompleted")
        print(f"Memori\t : {process.memory_info().rss / 1024 ** 2} MB")
        print(f"Time\t : {time.time() - start} seconds")
        print(f"Total number of steps climbed\t : {self.steps_climbed}")
        print(f"Number of random restarts\t : {self.random_restarts}")
        print(
            f"Steps climbed after last restart : {self.steps_climbed_after_last_restart}"
        )
        # return solution
        return solution


# if __name__ == "__main__":
#     n_queen_hc = HillClimbingRandomRestart(
#         int(input("Masukkan jumlah queen : ")))
#     solution = n_queen_hc.print_solution_and_status()
