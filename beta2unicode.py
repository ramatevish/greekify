    # beta2unicode.py
#
# Version 2004-11-23
#
# James Tauber
# http://jtauber.com/
#
# You are free to redistribute this, but please inform me of any errors
#
# USAGE:
#
# trie = beta2unicodeTrie()
# beta = "LO/GOS\n";
# unicode, remainder = trie.convert(beta)
#
# - to get final sigma, string must end in \n
# - remainder will contain rest of beta if not all can be converted

class Trie:
    def __init__(self):
        self.root = [None, {}]

    def add_to_corpus(self, word, value):
        curr_node = self.root
        for ch in word:
            curr_node = curr_node[1].setdefault(ch, [None, {}])
        curr_node[0] = value

    def find(self, key):
        curr_node = self.root
        for ch in key:
            try:
                curr_node = curr_node[1][ch]
            except KeyError:
                return None
        return curr_node[0]

    def findp(self, key):
        curr_node = self.root
        remainder = key
        for ch in key:
            try:
                curr_node = curr_node[1][ch]
            except KeyError:
                return (curr_node[0], remainder)
            remainder = remainder[1:]
        return (curr_node[0], remainder)

    def convert(self, keystring):
        valuestring = ""
        key = keystring
        while key:
            value, key = self.findp(key)
            if not value:
                return (valuestring, key)
            valuestring += value
        return (valuestring, key)

def beta2unicodeTrie():
    t = Trie()

    t.add_to_corpus("*A",      u"\u0391")
    t.add_to_corpus("*B",      u"\u0392")
    t.add_to_corpus("*G",      u"\u0393")
    t.add_to_corpus("*D",      u"\u0394")
    t.add_to_corpus("*E",      u"\u0395")
    t.add_to_corpus("*Z",      u"\u0396")
    t.add_to_corpus("*H",      u"\u0397")
    t.add_to_corpus("*Q",      u"\u0398")
    t.add_to_corpus("*I",      u"\u0399")
    t.add_to_corpus("*K",      u"\u039A")
    t.add_to_corpus("*L",      u"\u039B")
    t.add_to_corpus("*M",      u"\u039C")
    t.add_to_corpus("*N",      u"\u039D")
    t.add_to_corpus("*C",      u"\u039E")
    t.add_to_corpus("*O",      u"\u039F")
    t.add_to_corpus("*P",      u"\u03A0")
    t.add_to_corpus("*R",      u"\u03A1")
    t.add_to_corpus("*S",      u"\u03A3")
    t.add_to_corpus("*T",      u"\u03A4")
    t.add_to_corpus("*U",      u"\u03A5")
    t.add_to_corpus("*F",      u"\u03A6")
    t.add_to_corpus("*X",      u"\u03A7")
    t.add_to_corpus("*Y",      u"\u03A8")
    t.add_to_corpus("*W",      u"\u03A9")

    t.add_to_corpus("A",      u"\u03B1")
    t.add_to_corpus("B",      u"\u03B2")
    t.add_to_corpus("G",      u"\u03B3")
    t.add_to_corpus("D",      u"\u03B4")
    t.add_to_corpus("E",      u"\u03B5")
    t.add_to_corpus("Z",      u"\u03B6")
    t.add_to_corpus("H",      u"\u03B7")
    t.add_to_corpus("Q",      u"\u03B8")
    t.add_to_corpus("I",      u"\u03B9")
    t.add_to_corpus("K",      u"\u03BA")
    t.add_to_corpus("L",      u"\u03BB")
    t.add_to_corpus("M",      u"\u03BC")
    t.add_to_corpus("N",      u"\u03BD")
    t.add_to_corpus("C",      u"\u03BE")
    t.add_to_corpus("O",      u"\u03BF")
    t.add_to_corpus("P",      u"\u03C0")
    t.add_to_corpus("R",      u"\u03C1")

    t.add_to_corpus("S\n",    u"\u03C2")
    t.add_to_corpus("S,",     u"\u03C2,")
    t.add_to_corpus("S.",     u"\u03C2.")
    t.add_to_corpus("S:",     u"\u03C2:")
    t.add_to_corpus("S;",     u"\u03C2;")
    t.add_to_corpus("S]",     u"\u03C2]")
    t.add_to_corpus("S@",     u"\u03C2@")
    t.add_to_corpus("S_",     u"\u03C2_")
    t.add_to_corpus("S",      u"\u03C3")
    t.add_to_corpus("S2",      u"\u03C2")
    

    t.add_to_corpus("T",      u"\u03C4")
    t.add_to_corpus("U",      u"\u03C5")
    t.add_to_corpus("F",      u"\u03C6")
    t.add_to_corpus("X",      u"\u03C7")
    t.add_to_corpus("Y",      u"\u03C8")
    t.add_to_corpus("W",      u"\u03C9")

    t.add_to_corpus("I+",     U"\u03CA")
    t.add_to_corpus("U+",     U"\u03CB")

    t.add_to_corpus("A)",     u"\u1F00")
    t.add_to_corpus("A(",     u"\u1F01")
    t.add_to_corpus("A)\\",   u"\u1F02")
    t.add_to_corpus("A(\\",   u"\u1F03")
    t.add_to_corpus("A)/",    u"\u1F04")
    t.add_to_corpus("A(/",    u"\u1F05")
    t.add_to_corpus("E)",     u"\u1F10")
    t.add_to_corpus("E(",     u"\u1F11")
    t.add_to_corpus("E)\\",   u"\u1F12")
    t.add_to_corpus("E(\\",   u"\u1F13")
    t.add_to_corpus("E)/",    u"\u1F14")
    t.add_to_corpus("E(/",    u"\u1F15")
    t.add_to_corpus("H)",     u"\u1F20")
    t.add_to_corpus("H(",     u"\u1F21")
    t.add_to_corpus("H)\\",   u"\u1F22")
    t.add_to_corpus("H(\\",   u"\u1F23")
    t.add_to_corpus("H)/",    u"\u1F24")
    t.add_to_corpus("H(/",    u"\u1F25")
    t.add_to_corpus("I)",     u"\u1F30")
    t.add_to_corpus("I(",     u"\u1F31")
    t.add_to_corpus("I)\\",   u"\u1F32")
    t.add_to_corpus("I(\\",   u"\u1F33")
    t.add_to_corpus("I)/",    u"\u1F34")
    t.add_to_corpus("I(/",    u"\u1F35")
    t.add_to_corpus("O)",     u"\u1F40")
    t.add_to_corpus("O(",     u"\u1F41")
    t.add_to_corpus("O)\\",   u"\u1F42")
    t.add_to_corpus("O(\\",   u"\u1F43")
    t.add_to_corpus("O)/",    u"\u1F44")
    t.add_to_corpus("O(/",    u"\u1F45")
    t.add_to_corpus("U)",     u"\u1F50")
    t.add_to_corpus("U(",     u"\u1F51")
    t.add_to_corpus("U)\\",   u"\u1F52")
    t.add_to_corpus("U(\\",   u"\u1F53")
    t.add_to_corpus("U)/",    u"\u1F54")
    t.add_to_corpus("U(/",    u"\u1F55")
    t.add_to_corpus("W)",     u"\u1F60")
    t.add_to_corpus("W(",     u"\u1F61")
    t.add_to_corpus("W)\\",   u"\u1F62")
    t.add_to_corpus("W(\\",   u"\u1F63")
    t.add_to_corpus("W)/",    u"\u1F64")
    t.add_to_corpus("W(/",    u"\u1F65")

    t.add_to_corpus("A)=",    u"\u1F06")
    t.add_to_corpus("A(=",    u"\u1F07")
    t.add_to_corpus("H)=",    u"\u1F26")
    t.add_to_corpus("H(=",    u"\u1F27")
    t.add_to_corpus("I)=",    u"\u1F36")
    t.add_to_corpus("I(=",    u"\u1F37")
    t.add_to_corpus("U)=",    u"\u1F56")
    t.add_to_corpus("U(=",    u"\u1F57")
    t.add_to_corpus("W)=",    u"\u1F66")
    t.add_to_corpus("W(=",    u"\u1F67")

    t.add_to_corpus("*A)",     u"\u1F08")
    t.add_to_corpus("*)A",     u"\u1F08")
    t.add_to_corpus("*A(",     u"\u1F09")
    t.add_to_corpus("*(A",     u"\u1F09")
    #
    t.add_to_corpus("*(\A",    u"\u1F0B")
    t.add_to_corpus("*A)/",    u"\u1F0C")
    t.add_to_corpus("*)/A",    u"\u1F0C")
    t.add_to_corpus("*A(/",    u"\u1F0F")
    t.add_to_corpus("*(/A",    u"\u1F0F")
    t.add_to_corpus("*E)",     u"\u1F18")
    t.add_to_corpus("*)E",     u"\u1F18")
    t.add_to_corpus("*E(",     u"\u1F19")
    t.add_to_corpus("*(E",     u"\u1F19")
    #
    t.add_to_corpus("*(\E",    u"\u1F1B")
    t.add_to_corpus("*E)/",    u"\u1F1C")
    t.add_to_corpus("*)/E",    u"\u1F1C")
    t.add_to_corpus("*E(/",    u"\u1F1D")
    t.add_to_corpus("*(/E",    u"\u1F1D")

    t.add_to_corpus("*H)",     u"\u1F28")
    t.add_to_corpus("*)H",     u"\u1F28")
    t.add_to_corpus("*H(",     u"\u1F29")
    t.add_to_corpus("*(H",     u"\u1F29")
    t.add_to_corpus("*H)\\",   u"\u1F2A")
    t.add_to_corpus(")\\*H",   u"\u1F2A")
    t.add_to_corpus("*)\\H",    u"\u1F2A")
    #
    t.add_to_corpus("*H)/",    u"\u1F2C")
    t.add_to_corpus("*)/H",    u"\u1F2C")
    #
    t.add_to_corpus("*)=H",    u"\u1F2E")
    t.add_to_corpus("(/*H",    u"\u1F2F")
    t.add_to_corpus("*(/H",    u"\u1F2F")
    t.add_to_corpus("*I)",     u"\u1F38")
    t.add_to_corpus("*)I",     u"\u1F38")
    t.add_to_corpus("*I(",     u"\u1F39")
    t.add_to_corpus("*(I",     u"\u1F39")
    #
    #
    t.add_to_corpus("*I)/",    u"\u1F3C")
    t.add_to_corpus("*)/I",    u"\u1F3C")
    #
    #
    t.add_to_corpus("*I(/",    u"\u1F3F")
    t.add_to_corpus("*(/I",    u"\u1F3F")
    #
    t.add_to_corpus("*O)",     u"\u1F48")
    t.add_to_corpus("*)O",     u"\u1F48")
    t.add_to_corpus("*O(",     u"\u1F49")
    t.add_to_corpus("*(O",     u"\u1F49")
    #
    #
    t.add_to_corpus("*(\O",    u"\u1F4B")
    t.add_to_corpus("*O)/",    u"\u1F4C")
    t.add_to_corpus("*)/O",    u"\u1F4C")
    t.add_to_corpus("*O(/",    u"\u1F4D")
    t.add_to_corpus("*(/O",    u"\u1F4D")
    #
    t.add_to_corpus("*U(",     u"\u1F59")
    t.add_to_corpus("*(U",     u"\u1F59")
    #
    t.add_to_corpus("*(/U",    u"\u1F5D")
    #
    t.add_to_corpus("*(=U",    u"\u1F5F")
    
    t.add_to_corpus("*W)",     u"\u1F68")
    t.add_to_corpus("*W(",     u"\u1F69")
    t.add_to_corpus("*(W",     u"\u1F69")
    #
    #
    t.add_to_corpus("*W)/",    u"\u1F6C")
    t.add_to_corpus("*)/W",    u"\u1F6C")
    t.add_to_corpus("*W(/",    u"\u1F6F")
    t.add_to_corpus("*(/W",    u"\u1F6F")

    t.add_to_corpus("*A)=",    u"\u1F0E")
    t.add_to_corpus("*)=A",    u"\u1F0E")
    t.add_to_corpus("*A(=",    u"\u1F0F")
    t.add_to_corpus("*W)=",    u"\u1F6E")
    t.add_to_corpus("*)=W",    u"\u1F6E")
    t.add_to_corpus("*W(=",    u"\u1F6F")
    t.add_to_corpus("*(=W",    u"\u1F6F")

    t.add_to_corpus("A\\",    u"\u1F70")
    t.add_to_corpus("A/",     u"\u1F71")
    t.add_to_corpus("E\\",    u"\u1F72")
    t.add_to_corpus("E/",     u"\u1F73")
    t.add_to_corpus("H\\",    u"\u1F74")
    t.add_to_corpus("H/",     u"\u1F75")
    t.add_to_corpus("I\\",    u"\u1F76")
    t.add_to_corpus("I/",     u"\u1F77")
    t.add_to_corpus("O\\",    u"\u1F78")
    t.add_to_corpus("O/",     u"\u1F79")
    t.add_to_corpus("U\\",    u"\u1F7A")
    t.add_to_corpus("U/",     u"\u1F7B")
    t.add_to_corpus("W\\",    u"\u1F7C")
    t.add_to_corpus("W/",     u"\u1F7D")

    t.add_to_corpus("A)/|",   u"\u1F84")
    t.add_to_corpus("A(/|",   u"\u1F85")
    t.add_to_corpus("H)|",    u"\u1F90")
    t.add_to_corpus("H(|",    u"\u1F91")
    t.add_to_corpus("H)/|",   u"\u1F94")
    t.add_to_corpus("H)=|",   u"\u1F96")
    t.add_to_corpus("H(=|",   u"\u1F97")
    t.add_to_corpus("W)|",    u"\u1FA0")
    t.add_to_corpus("W(=|",   u"\u1FA7")

    t.add_to_corpus("A=",     u"\u1FB6")
    t.add_to_corpus("H=",     u"\u1FC6")
    t.add_to_corpus("I=",     u"\u1FD6")
    t.add_to_corpus("U=",     u"\u1FE6")
    t.add_to_corpus("W=",     u"\u1FF6")

    t.add_to_corpus("I\\+",   u"\u1FD2")
    t.add_to_corpus("I/+",    u"\u1FD3")
    t.add_to_corpus("I+/",    u"\u1FD3")
    t.add_to_corpus("U\\+",   u"\u1FE2")
    t.add_to_corpus("U/+",    u"\u1FE3")

    t.add_to_corpus("A|",     u"\u1FB3")
    t.add_to_corpus("A/|",    u"\u1FB4")
    t.add_to_corpus("H|",     u"\u1FC3")
    t.add_to_corpus("H/|",    u"\u1FC4")
    t.add_to_corpus("W|",     u"\u1FF3")
    t.add_to_corpus("W|/",    u"\u1FF4")
    t.add_to_corpus("W/|",    u"\u1FF4")

    t.add_to_corpus("A=|",    u"\u1FB7")
    t.add_to_corpus("H=|",    u"\u1FC7")
    t.add_to_corpus("W=|",    u"\u1FF7")

    t.add_to_corpus("R(",     u"\u1FE4")
    t.add_to_corpus("*R(",    u"\u1FEC")
    t.add_to_corpus("*(R",    u"\u1FEC")

#    t.add_to_corpus("~",      u"~")
#    t.add_to_corpus("-",      u"-")

#    t.add_to_corpus("(null)", u"(null)")
#    t.add_to_corpus("&", "&")

    t.add_to_corpus("0", u"0")
    t.add_to_corpus("1", u"1")
    t.add_to_corpus("2", u"2")
    t.add_to_corpus("3", u"3")
    t.add_to_corpus("4", u"4")
    t.add_to_corpus("5", u"5")
    t.add_to_corpus("6", u"6")
    t.add_to_corpus("7", u"7")
    t.add_to_corpus("8", u"8")
    t.add_to_corpus("9", u"9")

    t.add_to_corpus("@", u"@")
    t.add_to_corpus("$", u"$")

    t.add_to_corpus(" ", u" ")

    t.add_to_corpus(".", u".")
    t.add_to_corpus(",", u",")
    t.add_to_corpus("'", u"'")
    t.add_to_corpus(":", u":")
    t.add_to_corpus(";", u";")
    t.add_to_corpus("_", u"_")

    t.add_to_corpus("[", u"[")
    t.add_to_corpus("]", u"]")

    t.add_to_corpus("\n", u"")

    
    return t
