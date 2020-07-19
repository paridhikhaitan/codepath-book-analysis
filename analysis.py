import string
from collections import Counter
from collections import defaultdict
import heapq
import random
import re

class LittleWomen:
    def __init__(self):
        self.remove = str.maketrans(dict.fromkeys(string.punctuation))

    def readFile(self, file_name):
        file_obj = open(file_name, "r")
        data = file_obj.read().translate(self.remove)
        return data

    def getTotalNumberOfWords(self, file_name):
        data = self.readFile(file_name)
        total_words = data.lower().split()
        return len(total_words)

    def getTotalUniqueWords(self, file_name):
        data = self.readFile(file_name)
        unique_words = set(data.lower().split())
        return len(unique_words)

    def createWordHeap(self, file_name, interesting):
        data = self.readFile(file_name)
        word_frequency = Counter(data.lower().split())

        if interesting:
            common_file = open("100_common.txt", "r")
            common_words = set(common_file.read().lower().split())
            heap = []
            for key, value in word_frequency.items():
                if key not in common_words:
                    heap.append((value, key))
        else:
            heap = [(value, key) for key, value in word_frequency.items()]

        heapq.heapify(heap)
        return heap

    def get20MostFrequentWords(self, file_name):
        NUMBER_OF_ELEMENTS = 20
        heap = self.createWordHeap(file_name, False)
        return [[element[1], element[0]] for element in heapq.nlargest(NUMBER_OF_ELEMENTS, heap)]

    def get20MostInterestingFrequentWords(self, file_name):
        NUMBER_OF_ELEMENTS = 20
        heap = self.createWordHeap(file_name, True)
        return [[element[1], element[0]] for element in heapq.nlargest(NUMBER_OF_ELEMENTS, heap)]

    def get20LeastFrequentWords(self, file_name):
        NUMBER_OF_ELEMENTS = 20
        heap = self.createWordHeap(file_name, False)
        return [[element[1], element[0]] for element in heapq.nsmallest(NUMBER_OF_ELEMENTS, heap)]
    
    def getFrequencyOfWord(self, file_name, word):
        word = word.lower()
        data = self.readFile(file_name)
        chapter_split = data.split("CHAPTER")
        freq_of_word = [0]*len(chapter_split)
        for index, chapter in enumerate(chapter_split):
            all_words = chapter.lower().split()
            words_counter = Counter(all_words)
            freq_of_word[index] = words_counter[word]

        return freq_of_word

    def getChapterQuoteAppears(self, file_name, quote):
        quote = quote.translate(self.remove)
        data = self.readFile(file_name)

        chapter_split = data.split("CHAPTER")
        for index, chapter in enumerate(chapter_split):
            if quote in chapter:
                return index - 1
        
        return -1

    def generateSentence(self, file_name):
        data = self.readFile(file_name)
        all_words = data.split()
        word_dict = defaultdict(list)
        word_counter = Counter(all_words)

        for index in range(1, len(all_words)):

            prev_word = all_words[index-1]
            curr_word = all_words[index]
            curr_word_freq = (-word_counter[curr_word], curr_word)

            word_dict[prev_word].append(curr_word_freq)
        
        return self.createSentence("The", 20, word_dict)
    
    def createSentence(self, word, sentence_len, word_dict):
        sentence = []
        for i in range(sentence_len):
            sentence.append(word)
            next_word = heapq.heappop(word_dict[word])
            word = next_word[1]
        
        return " ".join(sentence)+"."

    def getAutocompleteSentence(self, file_name, start_sentence):
        file_object = open(file_name, "r")
        data = file_object.read()
        data = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)(\s|[A-Z].*)', data)
        self.root = TrieNode(-1)

        for sentence in data:
            self.createTree(sentence)
        
        self.allSentences(start_sentence)

    def createTree(self, sentence):
        temp = self.root

        for char in sentence:
            if char not in temp.children:
                temp.children[char] = TrieNode(char)
            temp = temp.children[char]
        
        temp.end_of_word = True
    
    def allSentences(self, start_sentence):

        temp = self.root
        result_sentences = []

        def getTree():
            temp = self.root
            for char in start_sentence:
                if char not in temp.children:
                    return False
                temp = temp.children[char]
            
        

        def remainingSentences(root, temp_sentence):
            if root.end_of_word == True:
                result_sentences.append(start_sentence+temp_sentence)
            
            for child in root.children:
                remainingSentences(root.children[child], temp_sentence+child)
        
        getTree()
        remainingSentences(temp, "")
        return result_sentences


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
print(little_women.getFrequencyOfWord("little_women.txt", "meg"))
print(little_women.getChapterQuoteAppears("little_women.txt", "If that's the way he's going to grow up, I wish he'd stay a boy"))
print(little_women.generateSentence("little_women.txt"))
print(little_women.getAutocompleteSentence("little_women.txt", "\"It's"))