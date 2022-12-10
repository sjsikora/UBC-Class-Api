def findInstancesOfTextBetweenText(text: str, start: str, end: str):
    instances = []
    while(True):

        indxStart = text.find(start)
        indxAfterStart = indxStart + len(start)
        stringAfterStart = text[indxAfterStart:]

        indxEndMod = stringAfterStart.find(end)
        trueindxEnd = len(text[:indxAfterStart]) + indxEndMod

        if indxStart == -1 or indxEndMod == -1:
            return instances        

        instances+= [text[indxAfterStart: trueindxEnd]]
        text = text[trueindxEnd + len(end):]


def findTextBetweenText(text: str, start: str, end: str):

    indxStart = text.find(start)
    indxAfterStart = indxStart + len(start)
    stringAfterStart = text[indxAfterStart:]

    indxEndMod = stringAfterStart.find(end)
    trueindxEnd = len(text[:indxAfterStart]) + indxEndMod

    if indxStart == -1 or indxEndMod == -1:
        return ''
    
    return text[indxAfterStart: trueindxEnd]