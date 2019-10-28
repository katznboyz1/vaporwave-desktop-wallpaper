#import statements
import PIL.Image, PIL.ImageFont, PIL.ImageDraw, datetime, json, random

#fetch the screen size
screenSize = json.loads(str(open('screenSize.json').read()))
screenSize[0], screenSize[1] = int(screenSize[0]), int(screenSize[1])

#calculate the artistic vanishing point of the screen
vanishingPoint = [int(screenSize[0] / 2), int(screenSize[1] / 2)]

#create a dictionary containing the colors for each time of the day
terrainAndSkyTimeColors = {
    'night':{
        'terrainColor':(63, 16, 120, 255),
        'terrainBorderColor':(27, 7, 51, 255),
    },
    'sunrise':{
        'terrainColor':(189, 43, 77, 255),
        'terrainBorderColor':(82, 19, 33, 255),
    },
    'day':{
        'terrainColor':(156, 12, 141, 255),
        'terrainBorderColor':(77, 7, 69, 255),
    },
    'sunset':{
        'terrainColor':(255, 105, 41, 255),
        'terrainBorderColor':(130, 55, 23, 255),
    }
}

#function to create the image of the billboard that the time will be on (returns the path to the output)
def createBillboardImage(path) -> str:

    #fetch the global variables needed
    global screenSize

    #convert the path variable to a string just in case something else is passed
    path = str(path)

    #create the new image, drawing surface, and font(s)
    image = PIL.Image.new('RGBA', screenSize, (0, 0, 0, 0))
    draw = PIL.ImageDraw.Draw(image)
    font = PIL.ImageFont.truetype('digital.ttf', int(screenSize[1] / 10))

    #get the time
    currentTime = datetime.datetime.now()
    currentTime = str(currentTime.strftime('%H:%M - %m/%d/%y'))
    
    #set the color data
    colorAndBorderData = {
        'border/legs':(20, 20, 20, 255), #for the border of the sign and the legs
        'background':(26, 0, 13, 255), #the background color of the sign behind the text
        'foreground':(191, 247, 255, 255), #the color of the text
        'lineWidth':5, #the line width of the border/legs in pixels
    }

    #calculate the text size for sizing the sign
    textSize = draw.textsize(currentTime, font)
    
    #calculate the topX, topY, width, height, textPaddingX, and textPaddingY of the billboard border
    billboardTextPadding = [int(screenSize[0] / 25), int(screenSize[0] / 25)]
    billboardSize = [int(textSize[0] + (billboardTextPadding[0] * 2)), int(textSize[1] + (billboardTextPadding[1] * 2))]
    billboardTopCoords = [int((screenSize[0] - billboardSize[0]) / 2), int((screenSize[1] - billboardSize[1]) / 3)]
    billboardLegHeight = int(billboardSize[1] / 1.5)
    billboardTextLegPositionsX = [int(billboardSize[0] / 4), int((billboardSize[0] / 4) * 3)]

    #create the border lines and sign background
    draw.rectangle([int(billboardTopCoords[0]), int(billboardTopCoords[1]), int(billboardTopCoords[0] + billboardSize[0]), int(billboardTopCoords[1] + billboardSize[1])], fill = colorAndBorderData['background'], outline = colorAndBorderData['border/legs'], width = colorAndBorderData['lineWidth'])
    
    #draw the sign legs
    draw.line([int(billboardTopCoords[0] + billboardTextLegPositionsX[0]), int(billboardTopCoords[1] + billboardSize[1]), int(billboardTopCoords[0] + billboardTextLegPositionsX[0]), int(billboardTopCoords[1] + billboardSize[1] + billboardLegHeight)], fill = colorAndBorderData['border/legs'], width = colorAndBorderData['lineWidth'])
    draw.line([int(billboardTopCoords[0] + billboardTextLegPositionsX[1]), int(billboardTopCoords[1] + billboardSize[1]), int(billboardTopCoords[0] + billboardTextLegPositionsX[1]), int(billboardTopCoords[1] + billboardSize[1] + billboardLegHeight)], fill = colorAndBorderData['border/legs'], width = colorAndBorderData['lineWidth'])

    #draw the text
    draw.text([int(billboardTopCoords[0] + billboardTextPadding[0]), int(billboardTopCoords[1] + billboardTextPadding[1])], currentTime, colorAndBorderData['foreground'], font = font)

    #crop the image to be just as big as the sign
    image = image.crop([int(billboardTopCoords[0] - billboardTextPadding[0]), int(billboardTopCoords[1] - billboardTextPadding[1]), int(billboardTopCoords[0] + billboardTextPadding[0] + billboardSize[0]), int(billboardTopCoords[1] + billboardTextPadding[1] + billboardSize[1] + billboardLegHeight)])

    #save the image
    image.save(path)

    #return the path to the output file
    return path

#function to create the ground and road
def createTerrainImage(path, timeOfDay) -> str:

    #fetch the global varilables eneded
    global screenSize, vanishingPoint, terrainAndSkyTimeColors

    #convert the path variable into a string just in case something else is passed
    path = str(path)

    #create the new image, drawing surface, and font(s)
    image = PIL.Image.new('RGBA', screenSize, (0, 0, 0, 0))
    draw = PIL.ImageDraw.Draw(image)
    font = PIL.ImageFont.truetype('digital.ttf', int(screenSize[1] / 10))

    #create the bounds for the mountain generation [STEPS, MAX_MOUNTAIN_GENERATION_STEP_LEFT, MIN_MOUNTAIN_GENERATION_RIGHT]
    groundLessThanGreaterThanMountainBounds = [20, 7, 13]

    #create the ground that is before the horizon with mountains from left to right
    groundPolygonVerticesTop = []
    for step in range(groundLessThanGreaterThanMountainBounds[0] + 1):
        xCoord, yCoord = int(((screenSize[0]) / 20) * step), vanishingPoint[1]
        if (step < groundLessThanGreaterThanMountainBounds[1] or step > groundLessThanGreaterThanMountainBounds[2]):
            yCoord = random.randint(int(screenSize[0] / 6), int(vanishingPoint[1]))
        else:
            pass
        groundPolygonVerticesTop.append((int(xCoord), int(yCoord)))

    #create the bottom of the ground polygon [LEFT_BOTTOM, RIGHT_BOTTOM]
    groundPolygonVerticesBottom = [(int(0), int(screenSize[1])), (int(screenSize[0]), int(screenSize[1]))]

    #get the colors for the terrain
    terrainColor = terrainAndSkyTimeColors[timeOfDay]['terrainColor']
    terrainBorderColor = terrainAndSkyTimeColors[timeOfDay]['terrainBorderColor']

    #draw the terrain polygon
    draw.polygon([groundPolygonVerticesBottom[0], *groundPolygonVerticesTop, groundPolygonVerticesBottom[1]], outline = terrainColor, fill = terrainColor)

    #draw the terrain top border
    draw.line(groundPolygonVerticesTop, fill = terrainBorderColor, width = 3)

    #coords for the bottom and top edges and center of the road [RIGHT, MIDDLE, LEFT]
    roadLineMarksWidthTop = int(screenSize[0] / 120)
    roadLineMarksWidthBottom = int(screenSize[0] / 4)
    roadLineMarksTop = [int((screenSize[0] / 2) - roadLineMarksWidthTop), int(screenSize[0] / 2), int((screenSize[0] / 2) + roadLineMarksWidthTop)]
    roadLineMarksBottom = [int((screenSize[0] / 2) - roadLineMarksWidthBottom), int(screenSize[0] / 2), int((screenSize[0] / 2) + roadLineMarksWidthBottom)]

    #draw the polygon for the road
    roadColor = (48, 48, 48, 255)
    draw.polygon([(int(roadLineMarksBottom[0]), int(screenSize[1])), (int(roadLineMarksTop[0]), int(vanishingPoint[1])), (int(roadLineMarksTop[-1]), int(vanishingPoint[1])), (int(roadLineMarksBottom[-1]), int(screenSize[1]))], outline = roadColor, fill = roadColor)

    #draw the lines for the road
    for line in range(len(roadLineMarksTop)):
        lineColor = (0, 0, 0, 255)
        if (line == 1):
            lineColor = (173, 162, 9, 255)
        draw.line([(roadLineMarksTop[line], vanishingPoint[1]), (roadLineMarksBottom[line], screenSize[1])], fill = lineColor, width = 2)

    #save the image
    image.save(path)

    #return the path to the output file
    return path

#calculate the time of day
timeOfDay = 'day' #keep fixed for testing versions

#generate the images
billboardImagePath = createBillboardImage('./outputs/billboard.png')
terrainImagePath = createTerrainImage('./outputs/terrain.png', timeOfDay)