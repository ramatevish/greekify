import os
import sys
import beta2unicode
from xml.dom.minidom import parse, parseString

def strip_xml(path):
    '''
    Given an input XML path from the Perseus Project, strip all tags and combine paragraphs into 1
    :param path: 
    '''
    if os.path.exists(path):
        root, ext = os.path.splitext(path)
        file = open(path, 'r')
        dom = parseString(file.read())
        
        

def main():
    print "test"
    
if __name__ == "__main__":
    main()