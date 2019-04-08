
import sys
import numpy as np
from collections import defaultdict

def referenceStr(reference):
    f = open(reference, 'r')
    first_line = True
    ref = ''
    for line in f:
        if first_line:
            first_line = False
            continue  # We skip the first line, since it
            # only contains the name of the chromosome the reads
            # came from.
        line = line.strip()
        ref += line  # We append each line to the output reference string.

    return ref

def referenceDict(ref):
    refDict = defaultdict(lambda: [])

    newElem = ref[0:10]
    newRef = ref[10:]

    refDict[newElem].append(0)

    pos = 1
    for element in newRef:
        newElem = newElem[1:]
        newElem += element
        refDict[newElem].append(pos)
        pos += 1

    return refDict

# opens the reads file and place them in a list
def splitReads(reads):
    f = open(reads).read().splitlines()

    tupleLst = []

    firstLine = True

    for lines in f:
        if firstLine:
            firstLine = False
            continue

        tupleLst.append(lines.split(',')[0])
        tupleLst.append(lines.split(',')[1])

    return tupleLst

def checkMatch(refStr, startStr, read):

    retVal = 0
    iStart = startStr

    quality = 0

    for i in range(0, 10): # this used to be 10 but doesnt work with 10, why?
        if refStr[iStart+i] == read[i]:
            quality += 1


    if quality >= 10: # can change this value to be more strict on the number of incorrect values
        retVal = 1

    return retVal

#
def checkDic(refStr, refDic, reads):

   qualityCheck = 0

   nucleotideArr = []

   for i in range(0, 9999):
       nucleotideArr.append([])

   counter = 0
   for readElem in reads:
       for i in range(0, 5):
           start = i * 10
           if readElem[start:start+10] in refDic:
               counter += 1
               readStart = refDic[readElem[start:start+10]][0] - i*10
               for k in range(0,50):
                   nucleotideArr[readStart+k].append(readElem[k])
               #for j in range(0, 5):
               #    jump = j*10
               #    qualityCheck += checkMatch(refStr, readStart+jump, readElem[jump:jump+10])

               break

   #print(counter)
   #print(nucleotideArr)
   return nucleotideArr



#def placePairs(refStr, refDic, readsTuples):

 #   return True


def largest(A, C, G, T):

    retVal = 'X'

    if A == 0 and C == 0 and G == 0 and T == 0:
        retVal = 'X'
    elif A >= C and A >= G and A >= T:
        retVal = 'A'
    elif C >= A and C >= G and C >= T:
        retVal = 'C'
    elif G >= A and G >= C and G >= T:
        retVal = 'G'
    elif  T >= A and T >= C and T >= G:
        retVal = 'T'

    return retVal


def findCommon(nucleotideArr):

    commonArr = []
    A = 0
    C = 0
    G = 0
    T = 0

    for elem in nucleotideArr:
        for nucleo in elem:
            if nucleo == 'A':
                A += 1
            elif nucleo == 'C':
                C += 1
            elif nucleo == 'G':
                G += 1
            elif nucleo == 'T':
                T += 1
        commonArr.append(largest(A, C , G, T))
        A = 0
        C = 0
        G = 0
        T = 0

    return commonArr


def findSNP(refStr, nucleotideArr):

    commonArr = findCommon(nucleotideArr)

    #SNP = []
    count = 0

    for i in range(0, len(refStr)): #len(refStr)
        if refStr[i] != commonArr[i]:
            count += 1
            #print(count)
            print(refStr[i] + ',' + commonArr[i] + ',' + str(i))



def main():
    reference = sys.argv[1]
    reads = sys.argv[2]

    refStr = referenceStr(reference)



    refDic = referenceDict(refStr)


    readLst = splitReads(reads) #this is a list

    nucleoArr = checkDic(refStr, refDic, readLst)

    #print(checkMatch("ACTGACTGGG", 0, "ACTGACTGTT"))

    print(len(refStr))
    print(len(readLst))

    print(findSNP(refStr, nucleoArr))

    #for i in range(0, 10):
     #   print(refStr[i])
      #  print(nucleoArr[i])

    #print(refDic)
    #print(reads)
    return




if __name__ == "__main__":
    main()