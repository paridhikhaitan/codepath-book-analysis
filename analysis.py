from __future__ import unicode_literals, print_function
# from spacy.lang.en import English # updated
import string
from collections import Counter
from collections import defaultdict
import heapq
import random
import re
import nltk

# Uncomment this if you need to download nltk
'''
I tried to use both nltk which is a Python library and
Regex to see the difference in how well they clear strings
'''
# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download()

from nltk import sent_tokenize


class LittleWomen:
    def __init__(self):
        self.remove = str.maketrans(dict.fromkeys(string.punctuation))

    # @param : file_name - name of the book
    # @return : the whole book as a string
    #
    # Function opens an external file and reads it
    def readFile(self, file_name):
        file_obj = open(file_name, "r")
        data = file_obj.read().translate(self.remove)
        file_obj.close()
        return data

    # @param : file_name - name of the book
    # @return : Total number of words in the book
    #
    # Function converts the book into an array of words
    # and returns the length of the array
    def getTotalNumberOfWords(self, file_name):
        data = self.readFile(file_name)
        total_words = data.lower().split()
        return len(total_words)

    # @param : file_name - name of the book
    # @return : Unique words in the book
    #
    # Stores all the words from the book in a set
    # which eliminates duplicate values

    def getTotalUniqueWords(self, file_name):
        data = self.readFile(file_name)
        unique_words = set(data.lower().split())
        return len(unique_words)

    # @param : file_name - name of the book
    #          interesting - flag to indicate if searching for interesting words
    # @return : Heap from the given word array
    #
    # Helper function that creates a word heap in O(n) time using heapify

    def createWordHeap(self, file_name, interesting):
        data = self.readFile(file_name)
        word_frequency = Counter(data.lower().split())

        if interesting:
            common_file = open("100_common.txt", "r")
            common_words = set(common_file.read().lower().split())
            common_file.close()
            heap = []
            for key, value in word_frequency.items():
                if key not in common_words:
                    heap.append((value, key))
        else:
            heap = [(value, key) for key, value in word_frequency.items()]

        heapq.heapify(heap)
        return heap

    # @param : file_name - name of the file
    # @return : Array of the most frequent words
    #
    # Creates a heap from all the words and returns the 20 most frequent ones
    def get20MostFrequentWords(self, file_name):
        NUMBER_OF_ELEMENTS = 20
        heap = self.createWordHeap(file_name, False)
        return [[element[1], element[0]] for element in heapq.nlargest(NUMBER_OF_ELEMENTS, heap)]

    # @param : file_name - name of the file
    # @return : Array of the most interesting frequent words
    #
    # Creates a heap from all the words and uses the list of 100_common
    # words to eliminate uninteresting ones
    def get20MostInterestingFrequentWords(self, file_name):
        NUMBER_OF_ELEMENTS = 20
        heap = self.createWordHeap(file_name, True)
        return [[element[1], element[0]] for element in heapq.nlargest(NUMBER_OF_ELEMENTS, heap)]

    # @param : file_name - name of the file
    # @return : Array of the least frequent words
    #
    # Creates a heap from all the words and returns the 20 least frequent ones
    def get20LeastFrequentWords(self, file_name):
        NUMBER_OF_ELEMENTS = 20
        heap = self.createWordHeap(file_name, False)
        return [[element[1], element[0]] for element in heapq.nsmallest(NUMBER_OF_ELEMENTS, heap)]

    # @param : file_name - name of the file
    #           word - to search for frequency
    # @return : Array of occurrence of a word by chapter
    #
    # Splits the data based on "CHAPTER" and then uses a dictionary to
    # find the frequency of words in that given chapter and appends
    # to return
    def getFrequencyOfWord(self, file_name, word):
        word = word.lower()
        data = self.readFile(file_name)
        chapter_split = data.split("CHAPTER")
        freq_of_word = [0]*(len(chapter_split)-1)
        for index, chapter in enumerate(chapter_split):
            all_words = chapter.lower().split()
            words_counter = Counter(all_words)
            freq_of_word[index-1] = words_counter[word]

        return freq_of_word

    # @param : file_name - name of the file
    #           quote - to search for in the chapters
    # @return : Chapter the quote is found in
    #           -1 if quote is not found
    #
    # Splits the data based on chapter and searches for the
    # quote in each chapter
    def getChapterQuoteAppears(self, file_name, quote):
        quote = quote.translate(self.remove)
        data = self.readFile(file_name)

        chapter_split = data.split("CHAPTER")
        for index, chapter in enumerate(chapter_split):
            if quote in chapter:
                return index - 1

        return -1

    # @param : file_name - name of the file
    # @return : String of 20 words in authors style
    #
    # Creates a mapping of current_word to (previous_word, occurrence)
    # And uses heap to pop out the word that is most common
    def generateSentence(self, file_name):
        data = self.readFile(file_name)
        all_words = data.lower().split()
        word_dict = defaultdict(list)
        word_counter = Counter(all_words)

        for index in range(1, len(all_words)):

            prev_word = all_words[index-1]
            curr_word = all_words[index]
            curr_word_freq = (-word_counter[curr_word], curr_word)

            word_dict[prev_word].append(curr_word_freq)

        return self.createSentence("the", 20, word_dict)

    # @param : file_name - name of the file
    # @return : String of 20 words in authors style
    #
    # Helper function to create heap and pop from it
    # and sets the next word based on previous word
    def createSentence(self, word, sentence_len, word_dict):
        sentence = []

        common_file = open("100_common.txt", "r")
        common_words = set(common_file.read().lower().split())
        common_file.close()

        for i in range(sentence_len):
            sentence.append(word)
            temp = word_dict[word]
            next_word = heapq.heappop(temp)
            word = next_word[1]

        return " ".join(sentence)+"."

    # @param : file_name - name of the file
    #           start_sentence - Starting quote 
    # @return : List of all sentences in the book
    #
    # Uses nltk to split the data into sentences.
    # Creates a Trie for all the sentences
    # Finds each autocomplete sentence and pushes it to the array
    def getAutocompleteSentence(self, file_name, start_sentence):
        file_object = open(file_name, "r")
        data = file_object.read()
        # From nltk used to convert the data into sentences
        data = sent_tokenize(data)
        self.root = TrieNode(-1)

        for index, sentence in enumerate(data):
            # sentence = sentence.replace("\n", " ")
            if len(sentence) != 0:
                self.createTree(sentence)

        return self.allSentences(start_sentence)

    # @param : sentence - To be added to the Trie
    # @return : None
    #
    # Adds each sentence to the Trie
    def createTree(self, sentence):
        temp = self.root

        for char in sentence:
            if char not in temp.children:
                temp.children[char] = TrieNode(char)
            temp = temp.children[char]

        temp.end_of_word = True

    # @param : start_sentence - Starting quote 
    # @return : Array of all the sentences
    #           String if no starting quote
    #
    # Helper function to find all the sentences in the Trie
    def allSentences(self, start_sentence):

        def getTree():
            temp = self.root
            for char in start_sentence:
                if char in temp.children:
                    temp = temp.children[char]
                else:
                    return -1

            return temp

        all_sentences = []

        def allSentences(root, sentence):
            if root.end_of_word == True:
                all_sentences.append(start_sentence + sentence)
            
            for char in root.children:
                allSentences(root.children[char], sentence + char)

        reduced_root = getTree()

        if reduced_root != -1:
            allSentences(reduced_root, "")
            return all_sentences

        return "No sentences that start with that!"
        

#Trie Class
class TrieNode:
    def __init__(self, val):
        self.children = {}
        self.val = val
        self.end_of_word = False


little_women = LittleWomen()
print(little_women.getTotalNumberOfWords("little_women.txt"))
print(little_women.getTotalUniqueWords("little_women.txt"))
print(little_women.get20MostFrequentWords("little_women.txt"))
print(little_women.get20MostInterestingFrequentWords("little_women.txt"))
print(little_women.get20LeastFrequentWords("little_women.txt"))
print(little_women.getFrequencyOfWord("little_women.txt", "Meg"))
print(little_women.getChapterQuoteAppears("little_women.txt", "If that's the way he's going to grow up, I wish he'd stay a boy"))
print(little_women.generateSentence("little_women.txt"))
print(little_women.getAutocompleteSentence("little_women.txt", "I can't get"))
