import numpy as np
import string

#alph_dic = dict(zip([c for c in string.ascii_uppercase], range(len(string.ascii_uppercase))))

class template:
    def __init__(self, password, size=3):
        self.size = size
        self.password = password
        self.template_size = np.power(size*2, 2)
        self.quoter_size = np.power(size,2)

        password_chars = []
        for char in password:
            if char not in password_chars:
                password_chars.append(char)

        if len(password_chars) != size*size:
            print("BAD PASSWORD SIZE !")
            return None

        self.password_chars = password_chars
        password_sorted = sorted(password_chars)

        sorting_dict = dict(zip(password_sorted, range(len(password_sorted))))
        self.password_pos = [ sorting_dict[c] for c in self.password_chars ]

        self.template = np.zeros((size*2, size*2), dtype=bool)
        div_ = (self.size*self.size)//4
        quoters_pos = [self.password_pos[:div_], self.password_pos[div_:div_*2],
                       self.password_pos[div_*2:div_*3], self.password_pos[div_*3:]]

        #q1
        for p in quoters_pos[0]:
            self.template[p//self.size, p%self.size] = True

        for p in quoters_pos[1]:
            self.template[p%self.size, self.size*2-1-p//self.size] = True

        for p in quoters_pos[2]:
            self.template[self.size*2-1-p//self.size, self.size*2-1-p%self.size] = True

        for p in quoters_pos[3]:
            self.template[self.size*2-1-p%self.size, p//self.size] = True

        indexes = np.arange(self.template_size).reshape(self.size*2, self.size*2)
        self.rot_quoters = [indexes[self.template],
                            indexes[np.rot90(self.template, k=-1)],
                            indexes[np.rot90(self.template, k=-2)],
                            indexes[np.rot90(self.template, k=-3)] ]

    def cript(self, de_msg):
        de_msg = np.array([c for c in de_msg])
        cr_msg = np.empty(self.template_size, dtype='<U1')
        for i in range(4):
            cr_msg[self.rot_quoters[i]] = de_msg[i*self.quoter_size:(i+1)*self.quoter_size]

        return "".join(cr_msg)

    def decript(self, cr_msg):
        cr_msg = np.array([c for c in cr_msg])
        #de_msg = np.empty(self.template_size, dtype='<U1')
        de_msg = ""

        for i in range(4):
            de_msg += "".join(cr_msg[self.rot_quoters[i]])
        return de_msg

class raster:
    def __init__(self, cr_msg, size=3):
        self.cr_msg = cr_msg
        self.size = size
        self.chunk_size = np.power(self.size*2, 2)

    def display_help(self):
        parts = [ self.cr_msg[i*self.chunk_size:(i+1)*self.chunk_size] for  i in range(len(self.cr_msg)//self.chunk_size)]
        for msg_part in parts:
            msg_len = len(msg_part)
            part1 = msg_part[:msg_len//2]
            part2 = msg_part[msg_len//2:][::-1]

            space = 1
            sep = " "*space
            part1 = sep.join([c for c in part1])
            part2 = sep.join([c for c in part2])

            part1_decimal = sep.join([str(i//10) for i in range(msg_len//2)])
            part1_unit = sep.join([str(i%10) for i in range(msg_len//2)])

            part2_decimal = sep.join([str(i//10) for i in list(range(msg_len//2, msg_len))[::-1]])
            part2_unit = sep.join([str(i%10) for i in list(range(msg_len//2, msg_len))[::-1]])

            print(part1_decimal)
            print(part1_unit)
            print(part1)
            print(part2)
            print(part2_unit)
            print(part2_decimal)
            print()



msg = "GRILLEXCIPHERXWASXFIRSTXPROPOSEDXBYX"
k = template("FLEISNRWO")
msg = "ZEONOUJEACDGEAMTLUSCOLMIUMEZKLEELDDUOZBUJNJSBCEOICIZEEMJMSYXPNXOXXPYMWRY"
cr_msg = k.cript(msg)
#print(msg)
#print(cr_msg)
#print(k.decript(cr_msg))

r = raster(msg)

r.display_help()


