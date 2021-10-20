from time import time
import copy

from src.constant import ColorConstant, ShapeConstant
from src.model import State
from src.utility import is_out, is_win, place

from typing import Tuple, List


class LocalSearchGroup22:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        selected_state = None
        selected_state_value = 0
        for new_state in self.state_generator(state,(state.round - 1) % 2 ):
            new_value = self.state_evaluator(new_state[0], (state.round-1) % 2)
            if(selected_state is None):
                selected_state = new_state
                selected_state_value = new_value
            if( new_value >= selected_state_value):
                selected_state = new_state
                selected_state_value = new_value

        best_movement = (selected_state[1],selected_state[2])
        return best_movement


    def state_evaluator(self, state: State, n_player:int):
        '''
        [DESC]
        Fungsi untuk mengembalikan nilai angka dari suatu state
        
        [PARAMS]
        state --> State dari game
        n_player --> 0 untuk player 1 dan 1 untuk player 2

        [RETURN]
        integer nilai dari state

        [MEKANISME]
        mengecek 4 kotak (window) secara horizontal, vertikal maupun diagonal


        '''
        # pada kasus salah satu player menang
        win = is_win(state.board)
        if win:
            if win[0] == state.players[n_player].shape and win[1] == state.players[n_player].color:
                return 99999
            else:
                return -99999

        state_value = 0
       # pengecekan window secara horizontal
        window = []
        for i in range(state.board.row):
            for j in range(state.board.col -3):
                for k in range(4):
                    pos = (i, j+k)
                    window.append(pos)
                state_value += self.window_evaluator(state, window, n_player)
        
       # pengecekan window secara vertikal
        window.clear()
        for j in range(state.board.col):
            for i in range(state.board.row -3):
                for k in range(4):
                    pos = (i+k, j)
                    window.append(pos)
                state_value += self.window_evaluator(state, window, n_player)

       # pengekan window secara diagonal naik
        window.clear()
        for i in range(state.board.row -3):
            for j in range(state.board.col -3):
                for k in range(4):
                    pos = (i+k, j+k)
                    window.append(pos)
                state_value += self.window_evaluator(state, window, n_player)

       # pengekan window secara diagonal turun
        window.clear()
        for i in range(3,state.board.row):
            for j in range(state.board.col-3):
                for k in range(4):
                    pos = (i-k, j+k)
                    window.append(pos)
                state_value += self.window_evaluator(state, window, n_player)
            
        return state_value

    def window_evaluator(self, state: State, window: List[Tuple[int, int]], n_player:int):
        '''
        Fungsi yang mengembalikan nilai dari suatu window

        '''

        score = 0
        # menghitung shape, color dan empty di window
        count_empty = 0
        count_own_shape = 0
        count_own_color = 0
        count_enemy_shape = 0
        count_enemy_color = 0
        for pos in window:
            # empty
            if state.board.board[pos[0]][pos[1]].color == ColorConstant.BLACK:
                count_empty += 1
            else:
                # shape
                if state.board.board[pos[0]][pos[1]].shape == state.players[n_player].shape:
                    count_own_shape += 1
                else:
                    count_enemy_shape +=1
                # color
                if state.board.board[pos[0]][pos[1]].color == state.players[n_player].color:
                    count_own_color += 1
                else:
                    count_enemy_color +=1

        # berdasarkan shape
        if count_own_shape == 4:
            score += 150
        elif count_own_shape == 3 and count_empty == 1:
            score += 10
        elif count_own_shape == 2 and count_empty == 2:
            score += 5

        if count_enemy_shape == 3 and count_empty == 1:
            score -= 8
        
        # berdasarkan color
        if count_own_color == 4:
            score += 150
        elif count_own_color == 3 and count_empty == 1:
            score += 10
        elif count_own_color == 2 and count_empty == 2:
            score += 5

        if count_enemy_color == 3 and count_empty == 1:
            score -= 8

        return score


    def state_generator(self, state:State, n_player) -> List[Tuple[State, int, ShapeConstant]]:
        '''
        [DESC]
        Fungsi pembangkit
        membangkitkan semua kemungkinan langkah yang bisa diambil saat ini
        mereturn List dari tuple yang berisi State, int col, dan Shape Constant 
        dari movement dari state awal ke state baru
        ada 2 * number of column kemungkinan 

        [PARAMS]
        state   --> state dari game
        n_player--> 0 untuk player 1 dan 1 untuk player 2

        [RETURN]
        List of tuple yang bersisi state, int kolom yang dipilih, dan ShapeConstant yang dipilih
        '''
        

        neighbour = []
        for j in range(state.board.col):
            # untuk circle
            copy_state = copy.deepcopy(state)
            temp_state = place(copy_state, n_player, ShapeConstant.CIRCLE, j)
            if temp_state != -1:
                neighbour.append((copy_state, j, ShapeConstant.CIRCLE))

            # untuk cross
            copy_state = copy.deepcopy(state)
            temp_state = place(copy_state, n_player, ShapeConstant.CROSS, j)
            
            if temp_state != -1:
                neighbour.append((copy_state, j, ShapeConstant.CROSS))

        return neighbour


    
