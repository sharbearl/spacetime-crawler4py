G_VALID_TOKEN_CHARACTERS = set(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 
 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 
 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 
 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', 
 '4', '5', '6', '7', '8', '9']) 

class TokenCounter:
    def __init__(self):
        self._counts = {}

    # Time complexity: O(1)
    # Explanation: Adding an entry to a python
    # dict runs in O(1) time. Finding the entry
    # and adding the associated value by amount
    # is also achieved in constant time since
    # python dicts are implemented as hash tables
    def addToken(self, word, amount = 1):
        if word in self._counts:
            self._counts[word] += amount
        else:
            self._counts[word] = amount
            
    # Time complexity: O(n) (n = len(words))
    # Explanation: We are calling addToken()
    # n times. Calling an O(1) operation n
    # times takes O(n) time
    def addTokensFromList(self, words):
        for word in words:
            self.addToken(word)
            
    # Time complexity: Time complexity: O(n) (n = len(words))
    # Explanation: We are calling addToken()
    # n times. Calling an O(1) operation n
    # times takes O(n) time
    def addTokensFromTokenCounter(self, words):
        for word, freq in words._counts.items():
            self.addToken(word, freq)

    def addTokensFromDict(self, words):
        for word, freq in words.items():
            self.addToken(word, freq)

    # Time complexity: O(1)
    # Explanation: Searching for and removing
    # an item in a python dict takes O(1) time
    def remove(self, word):
        if word not in self._counts:
            return
        del self._counts[word]
        
    # Time complexity: O(1)
    # Explanation: Just simply returns
    # the counts member variable. Because
    # it is returned by reference and not copied
    # over, it is done in constant time.
    def counts(self):
        return self._counts

# Time complexity: O(1)
# Explanation: Seeing if an object is in a python set
# takes O(1) time on average since python sets are implemented
# using hashing
def isPartOfToken(letter):
    return letter in G_VALID_TOKEN_CHARACTERS
    
def tokenize(text):
    # The main juice
    # The main sauce
    tokens = []
    curToken = []
    for curChar in text:
        # curChar is the current character we're reading here

        # if it's a valid character, add it to the current token
        if isPartOfToken(curChar):
            curToken.append(curChar)
            continue
        # if it's not a valid character, add what we have to the tokens
        # we only do this if curToken != "" though
        elif len(curToken):
            tokens.append("".join(curToken).lower())
            curToken = []
            continue
    # add one more time
    if len(curToken):
        tokens.append("".join(curToken).lower())
    return tokens

def computeWordFrequencies(tokens):
    ret = TokenCounter()
    ret.addTokensFromList(tokens)
    return ret

def printFrequencies(frequencies):
    toSort = [(token, freq) for token, freq in frequencies.items()]
    toSort.sort(key = lambda pair : pair[1], reverse = True)
    for token, freq in toSort:
        print(token, '\t', freq, sep='')
