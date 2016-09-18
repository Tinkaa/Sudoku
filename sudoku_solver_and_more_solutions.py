import random
import copy
import time
import math

#the global variables being used
filename=None
count_rec=0
size=None
more_sol=False

def sudoku_solver(line):
    """
    Creates a dictionary with the value for every place in the sudoku
    Moreover, it calls the functions find_possible_numbers and look
    Input:
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
    values_all,possibilities=find_possible_numbers(values_all)
    look(values_all, possibilities)
    
def more_solutions(values_all):
    """
    Checks whether there are several solutions for the given sudoku
    Input:
    values_all: dictionary of the value of every box. If a box is empty, it has value 0
    Return:
    several: a boolean indicating whether there are several solutions
    """
    global count_rec
    count_rec=0
    global size
    size=int(math.sqrt(len(values_all)))
    global count_sols
    count_sols=0
    global several
    several=False
    global more_sol
    more_sol=True
    values_all,possibilities=find_possible_numbers(values_all)
    look(values_all, possibilities,)
    return several
    
def find_possible_numbers(values_all):   
    """
    Sees if values of squares can be deduced by looking at the values of the neighbouring row,column and square.
    If this is the case, the new values will be inserted in values_all
    Input:
    values_all: dictionary of the value of every box. If a box is empty, it has value 0
    Returns:
    values_all: the adjusted version of the inserted values_all dictionary
    possibilties: a dictionary which indicates which values every empty box could have
    """
    possibilities=dict()
    for key, value in values_all.items():
        if value==0:
            possibilities[key]=list(range(1,size+1))
           
    for key, value in possibilities.items():
        num_check=[]
        hor,ver=divmod(key,size)
        num_check.extend(hor_row(key,ver))
        num_check.extend(ver_row(key,hor))
        num_check.extend(square(key,hor,ver))
    
        for x in num_check:
            #if the value of key x in the possible values of the current key, remove this value from the list of possibilities
            if values_all[x] in value:
                value.remove(values_all[x])
    
    to_del=[]
    for key, value in possibilities.items():
        #if there is only one possibility left, this is the value that the current key should have. So then set this possibilty as the value of the key and add the key to the list of keys to be deleted from the possibilities dictionary
        if len(value)==1:
            #print(key)
            values_all[key]=value[0]
            to_del.append(key)
    for x in to_del:
        possibilities.pop(x)
    #if there are keys that have to be deleted from the possibilties dictionary i.e. new numbers are found, execute the function again, as there is a change that there are now new keys of which the value can be found. 
    if len(to_del)!=0:
        values_all, possibilities=find_possible_numbers(values_all)  
    return values_all, possibilities
    
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

def look(values_all,possibilities):
    """
    This is actually the most important function. 
    It calls all the other functions at the correct point of time.
    Input:
    values_all: dictionary of the value of every box. If a box is empty, it has value 0
    possibilties: a dictionary which indicates which values every empty box could have
    """
    global count_rec
    count_rec+=1
    if len(possibilities.keys())==0:
        if contr(values_all,possibilities):
            return
        else:
            if more_sol:
                global count_sols
                count_sols+=1
                if count_sols>1:
                    global several
                    several=True
                return
            else:
                return write_sol(values_all)
   #if not more than 50 recursion depth
    if count_rec<20:

        #if there are still keys with possibilities (i.e. more than one possibility for a key) left, choose a random key which has possibilities left 
        key=random.choice(list(possibilities.keys()))
        #print(possibilities[key])
        hor,ver=divmod(key,size)
        #get the keys that are in the same square
        sq_neigh=square(key,hor,ver)
        sq_neigh.append(key)
        ch,values_all, possibilities=look_one(sq_neigh, values_all, possibilities)
        
        #if something has changed, start look again
        if ch:
            look(values_all, possibilities)
        #else do the same as before, but now check for the horizontal neighbours
        else:
            hor_neigh=hor_row(key,ver)
            hor_neigh.append(key)
            ch,values_all,possibilities=look_one(hor_neigh, values_all, possibilities)
            if ch:
                look(values_all,possibilities)
            #if still no change, check for the vertical neighbours
            else:
                ver_neigh=ver_row(key,hor)
                ver_neigh.append(key)
                ch, values_all, possibilities=look_one(ver_neigh, values_all, possibilities)
                look(values_all,possibilities)
    #if after more than 50 recursions no solution is found
    else:
        count_rec=0
        #choose the key with the leas possibilities
        val_sor=sorted(possibilities, key=lambda k: len(possibilities[k]))
        try_left=possibilities[val_sor[0]]
        key=val_sor[0]
        #try the possiblities for the chosen key and see if the sudoku now can be solved. 
        for i in random.sample(try_left, len(try_left)):
            values_all_new=copy.copy(values_all)
            values_all_new[key]=i
            values_all_new,possibilities=find_possible_numbers(values_all_new)
            look(values_all_new, possibilities)

def contr(values_all,possibilities):
    """
    Checks whether there are any contradictions in the (partly) filled in sudoku
    Input:
    values_all: dictionary of the value of every box. If a box is empty, it has value 0
    possibilties: a dictionary which indicates which values every empty box could have
    Return:
    A boolean which indicates whether there is a contradiction
    """
    
    #if there is a key that is still in the possibilities dict but doesnt have any possible values left, then there is a contradiction
    for pos in possibilities.values():
        if pos==[]:
            return True
    
    f=size
    #get a list with the first key of every horizontal row
    p=[x*f for x in range(0,size)]
    for i in p:
        #get all keys horizontal row
        hor,ver=divmod(i,size)
        hor_r=hor_row(i,ver)
        hor_r.append(i)
        val_li=[]
        for x in hor_r:
            #if the key already has a value, append it to the val_li list
            if values_all[x]!=0:
                val_li.append(values_all[x])
        #if a value appears more than once in the list, i.e. in the horizontal row, then there is a contradiction (return True)
        for t in range(1,size+1):
            if val_li.count(t)>1:
                return True
    #do the same for the horizontal rows
    for i in range(0,size):
        hor,ver=divmod(i,size)
        ver_r=ver_row(i,hor)
        ver_r.append(i)
        val_li=[]
        for x in ver_r:
            if values_all[x]!=0:
                val_li.append(values_all[x])
                for t in range(1,size+1):
                    if val_li.count(t)>1:
                        return True
    
    return False




def look_one(neighs, values_all, possibilities):
    """
    Checks if one of the keys has a possible value which all neighbours don't have as possible value
    Input: 
    neighs: a list of keys which are in the same row, column or square
    values_all: dictionary of the value of every box. If a box is empty, it has value 0
    possibilties: a dictionary which indicates which values every empty box could have
    Returns:
    change: boolean which indicates whether a change has been made in the values_all dict
    values_all: the possibly changed values_all dict
    possibilities: the possibly changed possibilities dict
    """
    change=False
    sq_all=dict()
    all_num=[]
    for key_sq in neighs:
        #if this key does not have a defined value yet, i.e. is in the possibilities dict
        if key_sq in possibilities.keys():
            #add the numbers that can be the value of this key to a new dict and a list (all_num)
            sq_all[key_sq]=possibilities[key_sq]
            all_num.extend(possibilities[key_sq])
    for i in range(1,size+1):
        #if a number only appears in all possibilities once
        if all_num.count(i)==1:
            change=True
            #change the value of this number in the values_all dict
            for key, value in sq_all.items():
                if i in value:
                    values_all[key]=i
                    possibilities.pop(key)
                    
                    values_all, possibilities=find_possible_numbers(values_all)
                    return change, values_all, possibilities
    return change, values_all, possibilities 


def write_sol(values_all):
    """
    Writes the found solution to the file.
    Input:
    values_all: dictionary of the value of every box. If a box is empty, it has value 0
    """
    x=0
    sol=open(filename[:-4]+'_sol.txt', 'a')
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
    filename='standard_4_create.txt' 
    f = open(filename, "r")
    sol=open(filename[:-4]+'_sol.txt', 'w')
    sol.close()
    numbs = f.read().split()
    sudoku_solver(numbs)

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
    print "the execution time was:", end - start