
import os
import time
import psutil


class BacktrackingDFS:
    def __init__(self, n):
        self.n = n
        self.status = False

    # is it possible to place a queen into (y,x)?
    def possible(self, board, y, x):

        # check for queens on row y
        for i in range(self.n):
            # if exist return false
            if board[y][i] == 1:
                return False

        # check for queens on column x
        for i in range(self.n):
            # if exists return false
            if board[i][x] == 1:
                return False

        # loop through all rows
        for i in range(self.n):
            # and columns
            for j in range(self.n):
                # if there is a queen
                if board[i][j] == 1:
                    # and if there is another on a diagonal
                    if abs(i - y) == abs(j - x):
                        # return false
                        return False

        # if every check clears, we can return true
        return True

    def solve(self, board):
        if self.n == 2 or self.n == 3:
            print(f"No Solution possible for {self.n} queens.")
            return

        # for every row
        for y in range(self.n):
            # for every column
            for x in range(self.n):
                # we can place if there is no queen in given position
                if board[y][x] == 0:
                    # if empty, check if we can place a queen
                    if self.possible(board, y, x):
                        # if we can, then place it
                        board[y][x] = 1
                        # pass board for recursive solution
                        self.solve(board)

                        # if we end up here, means we searched through all children branches
                        # if there are 8 queens
                        if sum(sum(a) for a in board) == self.n:
                            # we are successful so return
                            self.status = True
                            return board

                        # remove the previous placed queen
                        board[y][x] = 0

        # means we searched the space, we can return our result
        return board

    def print_solution_and_status(self, board):
        print(f"Solving {self.n} queen problem with backtracking")
        # initialize time and memory usage
        start = time.time()
        process = psutil.Process(os.getpid())
        # get the solution
        solution = self.solve(board.copy())
        # print the solution
        print()
        for i in range(self.n):
            for j in range(self.n):
                print(solution[i][j], end=" ")
            print()
        # print complexity
        print("\nStatus\t :", "Complete" if self.status else "Uncompleted")
        print(f"Memori\t : {process.memory_info().rss / 1024 ** 2} MB")
        print(f"Time\t : {time.time() - start} seconds")
        # return solution
        return solution


# #%%
# main
# if __name__ == "__main__":
#     n = int(input("Masukkan jumlah queen : "))
#     board = [[] for i in range(n)]
#     for i in range(n):
#         for j in range(n):
#             board[i].append(0)

#     n_queen_backtracking = BacktrackingDFS(n)
#     solution = n_queen_backtracking.print_solution_and_status(board)

    # plot(solution)
