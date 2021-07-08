#張哲銘 60947061s
import tkinter as tk
from tkinter import filedialog
from tkinter.simpledialog import askinteger
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import random
import math
from scipy import misc
import os

root = tk.Tk()
root.title('AIP 60947061s')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(str(screen_width) + 'x' + str(screen_height))

top_frame = tk.Frame(root)
top_frame.pack()

bottom_frame = tk.Frame(root)
bottom_frame.pack()

def new_image():
    try:
        for widget in bottom_frame.winfo_children():
            widget.destroy()
    except:
        pass
    global file_path, img_gray, new_img, new_img_gray, flag
    resized = False
    file_path = filedialog.askopenfilename()
    img = Image.open(file_path)
    img_message = img.format +' '+ str(img.size)
    img_width, img_height = img.size
    if img_width > screen_width / 2 or img_height > screen_height / 2:
        resized = True
        if img_width > img_height:
            img = img.resize((int(img_width * (screen_width / img_width) / 2), int(img_height * (screen_width / img_width) / 2)))
        else:
            img = img.resize((int(img_width * (screen_height / img_width) / 2), int(img_height * (screen_height / img_width) / 2)))
    img_gray = img.convert('L')
    new_img = ImageTk.PhotoImage(img)
    new_img_gray = ImageTk.PhotoImage(img_gray)
    imLabel = tk.Label(bottom_frame, image = new_img).pack()
    if resized:
        tk.messagebox.showinfo('圖片資訊', img_message +"\n重新縮放尺寸")
    else:
        tk.messagebox.showinfo('圖片資訊', img_message +"\n圖片大小未改變")
    flag = True
    root.mainloop()

def gray_image():
    try:
        for widget in bottom_frame.winfo_children():
            widget.destroy()
    except:
        pass
    global new_img, new_img_gray, flag
    if flag == False:
        tk.messagebox.showinfo("操作錯誤", "請先新增圖片")
        root.mainloop()
    imLabel_left = tk.Label(bottom_frame, image = new_img).pack(side = tk.LEFT)
    imLabel_right = tk.Label(bottom_frame, image = new_img_gray).pack(side = tk.RIGHT)
    root.mainloop()

def set_histogram():
    try:
        for widget in bottom_frame.winfo_children():
            widget.destroy()
        plt.clf()
    except:
        pass
    global file_path, new_img_gray, flag
    if flag == False:
        tk.messagebox.showinfo("操作錯誤", "請先新增圖片")
        root.mainloop()
    img_gray = np.array(Image.open(file_path).convert('L'))
    plt.hist(img_gray.ravel(), 256, [0, 256])
    plt.savefig("histogram.png")
    img_gray_histogram = ImageTk.PhotoImage(Image.open("histogram.png").convert('L'))
    imLabel_left = tk.Label(bottom_frame, image = new_img_gray).pack(side = tk.LEFT)
    imLabel_right = tk.Label(bottom_frame, image = img_gray_histogram).pack(side = tk.RIGHT)
    os.remove("histogram.png")
    root.mainloop()

def AWGN():
    try:
        for widget in bottom_frame.winfo_children():
            widget.destroy()
        plt.clf()
    except:
        pass
    global img_gray, flag
    if flag == False:
        tk.messagebox.showinfo("操作錯誤", "請先新增圖片")
        root.mainloop()
    AWGN_img = np.array(img_gray)
    n = askinteger("輸入整數", "輸入雜訊值\nGray - level range(0~255)")
    rows, cols = AWGN_img.shape
    for i in range(rows):
        for j in range(0, cols - 1, 2):
            r1 = random.random()
            r2 = random.random()
            z1 = n * math.cos(2 * math.pi * r2) * math.sqrt( - 2 * np.log(r1))
            z2 = n * math.sin(2 * math.pi * r2) * math.sqrt( - 2 * np.log(r1))
            AWGN_img[i, j] = AWGN_img[i, j] + z1
            if(AWGN_img[i, j] < 0):
                AWGN_img[i, j] = 0
            elif(AWGN_img[i, j] > 255):
                AWGN_img[i, j] = 255
            else:
                pass
            AWGN_img[i, j + 1] = AWGN_img[i, j + 1] + z2
            if(AWGN_img[i, j + 1] < 0):
                AWGN_img[i, j + 1] = 0
            elif(AWGN_img[i, j + 1] > 255):
                AWGN_img[i, j + 1] = 255
            else:
                pass
    misc.imsave("AWGN.png", AWGN_img)
    AWGN_histogram_img = np.array(Image.open("AWGN.png"))
    plt.hist(AWGN_histogram_img.ravel(), 256, [0, 256])
    plt.savefig("histogram.png")
    AWGN_img = ImageTk.PhotoImage(Image.open("AWGN.png"))
    AWGN_histogram = ImageTk.PhotoImage(Image.open("histogram.png").convert('L'))
    imLabel_left = tk.Label(bottom_frame, image = AWGN_img).pack(side = tk.LEFT)
    imLabel_right = tk.Label(bottom_frame, image = AWGN_histogram).pack(side = tk.RIGHT)
    os.remove("AWGN.png")
    os.remove("histogram.png")
    root.mainloop()
    
new_button = tk.Button(top_frame, text = '新增圖片', fg = 'black', command = new_image).pack(side = tk.LEFT)    
gray_button = tk.Button(top_frame, text = '灰階圖片', fg = 'black', command = gray_image).pack(side = tk.LEFT)
histogram_button = tk.Button(top_frame, text = '灰階直方圖', fg = 'black', command = set_histogram).pack(side = tk.LEFT)
noise_button = tk.Button(top_frame, text = '加性高斯白雜訊', fg = 'black', command = AWGN).pack(side = tk.LEFT)
file_path = None
img_gray = None
new_img = None
new_img_gray = None
flag = False
root.mainloop()
