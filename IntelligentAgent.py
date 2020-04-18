import random
from BaseAI import BaseAI
import math
import numpy as np
import time
from numpy.random import choice

W = np.zeros((4,4))
W[0][0] = 6
W[0][1] = 5
W[0][2] = 4
W[0][3] = 3
W[1][0] = 5
W[1][1] = 4
W[1][2] = 3
W[1][3] = 2
W[2][0] = 4
W[2][1] = 3
W[2][2] = 2
W[2][3] = 1
W[3][0] = 3
W[3][1] = 2
W[3][2] = 1
W[3][3] = 0

class IntelligentAgent(BaseAI):
    def getMove(self, grid):
        moveset = grid.getAvailableMoves()
        maxUtility = -np.inf
        '''if len(moveset) == 4:
            moveset2 = []
            moveset2.append(moveset[0])
            moveset2.append(moveset[2])
            moveset2.append(moveset[1])
            moveset2.append(moveset[3])
        else:
            moveset2 = moveset'''
        for x in moveset:
            move = x[0]
            #print ("check0")
            clone_grid_move = grid.clone()
            clone_grid_move.move(x[0])
            (state, utility) = Decision(clone_grid_move)
            #print (utility)
            if utility > maxUtility:
                move_choice = move
                maxUtility = utility
        return move_choice

def Decision(state):
    a = -math.inf
    b = math.inf
    depth = 0 
    start_time = time.time()
    #print ('start', start_t)
    (child, utility) = Minimize(state, a, b, depth, start_time)
    return (child, utility)
    
def Maximize(state, a, b, depth, start_time):
    moveset = state.getAvailableMoves()
    depth = depth + 1
    #print (time.clock())
    if len(moveset) == 0 or depth == 3 or (time.clock() - start_time) > 0.05:
        #print("check1")
        return (None, Utility(state))
    #print ("check2")
    maxChild = None
    maxUtility = -math.inf
    for i in (moveset):
        (x, utility) = Minimize(i[1], a, b, depth, start_time)
        if utility > maxUtility:
            maxChild = i[0]
            maxUtility = utility
        if maxUtility >= b:
            break
        if maxUtility > a:
            a = maxUtility     
    return (maxChild, maxUtility)
        
def Minimize(state, a, b, depth, start_time):
    availablepos = state.getAvailableCells()
    depth = depth + 1
    if len(availablepos) == 0 or depth == 3 or (time.clock() - start_time) > 0.05:
        return (None, Utility(state))
    minChild = None
    minUtility = +math.inf
    children = []
    for pos in availablepos:
        clone2 = state.clone()
        clone4 = state.clone()
        clone2.insertTile(pos, 2)
        clone4.insertTile(pos, 4)
        children.append((clone2, clone4))
    for child in children:
        pick = choice([0,1], 1, p=[0.9, 0.1])
        choose = pick[0]
        (x, utility) = Maximize(child[choose], a, b, depth, start_time)
        if utility < minUtility:
            minChild = child
            minUtility = utility
        if minUtility <= a:
            break
        if minUtility < b:
            b = minUtility
    return (minChild, minUtility)

def Utility(state):
    score = 0  
    values = []
    count_zero = 0
    for i in range(0, 4):  
        for j in range(0, 4):
            val = state.getCellValue((i, j))
            if val != 0:
                score += W[i][j] * (val) 
                values.append(val)
            else:
                count_zero += 1
    max_tile = math.log2(state.getMaxTile())
    mean_empty_tile = math.log2(np.mean(values)) + count_zero
    values = np.sort(values)
    l = len(values)
    median_tile = math.log2(values[int(l/2)])
    (mono, smooth) = monotonicity(state)
    h_value = 5 * smooth + 0.8 * mono + 2 * score +  1 * max_tile + 1.2 * mean_empty_tile + 0.2 * median_tile
    return h_value

def monotonicity(state):
    x_mono_val = []
    smooth = []
    for i in range(0, 4):  
        val = 0
        same_val = 0
        for j in range(0, 3):
            cell_val = state.getCellValue((i,j))
            nex_cell_val = state.getCellValue((i,j+1))
            if nex_cell_val < cell_val:
                val += math.log2(cell_val - nex_cell_val)
            elif nex_cell_val > cell_val:
                val += -math.log2(nex_cell_val - cell_val)
            else:
                if nex_cell_val != 0 and cell_val != 0:
                    same_val = same_val + math.log2(nex_cell_val)*W[i][j]
        smooth.append(same_val)
        x_mono_val.append(val)
    y_mono_val = []
    for i in range(0, 4):  
        val = 0
        same_val = 0
        for j in range(0, 3):
            cell_val = state.getCellValue((j,i))
            nex_cell_val = state.getCellValue((j+1,i))
            if nex_cell_val < cell_val:
                val += math.log2(cell_val - nex_cell_val)
            elif nex_cell_val > cell_val:
                val += -math.log2(nex_cell_val - cell_val)
            else:
                if nex_cell_val != 0 and cell_val != 0:
                    same_val = same_val + math.log2(nex_cell_val)*W[i][j]
        smooth.append(same_val)
        y_mono_val.append(val)
    #print (smooth)
    return (np.sum(x_mono_val) + np.sum(y_mono_val), np.sum(smooth))    
        
    
    

    
    