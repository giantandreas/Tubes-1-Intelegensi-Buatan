'''
Ini buat nyimpan fungsi evaluator lama aja

    def state_evaluator(self, state: State, n_player:int):
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


'''