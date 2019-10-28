#import statements
import PIL.Image, PIL.ImageFont, PIL.ImageDraw, datetime, json

#fetch the screen size
screenSize = json.loads(str(open('screenSize.json').read()))
screenSize[0], screenSize[1] = int(screenSize[0]), int(screenSize[1])

#calculate the artistic vanishing point of the screen
vainishingPoint = [int(screenSize[0] / 2), int(screenSize[1] / 2)]

#create a function to calculate the edge of a line that is rotated at a certain degree

#function to create the image of the billboard that the time will be on (returns the path to the output)
def createBillboardImage(path) -> str:

    #fetch the global variables needed
    global screenSize, vanishingPoint

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
    billboardLegHeight = int(billboardSize[1] / 3)

    #create the border lines
    draw.rectangle([int(billboardTopCoords[0]), int(billboardTopCoords[1]), int(billboardTopCoords[0] + billboardSize[0]), int(billboardTopCoords[1] + billboardSize[1])], fill = colorAndBorderData['background'], outline = colorAndBorderData['border/legs'], width = colorAndBorderData['lineWidth'])
    draw.text([int(billboardTopCoords[0] + billboardTextPadding[0]), int(billboardTopCoords[1] + billboardTextPadding[1])], currentTime, colorAndBorderData['foreground'], font = font)

    #save the image
    image.save(path)

    #return the path to the output file
    return path

createBillboardImage('./outputs/billboard.png')