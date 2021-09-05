from PIL import Image

im = Image.open(r"./enemies.png")
width, height = im.size
names = ["red", "pink", "blue", "yellow"]

directions = ["left", "up", "down"]
size = 14

positions = [(i*16 + k*48, j*15) for k in range(4)
             for j in range(2) for i in range(3)]

for i in range(len(positions)):
    (left, top) = positions[i]
    name = names[i // 6]
    direction = directions[(i % 6) // 2]
    im1 = im.crop((left, top, left + size, top + size))
    im1.save('./assets/enemies/' + name + "/" + direction + "_" +
             str(i % 2 + 1) + ".png", format="png")
    if direction == "left":
        im2 = im1.transpose(Image.FLIP_LEFT_RIGHT)
        im2.save('./assets/enemies/' + name + "/right_" +
             str(i % 2 + 1) + ".png", format="png")
