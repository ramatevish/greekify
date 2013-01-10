# -*- coding: utf8 -*-
import os
import re
import beta2unicode
from xml.dom.minidom import parseString
from corpus import Corpus
import unicodedata
import pickle


def strip_accents(s):
    '''
    Strips accents and breathing marks from unicode. Thanks to Martin Miller (http://stackoverflow.com/users/355230/martineau) for this.
    :param s:
    '''
    return u''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def strip_xml(path):
    '''
    Given an input XML path from the Perseus Project, strip all tags and 
    combine paragraphs into a string
    :param path: 
    '''
    #open file
    file_ = open(path, 'r')
    
    #parse string, combine paragraphs
    dom = parseString(file_.read())
    file_.close()
    text = dom.getElementsByTagName('p')[1:]
    
    
    merge = ''
    for paragraph in text:
        merge += paragraph.toxml()
        
    #remove anything bracketed, and punctuation
    beta_code = re.sub(r"\<.*?\>", "", merge)
    beta_code = re.sub(r"\.?\,?\:?\;?\'?\-?", "", beta_code)
    beta_code = re.sub(r"[ \t\r\n]", " ", beta_code)
    beta_code = re.sub(r"\s+", " ", beta_code)

    return beta_code

def convert_to_terminal_sigmas(ascii_word, converter):
    ascii_word = ascii_word.upper()
    #get last occurrence of S in word - need to see if python has better strrchr function
    index = len(ascii_word)
    try:
        index = (len(ascii_word) - 1) - ascii_word[::-1].index('S')
        if ascii_word[index:] == "S":
            return ascii_word + "2"
    except:
            return ascii_word

def convert_beta_to_unicode(text):
    '''
    Give a string of Beta Code (see http://en.wikipedia.org/wiki/Beta_code) 
    tokenize and convert to unicode_
    :param text:
    '''
    #tokenize text on spaces
    tokens = text.split(' ')
    
    #create converter object
    converter = beta2unicode.beta2unicodeTrie()
    
    #iterate over tokens, capitalize them, and convert, adding unicode_ translation to string
    converted = u""
    for word in tokens:
        word_ = convert_to_terminal_sigmas(word, converter)
        unicode_word, _ = converter.convert(word_)
        converted += unicode_word + " "
    converted = converted[:-1]
    
    return converted

def strip_convert_and_store(path):
    '''
    Given a path name for an xml file from the Perseus Project, saves the betacode and unicode versions of the text
    :param path:
    '''
    #check to make sure we have a valid path
    if os.path.exists(path):
        betacode = strip_xml(path)
        unicode_ = convert_beta_to_unicode(betacode)
        
        #create unicode file
        root, _ = os.path.splitext(path)
        uni = open(root+".unicode", 'w')
        
        uni.write(unicode_.encode("utf-8", "ignore"))
        
        uni.close()
        
        return betacode, unicode_
        
    else:
        print("Error converting " + path + "\n")
        return None
        #throw error

def parse_corpus(force_reparse = 0):
    '''
    Enters the corpus directory where this script is run from and goes through all xml files, and proccess them using strip_convert_and_store
    '''
    if force_reparse == 1:
        print("Force reparse!\n")
    
    files = os.listdir('./corpus')
    
    #only keep xml files
    files = [file_ for file_ in files if ".xml" in file_]
    
    #for counter
    num = len(files)
    cur = 1
    
    print("Parsing " + str(num) + " total files.")
    
    #iterate over all xml files in directory and proccess
    for file_ in files:
        try:
            
            print("Processing " + file_ + " (" + str(cur) + " of " + str(num) + ")")
            cur += 1
            
            root, ext = os.path.splitext(file_)
            
            #if we have forced a reparse, or the unicode doesn't exits, parse
            if force_reparse == 1 or not os.path.exists("./corpus/" + root + '.unicode'):
                strip_convert_and_store("./corpus/" + file_)
        
        except UnicodeEncodeError:
            print("UnicodeEncodeError, skipping\n")
            pass

def create_dict():
    '''
    Using parsed unicode files stored in the corpus folder, adds words from each to corpus object for use later
    '''
    corpus = Corpus()
    
    CORPUS_DIR = "./corpus"
    
    files = os.listdir(CORPUS_DIR)
    
    print(files)
    #only keep unicode files
    files = [file_ for file_ in files if ".unicode" in file_]
    
    #counter
    num_files = len(files)
    current = 1
    
    print("\nAdding " + str(num_files) + " total files.")
    
    #iterate over all xml files in directory and process
    for file_ in files:
        print("Adding " + file_ + " (" + str(current) + " of " + str(num_files) + ") to corpus")
        current += 1
        
        #if the pre-processed unicode file exits, add to corpus
        if os.path.exists(os.path.join(CORPUS_DIR, file_)):
            
            unicode_ = open(os.path.join(CORPUS_DIR, file_)).read().decode("utf-8")
            
            #split file and add words
            for word in unicode_.split(" "):
                corpus.add_to_corpus(word)
                
    print("Corpus successfully built. Saving corpus to corpus.pickle")
    file_ = open("./corpus.pickle","w")
    pickle.dump(corpus,file_)
    

def main():
    #strip_convert_and_store('./corpus/aristid.orat_gk.xml')
    parse_corpus(force_reparse=1)
    create_dict()
    
if __name__ == "__main__":
    main()