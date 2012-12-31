import os
import sys
import re
import io
from IPython.core.ultratb import generate_tokens
from lib2to3.fixer_util import String

class Word:
    def __init__(self, word):
        self.word = word
        self.count = 1
        
    def __str__(self):
        return self.word + ": " + str(self.count)
    
    def increment(self):
        self.count += 1
        
class Key:
    def __init__(self, flat_word):
        self.flat_word = flat_word
        self.words = {}
        
    def __str__(self):
        out = self.flat_word + ":\n"
        for word in self.words.items():
            out += "\t" + word[0] + ": " + str(word[1].count) + "\n"
        return out
        
    def add(self, word):
        res = self.words.get(word)
        if res:
            res.increment()
        else:
            self.words[word] = Word(word)
            


    
    
def main():
    return None
    #make_dict('./corpus/01_gk.unicode')

if __name__ == "__main__":
    main()