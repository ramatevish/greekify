# -*- coding: utf8 -*-
import unicodedata

def strip_accents(s):
    '''
    Strips accents and breathing marks from unicode. Thanks to Martin Miller (http://stackoverflow.com/users/355230/martineau) for this.
    :param s:
    '''
    return u''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

class CWord:
    def __init__(self, flat_word):
        self.flat_word = flat_word
        self.unique_words = {}

    def __str__(self):
        out = self.flat_word + ":\n"
        for key in self.unique_words.items():
            out += "\t" + key[0] + ", " + str(key[1]) + "\n"
        return out

    def __repr__(self):
        out = self.flat_word + ":\n"
        for key in self.unique_words.items():
            out += "\t" + self.unique_words[key] + "\n"
        return out

    def add_unique_word(self, word):
        res = self.unique_words.get(word)
        if res:
            self.unique_words[word] = res + 1
        else:
            self.unique_words[word] = 1
            
class Corpus:
    def __init__(self):
        self.corpus = {}
        self.entries = 0
        self.unique_entries = 0
    
    def __str__(self):
        out = "Corpus(entries=%d, unique_entries=%d " % (self.entries, self.unique_entries) + "corpus=\n"
        for key in self.corpus:
            out += str(self.corpus[key]) + "\n"
        return out
    
    def __repr__(self):
        out = "Corpus(entries=%d, unique_entries=%d " % (self.entries, self.unique_entries) + "corpus=\n"
        for key in self.corpus:
            out += str(self.corpus[key]) + "\n"
        return out
    
    def add_to_corpus(self, word):
        flat_word = strip_accents(word)
        
        #if we haven't seen the flattened word yet, add it and the unique word to corpus
        if flat_word not in self.corpus:
            new_flat_word = CWord(flat_word)
            new_flat_word.add_unique_word(word)
            self.corpus[flat_word] = new_flat_word
            self.entries += 1
            self.unique_entries += 1
            print("Added word " + word)
        else:
            self.corpus[flat_word].add_unique_word(word)
            self.unique_entries += 1
            print("Added word " + word)
                    
def main():
    corpus = Corpus()
    corpus.add_to_corpus(u"tóm")
    corpus.add_to_corpus(u"tòm")
    corpus.add_to_corpus(u"tom")
    corpus.add_to_corpus(u"dróll")
    corpus.add_to_corpus(u"dròll")
    print(corpus)
    #make_dict('./corpus/01_gk.unicode')

if __name__ == "__main__":
    main()