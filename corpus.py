import unicodedata

def strip_accents(s):
    '''
    Strips accents and breathing marks from unicode. Thanks to Martin Miller (http://stackoverflow.com/users/355230/martineau) for this.
    :param s:
    '''
    return u''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

class Word:
    def __init__(self, word):
        self.word = word
        self.count = 1

    def __str__(self):
        return self.word + ": " + str(self.count)

    def increment(self):
        self.count += 1

class CWord:
    def __init__(self, flat_word):
        self.flat_word = flat_word
        self.unique_words = {}

    def __str__(self):
        out = self.flat_word + ":\n"
        for key in self.unique_words.items():
            out += "\t" + self.unique_words[key] + "\n"
        return out

    def __repr__(self):
        out = u""
        for word in self.unique_words.items():
            out += "\t" + word.word + ": " + str(word.count) + "\n"
        return out

    def add_unique_word(self, word):
        res = self.unique_words.get(word)
        if res:
            res.increment()
        else:
            self.unique_words[word] = Word(word)
            
class Corpus:
    def __init__(self):
        self.corpus = {}
    
    def __str__(self):
        out = ""
        for key in self.corpus:
            out += out + str(self.corpus[key]) + "\n"
        return out
    
    def __repr__(self):
        out = u""
        for key in self.corpus:
            out += out + self.corpus[key] + "\n"
        return out
    
    def add_to_corpus(self, word):
        flat_word = strip_accents(word)
        if flat_word not in self.corpus:
            self.corpus[flat_word] = CWord(flat_word).add_unique_word(word)
        else:
            self.corpus[flat_word].add_unique_word(word)
                    
def main():
    return None
    #make_dict('./corpus/01_gk.unicode')

if __name__ == "__main__":
    main()