import csv
import pysat
import numpy as np
import minisat
import os

#taking input from csv file
file = open("./input5.csv")
inputs = csv.reader(file)
#input dimension of sudoku in p
p = int(input())  
sudoku1 = []
sudoku2 = []
for i in range(p*p):
    sudoku1.append(next(inputs))
for i in range(p*p):
    sudoku2.append(next(inputs))
file.close()

digits = range(0,p*p)

#1st sudoku 
grid1 = []

for i in digits:
    for j in digits:
        grid1.append(int(sudoku1[i][j]))

grid1 = np.reshape(grid1, (p*p,p*p))

#2nd sudoku 
grid2 = []

for i in digits:
    for j in digits:
        grid2.append(int(sudoku2[i][j]))

grid2 = np.reshape(grid2, (p*p,p*p))

#representing each possible value in a cell with unique number for sudoku1
def v1(i,j,d):
    return (pow(p,4))*i + p*p*j +d

#representing each possible value in a cell with unique number for sudoku2
def v2(i,j,d):
    return ((pow(p,4))*i + p*p*j +d+ ((pow(p,6)) + pow(p,4) + p*p))

def sudoku_clauses():
    res = []
    # for all cells, ensure that the each cell:
    for i in range(1, pow(p,2)+1):
        for j in range(1, pow(p,2)+1):
            # denotes (at least) one of the (p*p) digits 
            res.append([v1(i, j, d) for d in range(1, pow(p,2)+1)])
            res.append([v2(i, j, d) for d in range(1, pow(p,2)+1)])
            # does not denote two different digits at once 
            for d in range(1, pow(p,2)+1):
                for dp in range(d + 1, pow(p,2)+1):
                    res.append([-v1(i, j, d), -v1(i, j, dp)])
                    res.append([-v2(i, j, d), -v2(i, j, dp)])
            # denotes no two corresponding numbers are same in both the sudokus
            for d in range(1,pow(p,2)+1):
                res.append([-v1(i,j,d),-v2(i,j,d)])

    # ensures no two given cells have same values
    def valid(cells):
        for i, xi in enumerate(cells):
            for j, xj in enumerate(cells):
                if i < j:
                    for d in range(1, pow(p,2)+1):
                        res.append([-v1(xi[0], xi[1], d), -v1(xj[0], xj[1], d)])
                        res.append([-v2(xi[0], xi[1], d), -v2(xj[0], xj[1], d)])

    # ensure rows and columns have distinct values
    for i in range(1, pow(p,2)+1):
        valid([(i, j) for j in range(1, pow(p,2)+1)])
        valid([(j, i) for j in range(1, pow(p,2)+1)])

    #ensure p*p sub-grids "regions" have distinct values
    i=1
    j=1
    while(i<=pow(p,2)):
        while(j<=pow(p,2)):
            valid([(i + k % p, j + k // p) for k in range(p*p)])
            j=j+p
        i=i+p
    return res

# main sudoku-solver function
def solve(grid1,grid2):
    clauses = sudoku_clauses()

    for i in range(1, pow(p,2)+1):
        for j in range(1, pow(p,2)+1):
            d1 = grid1[i - 1][j - 1]
            d2 = grid2[i - 1][j - 1]
            # For each digit already known, a clause (with one literal)
            if d1!=0:
                clauses.append([v1(i, j, d1)])
            if d2!=0:
                clauses.append([v2(i, j, d2)])

    # solve the SAT problem
    with open('tmp.cnf', 'w') as f:
      f.write("p cnf {} {}\n".format(2*pow(p,6), len(clauses)))
      for c in clauses:
        c.append(0)
        f.write(" ".join(map(str,c)) + "\n")
    
    os.system("minisat tmp.cnf tmp.sat")

    with open("tmp.sat","r") as satfile:
      for line in satfile:
        if line.split()[0] == "UNSAT":
            print("no solution")
        elif line.split()[0]=="SAT":
            pass
        else:
            assignment = [int(x) for x in line.split()]
            
            # printing sudokus pair in the form of a matrix of dimension (p*p,p*p)
            with open("./output5.csv","w") as f:
                writer = csv.writer(f)

                for i in range(1,pow(p,2)+1):
                    c=[]
                    for j in range(1,pow(p,2)+1):
                        for k in range(1,pow(p,2)+1):
                            if v1(i,j,k) in assignment:
                                c.append(k)
                                break
                    writer.writerow(c)

                for i in range(1,pow(p,2)+1):
                    c=[]
                    for j in range(1,pow(p,2)+1):
                        for k in range(1,pow(p,2)+1):
                            if v2(i,j,k) in assignment:
                                c.append(k)
                                break
                    writer.writerow(c)

solve(grid1,grid2)