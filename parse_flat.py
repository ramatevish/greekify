# -*- coding: utf8 -*-
import pickle
import corpus
import sys
import traceback
import re
import textwrap
import datetime
import string
import os

CORPUS_LOCATION = u"./corpus.pickle"
MAINTAINER_EMAIL = u"alexandermatevish@gmail.com"
ERROR_CONTACT_MAINTAINER = u"If this error continues to show up, email the maintainer at " + MAINTAINER_EMAIL \
                                + " with a copy of all of the programs output, your corpus file, file, and a " \
                                + "simple explanation of the error."
#len 8
START_HIGHLIGHT = u"\x1B[31;40m"\
#len 4
END_HIGHLIGHT = u"\x1B[0m" 

def load_corpus(corpus=CORPUS_LOCATION):
    '''
    Tries to return the corpus from the serialized corpus generated by parse_corpus or 
    prints an error message and returns 1 if the corpus fails to load
    :param corpus: the location of the corpus to load if not using the default 
                        "./corpus.pickle"
    '''
    try:
        file_ = open(corpus,"r")
        corpus = pickle.load(file_)
        print_box(u"Corpus loaded (Entries: "+ str(corpus.entries) + ", Unique Entries: " \
                  + str(corpus.unique_entries) + ")", u"✔")
        return corpus
    
    except Exception, e:
        print_error("Corpus failed to load", e, "Try re-running parse_corpus or emailing the maintainer with this error message and your corpus file.")
        return 1
        
def get_word_array(cword):
    '''
    Given a CWord object, returns a list of tuples containing each unique
    iteration of the flat word and the percentage of times that iteration
    was seen.
    :CWord cword: object you wish to get words and percentages from
    '''
    total = 0.
    for word in cword.unique_words:
        total += cword.unique_words[word]
        
    words = []
    for word in cword.unique_words:
        words.append((word, round(cword.unique_words[word]/total,2)))
    
    return words

def lookup_word(corpus, word):
    choices = None
    try:
        cword = corpus[word]
        choices = get_word_array(cword)
        
        #sort list on occurrence (2nd element)
        choices = sorted(choices, key=lambda tup: tup[1], reverse=True)
        
    except KeyError:
        key_error_string = "Couldn't find " + word + " in the corpus. \nPerhaps there is  an unrecognized punctuation mark or incorrect character?"
        print_box(key_error_string, "")
    
    return choices

def choices_string(word, choices):
    '''
    Given a string and a tuple, containing a word and a percentage, returns a
    nicely formatted string.
    :string word: the flat word
    :list choices: the list of tuples
    '''
    string = "Replace " + word + " with:\n"
    i = 1
    try:
        for op in choices:
            string += str(i) + ") " + op[0] + ": " + str(op[1]) + "\n"
            i += 1
    except TypeError:
        pass
    
    return string

def get_choice(choices):
    err_str = ""
    ret = ""
    
    #quit, add word, save
    allowed_values = "qa"
    
    try:
        choice = raw_input("? ")
        choice = int(choice)
        
        if isinstance(choice, int) and (choice < 1 or choice > len(choices)):
            err_str = "Integers between 1 and " + str(len(choices)) + " or " \
            + ", ".join(allowed_values) + " please.\n"
       
        else:
            ret = choice
            
#    except NameError:
#        print("NameError")
#        if len(choice) == 1 and choice in allowed_values:
#            ret = choice
#        else:
#            err_str = "Integers between 1 and " + str(len(choices)) + " or " \
#                + ", ".join(allowed_values) + " please.\n"
        
    except ValueError:
        if len(choice) == 1 and choice in allowed_values:
            ret = choice
        else:
            err_str = "Integers between 1 and " + str(len(choices)) + " or " \
                + ", ".join(allowed_values) + " please.\n"
    
    return err_str, ret

def print_box(string, title="", pad=False, style="single", width=120):
    '''
    Used to print well-formatted boxes for emphasis. Can pass title=desiredtitle,
    to print a title, set pad=True to have interior margins, set 
    style="single|bold|double" to set border stule, and set width=desiredwidth to
    set the wrap width (this sets the max size, but the width may be smaller if
    no lines are greater than the width)
    Still derps if title is too large
    :string string: text inside the box
    :string title: text in title
    :bool pad: set vertical padding to 1
    :string style: box border style
    :int width: line wrap width
    '''
    styles = {"double": u"╔═╗║╚═╝", "single": u"┌─┐│└─┘", "bold": u"┏━┓┃┗━┛"}
    
    # check to make sure the style is valid, else default to single
    if style not in styles:
        style = "single"
    
    #set and decode
    box_style = styles[style]
    
    #split on defined linebreaks
    unwrapped_lines = string.split("\n")

    #wrap lines that go over width
    lines = []
    for line in unwrapped_lines:
        wrapped = textwrap.wrap(line, width - 4)
        for sub_line in wrapped:
            lines.append(sub_line)
            
    #pad top and bottom if requested
    if pad == True:
        lines.append("\n")
        lines.insert(0, "\n")

    #widen box to necessary width
    longest_line = max([max([len(line.strip()) for line in lines]) + 4, len(title) + 6])
    
    #create title
    padding = (" " if title != "" else "")
    top = box_style[0] + box_style[1] + padding + title + padding + box_style[1]
    
    #this is inefficient, look into re methods
    while len(top) < longest_line:
        top += box_style[1]
    top += box_style[2] + "\n"
    
    #middle
    middle = ""
    for line in lines:
        l = box_style[3] + " " + line.strip()
        
        #workaround for highlighting characters
        adj_len = len(top) - 3
        if START_HIGHLIGHT in line:
            adj_len += 6
        if END_HIGHLIGHT in line:
            adj_len += 6
            
        while len(l) < adj_len:
            l += " "
        middle += l + " " + box_style[3] + "\n"
        
    bottom = box_style[4]
    #this is inefficient as balls, look into re methods
    while len(bottom) < longest_line:
        bottom += box_style[5]
    bottom += box_style[6] + "\n"
    
    #the newline in front is used to prevent the box from breaking when unsync. out
    #@todo find a better way to prevent breaking that doesn't require new line
    print(top + middle + bottom)
    
def print_line(style="single", width=80):
    '''
    Prints a line with the desired style, and width
    :param style: set line style to "single|bold|double" (default: "single)
    :param width: set line width (default: 80)
    '''
    styles = {"double": u"═", "single": u"─", "bold": u"━"}
    
    # check to make sure the style is valid, else default to single
    if style not in styles:
        style = "single"
    
    #set and decode
    line_style = styles[style]
    
    line = "\n"
    while len(line) < width:
        line += line_style
    line += "\n"
        
    print(line)
    
def print_error(simple_errorstring, exception, explanation):
    '''"./parsed-" + time_
    Prints consistent, well formatted exception messages.
    :string simple_errorstring: the short, user readable explanation of the failure
    :Exception exception: the exception object thrown
    :string explanation: a string explaining how to possibly fix the problem,
                            or an in-depth explanation
    '''
    print_box(simple_errorstring + ": " + str(exception) + "\n" + explanation + \
                "\n" + ERROR_CONTACT_MAINTAINER, title=u"❗")
    
def color_string(str_, substr, start):
    index = string.find(str_[start:], substr)    
    new_string = str_[:(index + start)] + START_HIGHLIGHT + str_[(index + start):(index + start + len(substr))] + \
                    END_HIGHLIGHT + str_[start+len(substr):]
    
    return new_string

def load_all(path):
    print_box("Beginning flat Greek parser. \n \
        For each word a list of potential accented versions of the flat word will be shown. \n \
        When prompted, enter one of the given numbers to replace the original with the selected word.", style="bold")
    
    res = 0
    
    #try to load corpus, if failure print explanation and error and exit with code 1
    corpus_ = load_corpus()
    if corpus_ == 1:
        res = 1
    
    #try to create a timestamped file of the result
    try:
        time_ = datetime.datetime.now().strftime('%b-%d-%I%M%p-%G')
        suffix = 1
        suffix_str = ""
        while os.path.isfile("./parsed-" + time_ + suffix_str):
            suffix_str = " (" + str(suffix) + ")"
            suffix += 1
            
        new_file = open("./parsed-" + time_ + suffix_str, "w")
        
    except Exception, e:
        print_error(u"Failed to create ./parsed-" + time_ + " (" + str(suffix) + ")", e, u"Make sure you have write access" \
                    + "to the directory you are currently in.")
        res = 1
    
    #try to load the specified file
    try:
        file_ = open(path, "r").read()
    except Exception, e:
        print_error("Failed to load the specified file \""+ path + "\"", e, "Try checking " \
                    + "your present working directory (type 'pwd' into the shell) or typing " \
                    + "out the entire file path.")
        res = 1
    
    return res, corpus_, file_, new_file

def add_word(corpus, word):
    print_box("To add a word to the corpus, type in the correct " + \
              "word and hit enter. You will be prompted to confirm " + \
              "that the word is correct","Add to corpus")
    try:
        valid = 0
        err_str = ""
        while not valid:
            if err_str != "": print(err_str)
            new_word = raw_input("word? ")
            if len(new_word) != len(word):
                err_str = "The word you entered is not of the correct length."
            else:
                valid = 1
    except Exception, e:
        print_error("Something went wrong", e)
    
    if valid:
        corpus.add_to_corpus(new_word.decode("utf-8"))
        
def unicode_iterable_to_string(unicode_iterable):
    string_ = "[\n"
    for item in unicode_iterable:
        string_ += re.sub(r"([\n])", r'\\n', item) + ", \n"
         
    return string_[:-2] + "\n]"

def parse_file(path, verbose=False):
    choice, corpus_, file_, new_file = load_all(path)
    
    #decode the file from bytestring to unicode
    file_ = file_.decode("utf-8")
    
    #if errors occured
    if choice == 1:
        return choice
    
    #create parsed file variable to save changes to
    parsed_file = file_
    
    #build sentence regex
    sentence_regex = '|'.join(map(re.escape, [".", "?", "!"]))
    
    #split on sentence delimiters, keep track of current # if s != "\n"
    sentences = [s for s in re.split(sentence_regex, file_)]
        
    sentence_tot = len(sentences)
    current_sentence = 0
    
    #regex generation for splitting
    word_regex = '|'.join(map(re.escape, [" ", ",", "?", "!", "\"", "'", "\\", "/", ";", ":", "-"]))
    
    parsed_sentence = ""
    file_col = 0
    
    for sentence in sentences:
        sentence_col = 0
        
        #increment counter and set next sentence
        current_sentence += 1
        parsed_sentence = sentence
        
        #reset choice to None
        choice = None
        
        for word in re.split(word_regex, sentence):
                        
            #print line for clairity
            print_line("bold", width=120)
            
            #get pointer string
            colored_string = color_string(parsed_sentence, word, sentence_col)

            #get options and sort
            choices = lookup_word(corpus_, word)
            
            #reset choice to None
            choice = None
            
            #if we find matching words that aren't empty
            if choices is not None and (u'', 1.0) not in choices:
                
                #print sentence number, sentence, and line to keep things clear
                print_box(colored_string, title="Parsing sentence (" + str(current_sentence) + " of " + str(sentence_tot) + ")", pad=1)
                
                #loop until valid selection given
                error_string = ""
                done_with_word = False
                
                while done_with_word is False:
                    #print options
                    print(choices_string(word, choices))
                    
                    #get raw input and try to make int or command
                    error_string, choice = get_choice(choices)
                    
                    #if our choice is valid
                    if error_string is "":
                        
                        if isinstance(choice, str) and len(choice) != 1:
                            print(choice)
                            
                        if choice == 'q':
                            new_file.write(parsed_file.encode("utf-8"))
                            return 0
                        
                        elif choice == 'a':
                            add_word(corpus_, word)

                        #if our input is a number
                        try:
                            if not isinstance(choice, str):
                                #get chosen word for CWord item
                                chosen_word = choices[choice - 1][0]
                                
                                print("Replacing " + word + " with " + chosen_word + "\n")

                                #update parsed_sentence and parsed_file
                                parsed_sentence = parsed_sentence[:sentence_col] + \
                                    parsed_sentence[sentence_col:].replace(word, chosen_word, 1)
                                parsed_file = parsed_file[:file_col] + \
                                    parsed_file[file_col:].replace(word, chosen_word, 1)
                                
                                #move char pointer
                                sentence_col += len(word)
                                file_col += len(word) 
                                
                                done_with_word = True
                                
                        except KeyError:
                            print("derp")
                    else:                
                        sentence_col += len(word)
                        file_col += len(word)
                        print(error_string)

            else:
                #if it isn't a word, increment pointer anyway so we know which char we're on
                sentence_col += len(word)
                file_col += len(word)
            
            #to account for regex split
            sentence_col += 1
            file_col += 1
        
    new_file.write(parsed_file.encode("utf-8"))
                    
    corpus_file = open(CORPUS_LOCATION, "w")
    pickle.dump(corpus_, corpus_file)
            
    
        
#def repl():
#    print_box("Beginning flat Greek repl. When prompted, enter your flat greek word and press enter. \
#        Then enter one of the given numbers to replace the original with the selected word.\n")
#    corpus_ = load_corpus()
#    replaced_string = ""
#    
#    while True:
#        try:
#            word = raw_input("word? ").strip()
#            choice = ""
#            if word != "":
#                #get options and sort
#                choices = lookup_word(corpus_, word)
#                
#                #loop until valid selection given
#                while type(choice) != int or len(choices) < choice or choice < 1:
#                    try:
#                        err_str = ""
#                        #print options
#                        choices_string(choices)
#                        
#                        #get raw input and try to make int
#                        choice = raw_input("choice? ")
#                        choice = int(choice)
#
#                    #error checking
#                    except NameError:
#                        err_str = "Integers between 1 and " + str(len(choices)) + " please.\n"
#                    except ValueError:
#                        err_str = "Integers between 1 and " + str(len(choices)) + " please.\n"
#                        
#                    if choice == "q":
#                        return 0
#                        
#                    if choice < 1 or choice > len(choices):
#                        err_str = "Integers between 1 and " + str(len(choices)) + " please.\n"
#                        
#                    print(err_str)
#                    
#
#                    
#                print("Replacing " + word + " with " + choices[choice - 1][0].encode( 'utf-8', 'ignore' ) + "\n")
#        except KeyError:
#            print("Sorry, " + word + " was not found in the corpus.\n")
#        
def flatten_corpus():
    corpus_ = open("./corpus/01_gk.unicode").read().decode( 'utf-8', 'ignore' )
    flat = corpus.strip_accents(corpus_)
    return flat
    
def main():
    try:
        #_file = open("./corpus/flat_test","w")
        #_file.write(flatten_corpus().encode("utf-8", "ignore"))
        #parse_file("./corpus/flat_test")
        #repl()
        if len(sys.argv) == 2:
            res = parse_file(sys.argv[1])
            if res == 0:
                print_box("Shutdown requested. Writing to file and exiting.")
            elif res == 1:
                print_box("Unexpected error; quitting", title="❗")
        else:
            print("Error: wrong number of arguments")
            
    # if keyboard interupt print then quit (no traceback)
    except KeyboardInterrupt:
        print_box("Forcable shutdown requested...exiting",title="❗")
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)
    
if __name__ == "__main__":
    main()