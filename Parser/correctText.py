def GetName(line:str):
    name = ""
    isName = False
    for i in line:
        if(i == "»"):
            isName = False
            return name
        if(isName):
            name += i
        if(i == "«"):
            isName = True
        
    return None 

def removeWhitespaace(line:str, character:str = " "):
    words = line.split(character)
    result = "".join(words)
    return result

def removePrefix(line: str):
    result = ""
    for i in range(len(line)):
        k = len(line) - i - 1
        if line[k] == "/":
            result = line[-i:]
            break
    return "bcitcobject/" + result

    






            