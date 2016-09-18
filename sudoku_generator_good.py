import random
import time
import math
#from sudoku_more_solutions_good import *
from sudoku_solver_and_more_solutions import *

filename=None
count_rec=0
size=None

def sudoku_generator(line):
    """
    Creates a dictionary with the value for every place in the sudoku
    Moreover, it calls the functions remove_cells, more_solutions and write_sol
    input:
    line=list of one unsolved sudoku
    """
    
    global count_rec
    count_rec=0
    values_all=dict()
    x=0
    for number in line:
        values_all[x]=int(number)
        x+=1
    global size
    size=int(math.sqrt(len(values_all)))
    values_all,cells_left=remove_cells(values_all)
    old_values=values_all.copy()
    several=more_solutions(values_all)
    write_sol(old_values)
    
def remove_cells(values_all, n=0):
    """
    Removes values of cells one by one until there are n filled cells left or no values can be removed anymore
    Input:
    values_all: dictionary of the value of every box. If a box is empty, it has value 0
    n: number of cells that should have a value (indicator for the difficulty of created sudoku)
    Returns:
    values_all: the adjusted version of the input values_all
    len(cells): the number of cells that have a value
    """
    
    def canbbea(values_all,cell,pos,value):
        """
        Checks if another cell now can get the value of the removed cell. If this is the case, this is not good since the sudoku becomes unsolvable or gets several solutions.
        Inputs:
        values_all: dictionary of the value of every box. If a box is empty, it has value 0
        cell: the cell that can possibly have the removed value
        pos: the position of the cell (ranges from 0 to size*size-1)
        value: the value of the removed cell
        Return:
        A boolean which indicates whether the value of the removed cell can be placed in the input cell
        """
        if values_all[pos] == value: 
            return True
        if values_all[pos] in range (1,size+1):             
            return False
        
        num_check=[]
        hor,ver=divmod(pos,size)
        num_check.extend(hor_row(pos,ver))
        num_check.extend(ver_row(pos,hor))
        num_check.extend(square(pos,hor,ver))
        num_check.remove(cell)
        for x in num_check:
            if values_all[x]==value:
                return False
        return True
    
    cells = set(range(size*size))
    cellsleft=cells.copy()
    while len(cells)>n and len(cellsleft):
        cell=random.choice(list(cellsleft))
        cellsleft.discard(cell)
        
        row = col = sq = False
        hor,ver=divmod(cell,size)
        in_row=hor_row(cell,ver)
        for x in in_row:
            if canbbea(values_all,cell,x,values_all[cell]): 
                row=True
        in_col=ver_row(cell,hor)
        for x in in_col:
            if canbbea(values_all,cell,x,values_all[cell]):
                col=True
        in_square=square(cell,hor,ver)
        for x in in_square:
            if canbbea(values_all,cell,x,values_all[cell]):
                sq=True       
        if row and col and sq:
            continue
        else:
            values_old=values_all.copy()
            values_all[cell]=0
            #several=more_solutions(values_all)
            values_all=values_old
            #if several:
             #   continue
            #else:
            values_all[cell]=0
            cells.discard(cell)
    return (values_all, len(cells))
    
def hor_row(key,ver):
    """
    returns the keys that are in the same horizontal row as the input key
    Input:
    key: the index of the square (ranging from 0 to size*size-1)
    ver: the column the square is in (ranging from 0 to size-1)
    Return:
    hor_neigh: a list of the keys that are in the same row as the input key
    """
    #gives horizontal keys left from current key
    hor_neigh=list(range(key-ver,key))
    #gives horizontal keys right from current key
    hor_neigh.extend(list(range(key+1, key+size-ver)))
    return hor_neigh
        
def ver_row(key,hor):
    """
    returns the keys that are in the same vertical row as the input key
    Input: 
    key: the index of the square (ranging from 0 to size*size-1)
    hor: the row the square is in (ranging from 0 to size-1)
    Return:
    ver_neigh: a list of the keys that are in the same column as the input key
    """
    ver_neigh=[]
    next_ver=key
    #gives the vertical keys (i.e. keys in the same vertical row) larger than the current key
    for i in range(hor+1,size):
        next_ver=next_ver+size
        ver_neigh.append(next_ver)
    next_ver=key
    #gives the vertical keys that are smaller than the current key
    for i in range(0,hor):
        next_ver=next_ver-size
        ver_neigh=[next_ver]+ver_neigh
        #ver_neigh.append(next_ver)
    return ver_neigh
    
def square(key,hor,ver):
    """
    returns the keys that are in the same square as the input key
    Input:
    key: the index of the square (ranging from 0 to size*size-1)
    hor: the row the square is in (ranging from 0 to size-1)
    ver: the column the square is in (ranging from 0 to size-1)
    Return:
    sq_neigh: a list of the keys that are in the same square as the input key
    """
    #get the horizontal and vertical position in the square (ranging from 0 to sqrt(size)) 
    size_sqrt=int(math.sqrt(size))       
    hor_sq=ver % size_sqrt
    ver_sq=hor % size_sqrt
    
    #exclude others square
    sq_neigh=[]
    #get horizontal neighbors in same row and left from key
    hor_neigh=list(range(key-hor_sq,key))
    #get horizontal neighbors in same row and right from key
    hor_neigh.extend(list(range(key+1,key+size_sqrt-hor_sq)))
        
    sq_neigh.extend(hor_neigh)
    hor_neigh.append(key)
    hor_neigh_ver=hor_neigh
    #vertical above key
    for i in range(key-ver_sq,key):
        #get the keys that are in the rows above the key but in the same square
        for x in hor_neigh:
            sq_neigh.append(x-size)
        #replace the hor_neigh by the keys just found of the row above. 
        hor_neigh=list(sq_neigh[-size_sqrt:])
        
    #vertical under key
    for i in range(key+1,key+size_sqrt-ver_sq):
        #get the keys that ar in the rows under the key but in the same square
        for x in hor_neigh_ver:
            sq_neigh.append(x+size)
        hor_neigh_ver=list(sq_neigh[-size_sqrt:])
    return sq_neigh

def write_sol(values_all):
    """
    Writes the found solution to the file.
    Input:
    values_all: dictionary of the value of every box. If a box is empty, it has value 0
    """
    x=0
    sol=open(filename[:-4]+'_create.txt', 'a')
    for value in values_all.values():
        sol.write(str(value))
        sol.write(' ')
        x+=1
        if x==size:
            sol.write('\n')
            x=0
    sol.write('\n')
    sol.close()

if __name__=='__main__':
    start = time.time()
    
#this depends on the format of the input. The uncommented now is for a file with one puzzle where the numbers are seperated by spaces and enters, the other one is for the 9x9 euler problemset
    global filename    
    filename='standard_4.txt' 
    f = open(filename, "r")
    sol=open(filename[:-4]+'_create.txt', 'w')
    sol.close()
    numbs = f.read().split()
    sudoku_generator(numbs)

#
#    filename='sudoku_euler.txt'
#    sol=open('sol_eul_3.txt', 'w')
#    eul=open('sol_eul_sum.txt', 'w')
#    eul.write('0')
#    eul.close()
#    sol.close()
#    with open(filename) as f:
#        for line in f:
#            if 'Grid' in line:
#                one_sudoku=(''.join(islice(f, 9))) 
#                sud_list=list(one_sudoku)
#                sud_list=[x for x in sud_list if x != '\n']
#                sud_list=''.join(sud_list)
#                #disp_sud.prt_grid(sud_list)
#                sudoku_solver(sud_list)



    end = time.time()
    print(end - start)