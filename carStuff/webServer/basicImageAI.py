from PIL import Image
bonus_val = 200
def getDirectionFromImage(image, lastDir):
    im = image
    pix = im.load()
    width = im.size[0]
    half_width = int(width /2)
    height = im.size[1]
    half_height = int(height/4)
    left = 0
    right = 0

    for y in range(height):
        for x in range(width):
            red = pix[x,y][0]
            green = pix[x,y][1]
            blue = pix[x,y][2]
            if red < 80 and green < 80 and blue > 80:
                if y < half_height:
                    bonus = bonus_val
                else:
                    bonus = 0
                if x < half_width:
                    left += 1 + bonus
                else:
                    right += 1 + bonus

    print(right)
    print(left)

    total = left + right
    if total > 0:
        # print (right/total)
        # print (left/total)
        difference = abs(left/total - right/total)
        # print (abs(difference))
    else:
        difference = 0
        return lastDir

    if difference < .1:
        lastDir = 0
    elif left > right:
        lastDir = -1
    else:
        lastDir = 1
    return lastDir

def getDirectionFromImageLocation(image_location, last_dir):
    im = Image.open(image_location)
    return getDirectionFromImage(im, last_dir)
   
# pix[0,0] = value  # Set the RGBA Value of the image (tuple)
# im.save('alive_parrot.png')  # Save the modified pixels as .png
