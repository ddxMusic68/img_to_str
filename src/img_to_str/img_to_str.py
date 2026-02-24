import cv2 as cv
import numpy as np
import pygame as pg
import os

def imgToStr(img:np.ndarray, size:tuple[int]=None, chars:list[str]=None, reverse:bool=None) -> list[str]:
    """takes in numpy arr as img and converts to str using chars (darkest -> brightest)"""
    if size is None:
        size = (100, 100)
    if chars is None:
        chars = ['@', '%', '#', '*', '+', '=', '-', ':', '.', ' ']
    if reverse is None:
        reverse = False

    if reverse:
        chars = chars[::-1]
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    rescaled = cv.resize(gray, size)
    div_amount = (256/(len(chars)-1))
    char_arr = []
    for row in rescaled:
        char_row = []
        for col in row:
            char_val = (chars[int(col//div_amount)])
            char_row.append(char_val)
        char_arr.append(char_row)
    return char_arr

def showImg(img:np.ndarray, chars:list[str]=None, size:tuple[int]=(100, 100), font_size:int=15, color:tuple[int]=(255, 255, 255), reverse:bool=None):
    pg.init()

    strIMG = imgToStr(img, size, chars, reverse)

    font = pg.font.Font("monofont.ttf", font_size)
    char_width, char_height = font.render("2", True, (255, 255, 255)).get_size()

    screen = pg.display.set_mode((size[1]*char_width, size[0]*char_width))
    clock = pg.time.Clock()
    running = True

    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill("black")

        for (counter, row) in enumerate(strIMG):
            s = ""
            for char in row:
                s += char
            screen.blit(font.render(s, True, color), (0, 0+char_width*counter))
        
        pg.display.flip()
        clock.tick(60)
    pg.quit()

def showVid(capture:cv.VideoCapture, chars:list[str]=None, size:tuple[int]=(100, 100), font_size:int=15, color:tuple[int]=(255, 255, 255), reverse:bool=None):
    pg.init()

    font = pg.font.Font("monofont.ttf", font_size)
    char_width, char_height = font.render("2", True, (255, 255, 255)).get_size()

    screen = pg.display.set_mode((size[1]*char_width, size[0]*char_width))
    clock = pg.time.Clock()
    running = True

    while running:
        # opencv logic 
        isTrue, frame = capture.read()
        strIMG = imgToStr(frame, size, chars, reverse)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill("black")

        for (counter, row) in enumerate(strIMG):
            s = ""
            for char in row:
                s += char
            screen.blit(font.render(s, True, color), (0, 0+char_width*counter))
        
        pg.display.flip()
        clock.tick(60)
    pg.quit()

def imgToFile(img:np.ndarray, filePath:str, spacer:str=" ", size:tuple[int]=None, chars:list[str]=None, reverse:bool=None):
    textIMG = imgToStr(img, size, chars, reverse)
    with open(filePath, "w") as f:
        for row in textIMG:
            for col in row:
                f.write(col+spacer)
            f.write('\n')

if __name__ == "__main__":
    img = cv.imread("bike.jpg")
    capture = cv.VideoCapture(0)

    imgToFile(img, os.path.join(os.curdir, "test.txt"), size=(400, 300), reverse=True)
    # showVid(capture, size=(80, 80), reverse=True)
    # showImg(img, size=(80, 80), reverse=False)