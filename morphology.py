class DictWord:
    def __init__(self,word,pos,root):
        self.word = word
        self.pos = pos
        self.root = root

class MorphRule:
    def __init__(self,id,keyword,chars,replacementChars,posOriginal,posNew):
        self.id = id
        self.keyword = keyword
        self.chars = chars
        self.replacementChars = replacementChars
        self.posOriginal = posOriginal
        self.posNew = posNew

class ResultWord:
    def __init__(self,word,pos,root,source,path):
        self.word = word
        self.pos = pos
        self.root = root
        self.source = source
        self.path = path


def main():

    dictList = []
    
    rulesList = []

    import sys

    with open(sys.argv[1], 'r') as dictionaryFile:
        #print(dictionaryFile.read())
            # Get next line from file
        dictPath = sys.argv[1]
        
        while True:
            line = dictionaryFile.readline().strip()
            lineWordList = line.split()

            #print(str(lineWordList))
            if(lineWordList.__len__() > 0): #Ignore empty lines
                if(lineWordList.__len__() == 4):
                    dictList.append(DictWord(lineWordList[0],lineWordList[1],lineWordList[3]))
                else:
                    dictList.append(DictWord(lineWordList[0],lineWordList[1],None))
            #print(str(dictList[0].word))
            
            # if line is empty
            # end of file is reached
            if not line:
                break

    with open(sys.argv[2], 'r') as rulesFile:
        while True:
            line = rulesFile.readline().strip()
            lineWordList = line.split()

            #print(str(lineWordList))
            if(lineWordList.__len__() > 0): #Ignore empty lines
                rulesList.append(MorphRule(lineWordList[0],lineWordList[1],lineWordList[2],lineWordList[3],lineWordList[4],lineWordList[6]))
                
            #print(str(ruleList[0].keyword))
            
            # if line is empty
            # end of file is reached
            if not line:
                break

    wordsList = []
    with open(sys.argv[3], 'r') as wordsFile:
        while True:
            line = wordsFile.readline().strip()

            if(line.__len__()>0):
                wordsList.append(line)
                #print(line)

            if not line:
                break
    
    resultWords = []
    for word in wordsList:
        
        foundInDictionary = False
        morphResultFound = False

        #See if it's in the dictionary
        for dictWord in dictList:
            if(word.lower() == dictWord.word.lower()):
                foundInDictionary = True
                if(dictWord.root != None):
                    resultWords.append(ResultWord(word,dictWord.pos,dictWord.root,"dictionary","-"))
                else:
                    resultWords.append(ResultWord(word,dictWord.pos,dictWord.word,"dictionary","-"))

        #Perform morphological analysis if the word isn't in the dictionary
        if not foundInDictionary:
            morphResultFound = morphologicalAnalyzer(word, rulesList, resultWords, dictList)

        #If it's not in the dictionary and no morphological analysis result was found, output the default.
        if not foundInDictionary and not morphResultFound:
            resultWords.append(ResultWord(word,"noun",word,"default","-"))

                    
    

    for word in resultWords:
        print("WORD=" +word.word + " " + "POS=" + word.pos + " " + "ROOT=" + word.root + " " + "SOURCE=" + word.source + " " + "PATH=" + word.path)



def morphologicalAnalyzer(wordParam, rulesListParam, resultListParam, dictList):
    resultFound = False
    for rule in rulesListParam:
        placeholderWord = wordParam
        if(rule.keyword == "SUFFIX"):
            #print(wordParam)
            if(wordParam.lower().endswith(rule.chars)):
              #  print("LOOKING FOR SUFFIX: " + rule.chars)
                
                placeholderWord = wordParam.removesuffix(rule.chars)
                if(rule.replacementChars != "-"):
                    placeholderWord = placeholderWord + rule.replacementChars 
                #else:
                 #   placeholderWord = placeholderWord + rule.replacementChars 
                resultListParam.append(ResultWord(wordParam,rule.posNew,placeholderWord,"morphology",rule.id))
             #       morphologicalAnalyzer(placeholderWord,rulesListParam,resultListParam,dictList)
                resultFound = True
        elif(wordParam.lower().startswith(rule.chars)):
              #print("LOOKING FOR PREFIX: " + rule.chars)
            placeholderWord = wordParam.removeprefix(rule.chars)
            if(rule.replacementChars != "-"):
                placeholderWord = rule.replacementChars + placeholderWord
            #print(placeholderWord)
            resultListParam.append(ResultWord(wordParam,rule.posNew,placeholderWord,"morphology",rule.id))
            resultFound = True
            #morphologicalAnalyzer(placeholderWord,rulesListParam,resultListParam,dictList)
    return resultFound

        

main()