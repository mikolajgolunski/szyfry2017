import numpy as np
import itertools

class jeff:
    def __init__(self, strips, cr_msg):
        self.strips = np.array([[char for char in arr] for arr in strips])
        self.strips_num = len(self.strips)
        self.ext_strips = np.tile(self.strips, 2)
        self.cripted_msg = cr_msg
    def display_htable(self, htable, header, rows, nnum):
        row_ = " {}".format("".join([ str(i).rjust(3) for i in range(len(rows)) ]))
        print(row_)
        row_ = "  {}".format(" ".join(header))
        print(row_)
        cnt = 0
        for table_row in htable:
            #row_ = "{}".format("".join([str(num).rjust(3) for num in table_row]))
            row_ = str(rows[cnt])
            row_ += "{}".format("".join([str(num).rjust(3) if num == nnum else "   " for num in table_row]))
            print(row_)
            cnt += 1

    def get_possible_order(self, expected_word):
        expected_word = expected_word[:self.strips_num]
        cripted_word = self.cripted_msg[:self.strips_num]
        #print(expected_word, cripted_word)

        #slide strips
        strips = self.ext_strips

        table_header = []
        table_rows = np.squeeze(self.ext_strips[:,0])
        table_pos = np.empty((self.strips_num, self.strips_num), dtype=int)
        for i, (expected_char, cripted_char) in enumerate(zip(expected_word, cripted_word)):
            table_header.append(expected_char+cripted_char)
            for j in range(self.strips_num):
                strip = strips[j]
                expected_pos = np.argmax(strip == expected_char)
                diff_pos = np.argmax(strip[expected_pos:] == cripted_char)
                table_pos[j][i] = diff_pos
        # check if connected
        connecting_nums = []
        for num in table_pos[0]:
            connected = np.all(np.any(table_pos == num, axis=0))
            if connected and (num not in connecting_nums):
                connecting_nums.append(num)


        if len(connecting_nums) == 0:
            #print("No connections, try diffrent expected string!")
            return [], 0
        elif len(connecting_nums) != 1:
            print("more than one connecting num, NEED UPDATE!!!")
            return
        gen_num  = connecting_nums[0]

        # check all possible diagonal
        #possible_in_row = np.sum(table_pos == gen_num, axis=1)
        possible_in_rows = []
        for i in range(len(table_pos)):
            possible_in_rows.append(np.where(table_pos[i] == gen_num)[0])
        possible_strip_order = []
        for possible_indexes in itertools.product(*possible_in_rows):
            if len(set(possible_indexes)) == self.strips_num:
                possible_strip_order.append(possible_indexes)
        #print(possible_strip_order)
        return possible_strip_order, gen_num

    def decript(self, strip_order, gen_num, cr_msg):
        self.strips_num

        de_msg = ""
        #ordered_strips = self.strips[list(strip_order)]
        ordered_strips = [None]*self.strips_num
        for ordered_i, unordered_i in zip(strip_order, range(self.strips_num)):
            ordered_strips[ordered_i] = self.strips[unordered_i]

        #print(ordered_strips)
        for i in range(len(cr_msg)):
            local_strip = i%self.strips_num
            strip = ordered_strips[local_strip]
            cr_char = cr_msg[i]
            cr_pos = np.argmax(strip == cr_char)
            de_char = np.roll(strip, gen_num-cr_pos)[0]
            de_msg += de_char

        #print("{} {}\n{}".format(strip_order, gen_num, de_msg))
        return(de_msg)

strips = [
    "ARINEJWSKBCDFGHLOPQTUVXYZM",
    "BDFGHLMNPQSTUVWXJERZYOCKIA",
    "CDFJMOPQTUVWXHENRYKZGALSIB",
    "DFGHJOPQRTUVWXMAKSYILNCEZB",
    "ERBCFHJKMPQSTUVXYZGWIDOLAN",
    "FGJKMQRSVWXYZANTOIPLUHBCDE",
    "GUSTAVEBRNDCFHIJKLMOPQWXYZ",
    "HJKMPQUVWXYZALSTIRDENOBCFG",
    "ILWYNKOXABCEFGHJMPQRSTUVZD",
    "JKMOPQSVWXYZALNTURIGBCDEFH"]

#del strips[1]
#del strips[5]
#print(strips)

from itertools import combinations
cripted_msg = "GSZVNYUQRHHHUYMDZFZRZOWUAAEIJHHYPVSZEQSWOQZWMDAGRUFYGVFKJCFRDHYMTKNGGNUMRRTTBNEHUMOFUFUXBAZFGUAAIFMRNXJCXJFUEUGVVQUNFRFGZOWGAWOQMQDKZFSZLXRTUNTWVTFBEYLYXMUFUGUINRXMQMBYBTPMOFTDBNEHYQJVKOLVKKWHHCJPVYXYLUPUPHUUESLYTXYEOMWPFVROYDUFKJGUFYKTYRFKDYHMTWOVFPEHAPFDWPFKWUNGXHXUAUXWFUZTPTYHMHUYMDZG"
#cripted_msg = cripted_msg[::-1]
#print(len(cripted_msg))
#cripted_msg = 'XPWVOPHUGLAIXLFIYSFOJALZOPNJRXBIAZQATKCJ'

#expected_msg = "AGENTREX"
#expected_msg = "AGENTMILL"
expected_msg = "UWAGAAGENCI"
expected_msg = "AGENTREX"
#expected_msg = "AFED"

expected_msg = "AGENTMILLER"
#expected_msg = "AGENTMILL"


for I in range(4, len(expected_msg)+1):
    print("")
    print("LEN:   {}".format(I))
    print("")
    for local_strips in combinations(range(10), I):
        lstrips = []
        for i in local_strips:
            lstrips.append(strips[i])

        je = jeff(lstrips, cripted_msg)
        possible_orders, gen_num = je.get_possible_order(expected_msg)
        if possible_orders == []:
            continue
        for strip_order in possible_orders:
            print(je.decript(strip_order, gen_num, cripted_msg))


#je.decript(cripted_msg, 6)
