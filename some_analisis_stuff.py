import numpy as np

import engine_connection as ec

class SomeAnalisisStuff(ec.Engine):
    def __init__(self, eng):
        self.eng = eng

    def moveDiffrence(self, start_pos, last_cp, move_count):
        bst_mov = ""
        # найти cp за лучший рекомендуемый следующий ход
        temp_because_yaneoura_besit = self.eng.cp_of_next_move(start_pos, depth=17)
        if temp_because_yaneoura_besit[1] == -111111111:
            bst_mov = temp_because_yaneoura_besit[0]
            mov_cp = self.eng.cp_of_current_move(start_pos, bst_mov, depth=17)[0]
        else:
            bst_mov,mov_cp = temp_because_yaneoura_besit
            mov_cp = int(min(abs(mov_cp), 10000)*np.sign(mov_cp))
        if move_count % 2 == 0:
            temp_sign = 1
        else:
            temp_sign = -1
        print(temp_sign, end=' ')
        if move_count != 1:
            ### разберись со знаками...
            print(mov_cp, last_cp, str(-temp_sign*(-last_cp - (np.sign(mov_cp)*temp_sign)*mov_cp)))
            mov_cp_diff = -temp_sign*(-last_cp - (np.sign(mov_cp)*temp_sign)*mov_cp)
        else:
            mov_cp_diff = mov_cp
            print('-', mov_cp ,last_cp, '-')
        return mov_cp, mov_cp_diff

    def ferreira(self):
        return 0

    def yamashita(self):
        return 0

    def moveClass(self):
        return 0