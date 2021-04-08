import sys
import os

from afunctions import *

lines = readFile("WSJ_02-21.pos")
emiTagWordDicDic, transiTagDicDic, wordInTrainList, wordTagTrainSequenceList = emissionTransitionTable(lines)
emiProbaTable, tranProbaTable = emiTranProbaTableFun(emiTagWordDicDic, transiTagDicDic, len(lines))
emitTranGrid = fowardPass(wordTagTrainSequenceList, wordInTrainList, emiProbaTable, tranProbaTable)

gridSequenceList = list(emitTranGrid)
gridSequenceList.sort(reverse=True)

tagSequence = []
for iC, seq in enumerate(gridSequenceList):
    tagColumn = emitTranGrid[seq]
    maxProbability = -999999999999999999
    maxTag = "???WanLim"
    currentTag = ""
    for ele in tagColumn:
        probability = tagColumn[ele]['probability']
        fromTag = tagColumn[ele]['from']
        if maxProbability < probability:
            maxProbability = probability
            maxTag = fromTag
        print("===>", ele)
    tagSequence.insert(0, maxTag)

# print(tagSequence)
