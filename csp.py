# N queen problem solver with CSP using forward checking
import os
import time
import psutil
import random


class Unassigned:
    def __init__(self, row, column):
        self.row = row
        self.column = column


class CSPForwardChecking:
    def __init__(self, n):
        self.n = n
        self.status = False

    def get_unassigned_from_constraint(self, board, queen):
        result = []

        for row in range(self.n):
            for col in range(queen + 1, self.n):
                if board[row][col] == 0 and self.is_correct(board, row, col):
                    result.append(Unassigned(row, col))

        return result

    def forward_check(self, board, row, queen):
        act_domain = self.get_rows_proposition(board, queen)
        tmp_domain = list(act_domain)

        for proposition_row in act_domain:
            if not self.is_correct(board, proposition_row, queen):
                tmp_domain.remove(proposition_row)

        return len(tmp_domain) == 0

    def is_correct(self, board, row, column):
        return (
            self.is_row_correct(board, row)
            and self.is_column_correct(board, column)
            and self.is_diagonal_correct(board, row, column)
        )

    def is_row_correct(self, board, row):
        for col in range(self.n):
            if board[row][col] == 1:
                return False

        return True

    def is_column_correct(self, board, column):
        for row in range(self.n):
            if board[row][column] == 1:
                return False

        return True

    def check_upper_diagonal(self, board, row, column):
        iter_row = row
        iter_col = column

        while iter_col >= 0 and iter_row >= 0:
            if board[iter_row][iter_col] == 1:
                return False

            iter_col -= 1
            iter_row -= 1

        return True

    def check_lower_diagonal(self, board, row, column):
        iter_row = row
        iter_col = column

        while iter_col >= 0 and iter_row < self.n:
            if board[iter_row][iter_col] == 1:
                return False

            iter_row += 1
            iter_col -= 1

        return True

    def is_diagonal_correct(self, board, row, column):
        return self.check_upper_diagonal(
            board, row, column
        ) and self.check_lower_diagonal(board, row, column)

    def get_rows_proposition(self, board, queen):
        rows = []

        for row in range(self.n):
            if self.is_correct(board, row, queen):
                rows.append(row)
        return rows

    def solve(self, board, queen):
        if self.n == queen:
            self.status = True
            return True

        if self.n == 2 or self.n == 3:
            print(f"No Solution possible for {self.n} queens.")
            return

        rows_proposition = self.get_rows_proposition(board, queen)

        for row in rows_proposition:
            board[row][queen] = 1
            domain_wipe_out = False

            for variable in self.get_unassigned_from_constraint(board, queen):
                if self.forward_check(board, variable.row, variable.column):
                    domain_wipe_out = True
                    break

            if not domain_wipe_out:
                print("bisa")
                if self.solve(board, queen + 1):
                    return True

            board[row][queen] = 0

    def print_solution_and_status(self, board):
        print(f"Solving {self.n} queen problem with CSP forward checking")
        # initialize time and memory usage
        start = time.time()
        process = psutil.Process(os.getpid())
        # get the solution
        solution = self.solve(board, 0)
        # print the solution
        # print(board)
        print()
        for i in range(self.n):
            for j in range(self.n):
                print(board[i][j], end=" ")
            print()
        # print complexity
        print("\nStatus\t :", "Complete" if self.status else "Uncompleted")
        print(f"Memori\t : {process.memory_info().rss / 1024 ** 2} MB")
        print(f"Time\t : {time.time() - start} seconds")
        # return board
        return board


# #%%
# if __name__ == "__main__":
#     n = int(input("Masukkan Jumlah Lizard : "))
#     board = [[] for i in range(n)]
#     for i in range(n):
#         for j in range(n):
#             board[i].append(0)

#     baby_lizard_csp = CSPForwardChecking(n)
#     solution = baby_lizard_csp.print_solution_and_status(board)
