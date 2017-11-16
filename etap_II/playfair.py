import numpy as np
import string
from itertools import product

class key:
    def __init__(self, chars, positions=None):
        if positions is None:
            string.ascii_uppercase
            alp = np.array([c for c in string.ascii_uppercase])
            alp = alp[np.logical_not(alp == "J")]

            keyword = []
            for char in chars:
                if char not in keyword:
                    keyword.append(char)
            keyword = np.array(keyword)

            diff = np.setdiff1d(alp, keyword)
            keyword = np.append(keyword, diff)
            self.chars = keyword
            b, a = np.meshgrid(np.arange(5), np.arange(5))
            self.positions = np.array([a.flatten(), b.flatten()]).T

        else:
            self.chars = np.array(chars)
            self.positions = np.array(positions)

    def display(self):
        print(self.get_matrix())

    def validate(self, keylen):
        shape = self.get_shape()
        if shape[0] != 5 and shape[1] != 5:
            return True

        alph = [ c for c in string.ascii_uppercase  if c != "J" ]
        alph_dic = dict(zip(alph, range(25)))

        for char, mpos in zip(self.chars, self.positions):
            pos = mpos[0]*5 + mpos[1]
            exp_pos = alph_dic[char]
            if not ( (pos < keylen) or (pos >= exp_pos and pos <= exp_pos+keylen) ):
                return False
        return True

    def fill(self, keylen):
        alph = [ c for c in string.ascii_uppercase  if c != "J" ]
        alph_dic = dict(zip(alph, range(25)))
        alph_rev_dic = dict(zip(range(25), alph))
        def get_possible_chars(start_char, end_char):

            char_list = []
            for i in range(alph_dic[start_char]+1, alph_dic[end_char]):
                char_list.append(alph_rev_dic(i))
            return char_list

        matrix = self.get_matrix()
        matrix_flat = matrix.flatten()

        key_chars = matrix_flat[:keylen]
        rest_chars = matrix_flat[keylen:]

        # find first non *
        li = 0
        # loop to end

        # add z if nessesery

    def get_level(self):
        alph = [ c for c in string.ascii_uppercase  if c != "J" ]
        """
        alph_dict = dict(zip(alph[:-1], alph[1:]))
        alph_dict["*"] = "-"
        alph_dict["Z"] = "-"
        """
        alph_dict = dict(zip(alph, range(25)))
        alph_dict["*"] = 100

        flat = self.get_matrix().flatten()
        level = 0

        # find first non * char
        start = 0
        while True:
            if flat[start] != "*":
                break
            start += 1
        prev_char = flat[start]

        for i in range(start+1, 25):
            cr_char = flat[i]
            if cr_char == "*":
                continue

            if  alph_dict[prev_char] < alph_dict[cr_char]:
                level += 1
                prev_char = cr_char

        """
            if flat[i+1] == alph_dict[flat[i]]:
                level += 1
        if flat[-1] == "Z":
            level += 1
        """
        return level

    def get_matrix(self):
        shape = self.get_shape()
        matrix = np.array([c for c in "*"*(shape[0]*shape[1])]).reshape(shape)
        for i in range(len(self.chars)):
            matrix[self.positions[i][0], self.positions[i][1]] = self.chars[i]
        return matrix

    def get_char_pos(self, char):
        return self.positions[self.chars == char][0]

    def get_shape(self):
        shape = (np.max(self.positions, axis=0))
        return (shape[0]+1, shape[1]+1)

    @staticmethod
    def get_possible(de_char, cr_char):
        de_char = [ c for c in de_char ]
        cr_char = [ c for c in cr_char ]
        print(de_char, cr_char)

        if de_char[0] in cr_char or de_char[1] in cr_char:
            if de_char[0] in cr_char:
                chars = [de_char[1], de_char[0], cr_char[0]]
            else:
                chars = [de_char[0], de_char[1], cr_char[1]]
            pos = np.array([[0,0], [0,1], [0,2]])
            pos_wrap = np.array([[0,3], [0,4], [0,0]])
            return [key(chars, pos), key(chars, pos[:,[1,0]]),
                    key(chars, pos_wrap), key(chars, pos_wrap[:,[1,0]])]


        key_list = []
        # 1. in line
        chars = np.array([de_char[0], cr_char[0], de_char[1], cr_char[1]])
        chars_inv = np.roll(chars, 2)
        # AaBb_
        pos = np.array([[0,0], [0,1], [0,2], [0,3]])
        key_list.append(key(chars, pos))
        key_list.append(key(chars_inv, pos))

        key_list.append(key(chars, pos[:,[1,0]]))
        key_list.append(key(chars_inv, pos[:,[1,0]]))

        # Aa_Bb
        pos = np.array([[0,0], [0,1], [0,3], [0,4]])
        key_list.append(key(chars, pos))
        key_list.append(key(chars_inv, pos))

        key_list.append(key(chars, pos[:,[1,0]]))
        key_list.append(key(chars_inv, pos[:,[1,0]]))

        # bAa_B
        pos = np.array([[0,1], [0,2], [0,4], [0,0]])
        key_list.append(key(chars, pos))
        key_list.append(key(chars_inv, pos))

        key_list.append(key(chars, pos[:,[1,0]]))
        key_list.append(key(chars_inv, pos[:,[1,0]]))

        # 2. diagonal
        for diag in product(range(1,5), range(1,5)):
            pos = [[0,0], [0, diag[1]], diag, [diag[0], 0]]
            key_list.append(key(chars, pos))
            key_list.append(key(chars_inv, pos))

            pos = [pos[1], pos[0], pos[3], pos[2]]
            key_list.append(key(chars, pos))
            key_list.append(key(chars_inv, pos))
        return key_list
    @staticmethod
    def merge_keys(key1, key2):
        common_chars = np.intersect1d(key1.chars, key2.chars)
        #key1.display()
        #key2.display()
        if common_chars.size == 0:
            return None

        # first common
        fcommon = common_chars[0]

        # key1 is fixed in place ...
        # how to move key2 to match key1
        #pos_diff = (key1.positions[key1.chars == fcommon]-key2.positions[key2.chars == fcommon])[0]
        pos_diff = key1.get_char_pos(fcommon) - key2.get_char_pos(fcommon)

        # check if common chars overlap
        for common_char in common_chars[1:]:
            k1_pos = key1.get_char_pos(common_char)
            k2_pos = key2.get_char_pos(common_char)
            if not np.array_equal(k1_pos, k2_pos+pos_diff):
                #print("NO OVERLAP ON COMMON")
                return None

        # cr implementation:: checking all position of other key (can skipp common)
        # check if uncommon(key1) overlap key2
        uncommon_k1 = np.setdiff1d(key1.chars, key2.chars) # check for overlap in key2
        #print("Checking uncommon of k1", uncommon_k1)
        for char in uncommon_k1:
            k1_pos = key1.get_char_pos(char)
            for k2_pos in key2.positions:
                if np.array_equal(k1_pos, k2_pos+pos_diff):
                    #print("OVERLAP - key1 key2")
                    return None

        # check if uncommon(key2) overlap key1
        uncommon_k2 = np.setdiff1d(key2.chars, key1.chars) # check for overlap in key1
        #print("Checking uncommon of k2", uncommon_k2)
        for char in uncommon_k2:
            k2_pos = key2.get_char_pos(char)
            for k1_pos in key1.positions:
                if np.array_equal(k1_pos, k2_pos+pos_diff):
                    #print("OVERLAP - key2 key1")
                    return None

        # SUCCESS, build new KEY
        # start with key1
        new_chars = [c for c in key1.chars]
        new_pos = [p for p in key1.positions]

        # add uncommon from key2
        for char in uncommon_k2:
            new_chars.append(char)
            new_pos.append(key2.get_char_pos(char)+pos_diff)

        # shift positions to start at 0 0
        new_pos = np.array(new_pos)
        new_pos = new_pos-np.min(new_pos, axis=0)

        k = key(new_chars, new_pos)
        if np.any(np.greater(k.get_shape(), (5,5))):
            return None
        return k

class playfair:
    # TO DO
    # add backup option
    # ! ! ! bug fix in drop durning attack ...
    # add key displaying method

    def __init__(self, cr_msg):
        self.cr_msg = cr_msg
        self.cr_msg_chars = [ char for char in self.cr_msg ]
        self.keys = None

    def drop_keys(self, keylen):
        valid_keys = []
        for k in self.keys:
            if k.validate(keylen):
                valid_keys.append(k)
        self.keys = valid_keys
    def fill_keys(self, keylen, key_id=None):
        if key_id==None:
            for k in self.keys:
                k.fill(keylen)
        else:
            self.keys[key_id].fill(keylen)

    def select_key(self, key_id):
        self.keys = [self.keys[key_id]]

    def attack(self, de_msg, cr_msg=None):
        de_msg_len = len(de_msg)
        de_msg_chars = [ char for char in de_msg ]

        de_msg_div = [ de_msg_chars[i*2:(i+1)*2 ] for i in range( int(de_msg_len*0.5))]

        if cr_msg is None:
            cr_msg = self.cr_msg[:de_msg_len]
        else:
            if len(cr_msg) != len(de_msg):
                print("cripted message is not equal decripted message!")
                return

        cr_msg_chars = [ char for char in cr_msg ]
        cr_msg_div = [ cr_msg_chars[i*2:(i+1)*2 ] for i in range( int(de_msg_len*0.5))]
        print("decripted:", de_msg_div)
        print("cripted  :", cr_msg_div)

        # initialize keys
        if self.keys is None:
            self.keys = key.get_possible(de_msg_div[0], cr_msg_div[0])
            """
            self.keys = []
            l1 =  key.get_possible(de_msg_div[0], cr_msg_div[0])
            l2 =  key.get_possible(de_msg_div[1], cr_msg_div[1])
            for k1, k2 in product(l1, l2):
                k = key.merge_keys(k1, k2)
                if k:
                    self.keys.append(k)
            """

        # go over all pairs in most sensible way
        to_attack = list(range(len(de_msg_div)))
        pair_chars = [ np.concatenate((de_msg_div[i], cr_msg_div[i])) for i in range(len(de_msg_div)) ]
        while to_attack != []:
            #self.display_keys()
            # if possible start with triplets
            # make common list
            key_chars = self.keys[0].chars
            # build new common
            common_list = [ np.intersect1d(key_chars, pair_chars[index]) for index in to_attack ]
            common_cnt = np.array([ len(common_list[i]) for i in range(len(to_attack)) ])

            triplet_list = np.array([ len(np.unique(pair_chars[index])) for index in to_attack ]) == 3
            have_common = common_cnt > 0
            #print(triplet_list)
            #print(have_common)

            if not any(have_common):
                print("Could not find any common in all list")

            triplet_list = np.logical_and(triplet_list, have_common)
            if any(triplet_list):
                print("Now lucky triplet!")
                local_index = np.argmax(triplet_list)
            else:
                local_index = np.argsort(common_cnt)[-1]
            common_index = to_attack[local_index]

            print("HAVE KEYS: {}".format(key_chars))
            print("ATTACKING ({}):{}  // commons:{}".format(common_index, pair_chars[common_index], common_list[local_index]))
            del to_attack[local_index]

            new_keys = []
            char_keys =  key.get_possible(de_msg_div[common_index], cr_msg_div[common_index])
            for k1, k2 in product(self.keys, char_keys):
                k = key.merge_keys(k1, k2)
                if k:
                    new_keys.append(k)
            self.keys = new_keys

            print("Keys: {}".format(len(self.keys)))

    def display_keys(self, sel=None):
        if sel is not None:
            print("Key:: {}".format(sel))
            self.keys[sel].display()
        else:
            for i in range(len(self.keys)):
                print("Key:: {}".format(i))
                self.keys[i].display()

    def decript(self, key_id=0, mode="div", r=False):
        key = self.keys[key_id]

        cr_msg_chars = [ char for char in self.cr_msg ]
        cr_msg_div = [ cr_msg_chars[i*2:(i+1)*2] for i in range(int(len(self.cr_msg)*0.5)) ]

        matrix = key.get_matrix()
        matrix_width = matrix.shape[1]
        de_msg_div = []

        for cr_pair in cr_msg_div:
            # 1 check is same row or column
            m_pos1 = matrix == cr_pair[0]
            abs_pos1 = np.argmax(m_pos1)
            pos1 = [np.floor_divide(abs_pos1, matrix_width), abs_pos1%matrix_width]

            m_pos2 = matrix == cr_pair[1]
            abs_pos2 = np.argmax(m_pos2)
            pos2 = [np.floor_divide(abs_pos2, matrix_width), abs_pos2%matrix_width]

            if np.sum(m_pos1) == 0 or np.sum(m_pos2) == 0:
                de_msg_div.append(["*", "*"])
                continue

            # same row
            if pos1[0] == pos2[0]:
                de_1 = matrix[pos1[0], pos1[1]-1]
                de_2 = matrix[pos2[0], pos2[1]-1]

            # same column
            elif pos1[1] == pos2[1]:
                de_1 = matrix[pos1[0]-1, pos1[1]]
                de_2 = matrix[pos2[0]-1, pos2[1]]

            else:
                de_1 = matrix[pos1[0], pos2[1]]
                de_2 = matrix[pos2[0], pos1[1]]

            de_msg_div.append([de_1, de_2])

        o_cr_msg = "".join(np.array(cr_msg_div).flatten())
        o_de_msg = "".join(np.array(de_msg_div).flatten())

        print("Key id: {}\n".format(key_id))

        if mode == "plain":
            print(o_de_msg)
            print(o_cr_msg)

        else:
            #devide into chunks
            chunks_num = np.floor_divide(len(o_cr_msg), 100) + 1
            cr_chunks = [ o_cr_msg[i*100:(i+1)*100] for i in range(chunks_num) ]
            de_chunks = [ o_de_msg[i*100:(i+1)*100] for i in range(chunks_num) ]

            for ichunk in range(chunks_num):
                cr_pairs = [ cr_chunks[ichunk][i*2:(i+1)*2] for i in range(50) ]
                de_pairs = [ de_chunks[ichunk][i*2:(i+1)*2] for i in range(50) ]

                header = str(ichunk*100).rjust(3)
                print(header)

                decimals = " "*14 + (" "*14).join([ str(s) for s in range(9)])
                print("   {}".format(decimals))

                single_ = " ".join([ str(a)+str(b) for a, b in zip(range(0,10,2), range(1,10,2))])
                single = " ".join([ single_ for i in range(10)])
                print("   {}".format(single))

                de_full = " ".join(de_pairs)
                print("   {}".format(de_full))

                cr_full = " ".join(cr_pairs)
                print("   {}".format(cr_full))

        if r:
            return o_de_msg

    def copy(self):
        copy = playfair(self.cr_msg)
        copy.keys = self.keys
        return copy


#msg = 'XELWAOHWUWYZMWIHOMNEOBTFWMIEIPIEANWLEOTOKNEBFCMFEXBLOLUCGRPIHBKYAOSBPMBNASCWOSYBSNVNKCELILUEUMLUHXBYBTNKALTBOEMPKEEIHBKGCWFVEKBA'
msg = "VXRCRUTOBIDNFMBXKNCLNCUCPTVHITMBOLALUFACCXITKAUAKZXKECODVIBLAVFRKWNDMBFWVABXNQDXCLMBTIMFMICNFRORDFLHKAADFDCNMBFWVUWLCMDNLCLVDNLAFTBTKZBRYIDALOOBVIDBVFMBFWBRKZOTUDELNDDRBTWKAXBNAPHUBLRNMBFWZPLOAGNCPAETALVHTHKWNCOFMBFMTMUBBPNCVTBLLAFHFOUKKMORWOROFHAFUBLZZVOBXKLTFUXHRBVHUBZPVHSICLMTHMORQWRY"

p = playfair(msg)
de_msg = "UWAGAXATAKNIEPRZYIACIELAMOZENA"
#de_msg = "ELEVENSURVIVORS"
p.attack(de_msg)


#p.attack("STOPDOSZTABUKORPUSUSTOSTOP", "TNNLRTTXQFIWGSILXNXNNQTNNL")

#"EWITHOUT"
#"OSYBSNVN"

