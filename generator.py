# -*- coding: utf-8 -*-


import re
from scipy import stats
from collections import Counter
import nltk

from importer import main as impmain


def Bigram(line):
    '''
    Creates tuples for bigram model. 
    
    Parameters: 
        line (str): String from which to generate the tuples. 
        
    Returns:
        tuples (arr): An array containing bigrams created from the line input. 
    '''
    tuples = []
    for i in range(len(line) - 1):
        tuples.append((line[i], line[i + 1]))
    return tuples


def globalize():
    '''
    Creates global variables for ease of access and generation while the program 
    is running. Also creates the bigram and trigram models for generation. 
    '''
    global mcr_minicorpus
    global mcr_bigrams
    global mcr_bg_count
    global bigram_freqs
    global bigram_cfd
    global bigram_pbs
    global mcr_trigrams
    global trigrams_freqs
    global trigram_cfd
    global trigram_pbs

    mcr_minicorpus = impmain()

    unigram_counts = Counter(mcr_minicorpus)

    mcr_bigrams = []

    mcr_bigrams += Bigram(mcr_minicorpus)
    mcr_bg_count = Counter(mcr_bigrams)

    bigram_freqs = nltk.FreqDist(mcr_bigrams)
    bigram_cfd = nltk.ConditionalFreqDist(mcr_bigrams)
    bigram_pbs = nltk.ConditionalProbDist(bigram_cfd, nltk.MLEProbDist)

    mcr_trigrams = [((mcr_minicorpus[i], mcr_minicorpus[i + 1]), mcr_minicorpus[i + 2]) for i in
                    range(len(mcr_minicorpus) - 2)]

    trigrams_freqs = nltk.FreqDist(mcr_trigrams)
    trigram_cfd = nltk.ConditionalFreqDist(mcr_trigrams)
    trigram_pbs = nltk.ConditionalProbDist(trigram_cfd, nltk.MLEProbDist)
    pass


def bigen(size, end):
    '''
    Generates lines based on bigram model. 
    
    Parameters:
        size (int): The number of words to be generated using the bigram model. 
        Method may generate more words if the second parameter is set to True. 
        end (bool): A boolean parameter to determine when the generation should stop. 
        If set to True, the method will keep generating words after the determined
        length is reached until </s> symbol is encountered. 
    Returns:
        res (str): Resulting lyrics generated using the bigram model. 
    '''
    current_word = "<s>"
    res = " "
    for i in range(size):
        probable_words = list(bigram_pbs[current_word].samples())
        word_probabilities = [bigram_pbs[current_word].prob(word) for word in probable_words]
        result = stats.multinomial.rvs(1, word_probabilities)
        index_of_probable_word = list(result).index(1)
        current_word = probable_words[index_of_probable_word]
        res = res + current_word + " "
    if (end):
        while current_word != "</s>":
            probable_words = list(bigram_pbs[current_word].samples())
            word_probabilities = [bigram_pbs[current_word].prob(word) for word in probable_words]
            result = stats.multinomial.rvs(1, word_probabilities)
            index_of_probable_word = list(result).index(1)
            current_word = probable_words[index_of_probable_word]
            res = res + current_word + " "
    res = re.sub("(<s>)* </s> (<s>)*", "\n", res)
    return res


def initialize():
    '''
    Creates the first element of the tuple to initialize trigram generation. 
    
    Returns: 
        inittuple (tuple): Tuple where the first element is <s> and the second
        element is generated using the bigram model. 
    '''
    probable_words = list(bigram_pbs["<s>"].samples())
    word_probabilities = [bigram_pbs["<s>"].prob(word) for word in probable_words]
    result = stats.multinomial.rvs(1, word_probabilities)
    index_of_probable_word = list(result).index(1)
    inittuple = ("<s>", probable_words[index_of_probable_word])
    return inittuple


def trigen(size, end):
    '''
    Generates lines based on trigram model. Uses bigram model to generate the first
    word to allow trigram generation. 
    
    Parameters:
        size (int): The number of words to be generated using the trigram model. 
        Method may generate more words if the second parameter is set to True. 
        end (bool): A boolean parameter to determine when the generation should stop. 
        If set to True, the method will keep generating words after the determined
        length is reached until </s> symbol is encountered. 
    Returns:
        res (str): Resulting lyrics generated using the trigram model. 
    '''
    curr_tuple = initialize()
    res = " "
    for i in range(size):
        probable_words = list(trigram_pbs[curr_tuple].samples())
        word_probabilities = [trigram_pbs[curr_tuple].prob(word) for word in probable_words]
        result = stats.multinomial.rvs(1, word_probabilities)
        index_of_probable_word = list(result).index(1)
        curr_tuple = (curr_tuple[1], probable_words[index_of_probable_word])
        res = res + curr_tuple[1] + " "
    if (end):
        while curr_tuple[1] != "</s>":
            probable_words = list(trigram_pbs[curr_tuple].samples())
            word_probabilities = [trigram_pbs[curr_tuple].prob(word) for word in probable_words]
            result = stats.multinomial.rvs(1, word_probabilities)
            index_of_probable_word = list(result).index(1)
            curr_tuple = (curr_tuple[1], probable_words[index_of_probable_word])
            res = res + curr_tuple[1] + " "

    res = re.sub("(<s>)* </s> (<s>)*", "\n", res)
    return res


def generator():
    '''
    Creates a song using bigram and trigram models. 
    Bigram and trigram usage as well as generation length is chosen arbitrarily. This can
    be used to receive input from the user in the future to generate a song accordingly. 
    
    Returns:
        res (str): Resulting lyrics generated using bigram and trigram models. 
    '''
    res = ""
    s_name = trigen(2, True)
    s_chorus = trigen(5, False)
    res += s_name[0:-1] + ", a song by My Computational Romance \n\n" + trigen(5, True)
    for i in range(3):
        res += "\n" + s_chorus + "\n" + trigen(10, True)
    res += bigen(2, True)
    return res


def main():
    return generator()
