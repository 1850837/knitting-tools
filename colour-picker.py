# from PIL import Image
# from PIL import ImageDraw

# img = Image.open('Full pattern but wider this time.png')
# # img.show()

# # Change the value of colors for number of colors desired
# # The methods need more investigation if unhappy
# # This simplifies an image by colour, but also returns an image object
# # The raw image would not work for the palette situation
# alteredImage = img.quantize(colors=6,method=2)
# # alteredImage.show()

# # This gets the palette from the image
# colourList = alteredImage.getpalette()[:18]

# # This turns the numbers into tuples so it's actually managable
# colours = [tuple(colourList[i : i+3]) for i in range(0, len(colourList), 3)]

# # This displays all the colours in the image
# def display_palette(colors, swatch_size=50):
#     # Create a long strip image to show all colors
#     palette_img = Image.new("RGB", (len(colors) * swatch_size, swatch_size))
#     draw = ImageDraw.Draw(palette_img)
    
#     for i, color in enumerate(colors):
#         draw.rectangle([i * swatch_size, 0, (i + 1) * swatch_size, swatch_size], fill=color)
    
#     palette_img.show()

# # display_palette(colours[:16])

# # Creating a list of colour names, and a matrix of these
# colourNames = ["aqua", "silver", "cobalt", "turquoise", "fushia", "mint"]
# # colourMat = [colours, colourNames]
# colourMap = dict(zip(colours, colourNames))

# # Create required variables
# width, height = alteredImage.size
# prevColour = (-1, -1, -1)
# currentCount = 0

# # Create text document for pattern
# # f = open("scales.txt", "x")
# with open("scales.txt", "w") as f:
#     f.write("Scales pattern:\n")

# for y in range(height):
#     with open ("scales.txt", "a") as f:
#         f.write(f"Row {y+1}: ")

#     for x in range(width):
#         rgb = img.getpixel((x,y))
#         rgbList = list(rgb)
#         rgbList.pop(3)
#         rgb = tuple(rgbList)

#         if rgb == prevColour:
#             currentCount = currentCount + 1
#         else:
#             if x != 0:
#                 colourName = colourMap[prevColour]
#                 with open ("scales.txt", "a") as f:
#                     f.write(f"SC{currentCount} in {colourName}, ")
            
#             currentCount = 1
#             prevColour = rgb

#     colourName = colourMap[prevColour]
#     with open ("scales.txt", "a") as f:
#         f.write(f"SC{currentCount} in {colourName}, ")
    
#     with open ("scales.txt", "rb+") as f:
#         f.seek(-2, 2)
#         f.truncate()

#     with open ("scales.txt", "a") as f:
#         f.write(".\n")

import math
from PIL import Image

# Use an exact dictionary. 
# TIP: If the names are still wrong, swap the RGB values here!
YARN_COLORS = {
    "aqua": (97, 173, 169),
    "silver": (195, 196, 190),
    "cobalt": (39, 46, 116),
    "turquoise": (2, 153, 169),
    "fushia": (179, 48, 113),
    "mint": (114, 193, 93)
}

def get_closest_yarn(pixel_rgb):
    r1, g1, b1 = pixel_rgb[:3] # Grab first 3 in case of RGBA
    min_dist = float('inf')
    match = "unknown"
    for name, (r2, g2, b2) in YARN_COLORS.items():
        dist = math.sqrt((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2)
        if dist < min_dist:
            min_dist = dist
            match = name
    return match

# Load and standardize
try:
    img = Image.open('Full pattern but wider this time.png').convert('RGB')
except FileNotFoundError:
    print("Error: Image file not found. Check the filename/extension!")
    exit()

width, height = img.size

with open("scales.txt", "w") as f:
    f.write("Crochet Pattern:\n")
    
    # We range (height-1, -1, -1) to start from the BOTTOM of the image.
    # Change to range(height) if you want to start from the TOP.
    for y in range(height - 1, -1, -1):
        row_num = height - y # This labels the bottom row as Row 1
        row_data = []
        
        # Start the row logic
        first_px = img.getpixel((0, y))
        prev_name = get_closest_yarn(first_px)
        count = 0
        
        for x in range(width):
            current_name = get_closest_yarn(img.getpixel((x, y)))
            
            if current_name == prev_name:
                count += 1
            else:
                row_data.append(f"SC{count} {prev_name}")
                count = 1
                prev_name = current_name
        
        # Final block of the row
        row_data.append(f"SC{count} {prev_name}")
        f.write(f"Row {row_num}: {', '.join(row_data)}.\n")

print("Done! Check scales.txt.")