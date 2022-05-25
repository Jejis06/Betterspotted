from PIL import Image, ImageFont, ImageDraw
import numpy as np
import random
import textwrap
from string import ascii_letters
import colorsys

def HSV2RGB(h,s,v):
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h/360,s/100,v/100))

def GENERATE_BACKGROUND(W,H,MODE):
    im = Image.new("RGB", (W, H))
    im = np.array(im)

    if MODE == 1: #random background and compleating font
        br = random.randint(0, 255)
        bg = random.randint(0, 255)
        bb = random.randint(0, 255)

        im = Image.new("RGB", (W, H),color=(br,bg,bb))
        im = np.array(im)

        crr = 255 - br
        grr = 255 - bg
        brr = 255 - bb

    elif MODE == 2: # rainbow
        x = 4
        i = 0

        tab = [
            (255, 107, 107),
            (255, 217, 61),
            (107, 203, 119),
            (77, 150, 255)
        ]

        crr = 255
        grr = 255
        brr = 255
        print(f"{H},{W}")
        for r in range(0, H):

            if (r%int(round(H/x)+1) == 0):
                h,s,v = tab[i]
                i += 1

            for c in range(0, W):
                im[r][c] =[h,s,v]
    elif MODE == 3: #random black white
        br = random.randint(0, 255)
        bg = br
        bb = br

        im = Image.new("RGB", (W, H), color=(br, bg, bb))
        im = np.array(im)

        crr = 255 - br
        grr = 255 - bg
        brr = 255 - bb

    return {"img":Image.fromarray(im, 'RGB'),"rgb":(crr,grr,brr)}




def GENERATE_PHOTO(msg,FONT,MODE,amm,W = 1080,H = 608):
    #basic backgroung
    power = 4
    o = GENERATE_BACKGROUND(W,H,MODE)
    img = o["img"]
    crr, grr, brr = o["rgb"]

    #EPIC ADDING TEXT TO THE GENERATED IMAGE
    if amm == 1:
        power = 1

    FS = int((int(W/H)*50)/(amm*power))

    font = ImageFont.truetype(FONT,FS)

    avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
    max_char_count = int(img.size[0] * .8 / avg_char_width)
    text = textwrap.fill(text=msg, width=max_char_count)

    font_color = (crr,grr,brr)#(237, 230, 211)



    while (font.getsize(text)[1]*len(text.split('\n')) > H):
        FS -= 5
        font = ImageFont.truetype(FONT, FS)
        avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
        max_char_count = int(img.size[0] * .9 / avg_char_width)
        text = textwrap.fill(text=msg, width=max_char_count)





    img_to_edit = ImageDraw.Draw(img)
    img_to_edit.multiline_text(xy=(img.size[0]/2, img.size[1] / 2), text=text, font=font, fill=font_color ,spacing=int(font.getsize(text)[1]/4),anchor='mm')


    return img

