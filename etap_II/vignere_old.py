import itertools
import enchant
import string
import re
import numpy as np


class vignere:
    def __init__(self, en_msg, key_len):
        self.en_msg = en_msg
        self.de_msg = ""

        self.key_len = key_len

        self.row_header  = np.array(list(string.ascii_uppercase))
        self.col_header = np.array([ str(s) for s in range(1, key_len+1)])

        self.table = np.empty((len(self.col_header), len(self.row_header)), dtype=self.col_header.dtype)
        self.table.fill("*")

        self.fully_linked = False

       # build table
    def display_table(self):
        displ_table = ""
        row_ = "***{}\n".format(" ".join(self.row_header))
        displ_table += row_
        row_ = "**{}\n".format("".join([str(num%10).rjust(2) for num in range(len(self.row_header))]))
        displ_table += row_

        row_ = "**%{}\n".format("-"*(len(row_)-3))
        displ_table += row_

        for i, row_num in enumerate(self.col_header):
            #row_ = "{}|{}\n".format(row_num.rjust(2), " ".join(self.table[i]))
            row_ = "{}|{}\n".format(str(i).rjust(2), " ".join(self.table[i]))
            displ_table += row_
        print(displ_table)

    def fill_table(self, de_str):
        de_parted = re.findall(".{" + "1,{}".format(self.key_len) + "}", de_str)
        en_msg_pos = 0
        for part_ in de_parted:
            for i, de_char in enumerate(part_):
                en_char = self.en_msg[en_msg_pos]
                self.table[i,self.row_header == de_char] = en_char

                en_msg_pos += 1
        self.sync_rows()

    def sync_rows(self):
        self.table_chars = [ [char for char in row if char != "*"] for row in self.table ]
        connections = [ [] for i in range(self.key_len) ]
        for irow in range(self.key_len):
            for jrow in range(irow+1, self.key_len):
                # check if connection irow  - jrow
                for char in self.table_chars[irow]:
                    if char in self.table_chars[jrow]:
                        connections[irow].append(jrow)
                        connections[jrow].append(irow)
                        break

        visited = []
        def build_complete(current_i, full_row):
            visited.append(current_i)
            current_row = self.table[current_i]

            # update full_row
            a = current_row[current_row != "*"]
            b = full_row[full_row != "*"]
            char_conn = a[np.argmax(np.in1d(a, b))]

            current_pos = np.argmax(current_row == char_conn)
            full_pos = np.argmax(full_row == char_conn)

            roll_ = current_pos - full_pos
            full_row = np.roll(full_row, roll_)

            full_row[current_row != "*"] = current_row[current_row != "*"]

            full_row = np.roll(full_row, -roll_)

            # go over pairs
            for to_visit in connections[current_i]:
                if to_visit in visited:
                    continue
                full_row = build_complete(to_visit, full_row)
            return full_row

        visited_update = []
        def visit_and_update(current_i, update_row):
            visited_update.append(current_i)
            current_row = self.table[current_i]
            a = current_row[current_row != "*"]
            b = update_row[update_row != "*"]
            char_conn = a[np.argmax(np.in1d(a, b))]

            current_pos = np.argmax(current_row == char_conn)
            update_pos = np.argmax(update_row == char_conn)
            roll_ = current_pos - update_pos

            self.table[current_i] = np.roll(update_row, roll_)


            for to_visit in connections[current_i]:
                if to_visit in visited_update:
                    continue
                visit_and_update(to_visit, update_row)

        # goo
        skip_cnt = 0
        for i in range(self.key_len):
            if i in visited:
                skip_cnt += 1
                continue

            filled_row = self.table[i].copy()
            filled_row = build_complete(i, filled_row)
            visit_and_update(i, filled_row)
        self.fully_linked = skip_cnt == self.key_len-1
        if self.fully_linked:
            print("Table is now fully linked!")

    def fill_alphabet(self):
        wrap_row = np.pad(self.table[0], (1,1), mode='wrap')
        string.ascii_uppercase

        ascii_pair_dic = dict(zip(string.ascii_uppercase, np.roll(list(string.ascii_uppercase), -2)))
        ascii_pair_dic["*"] = "-"
        ascii_char_dic = dict(zip(string.ascii_uppercase, np.roll(list(string.ascii_uppercase), -1)))

        for i in range(1, len(wrap_row)-1):
            char = wrap_row[i]
            if char != "*":
                continue
            if ascii_pair_dic[wrap_row[i-1]] != wrap_row[i+1]:
                continue
            self.table[0][i-1] = ascii_char_dic[wrap_row[i-1]]
        self.sync_rows()
    def get_missing_chars(self):
        return [ char for char in string.ascii_uppercase if char not in self.table[0] ]

        # find groups
    def dict_force(self, start, end, row=0):
        end += 1
        missing = self.get_missing_chars()

        dic = enchant.Dict("PL_pl")
        word = self.table[row][start:end].copy()
        mask = (word == "*")
        stars = int(np.sum(word == "*"))

        for perm in itertools.permutations(missing, stars):
            word[mask] = np.array(perm)
            word_str = "".join(word)
            if dic.check(word_str):
                print(word_str)

    def fill_solved(self):
        pass

vin = vignere("XQQBZPYNZXDBLYBXTAFJTRYGKCJOHIEHXGDYVBBIDCQOL", 6)
vin.fill_table("KRYPTOLOGIACZYLINAUKA")
#vin.fill_alphabet()
#vin.sync_rows()
#vin.display_table()

#vin.dict_force(12, 18)
