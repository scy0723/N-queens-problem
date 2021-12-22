global N, method
global solved

#--------bfs-----------
def bfs_check(board):
    num = len(board)
    if num > 1:
        for i in range(num-1, 0, -1):
            for j in range(i-1, -1, -1):
                # column
                if board[i] == board[j]:
                    return False
                # diagonal
                if board[i] == board[j]+(i-j):
                    return False
                if board[i] == board[j]-(i-j):
                    return False
    return True

def bfs(board):
    global N, solved, method
    solved=0
    queue = []
    queue.append(board)

    while True:
        if(len(queue) >= 1):
            current = queue.pop(0)
        else:
            return []
        if len(current) != N:
            for j in range(N):
                lastpos = 0
                if(len(current) == 0):
                    lastpos = N + 10
                else:
                    lastpos = current[len(current)-1]
                if j < lastpos-1 or j > lastpos+1:
                    newBoard = current[:]
                    newBoard.append(j)
                    if bfs_check(newBoard):
                        queue.append(newBoard)
        else:
            solved=1
            queue.insert(0, current)
            fileName= str(N)+"_"+method+"_output.txt"
            file = open(fileName, "w")
            for i in current:
                file.write(str(i)+" ")
            break
        
    return queue

#------hill climbing------
import random

def HC_initial_state(N): # random
    new_board = []
    for i in range(N):
        new_board.append(random.randint(0, N-1))
    return new_board


def HC_count(node, n):
    attacking = 0
    # check attack (count)
    for i in range(n-1):
        for j in range(i+1, n):
            if node[i] == node[j] or node[i] == (node[j] + (j-i)) or \
                    node[i] == (node[j] + (i-j)):
                attacking += 1

    return attacking

def HC_change(board, n):
    queens = []
    for row in range(n):
        cur_pos = board[row]
        # place the queen (current row)
        for pos in range(n): 
            q = board[:]
            if pos != cur_pos: # skip original position
                q[row] = pos
                queens.append(q) # generated queens
    return queens


def hc(current, n):
    while True:
        E = [] 
        queens = []
        current_state = HC_count(current, n)
        queens = HC_change(current, n)
        count = 0
        for x in queens:
            E.append(HC_count(x, n))
            count = count + 1

        min_value = min(E)

        if current_state <= min_value:
            return current, current_state
        # assign the best case to the current node and go back
        else:
            best = [i for i, x in enumerate(E) if x == min_value]
            new = best[random.randrange(len(best))]
            current = queens[new]

#------Forward checking------

import numpy as np

def csp(grid, queen,n,N):
    if len(grid) == queen:
        if(n==N):
            fileName= str(n)+"_csp_output.txt"
            file = open(fileName, "w")
            for i in range(n):
                for j in range(n):
                    if (grid[i][j]==1):
                        file.write(str(j)+" ")
        return True
    rowsProposition = getRowsProposition(grid, queen)
    for row in rowsProposition:
        grid[row][queen] = 1
        domainWipeOut = False
        for variable in csp_change(grid, queen):
            if fc(grid, variable.row, variable.column):
                domainWipeOut = True
                break
        if not domainWipeOut:
             if csp(grid, queen + 1,n,N):
                 return True
        grid[row][queen] = 0

def csp_change(grid, queen):
    result = []
    for row in range(len(grid)):
        for col in range(queen+1, len(grid)):
            if grid[row][col] == 0 and is_correct(grid, row, col):
                result.append(Unassigned(row, col))
    return result

def fc(grid, row, queen):
    actual = getRowsProposition(grid, queen)
    tmp = list(actual)
    for i in actual:
        if not is_correct(grid, i, queen):
            tmp.remove(i)
    return len(tmp) == 0


def is_correct(grid, row, column):
    return rowb(grid,row) and  columnb(grid, column) and upb(grid, row ,column) and downb(grid, row, column)

def rowb(grid, row):
    for col in range(len(grid)):
        if grid[row][col] == 1:
            return False
    return True
def columnb(grid, column):
    for row in range(len(grid)):
        if grid[row][column] == 1:
            return False
    return True
def upb(grid, row, column):
    iterRow = row
    iterCol = column
    while iterCol >= 0 and iterRow >= 0:
        if grid[iterRow][iterCol] == 1:
            return False
        iterCol -= 1
        iterRow -= 1
    return True
def downb(grid, row, column):
    iterRow = row
    iterCol = column
    while iterCol >= 0 and iterRow < len(grid):
        if grid[iterRow][iterCol] == 1:
            return False
        iterRow += 1
        iterCol -= 1
    return True


def getRowsProposition(grid, queen):
    rows = []
    for row in range(len(grid)):
        if is_correct(grid, row, queen):
            rows.append(row)
    return rows


class Unassigned:

    def __init__(self, row, column):
        self.row = row
        self.column = column


def csp_grid(N):
    return np.array(np.zeros(shape = (N,N), dtype=int))

                
def main():
    global N, solved, method
    
    file = open("input.txt", "r")
    strings = file.readlines()

    
    for i in range (len(strings)):
        lines=strings[i].split(" " or "\n")
        N=int(lines[0])
        method=lines[1].strip()
        
        if(method=='bfs'):
            board = []
            final = bfs(board)
            if(solved==0):
                fileName= str(N)+"_"+method+"_output.txt"
                file = open(fileName, "w")
                file.write("no solution!")
                
        elif(method=='hc'):
            board = []
            restarts = 0
            max_restart=100
            fileName= str(N)+"_"+method+"_output.txt"
            file = open(fileName, "w")
            while True:
                board = HC_initial_state(N)
                solution, state = hc(board, N)
                if state == 0:
                    for i in solution:
                        file.write(str(i)+" ")
                    break
                else:
                    restarts += 1
                    if(restarts == max_restart):
                        file.write("no solution!")
                        break
                    
        elif(method=="csp"):
            for n in range(N+1):
                csp(csp_grid(n), 0,n,N)
            if (N==2 or N==3):
                fileName= str(N)+"_"+method+"_output.txt"
                file = open(fileName, "w")
                file.write("no solution!")
        i+=1

    file.close()


main()
