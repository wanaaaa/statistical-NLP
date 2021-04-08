import sys
import os

from afunctions import *

lines = readFile("WSJ_02-21.pos")
emiTagWordDicDic, transiTagDicDic, wordInTrainList, wordTagSequenceList = emissionTransitionTable(lines)

emiProbaTable, tranProbaTable = emiTranProbaTableFun(emiTagWordDicDic, transiTagDicDic, len(lines))

# print(emiProbaTable)
emitTranGrid = {}
for iC, wordTag in enumerate(wordTagSequenceList):
    observedWord = list(wordTag)[0]
    # print(iC, wordTag, observedWord)
    emitTranGrid[iC] = {}
    if observedWord in wordInTrainList == False:
        print("unseen word==========================>>>>>>>>>")
        break
    if iC == 0:
        for iCC, tagInEmi in enumerate(emiProbaTable):
            iniTranPro = tranProbaTable[tagInEmi]["initPro###WanLim"]
            # print("****>>",observedWord, tagInEmi, emiProbaTable[tagInEmi])
            if observedWord in emiProbaTable[tagInEmi].keys():
                emiPro = emiProbaTable[tagInEmi][observedWord]
                # print("asdasd==>", observedWord, tagInEmi)
            else:
                emiPro = 0
            finalPro = iniTranPro*emiPro
            temDic = {}
            temDic["probability"] = finalPro
            temDic["from"] = "no"
            emitTranGrid[iC][tagInEmi] = temDic
            # print("---->", emitTranGrid[iC])
        # print(emitTranGrid)
        continue

    for iCC, currentTag in enumerate(emiProbaTable):
        maxPro = -99999999999
        maxProTag = "WanLim"
        for iCCC, previousTag in enumerate(emiProbaTable):
            print("ASDFASDF===>",iC, currentTag, previousTag,  emitTranGrid[iC -1][previousTag])
            preTagPro = emitTranGrid[iC -1][previousTag]["probability"]
            if currentTag in tranProbaTable[previousTag].keys():
                preTagTranPro = tranProbaTable[previousTag][currentTag]
            else:
                preTagTranPro = 0
            transitPro = preTagPro * preTagTranPro
            if transitPro > maxPro:
                maxPro = transitPro
                maxProTag = previousTag
        # print("asdasdf--->", currentTag, observedWord)
        if observedWord in emiProbaTable[currentTag]:
            emiPro = emiProbaTable[currentTag][observedWord]
        else:
            emiPro = 0

        temDic = {}
        # temDic["probability"] = maxPro*emiPro
        temDic["probability"] = maxPro*emiPro*1000
        temDic["from"] = maxProTag
        emitTranGrid[iC][currentTag] = temDic
        # emitTranGrid[iC][currentTag] = maxPro*emiPro
    print("====>",iC, emitTranGrid[iC])

    if iC == 10:
        break

# for key in emitTranGrid:
#     print(key, emitTranGrid[key])
