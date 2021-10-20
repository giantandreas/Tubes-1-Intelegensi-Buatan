import random
from time import time
import copy

from src.constant import ShapeConstant
from src.model import State
from src.utility import place

from typing import Tuple, List


class LocalSearch:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        state_value_now = self.state_value(state)
        print("sebelum = " + str(state_value_now))
        selected_state = None
        selected_state_value = 0
        for new_state in self.state_generator(state,(state.round - 1) % 2 ):
            print("kolom = " + str(new_state[1]))
            print("shape = " + new_state[2])
            new_value = self.state_value(new_state[0])
            if( selected_state is None):
                selected_state = new_state
                selected_state_value = new_value
            if( new_value > selected_state_value):
                selected_state = new_state
                selected_state_value = new_value

        best_movement = (selected_state[1],selected_state[2])
        return best_movement

    def state_value(self, state: State):
        value_color = 0
        value_shape = 0
        for titik in (self.baris_titik_tertinggi(state)):    # titik : offset 0 itu kolom dan 1 itu baris
            if(titik[1] >= state.board.row):    # ketika di awal
                continue

            is_enemy_shape = state.board.board[titik[1]][titik[0]].shape == state.players[(state.round) % 2].shape 
            is_enemy_color = state.board.board[titik[1]][titik[0]].color == state.players[(state.round) % 2].color 
            if((not is_enemy_color) and (not is_enemy_shape)):
                continue
            else:              
                # untuk vertical
                if(is_enemy_shape):
                    print("masuk pertama shape")
                    value_shape -= 2
                if(is_enemy_color):
                    print("masuk pertama color")
                    value_color -=1
                for j in range(state.board.row-titik[1]-1):
                    is_enemy_color = is_enemy_color and state.board.board[ titik[1] + j + 1 ][titik[0]].color == state.players[(state.round) % 2].color
                    is_enemy_shape = is_enemy_shape and state.board.board[ titik[1] + j + 1 ][titik[0]].shape == state.players[(state.round) % 2].shape

                    if(is_enemy_color):
                        print("masuk sini color vertical")
                        value_color -= 1
                    if(is_enemy_shape):
                        print("masuk sini shape vertical")
                        value_shape -= 2
                    if((not is_enemy_color) and (not is_enemy_shape)):
                        break

                # untuk horizontal
                kesamaan_warna_ditemukan = False
                kesamaan_bentuk_ditemukan = False
                titik_mulai_shape = None
                titik_akhir_shape = None
                titik_mulai_color = None
                titik_akhir_color = None
                color_value_temp = 0
                shape_value_temp = 0
                color_done = False
                shape_done = False
                for j in range (state.board.col):
                    if(j == titik[1]):
                        continue

                    if(state.board.board[titik[1]][j].shape == state.players[(state.round) % 2].shape and not kesamaan_bentuk_ditemukan):
                        kesamaan_bentuk_ditemukan = True
                        titik_mulai_shape = j
                    if(state.board.board[titik[1]][j].shape != state.players[(state.round) % 2].shape and kesamaan_bentuk_ditemukan):
                        kesamaan_bentuk_ditemukan = False
                        titik_akhir_shape = j
                        if(titik[0] in range(titik_mulai_shape,titik_akhir_shape+1,1)):
                            print("masuk sini shape horizontal")
                            print("nilainya = " + str(shape_value_temp))
                            value_shape += shape_value_temp
                            shape_done = True
                    if(state.board.board[titik[1]][j].color == state.players[(state.round) % 2].color and not kesamaan_warna_ditemukan):
                        kesamaan_warna_ditemukan = True
                        titik_mulai_color = j
                    if(state.board.board[titik[1]][j].color != state.players[(state.round) % 2].color and kesamaan_warna_ditemukan):
                        kesamaan_warna_ditemukan = False
                        titik_akhir_color = j
                        if(titik[0] in range(titik_mulai_color,titik_akhir_color+1,1)):
                            print("masuk sini color horizontal")
                            print("nilainya = " + str(color_value_temp))
                            value_color += color_value_temp
                            color_done = True
                    
                    if(shape_done and color_done):
                        break
                    
                    if(kesamaan_bentuk_ditemukan):
                        
                        shape_value_temp -= 2
                    if(kesamaan_warna_ditemukan):
                        color_value_temp -=1
                    
                # untuk diagonal 1
                kesamaan_warna_ditemukan = False
                kesamaan_bentuk_ditemukan = False
                titik_mulai_shape = None
                titik_akhir_shape = None
                titik_mulai_color = None
                titik_akhir_color = None
                color_value_temp = 0
                shape_value_temp = 0
                color_done = False
                shape_done = False
                for titik_diagonal in self.diagonal_1(state.board.row,state.board.col,titik):
                    if(titik_diagonal[1] == titik[1] and titik_diagonal[0] == titik[0]):
                        continue
                    print("titik diagonal 1: kol " + str(titik_diagonal[1]) + " row " + str(titik_diagonal[0]))
                    if(state.board.board[titik_diagonal[1]][titik_diagonal[0]].shape == state.players[(state.round) % 2].shape and not kesamaan_bentuk_ditemukan):
                        kesamaan_bentuk_ditemukan = True
                        titik_mulai_shape = titik_diagonal
                    if(state.board.board[titik_diagonal[1]][titik_diagonal[0]].shape != state.players[(state.round) % 2].shape and kesamaan_bentuk_ditemukan):
                        kesamaan_bentuk_ditemukan = False
                        titik_akhir_shape = titik_diagonal
                        if(titik[1] >= titik_mulai_shape[1] and titik[0] <= titik_akhir_shape[0]):
                            print("masuk sini shape diagonal 1")
                            print("nilainya = " + str(shape_value_temp))

                            value_shape += shape_value_temp
                            shape_done = True
                    if(state.board.board[titik_diagonal[1]][titik_diagonal[0]].color == state.players[(state.round) % 2].color and not kesamaan_warna_ditemukan):
                        kesamaan_warna_ditemukan = True
                        titik_mulai_color = titik_diagonal
                    if(state.board.board[titik_diagonal[1]][titik_diagonal[0]].color != state.players[(state.round) % 2].color and kesamaan_warna_ditemukan):
                        kesamaan_warna_ditemukan = False
                        titik_akhir_color = titik_diagonal
                        if(titik[1] >= titik_mulai_color[1] and titik[0] <= titik_akhir_color[0]):
                            print("masuk sini color diagonal 1")
                            print("nilainya = " + str(color_value_temp))

                            value_color += color_value_temp
                            color_done = True
                    
                    if(shape_done and color_done):
                        break

                    if(kesamaan_bentuk_ditemukan):
                        shape_value_temp -= 2
                    if(kesamaan_warna_ditemukan):
                        color_value_temp -=1

                # untuk diagonal 2
                kesamaan_warna_ditemukan = False
                kesamaan_bentuk_ditemukan = False
                titik_mulai_shape = None
                titik_akhir_shape = None
                titik_mulai_color = None
                titik_akhir_color = None
                color_value_temp = 0
                shape_value_temp = 0
                color_done = False
                shape_done = False
                for titik_diagonal in self.diagonal_2(state.board.row,state.board.col,titik): # disini ada masalah, shape lawan bakal di buat jadinya
                    if(titik_diagonal[1] == titik[1] and titik_diagonal[0] == titik[0]):
                        continue
                    print("titik diagonal 2: kol " + str(titik_diagonal[1]) + " row " + str(titik_diagonal[0]))
                    if(state.board.board[titik_diagonal[1]][titik_diagonal[0]].shape == state.players[(state.round) % 2].shape and not kesamaan_bentuk_ditemukan and not shape_done):
                        kesamaan_bentuk_ditemukan = True
                        titik_mulai_shape = titik_diagonal
                    if(state.board.board[titik_diagonal[1]][titik_diagonal[0]].shape != state.players[(state.round) % 2].shape and kesamaan_bentuk_ditemukan):
                        kesamaan_bentuk_ditemukan = False
                        titik_akhir_shape = titik_diagonal
                        is_in_column_range = titik[1] in range(titik_mulai_shape[1],titik_akhir_shape[1]+1,1) or titik[1] in range(titik_akhir_shape[1],titik_mulai_shape[1]-1,-1)
                        is_in_row_range = titik[0] in range(titik_mulai_shape[0],titik_akhir_shape[0]+1,1) or titik[0] in range(titik_akhir_shape[0],titik_mulai_shape[0]-1,-1)
                        if(is_in_column_range and is_in_row_range):
                            print("masuk sini shape diagonal 2")
                            print("nilainya = " + str(shape_value_temp))
                            value_shape += shape_value_temp
                            shape_done = True
                    if(state.board.board[titik_diagonal[1]][titik_diagonal[0]].color == state.players[(state.round) % 2].color and not kesamaan_warna_ditemukan and not color_done):
                        kesamaan_warna_ditemukan = True
                        titik_mulai_color = titik_diagonal
                    if(state.board.board[titik_diagonal[1]][titik_diagonal[0]].color != state.players[(state.round) % 2].color and kesamaan_warna_ditemukan):
                        kesamaan_warna_ditemukan = False
                        titik_akhir_color = titik_diagonal
                        is_in_column_range = titik[1] in range(titik_mulai_color[1],titik_akhir_color[1]+1,1) or titik[1] in range(titik_akhir_color[1],titik_mulai_color[1]-1,-1)
                        is_in_row_range = titik[0] in range(titik_mulai_color[0],titik_akhir_color[0]+1,1) or titik[0] in range(titik_akhir_color[0],titik_mulai_color[0]-1,-1)
                        if(is_in_column_range and is_in_row_range):
                            print("masuk sini color diagonal 2")
                            print("nilainya = " + str(color_value_temp))
                            value_color += color_value_temp
                            color_done = True
                    
                    if(shape_done and color_done):
                        break

                    if(kesamaan_bentuk_ditemukan):
                        shape_value_temp -= 2
                    if(kesamaan_warna_ditemukan):
                        color_value_temp -=1
        nilai = value_color + value_shape
        print("sesudah = " + str(nilai))
        return value_color + value_shape

    def baris_titik_tertinggi(self, state: State) -> List[Tuple[int,int]]:
        result = []
        for i in range(state.board.col):
            baris = 0
            for j in range(state.board.row):
                if(state.board.board[j][i].shape != "-" and state.board.board[j][i].color != "BLACK"):
                    break
                baris = j  #perlu dipastikan baris ga balik nilai ke 0
            result.append([i,baris+1]) #i kolom dan j baris
        return result
            
    def diagonal_1(self, row: int, column: int, position: Tuple[int,int]) -> List[Tuple[int,int]]:
        # j baris, i kolom | offset 0 baris, 1 kolom
        result = []
        if(position[0] > position[1]):
            i = position[0] - position[1] # kolom
            j = 0 # baris
            while( i < column and j < row):
                result.append([i,j])
                i+=1
                j+=1
        else :
            i = 0
            j = position[1] - position[0] 
            while( i < column and j < row):
                result.append([i,j])
                i+=1
                j+=1
        return result

    def diagonal_2(self,row: int, column: int, position: Tuple[int,int]) -> List[Tuple[int,int]]:
        result = []
        if(position[0] < row-position[1]-1):
            i = 0
            j = position[1] + position[0]
            while(i < column and j >= 0):
                if(i >= 0 and j < row):
                    result.append([i,j])
                i+=1
                j-=1
        else :
            j = 0
            i = position[0] + position[1]
            while(i >= 0 and j < row):
                if(i <column and j >= 0):
                    result.append([i,j])
                i-=1
                j+=1
        return result


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
            if temp_state != -1:
                neighbour.append((copy_state, j, ShapeConstant.CIRCLE))

            # untuk cross
            copy_state = copy.deepcopy(state)
            temp_state = place(copy_state, n_player, ShapeConstant.CROSS, j)
            
            if temp_state != -1:
                neighbour.append((copy_state, j, ShapeConstant.CROSS))

        return neighbour

    
