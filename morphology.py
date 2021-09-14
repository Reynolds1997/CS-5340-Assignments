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
            morphResultFound = morphologicalAnalyzer(word, rulesList, resultWords, dictList,"")

        #If it's not in the dictionary and no morphological analysis result was found, output the default.
        if not foundInDictionary and not morphResultFound:
            resultWords.append(ResultWord(word,"noun",word,"default","-"))

                    
    
    prevWord = ""
    for word in resultWords:
        currentWord = word.word
        #print("CURRENT WORD: " + currentWord)
        #print("PREV WORD: " + prevWord)
        if currentWord != prevWord and prevWord != "": 
            print("")
        print("WORD=" +word.word + " " + "POS=" + word.pos + " " + "ROOT=" + word.root + " " + "SOURCE=" + word.source + " " + "PATH=" + word.path)
        prevWord = currentWord


def morphologicalAnalyzer(wordParam, rulesListParam, resultListParam, dictList,originID):
    resultFound = False

    for rule in rulesListParam:
        placeholderWord = wordParam
        placeholderPOS = ""
        ruleID = ""

        wordCapFound = False
        if(rule.keyword == "SUFFIX" and wordParam.lower().endswith(rule.chars.lower())):
            placeholderWord = wordParam.removesuffix(rule.chars)
            if(rule.replacementChars != "-"):
                placeholderWord = placeholderWord + rule.replacementChars 
            placeholderPOS = rule.posNew
            wordCapFound = True
        elif(rule.keyword == "PREFIX" and wordParam.lower().startswith(rule.chars.lower())):
            placeholderWord = wordParam.removeprefix(rule.chars)
            if(rule.replacementChars != "-"):
                placeholderWord = rule.replacementChars + placeholderWord
            placeholderPOS = rule.posNew
            wordCapFound = True

        if(wordCapFound):
            wordMatchFound = False
            for word in dictList:
                print("Original word: " + wordParam)
                print(placeholderWord + " vs " + word.word)
                print(placeholderPOS + " vs " + word.pos)
                if(word.word.lower() == placeholderWord.lower() and word.pos == placeholderPOS):
                    resultFound = True
                    if(originID != ""):
                        ruleID = originID+","+rule.id
                    else:
                        ruleID = rule.id
                    resultListParam.append(ResultWord(wordParam,rule.posNew,placeholderWord,"morphology",ruleID))
                    wordMatchFound = True
                    break
            if (wordMatchFound == False):
                #print(wordParam + " becomes " + placeholderWord)
                #print(placeholderWord + " vs " + word.word)
                #print(placeholderPOS + " vs " + word.pos)
                resultFound = morphologicalAnalyzer(placeholderWord.lower(),rulesListParam,resultListParam,dictList,rule.id)    

    return resultFound

   







    

        

main()