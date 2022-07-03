import csv
from pysat.solvers import Solver
import numpy as np
import random
# import timeit

#taking input from user of 'k' as p to generate two sudokus of size (k*k)*(k*k)
p = int(input())

#start=timeit.default_timer()

#range of values which can be put in sudokus
digits = range(1,p*p+1)

#repsolenting each possible value at a place with unique number
#for 1st sudoku
def v(i,j,d):
    return (pow(p,4))*i + p*p*j +d
#for 2nd sudoku
def v2(i,j,d):
    return ((pow(p,4))*i + p*p*j +d+ ((pow(p,6)) + pow(p,4) + p*p))

def sudoku_clauses():
    
    #array storing the clauses
    res = []
    
    for i in digits:
        for j in digits:

            # for each place having at least one of the 9 digits
            res.append([v(i, j, d) for d in digits])
            res.append([v2(i, j, d) for d in digits])

            #for no two different digits at one place at same time
            for d in digits:
                for dp in range(d + 1, pow(p,2)+1):
                    res.append([-v(i, j, d), -v(i, j, dp)])
                    res.append([-v2(i, j, d), -v2(i, j, dp)])

            # for both sudokus not containg same valus at corresponding position
            for d in digits:
                res.append([-v(i,j,d),-v2(i,j,d)])


    def valid(cells):
        
        # ensures that the cells contain distinct values.
        for i, xi in enumerate(cells):
            for j, xj in enumerate(cells):
                if i < j:
                    for d in digits:
                        res.append([-v(xi[0], xi[1], d), -v(xj[0], xj[1], d)])
                        res.append([-v2(xi[0], xi[1], d), -v2(xj[0], xj[1], d)])

    # ensures rows and columns have distinct values
    for i in digits:
        valid([(i, j) for j in digits])
        valid([(j, i) for j in digits])

    # ensures pxp sub-grid have distinct values ranging in digits
    i=1
    j=1
    while(i<=pow(p,2)):
        while(j<=pow(p,2)):
            valid([(i + k % p, j + k // p) for k in range(p*p)])
            j=j+p
        i=i+p

    return res

global cl
cl = sudoku_clauses() #array containing all the basic sudoku-pair conditions

def puzzle():

    clauses = Solver()
    clauses.append_formula(cl)
    #print(clauses)

    clauses.solve()
    res = clauses.get_model() # array containing the integers representing the solution from sat solver

    inp=[]  #the values in sudokus which has to be checked for creating holes
    filled=[] #array with the values of each filled cell in sudokus after repeatidly creating holes as well as satisfying conditions

    #storing result in the arrays
    for i in res:
        if(i>=v(1,1,1)):
                inp.append(i)
                filled.append(i)

    clauses.delete()
    


    flag=1
    while(flag):
        
        #array initial sudoku clauses
        clauses1=sudoku_clauses()
        clauses2=sudoku_clauses()


        if(len(inp)!=0):
            a = int(random.choice(inp)) #randomly removing an element from sudokus
        else:
            flag=0 #if no more options left
            break
                
        #removing the value from the arrays
        inp.remove(a) 
        filled.remove(a)
        #print(len(filled))
            
                
        # adding clauses to have filled ones as initial conditions
        for c in filled:
            clauses1.append([c])
            clauses2.append([c])

        #sat soving the sudoku pairs with holes
        y=Solver()
        y.append_formula(clauses1)

        y.solve()
        re = y.get_model()

        
        #appending the list with negation of solution found
        new=[]
        for c in re:
            if(c not in filled):
                if (c>0) : 
                    new.append(-c)
        clauses2.append(new)

        # print(len(clauses1))
        # print(len(clauses2))

        #sat solving with conditon of not filling holes with exactly same value again (negation condition)
        z=Solver()
        z.append_formula(clauses2)
        #print(z.solve())

        
        if(z.solve()): 
            filled.append(a) #no unique solution i.e., not minimal case
        else:
            pass
        

        z.delete()
        y.delete()
        
    
    return filled

    
solution = puzzle() #the array with filled elements
#print(len(solution))

with open("assignment_1_200004_200483/sudoku_generator/output2.csv","w") as f:
    writer = csv.writer(f)

    for i in digits:
        c=[]
        for j in digits:
            x=0
            for k in digits:
                if(v(i,j,k) in solution):
                    c.append(str(k))
                    x=1
            if(x==0):
                c.append(str(0))    #if not filled then it is hole
        writer.writerow(c)

    for i in digits:
        c=[]
        for j in digits:
            x=0
            for k in digits:
                if(v2(i,j,k) in solution):
                    c.append(str(k))
                    x=1
            if(x==0):
                c.append(str(0))
        writer.writerow(c)

# end=timeit.default_timer()
# print(end-start)