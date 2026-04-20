from PIL import Image
from PIL import ImageDraw

img = Image.open('Full pattern until legs (Edited) (Edited) (Edited).png')

# Change the value of colors for number of colors desired
# The methods need more investigation if unhappy
# This simplifies an image by colour, but also returns an image object
# The raw image would not work for the palette situation
alteredImage = img.quantize(colors=6,method=2)

# This gets the palette from the image
colourList = alteredImage.getpalette()[:18]

# This turns the numbers into tuples so it's actually managable
colours = [tuple(colourList[i : i+3]) for i in range(0, len(colourList), 3)]

# This displays all the colours in the image
def display_palette(colors, swatch_size=50):
    # Create a long strip image to show all colors
    palette_img = Image.new("RGB", (len(colors) * swatch_size, swatch_size))
    draw = ImageDraw.Draw(palette_img)
    
    for i, color in enumerate(colors):
        draw.rectangle([i * swatch_size, 0, (i + 1) * swatch_size, swatch_size], fill=color)
    
    palette_img.show()

# display_palette(colours[:16])

# Creating a list of colour names, and a matrix of these
colourNames = ["aqua", "silver", "cobalt", "turquoise", "fushia", "mint"]
# colourMat = [colours, colourNames]
colourMap = dict(zip(colours, colourNames))

# Create required variables
width, height = alteredImage.size
prevColour = (-1, -1, -1)
currentCount = 0

# Create text document for pattern
# f = open("scales.txt", "x")
with open("scales.txt", "w") as f:
    f.write("Scales pattern:\n")

for y in range(height):
    with open ("scales.txt", "a") as f:
        f.write(f"Row {y+1}: ")

    for x in range(width):
        rgb = img.getpixel((x,y))
        rgbList = list(rgb)
        rgbList.pop(3)
        rgb = tuple(rgbList)

        if rgb == prevColour:
            currentCount = currentCount + 1
        else:
            if x != 0:
                colourName = colourMap[prevColour]
                with open ("scales.txt", "a") as f:
                    f.write(f"SC{currentCount} in {colourName}, ")
            
            currentCount = 1
            prevColour = rgb

    colourName = colourMap[prevColour]
    with open ("scales.txt", "a") as f:
        f.write(f"SC{currentCount} in {colourName}, ")
    
    with open ("scales.txt", "rb+") as f:
        f.seek(-2, 2)
        f.truncate()

    with open ("scales.txt", "a") as f:
        f.write(".\n")

