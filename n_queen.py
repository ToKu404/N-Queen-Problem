from algorithm.hc_rand_restart import HillClimbingRandomRestart
from algorithm.genetic_algorithm import GeneticAlgorithm
from algorithm.csp import CSPForwardChecking
from algorithm.backtracking import BacktrackingDFS
if __name__ == "__main__":
    print('------- N-QUEEN PROBLEM --------')
    print('\nSilahkan Pilih Algoritma : \n1.Hill Climbing Random Restart\n2.Genetic Algorithm\n3.CSP Forward Checking\n4.CSP Backtracking')
    i = 0
    while(i <= 0 or i > 4):
        i = int(input('Pilihan : '))
        if not (i > 0 and i < 5):
            print('Input Salah')
    n = 0
    while(n <= 3):
        n = int(input("Masukkan Jumlah Queen : "))
        if(n <= 3):
            print('Input Lizard harus > 3')
    if(i == 1):
        lizard_h = HillClimbingRandomRestart(n)
        lizard_h.print_solution_and_status()
    elif(i == 2):
        max_fitness = (n * (n - 1)) / 2
        population = [GeneticAlgorithm.random_chromosome(
            n) for _ in range(100)]
        generation = 1
        lizard_ga = GeneticAlgorithm(n, max_fitness, population, generation)
        lizard_ga.print_solution_and_status()
    elif(i == 3):
        board = [[] for i in range(n)]
        for i in range(n):
            for j in range(n):
                board[i].append(0)
        baby_lizard_csp = CSPForwardChecking(n)
        solution = baby_lizard_csp.print_solution_and_status(board)
    elif(i == 4):
        board = [[] for i in range(n)]
        for i in range(n):
            for j in range(n):
                board[i].append(0)
        n_queen_backtracking = BacktrackingDFS(n)
        solution = n_queen_backtracking.print_solution_and_status(board)
