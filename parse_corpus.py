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
        
    #remove anything bracketed
    beta_code = re.sub(r'\<.*?\>', '', merge)
    
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

def strip_convert_and_store(path):
    #check to make sure we have a valid path
    if os.path.exists(path):
        betacode = strip_xml(path)
        unicode = convert_to_unicode(betacode)
        
        #create betacode file and unicode file
        root, ext = os.path.splitext(path)
        beta = open(root+"-betacode", 'w')
        uni = open(root+"-unicode", 'w')
        beta.write(betacode.encode("utf16"))
        uni.write(unicode.encode("utf16"))
        beta.close()
        uni.close()
        
    else:
        return None
        #throw error

def main():
    strip_convert_and_store('./corpus/02_gk.xml')
    
if __name__ == "__main__":
    main()