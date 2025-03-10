

def benchmark1():
    '''
        (1,1)<-4,6
        (3,2)<-6/9
        (3,8)<-6/9
        (8,2)<-4/6
        (8,8)<-4/6
        No other cell in column 2 and 8 can have 6
        (0,2)<-2,4
        (0,1)<-4,6,8
        (0,8)<-4,8
        Since (1,1),(0,1),(0,8) each shows possibility of 4 therefore if 4 is present in anyone of them then 4 cannot be present in (0,2)
        Consider if 4 is not present in any of the 3 then following should hold
        (1,1)<-6
        (0,8)<-8
        (0,1)<-6,8 This contradicts as (0,1) can neither have 6 or 8.
        Therefore any one of the above three has 4 in it.
        Therefore (0,2) dosent have 4.So it has 2
        (0,1)<-2 
        dump your findings here
    '''
    puzzle = [
        [9, 0, 0, 0, 5, 1, 7, 3, 0],
        [1, 0, 7, 3, 9, 8, 2, 0, 5],
        [5, 0, 0, 0, 7, 6, 0, 9, 1],
        [8, 1, 0, 7, 2, 4, 3, 5, 0],
        [2, 0, 0, 1, 6, 5, 0, 0, 7],
        [0, 7, 5, 9, 8, 3, 0, 1, 2],
        [0, 2, 1, 5, 3, 7, 0, 0, 0],
        [7, 5, 8, 6, 4, 9, 1, 2, 3],
        [3, 9, 0, 8, 1, 2, 5, 7, 0]
    ]

    cell = (0,2)

    value = 2

    return puzzle, cell, value


def benchmark2():
    '''
        (0,3)<-2/4
        (3,2)<-6/9
        (3,8)<-6/9
        (8,2)<-4/6
        (8,8)<-4/6
        No other cell in column 2 and 8 can have 6
        (0,2)<-2,4
        (0,8)<-4,8
        Since cell (0,3)/(0,2) one has 2 and other 4 Therefor no 2/4 in the entire row
        (0,8)<-8
        (0,1)<-6
        dump your findings here
    '''
    puzzle = [
        [9, 0, 0, 0, 5, 1, 7, 3, 0],
        [1, 0, 7, 3, 9, 8, 2, 0, 5],
        [5, 0, 0, 0, 7, 6, 0, 9, 1],
        [8, 1, 0, 7, 2, 4, 3, 5, 0],
        [2, 0, 0, 1, 6, 5, 0, 0, 7],
        [0, 7, 5, 9, 8, 3, 0, 1, 2],
        [0, 2, 1, 5, 3, 7, 0, 0, 0],
        [7, 5, 8, 6, 4, 9, 1, 2, 3],
        [3, 9, 0, 8, 1, 2, 5, 7, 0]
    ]

    cell = (0,1)

    value = 6

    return puzzle, cell, value
def benchmark3():

    '''
    (0,1)<-2,4,6,8
    (0,2)<-2,4
    (0,8)<-4,8
    (1,1)<-4,6
    (2,2)<-2,3,4
    (3,2)<-6/9
    (3,8)<-6/9
    (8,2)<-4/6
    (8,8)<-4/6
    2 cannot be there in (2,2). If present then 4 at (0,2) ,6 at (1,1),8 at (0,8) and we cannot have 2 at (0,1) as all other possibilties rolled out.
    4 cannot be present at (2,2). If present then 2 at(0,2),6 at (1,1), 8 at (0,1), 4 at (0,8). Now simultaneously 4 cannot be present both at (0,8) and (2,2)
    This is because 4 will be present at either of the two positions ->(3,2)/(8,8) or (3,8)/(8,2)
    therefore 3 at (2,2).


        dump your findings here
    '''
    puzzle = [
        [9, 0, 0, 0, 5, 1, 7, 3, 0],
        [1, 0, 7, 3, 9, 8, 2, 0, 5],
        [5, 0, 0, 0, 7, 6, 0, 9, 1],
        [8, 1, 0, 7, 2, 4, 3, 5, 0],
        [2, 0, 0, 1, 6, 5, 0, 0, 7],
        [0, 7, 5, 9, 8, 3, 0, 1, 2],
        [0, 2, 1, 5, 3, 7, 0, 0, 0],
        [7, 5, 8, 6, 4, 9, 1, 2, 3],
        [3, 9, 0, 8, 1, 2, 5, 7, 0]
    ]

    cell = (2,2)

    value = 3

    return puzzle, cell, value

def benchmark4():
    '''
    (3,2)<-6/9
    (3,8)<-6/9
    (8,2)<-4/6
    (8,8)<-4/6
    (5,6)<-4,6
    (2,6)<-4,8
    (0,8)<-4,8
    If 4 at (8,8) then 8 at (0,8),6 at (3,8),4 at (2,6). Then at (5,6) neither 4/6 can be there whoch contradicts.
    Therefore 6 at (8,8) and therefore 6 at (3,2)
        dump your findings here
    '''
    puzzle = [
        [9, 0, 0, 0, 5, 1, 7, 3, 0],
        [1, 0, 7, 3, 9, 8, 2, 0, 5],
        [5, 0, 0, 0, 7, 6, 0, 9, 1],
        [8, 1, 0, 7, 2, 4, 3, 5, 0],
        [2, 0, 0, 1, 6, 5, 0, 0, 7],
        [0, 7, 5, 9, 8, 3, 0, 1, 2],
        [0, 2, 1, 5, 3, 7, 0, 0, 0],
        [7, 5, 8, 6, 4, 9, 1, 2, 3],
        [3, 9, 0, 8, 1, 2, 5, 7, 0]
    ]

    cell = (3,2)

    value = 6

    return puzzle, cell, value

def benchmark5():
    '''
   (3,2)<-6/9
    (3,8)<-6/9
    (8,2)<-4/6
    (8,8)<-4/6
    (0,8)<-4/8
    (2,6)<-4,8
    (1,7)<-4/6
    (1,7) can have 6 only
   (0,2)<-2/4
   (0,3)<-2/4
   (0,8) cannot has 4 so (0,8)<-8
   (2,6)<-4
   (5,6)<-6
   (3,8)<-9
   (6,8)<-4
   (8,8)<-6
   (6,7)<-8
   (6,6)<-9
   dump your findings here
    '''
    puzzle = [
        [9, 0, 0, 0, 5, 1, 7, 3, 0],
        [1, 0, 7, 3, 9, 8, 2, 0, 5],
        [5, 0, 0, 0, 7, 6, 0, 9, 1],
        [8, 1, 0, 7, 2, 4, 3, 5, 0],
        [2, 0, 0, 1, 6, 5, 0, 0, 7],
        [0, 7, 5, 9, 8, 3, 0, 1, 2],
        [0, 2, 1, 5, 3, 7, 0, 0, 0],
        [7, 5, 8, 6, 4, 9, 1, 2, 3],
        [3, 9, 0, 8, 1, 2, 5, 7, 0]
    ]

    cell = (6,6)

    value = 9

    return puzzle, cell, value