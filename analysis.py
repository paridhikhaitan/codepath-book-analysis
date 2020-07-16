import string
from collections import Counter
import heapq

class LittleWomen:
    def __init__(self):
        self.remove = str.maketrans(dict.fromkeys(string.punctuation))

    def readFile(self, file_name):
        file_obj = open(file_name, "r")
        data = file_obj.read().translate(self.remove)
        return data.lower()

    def getTotalNumberOfWords(self, file_name):
        data = self.readFile(file_name)
        total_words = data.split()
        return len(total_words)

    def getTotalUniqueWords(self, file_name):
        data = self.readFile(file_name)
        unique_words = set(data.split())
        return len(unique_words)

    def createWordHeap(self, file_name):
        data = self.readFile(file_name)
        word_frequency = Counter(data.split())
        heap = []

        for key, value in word_frequency.items():
            heapq.heappush(heap, (value, key))
        
        return heap

    def get20MostFrequentWords(self, file_name):
        NUMBER_OF_ELEMENTS = 20
        heap = self.createWordHeap(file_name)
        return [[element[1], element[0]] for element in heapq.nlargest(NUMBER_OF_ELEMENTS, heap)]

    def get20MostInterestingFrequentWords(self, file_name):
        common_file = open("100_common.txt", "r")
        common_words = set(common_file.read().split())
        data = self.readFile(file_name)
        word_frequency = Counter(data.split())
        NUMBER_OF_ELEMENTS = 20
        heap = []

        for key, value in word_frequency.items():
            if key not in common_words:
                heapq.heappush(heap, (value, key))
        
        return [[element[1], element[0]] for element in heapq.nlargest(NUMBER_OF_ELEMENTS, heap)]

    def get20LeastFrequentWords(self, file_name):
        NUMBER_OF_ELEMENTS = 20
        heap = self.createWordHeap(file_name)
        return [[element[1], element[0]] for element in heapq.nsmallest(NUMBER_OF_ELEMENTS, heap)]
    
    def getFrequencyOfWord(self, file_name):
        data = self.readFile(file_name)
        chapter_split = data.split("chapter")
        print(chapter_split)
        return

little_women = LittleWomen()
# print(little_women.getTotalNumberOfWords("little_women.txt"))
# print(little_women.getTotalUniqueWords("little_women.txt"))
# print(little_women.get20MostFrequentWords("little_women.txt"))
#print(little_women.get20MostInterestingFrequentWords("little_women.txt"))
print(little_women.get20LeastFrequentWords("little_women.txt"))
print(little_women.getFrequencyOfWord("little_women.txt"))
