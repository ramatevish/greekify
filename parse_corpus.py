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

def convert_to_unicode(text):
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
        unicode_, _ = converter.convert(word.upper())
        converted += unicode_ + " "
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
        unicode_ = convert_to_unicode(betacode)
        
        #create betacode file and unicode file
        root, _ = os.path.splitext(path)
        beta = open(root+".betacode", 'w')
        uni = open(root+".unicode", 'w')
        
        beta.write(betacode)
        uni.write(unicode_.encode("utf-8", "ignore"))
        
        beta.close()
        uni.close()
        
        return betacode, unicode_
        
    else:
        return None
        #throw error

def parse_corpus():
    '''
    Enters the corpus directory where this script is run from and goes through all xml files, and proccess them using strip_convert_and_store
    '''
    files = os.listdir('./corpus')
    
    #counter
    num = len(files)
    cur = 1
    print(str(num) + " total files.")
    
    #iterate over all xml files in directory and proccess
    for file_ in files:
        
        print("Processing " + file_ + " (" + str(cur) + " of " + str(num) + ")")
        cur += 1
        
        _, ext = os.path.splitext(file_)
        #and (not os.path.exists("./corpus/" + root + '.betacode')) and (not os.path.exists("./corpus/" + root + '.unicode')):
        if ext == '.xml':
            strip_convert_and_store("./corpus/" + file_)
            
    
            
def create_dict():
    '''
    Using parsed unicode files stored in the corpus folder, adds words from each to corpus object for use later
    '''
    corpus = Corpus()
    
    files = os.listdir('./corpus')
    
    #counter
    num_files = len(files)
    current = 0
    
    print(str(num_files) + " total files.")
    
    #iterate over all xml files in directory and process
    for file_ in files:
        print("Adding " + file_ + " (" + str(current) + " of " + str(num_files) + ") to corpus")
        current += 1
        root, _ = os.path.splitext(file_)
        
        #if the pre-processed unicode file exits, add to corpus
        if os.path.exists(os.path.join("./corpus", root + ".unicode")):
            
            unicode_ = open(os.path.join("./corpus", root + ".unicode"),"r").read().decode("utf-8")
            
            #split file and add words
            for word in unicode_.split(" "):
                corpus.add_to_corpus(word)
                
    file_ = open("./corpus.pickle","w")
    pickle.dump(corpus,file_)
    

def main():
    #strip_convert_and_store('./corpus/aristid.orat_gk.xml')
    parse_corpus()
    create_dict()
    
if __name__ == "__main__":
    main()