from PIL import Image, ImageOps
import json
import random as r
with open("Components.json", "r") as listJsonFile :
    jsonData = json.load(listJsonFile)

with open("Filters.json", "r") as filtersJsonFile :
    filtersData = json.load(filtersJsonFile)

def WeightOfRarity(rarity):
    switcher = {
        "common": 1,
        "uncommon": 0.75,
        "rare": 0.5,
        "epic": 0.2,
        "legendary": 0.05,
    }
    return switcher.get(rarity, 1)

def PointOfRarity(rarity):
    switcher = {
        "common": 0,
        "uncommon": 1,
        "rare": 2,
        "epic": 3,
        "legendary": 5,
    }
    return switcher.get(rarity, 1)

def IdOfRarity(id):
    switcher = {
        0: "Neutral",
        1: "Yellow",
        2: "Red",
        3: "Blue",
        4: "Broken",
        5: "Mutant",
    }
    return switcher.get(id, 0)

def AddImage(address, mirror=False, addToID=True, useSymmetry=False, useFilters=True):
    if symmetry == False :
        useSymmetry = False
    if not useSymmetry:

        weightList = []
        for component in address :
            rarity = WeightOfRarity(component["rarity"])
            weightList.append(rarity)
        
        item = ChoiceWithFilter(address, weightList, useFilters)

        category = GetCategoryOfComponentFromPath(item["path"])
        rarity = item["rarity"]
        type = item["type"]
        print(f"{category} : {rarity} ({type})")

        if symmetry and (address == jsonDetailsArm or address == jsonDetailsLeg):
            symmetryList.append(item)

        x = item["pos"]["x"]
        y = item["pos"]["y"]

        image = Image.open(item["path"])
        if mirror == True :
            image = ImageOps.mirror(image)
            x = 64 - x - image.width

        UpdatingImageList(image, x, y)
    else:
        item = symmetryList[0]
        symmetryList.remove(item)

        x = item["pos"]["x"]
        y = item["pos"]["y"]

        category = GetCategoryOfComponentFromPath(item["path"])
        rarity = item["rarity"]
        type = item["type"]
        print(f"{category} : {rarity} ({type})")

        image = Image.open(item["path"])
        image = ImageOps.mirror(image)
        x = 64 - x - image.width
        UpdatingImageList(image, x, y)

    if addToID:
        UpdateCyberID(address, item)
    AddPointToClass(item)
        
def UpdatingImageList(image, x, y):
    listOfImage.append(image)
    xListOfAnchor.append(x)
    yListOfAnchor.append(y)

def UpdateCyberID(address, item):
    index = address.index(item)
    rarity = item["rarity"]
    global cyberId
    cyberId =  cyberId + f"{index}{rarity[0]}"

def GetCategoryOfComponentFromPath(path):
    path2 = path.partition("/")[2]
    path3 = path2.partition("/")[2]
    path4 = path3.partition("/")[0]
    return path4

def AddPointToClass(item):
    global neutralPoint
    global yellowPoint
    global redPoint
    global bluePoint
    global brokenPoint
    global mutantPoint
    type = item["type"]
    numberOfPoints = PointOfRarity(item["rarity"])
    match type:
        case "neutral":
            neutralPoint += numberOfPoints
        case "yellow":
            yellowPoint += numberOfPoints
        case "red":
            redPoint += numberOfPoints
        case "blue":
            bluePoint += numberOfPoints
        case "broken":
            brokenPoint += numberOfPoints
        case "mutant":
            mutantPoint += numberOfPoints
        case _:
            neutralPoint += numberOfPoints

def ShowClassPoint():
    listOfPoint = [neutralPoint, yellowPoint, redPoint, bluePoint, brokenPoint, mutantPoint]
    i = 0
    for point in listOfPoint:
        if point != 0:
            print(f"{IdOfRarity(i)} : {point}")
        i += 1

def ChoiceWithFilter(address, weights, useFilters=True):
    correct = not useFilters
    choice = r.choices(address, weights=weights, k=1)
    item = choice[0]
    while not correct :
        choice = r.choices(address, weights=weights, k=1)
        item = choice[0]
        correct = CheckIncludeFilters(item)
    return item

def CheckIncludeFilters(item):
    check = True
    generalFilters = filtersData["Include"]["General"]
    rarities = generalFilters["rarities"]
    types = generalFilters["types"]
    if rarities:
        for rarity in rarities:
            if item["rarity"] == rarity:
                check = True
                break
            else :
                check = False
    if types:
        for type in types:
            if item["type"] == type:
                check = True
                break
            else : 
                check = False
    return check


#definition
symmetry = True

#do not touch
symmetryList = []
listOfImage = []
xListOfAnchor =[]
yListOfAnchor =[]

neutralPoint = 0
yellowPoint = 0
redPoint = 0
bluePoint = 0
brokenPoint = 0
mutantPoint = 0

cyberId = ""
if symmetry :
    cyberId = "S"
listOfFinalImage = []

#****************************************
jsonBackground = jsonData["Background"]
#****************************************
jsonBody = jsonData["Body"]

jsonHead = jsonBody["Head"]
jsonLeftArm = jsonBody["Left Arm"] 
jsonRightArm = jsonBody["Right Arm"]
jsonLeftLeg = jsonBody["Left Leg"] 
jsonRightLeg = jsonBody["Right Leg"]
#****************************************
jsonDetails = jsonData["Details"]

jsonDetailsEye = jsonDetails["Eye"]
jsonDetailsHead = jsonDetails["Head"]
jsonDetailsArm = jsonDetails["Arms"]
jsonDetailsLeg = jsonDetails["Legs"]



background = Image.open(jsonBackground[0])

#Creating Robot
AddImage(jsonHead, addToID=False, useFilters=False)
AddImage(jsonLeftArm, addToID=False, useFilters=False)
AddImage(jsonRightArm, addToID=False, useFilters=False)
AddImage(jsonLeftLeg, addToID=False, useFilters=False)
AddImage(jsonRightLeg, addToID=False, useFilters=False)

AddImage(jsonDetailsEye, useFilters=False)
AddImage(jsonDetailsHead)
AddImage(jsonDetailsHead)
AddImage(jsonDetailsHead)
AddImage(jsonDetailsArm)
AddImage(jsonDetailsArm)
AddImage(jsonDetailsLeg)
AddImage(jsonDetailsLeg)

AddImage(jsonDetailsArm, mirror=True, useSymmetry=True)
AddImage(jsonDetailsArm, mirror=True, useSymmetry=True)
AddImage(jsonDetailsLeg, mirror=True, useSymmetry=True)
AddImage(jsonDetailsLeg, mirror=True, useSymmetry=True)

print("id = " + cyberId)
ShowClassPoint()
iteration = 0
#Corps
for i in listOfImage :
    background.paste(i, (xListOfAnchor[iteration], yListOfAnchor[iteration]), i)
    iteration += 1
#Details




listOfFinalImage.append(background)
# listOfFinalImage[0] = listOfFinalImage[0].resize((320,320), Image.BICUBIC)
listOfFinalImage[0].save("Cyber.png", format="png")