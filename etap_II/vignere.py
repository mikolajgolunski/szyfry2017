import itertools
import string
import re
import numpy as np

# self correlaton
def scorr(msg, max_n=12):
    msg = np.array([char for char in msg])
    msg_len = len(msg)
    cor_list = np.zeros(max_n-1, dtype=float)
    for n in range(1, max_n):
        cor_list[n-1] = np.sum(msg == np.roll(msg, n))/float(msg_len)
    for i in (np.argsort(cor_list)[::-1])[:3]:
        print(i+1, cor_list[i])



class vignere:
    def __init__(self, cr_msg, key_len):
        self.cr_msg = cr_msg
        self.de_msg = ""

        self.key_len = key_len

        self.row_header  = np.array(list(string.ascii_uppercase))
        self.col_header = np.array([ str(s) for s in range(1, key_len+1)])

        self.table = np.empty((len(self.col_header), len(self.row_header)), dtype=self.col_header.dtype)
        self.table.fill("*")

        self.fully_linked = False

        self.alph = np.array([char for char in string.ascii_uppercase])
        self.alph_dic = dict(zip(self.alph, range(len(self.alph))))
       # build table
    def display(self):
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

    def set_key(self, key):
        keys = np.array([c for c in key])
        pos = np.argmax(keys == self.table[0])
        self.table[0] = np.roll(keys, -pos)

    def fill_table(self, de_str):
        de_parted = re.findall(".{" + "1,{}".format(self.key_len) + "}", de_str)
        cr_msg_pos = 0
        for part_ in de_parted:
            for i, de_char in enumerate(part_):
                en_char = self.cr_msg[cr_msg_pos]
                self.table[i,self.row_header == de_char] = en_char

                cr_msg_pos += 1
        self.sync_rows()

    def fill_word(self, de_str, pos):
        for i, de_char in zip(range(pos, pos+len(de_str)), de_str):
            cr_char = self.cr_msg[i]
            self.table[i%self.key_len, self.row_header == de_char] = cr_char
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

    def fill_full_alphabet(self, row=0):
        self.alph
        present_chars = self.table[row][self.table[row] != "*"]
        key_pos = np.argmax(self.table[row] == present_chars[0])
        alph_pos = np.argmax(self.alph == present_chars[0])
        self.table[row] = np.roll(self.alph,  key_pos-alph_pos)
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

    def guess(self, guessed, cr_char, pos):
        self.table[pos][self.alph_dic[guessed]] = cr_char
        self.sync_rows()

    def decript(self, segmented=False):
        de_msg = ""
        help_msg = ""
        for i, cr_char in enumerate(self.cr_msg):
            char_table = np.where(self.table[i%self.key_len] == cr_char)[0]
            if char_table.shape[0] == 0:
                de_char = "*"
                #de_char = "[{},{}]".format(i%self.key_len, cr_char)
                #de_char = "{}".format(i%self.key_len)
                help_msg += "{}".format(i%self.key_len)
            else:
                de_char = self.alph[char_table[0]]
                help_msg += " "
            de_msg += de_char

        if segmented:
            for i in range(0, len(self.cr_msg), 10):
                line = str(i).ljust(4)
                line += " ".join(str(char) for char in range(10))
                print(line)
                line = " "*4
                line += " ".join(self.cr_msg[i:i+10])
                print(line)
                line = " "*4
                line += " ".join(de_msg[i:i+10])
                print(line)
                print()

        else:
            print(self.cr_msg)
            print(de_msg)
            print(help_msg)

    def copy(self):
        copy = vignere(self.cr_msg, self.key_len)
        copy.table = self.table.copy()
        copy.fully_linked = self.fully_linked
        return copy


#msg = "XQQBZPYNZXDBLYBXTAFJTRYGKCJOHIEHXGDYVBBIDCQOLRAYANBFHDINRDJUVBCXJCLYORODEMQGYAZNWNNDYMQQMLBYHHUMGDFKTJQGQEUOMWXHIGVBKXJBVU"
#msg = "GSZVNYUQRHHHUYMDZFZRZOWUAAEIJHHYPVSZEQSWOQZWMDAGRUFYGVFKJCFRDHYMTKNGGNUMRRTTBNEHUMOFUFUXBAZFGUAAIFMRNXJCXJFUEUGVVQUNFRFGZOWGAWOQMQDKZFSZLXRTUNTWVTFBEYLYXMUFUGUINRXMQMBYBTPMOFTDBNEHYQJVKOLVKKWHHCJPVYXYLUPUPHUUESLYTXYEOMWPFVROYDUFKJGUFYKTYRFKDYHMTWOVFPEHAPFDWPFKWUNGXHXUAUXWFUZTPTYHMHUYMDZG"
msg = "EWDOSWICSTOREHPNAGCJEZANTYSKROOTNFKOGSZPTOIECEGOLDOIWUSTDZOZINIOPASEMESEOTDAWWNITIEOBERESTCNOEOPPHEDSCZRONAOPAPRLZWPYICNAAJLNSEZTWYWKODIZASCTOOOSRPEOWKRNNETAEPWTNICAIIOCCDRELZYEDSHEOOMWNSOASTDOJOJUSSCZSDNIZYPOAMCOZHKJZTADKAZUEGRZUOASTNEOSGPKABPOOOODETAOPDWOIOMELIPXICXSAXXRZXIACNJXXIASTKT"
msg = "DWPALSRCKVKXIOJYCAJIGUEVUFMJVRTLYXGMTOATPNCQRJHFOLPNSGPOEFCPVRGDINXIDBMCSFWLYFTBVPGZQCRVDJHULDVXGIGGSXZGLTPATGQLWQCJMHCZSIJENJSLUAYQVRTBDMWMMGDHUWVBSOQPAAPVXHJHLBNBWFDJWHQOMURSUSDMHMEQPUEDQRPMCGNZFWYWJSMSDVUYDWGALBQEBEULWLPGNBPUGQNLTOMIVDHDYELEUCBHUDOKJSGPSPBJDJNOMSNBOGMJRALXCUWVPNJPVOXSRATCNHFRCJNSFFYGZEYTYMZJMUNUWDXPZQFTIKGOCXVIGKQLNJIWPXYJNYLTUJCCGYNBAVGWDYBMBGVXFYQUWNYTFQFXMBBVLPOLUREWQELSZTUVKIVAXWCADRGKAMPWEWWIPSNEGMLXZYFFYGRDLYAIKJXHJSLSSCJMVGRQCOABTVTFOIORSQVRTLYXGMAGAQXTXKLZGKQLMZXPJIDSRCRVAXAQEGCQRJHFOLKOKGFRFZJIOZGJLIFNYXU"

#msg = "PGZQYLDDDIMLCVBWUGYICZRLPQETMAXOFUQNLODIXESGTQLVDEWPAWSKLWMFWWEODIXESGTQLVDEWORQZIIOHXTISLRANOECTLMZOKWQELSJKRMFWSHQTONOECTLMZOKWQELSVXSFFJCUPDNQRLKNRQYJXKIUONYPHHPBBHRSMBLIAFQWFYAKUDTFCPIYUJMVGDHWIEZJDLBAQSRUOOIBWUKVRKHDGPJEYFELVVQJNLTWRTUAKDVQFNSEJYYNXXTMENVMLYQJZVKCDLFEELVIFNBQKEXSRATWYTHHKDDEZOKBXCQFAWFRXQQXKKQJJDGTQHQINNRLKFAGHSXSSMFZXPIRKENVEZX"


v = vignere(msg, 26)
#@v.fill_table("ISEELOVEICANSEEICANSEE")
v.fill_table("IXSEEXLOVEXIXCANXSEEXPASSIONXIXFEELXDANGERXIXFEELXOBSESSIONX")
#v.decript()
#v.fill_table("DOWSZYSTKICHJEDNOSTEK")
#v.fill_table("KRYPTOLOGIACZYLINAUKA")
#v.fill_table("REXMELDUJES")
#v.fill_table("UWAGAA")


"""
strings = ["OSZCHSZNEAWGESLQTIVYTEPOVRESAVVMUEYWPPWNASHIORECHICCHWYVZHQGESLDCSONPSVSKAKZPRESYEQNJGESCIVSCAOHZT", #4
           "OSSHKBODIPOFESEVWRKOXHGGCDPEGGZTSNNRDXGTHLDXDIDEZWOXCQZWITFPKICBSNXYCBQWTKGTBNESLBGEZHZHKBAEIKIAVSLRQUDXDI",
           "OSPFKIYWPNGCXTWBTMOHZTQHCDUALGHWYMACMVKBJWPCASPFKIYWPNVSCSVSCSKRPVSONWESZHJWPTNNJNWQTIHODXKDZHSFZXJOOVQULPEBTIOHZT",
           "OSHSHNMYHMCCCDTVWJFHTKNRYMTPHELORBSBCKPGWMLGYBGGZTLRHEKCBTQQZXGSSPTIYSSEZDTKCFESEICFTPZBKQCSSSSFESE",
           "OSZFFKESUOKAAEJWTWPCAXNNPGEOVSIDLREOFXNNJQQXPTKNJGFSDXKDEVVSNMWNPVKNPVKYZRPFFHAFKIJWPRWXPNLFLAUADONNJHHSDXKD",
           "OSYNHENHPNXOEINWTTNNPGEKFHAFKIJWPDWDWEJCHEJSYEPFKIYWLDAFZDAFZWPCASZFFKESUHVWPWESNSCWPRVOASNCHCJIXINRHEVSCSOHZT",
           "OSLWPVSGKIFYZQLOYMEGESLCOHWQAPQHZRNSKINKZAURZHUGASVMNNEHCDAQTIFYZQLOYMEGESLZLGVBTOKQKIGIUISDFRGQTIVSMVWGESL",
           "OSIKNRNMTCPNEIGBWFESEHUVPROTDBCSLRBNHDVHFMPXGSMMPVDLWROIBGOJLPPHUATSLTDVPGBBBHEWIHDCZXTFCTTICGSXLNPVMFESE"]

for s in strings:
    scorr(s)
    print("-----")

decoded=["DODOWODZTWASTOPCIEZKIATAKNIEPRZYJACIELAZPOLUDNIOWEGOWSCHODUSTOPPROSZEOZEZWOLENIENAUZYCIEREZERWSTOP", #0
         "DODOWODZTWASTOPCIEZKIOSTRZALSTOPDUZESTRATYSTOPPROSZEODOSTARCZENIEAMUNICJIGRANATOWISRODKOWOPATRUNKOWYCHSTOP", #1
         "DOTRZECIEJKOMPANIISTOPUTRZYMACLINIEOBRONYSTOPOTRZECIEJZEROZEROODERWACSIEODNIEPRZYJACIELASTOPODWROTNADRUGALINIESTOP", #2
         "DOSZTABUSTOPRZECIWUDERZENIEWTRAKCIEORGANIZACJISTOPWYTRZYMACDOTRZECIEJZEROZEROSTOPPOSILKIWDRODZESTOP", #3
         "DODRUGIEJKOMPANIISTOPTRZECIAKOMPANIAUTRZYMUJEPOZYCJESTOPTRZECIAZEROZEROKONTRUDERZENIENAJEJPRAWYMSKRZYDLESTOP", #4
         "DOCZWARTEJBATERIIPRZECIWUDERZENIEZAPLANOWANENATRZECIAZEROZEROSTOPODRUGIEJDZIESIECOGIENZAPOROWYNUMERDWAZEROSTOP", #5
         "DOPIERWSZEJKOMPANIISTOPODDACPLUTONREZERWOWYDODYSPOZYCJITRZECIEJKOMPANIISTOPLACZNIKOCZEKUJEWPUNKCIEZEBRASTOP", #6
         "DOTRZECIEJBATERIISTOPOGIENZAPOROWYNAWZGORZETRZYZEROSIEDEMNAWALAOGNIOWAPIECMINUTSTOPPOTEMOGIENNEKAJACYSTOP"] #7
v = vignere(strings[7], 6)
try:
    v.fill_table(decoded[7])
except ValueError:
    pass
try:
    v.fill_word("STOP", len(v.cr_msg)-4)
except ValueError:
    pass

v.fill_full_alphabet()
v.decode()

"""
#vin = vignere("XQQBZPYNZXDBLYBXTAFJTRYGKCJOHIEHXGDYVBBIDCQOL", 6)
#vin.fill_table("KRYPTOLOGIACZYLINAUKA")
#vin.decode("ZEGAR")

#vin.fill_alphabet()
#vin.sync_rows()
#vin.display()

#"DODRUGIEJKOMPANIISTOPTRZECIAKOMPANIAUTRZYMUJEPOZYCJESTOP TRZECIA ZERO ZERO KONTR UDERZENIE NAJEJPRAWYMSKRZYDLESTOP", #4
#"OSZFFKESUOKAAEJWTWPCAXNNPGEOVSIDLREOFXNNJQQXPTKNJGFSDXKD EVVSNMW NPVK NPVK YZRPF FHAFKIJWP RWXPNLFLAUADONNJHHSDXKD",
#vin.dict_force(12, 18)


