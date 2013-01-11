Your flat character input file must use greek characters from the Greek and Coptic block of Unicode.

Any sigma at the end of a word will automatically converted to a terminal sigma in the corpus. This means you need to input flat files that have terminal sigmas at the end, or the dictionary won't be able to find the word - this may be changed in the future so that greekify automatically checks both varients against the corpus, but as of the current release this isn't the case.
