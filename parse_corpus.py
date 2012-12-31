import os
import sys
import re
import beta2unicode
from xml.dom.minidom import parse, parseString

def strip_xml(path):
    '''
    Given an input XML path from the Perseus Project, strip all tags and 
    combine paragraphs into a string
    :param path: 
    '''
    #open file
    root, ext = os.path.splitext(path)
    file = open(path, 'r')
    
    #parse string, combine paragraphs
    dom = parseString(file.read())
    file.close()
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
    tokenize and convert to unicode
    :param text:
    '''
    #tokenize text on spaces
    tokens = text.split(' ')
    
    #create converter object
    converter = beta2unicode.beta2unicodeTrie()
    
    #iterate over tokens, capitalize them, and convert, adding unicode translation to string
    converted = ""
    for word in tokens:
        unicode, junk = converter.convert(word.upper())
        converted += unicode+" "
    converted = converted[:-1]
    
    return converted

def convert_to_flat_unicode(text):
    '''
    Give a string of Beta Code (see http://en.wikipedia.org/wiki/Beta_code) 
    tokenize and convert to flat unicode
    :param text:
    '''
    #strip accents, etc. from betacode
    flat_beta_code = re.sub(r"\)?\(?\\?\=?\/?\+?\|?\&?\'?", "", text)
    
    #tokenize text on spaces
    tokens = flat_beta_code.split(' ')
    
    #create converter object
    converter = beta2unicode.beta2unicodeTrie()
    
    #iterate over tokens, capitalize them, and convert, adding unicode translation to string
    converted = ""
    for word in tokens:
        unicode, junk = converter.convert(word.upper())
        converted += unicode+" "
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
        unicode = convert_to_unicode(betacode)
        flat_unicode = convert_to_flat_unicode(betacode)
        
        #create betacode file and unicode file
        root, ext = os.path.splitext(path)
        beta = open(root+".betacode", 'w')
        uni = open(root+".unicode", 'w')
        flat_uni = open(root+".flat_unicode", 'w')
        beta.write(betacode)
        uni.write(unicode)
        flat_uni.write(flat_unicode)
        beta.close()
        uni.close()
        flat_uni.close()
        
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
    for file in files:
        
        print("Processing " + file + " (" + str(cur) + " of " + str(num) + ")")
        cur += 1
        
        root, ext = os.path.splitext(file)
        #and (not os.path.exists("./corpus/" + root + '.betacode')) and (not os.path.exists("./corpus/" + root + '.unicode')):
        if ext == '.xml':
            strip_convert_and_store("./corpus/" + file)
    
    
def main():
    #strip_convert_and_store('./corpus/aristid.orat_gk.xml')
    parse_corpus()
    
if __name__ == "__main__":
    main()