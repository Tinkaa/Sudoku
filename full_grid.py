import math
from collections import deque
import random

def standard_sudoku(size,filename):
    """
    Generates the simplest solved size x size sudoku.
    Writes this to a file and returns a list of length size*size, indicating the value of every square.
    Input:
    Size: the length and therefore also width of the sudoku
    Filename: the name of the file the shuffled sudoku should be written to. e.g. 'shuffled_sud.txt'
    Return: 
    sud_list: a list of length size*size indicating the value of every square
    """
    row=range(1,size+1)
    size_sqrt=int(math.sqrt(size))
    sol=open(filename, 'w')
    sud_list=[]
    l=0
    for i in xrange(size):
        for x in row:
            sol.write(str(x))
            sol.write(' ')
            sud_list.append(x)
        sol.write('\n')
        l+=1
        #rotate row to the left by sqrt(size) or sqrt(size)+1 if row of new square.
        row=deque(row)
        if l%size_sqrt==0:
            row.rotate(-size_sqrt-1)
        else:
            row.rotate(-size_sqrt)
    sol.close()
    return sud_list
    
def shuffle(sudoku,size,filename,rep):
    """
    Uses several operations to shuffle a solved sudoku. When finished, it calls the write_sudoku function.
    Inputs:
    Sudoku: a list with the values of a solved sudoku that has to be shuffled
    Size: the length and therefore also width of the sudoku
    Filename: the name of the file the shuffled sudoku should be written to. e.g. 'shuffled_sud.txt'
    Rep: the number of times a shuffle operation should be done
    """
    
    size_sqrt=int(math.sqrt(size))
    for n in range(rep):
        # 5 shuffle operations are implemented. Row: swap two rows who are in the same square, col: same as row but columns,
        #s_hor: swap two full horizontal blocks of squares. s_ver: same as s_hor but then vertical, num: swap all occurences of two numbers
        # see https://www.quora.com/How-are-Sudoku-puzzles-made for pictures
        c=random.choice(['row','col','s_hor','s_ver','num'])
        i=random.choice(range(size_sqrt))
        if c=='row':
            x=random.choice(range(size_sqrt))
            g=random.choice([t for t in xrange(size_sqrt) if t != x])
            f=(i*size_sqrt+x)*size
            s=(i*size_sqrt+g)*size
            for l in range(size):
                sudoku[f+l],sudoku[s+l]=sudoku[s+l],sudoku[f+l]
        if c=='col':
            x=random.choice(range(size_sqrt))
            g=random.choice([t for t in xrange(size_sqrt) if t != x])
            f=i*size_sqrt+x
            s=i*size_sqrt+g
            for l in range(0,size*size,size):
                sudoku[f+l],sudoku[s+l]=sudoku[s+l],sudoku[f+l]
        if c=='s_hor':
            x=random.choice([t for t in xrange(size_sqrt) if t != i])
            f=i*size_sqrt*size
            s=x*size_sqrt*size
            for l in range(size_sqrt*size):
                sudoku[f+l],sudoku[s+l]=sudoku[s+l],sudoku[f+l]
        if c=='s_ver':
            x=random.choice([t for t in xrange(size_sqrt) if t != i])
            f=i*size_sqrt
            s=x*size_sqrt   
            for k in range(size_sqrt):
                for l in range(0,size*size,size):
                    sudoku[f+l+k],sudoku[s+l+k]=sudoku[s+l+k],sudoku[f+l+k]
        if c=='num':
            i=random.choice(range(1,size+1))
            x=random.choice([t for t in xrange(1,size+1) if t != i])
            for idx, item in enumerate(sudoku):
                if item == i:
                    sudoku[idx] =x
                if item==x:
                    sudoku[idx]=i
        
    write_sol(sudoku,size,filename)

def write_sol(sudoku,size,filename):
    """
    Writes a list of values of the squares to a file. Where each number is seperated by a space and every row is seperated by an enter
    Input:
    Sudoku: a list with the value of every square
    Size: the length and therefore also width of the sudoku
    Filename: the name of the file the shuffled sudoku should be written to. e.g. 'shuffled_sud.txt'
    """
    sol=open(filename, 'w')
    x=0
    for i in sudoku:
        sol.write(str(i))
        sol.write(' ')
        x+=1
        if x==size:
            sol.write('\n')
            x=0
    sol.close()
    
    
    
if __name__ == "__main__":
    sud_list=standard_sudoku(4,'standard_4.txt')
    shuffle(sud_list,4,'standard_4.txt',100)
    