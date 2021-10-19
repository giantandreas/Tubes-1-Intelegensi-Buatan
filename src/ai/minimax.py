from os import stat
import random
from time import time
import copy

from src.constant import ColorConstant, ShapeConstant
from src.model import State
from src.utility import is_out, is_win, place

from typing import Tuple, List

############################################

class Node:
    # kelas untuk membangun tree dari minimax
    def __init__(self, value: int, state: State, movement: Tuple[int, ShapeConstant]):
        self.value = value
        self.state = state
        self.movement = movement
        self.children = []
        self.selected_child= None

    def add_child(self, state: State, movement: Tuple[int, ShapeConstant]):
        self.children.append(Node(None, state, movement))

############################################


class Minimax:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
            
        node = Node(0, state, None)
        best_move = self.minimax(node, 1, True, n_player)

        move = best_move.selected_child.movement

        print("Selected value= "+str(best_move.selected_child.value))

        best_movement= (move[0], move[1])

        return best_movement

    def minimax(self, node: Node, depth: int, max:bool, n_player:int) -> Node:
        '''
        Melakukan pembangunan node tree sekaligus menjalankan algoritma minimax
        alpha beta prunning masi belum di implementasikan

        merupakan fungsi rekursif dengan base depth=0 atau kondisi menang

        '''

        # Jika sudah mencapai batas kedalaman tree atau salah satu pemain menang
        if depth==0 or is_win(node.state.board):
            node.value = self.state_evaluator(node.state, n_player)
            return node
        
        if max:     # jika memaksimalkan
            maxEval = -9999
            neighbour = self.state_generator(node.state, n_player)

            for n in neighbour:
                move = (n[1], n[2])
                node.add_child(n[0], move)
            
            for child in node.children:
                eval = self.minimax(child, depth-1, False, n_player)
                if eval.value > maxEval:
                    maxEval = eval.value
                    node.selected_child = eval
            
            node.value = maxEval
            return node
        
        else:       # jika meminimalkan
            minEval = 9999
            neighbour = self.state_generator(node.state, abs(n_player-1))

            for n in neighbour:
                move = (n[1], n[2])
                node.add_child(n[0], move)
            
            for child in node.children:
                eval = self.minimax(child, depth-1, True, n_player)
                if eval.value < minEval:
                    minEval = eval.value
                    node.selected_child = eval
            
            node.value = minEval
            return node
        

    def state_evaluator(self, state: State, n_player:int):
        '''
        rencana state evalutaor
        kan punya kita shape nya circle warnanya merah

        evaluator = shape + color
        ## evaluasi by color
        setiap kolom adjacent 

        ## evaluasi by shape
        setiap kolom adjacent

        jika shape bukan circle ataupun warna merah, negatifin 

        jumlahin
        dapat

        ini code yang masih work untuk player 1 aja

        '''
        jumlah =0

        # pada kasus salah satu player menang
        print("##############################")
        win = is_win(state.board)
        if win:
            if win[0] == state.players[n_player].shape and win[1] == state.players[n_player].color:
                return 999
            else:
                return -999

        for i in range(state.board.row):
            for j in range(state.board.col):
                if (state.board.board[i][j].color == ColorConstant.BLACK):
                    next
                else:
                    # by shape
                    adj = self.get_adjacent(state, i, j)
                    if state.board.board[i][j].shape == state.players[n_player].shape:
                        print("shape sendiri")
                        for pos in adj:
                            if(state.board.board[pos[0]][pos[1]].shape == state.players[n_player].shape):
                                jumlah += 5
                            elif(state.board.board[pos[0]][pos[1]].shape == state.players[abs(n_player-1)].shape):
                                next
                            else:
                                jumlah += 1
                    else:
                        print("shape musuh")
                        for pos in adj:
                            if(state.board.board[pos[0]][pos[1]].shape == state.players[abs(n_player-1)].shape):
                                jumlah -= 5
                            elif(state.board.board[pos[0]][pos[1]].shape == state.players[n_player].shape):
                                next
                            else:
                                jumlah -= 1
                        
                    if (state.board.board[i][j].color == state.players[n_player].color):
                        print("color sendiri")
                        for pos in adj:
                            if(state.board.board[pos[0]][pos[1]].color == state.players[n_player].color):
                                jumlah += 5
                            elif(state.board.board[pos[0]][pos[1]].color == state.players[abs(n_player-1)].color):
                                next
                            else:
                                jumlah += 1

                    else:
                        print("color musuh")
                        for pos in adj:
                            if(state.board.board[pos[0]][pos[1]].color == state.players[abs(n_player-1)].color):
                                jumlah -= 5
                            elif(state.board.board[pos[0]][pos[1]].color == state.players[n_player].color):
                                next
                            else:
                                jumlah -= 1

        return jumlah

    def get_adjacent(self,state, x, y) -> List[List[int]]:
        adjacent = []

        # atas bawah dan sudut
        p = [x, y+1]
        if not is_out(state.board, p[0], p[1]):
            adjacent.append(p)

            p = [x-1, y+1]
            if not is_out(state.board, p[0], p[1]):
                adjacent.append(p)
            
            p = [x+1, y+1]
            if not is_out(state.board, p[0], p[1]):
                adjacent.append(p)
        
        p = [x, y-1]
        if not is_out(state.board, p[0], p[1]):
            adjacent.append(p)

            p = [x-1, y-1]
            if not is_out(state.board, p[0], p[1]):
                adjacent.append(p)
            
            p = [x+1, y-1]
            if not is_out(state.board, p[0], p[1]):
                adjacent.append(p)
        
        # kanan kiri
        p = [x+1, y]
        if not is_out(state.board, p[0], p[1]):
            adjacent.append(p)
        
        p = [x-1, y]
        if not is_out(state.board, p[0], p[1]):
            adjacent.append(p)

        return adjacent

    def state_generator(self, state:State, n_player) -> List[Tuple[State, int, ShapeConstant]]:
        # Fungsi pembangkit
        # membangkitkan semua kemungkinan langkah yang bisa diambil saat ini
        # mereturn List dari tuple yang berisi State, int col, dan Shape Constant dari movement
        # ada 2 * number of column kemungkinan 

        neighbour = []
        for j in range(state.board.col):
            # untuk circle
            copy_state = copy.deepcopy(state)
            temp_state = place(copy_state, n_player, ShapeConstant.CIRCLE, j)
            if temp_state:
                neighbour.append((copy_state, j, ShapeConstant.CIRCLE))

            # untuk cross
            copy_state = copy.deepcopy(state)
            temp_state = place(copy_state, n_player, ShapeConstant.CROSS, j)
            
            if temp_state != -1:
                neighbour.append((copy_state, j, ShapeConstant.CROSS))

        return neighbour







