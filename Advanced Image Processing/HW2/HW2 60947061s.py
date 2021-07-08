#張哲銘 60947061s
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

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
    global file_path
    global new_img
    global new_img_gray
    file_path = filedialog.askopenfilename()
    img = Image.open(file_path)
    print (img.format, img.size) 
    img_width, img_height = img.size
    if img_width > screen_width / 2 or img_height > screen_height / 2:
        if img_width > img_height:
            img = img.resize((int(img_width * (screen_width / img_width) / 2), int(img_height * (screen_width / img_width) / 2)))
        else:
            img = img.resize((int(img_width * (screen_height / img_width) / 2), int(img_height * (screen_height / img_width) / 2)))
    img_gray = img.convert('L')
    new_img = ImageTk.PhotoImage(img)
    new_img_gray = ImageTk.PhotoImage(img_gray)
    imLabel = tk.Label(bottom_frame, image = new_img).pack()
    root.mainloop()

def gray_image():
    try:
        for widget in bottom_frame.winfo_children():
            widget.destroy()
    except:
        pass
    global new_img
    global new_img_gray
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
    global file_path
    global new_img_gray
    img_gray = cv.imdecode(np.fromfile(file_path, dtype = np.uint8), - 1)
    plt.hist(img_gray.ravel(), 256, [0, 256])
    plt.savefig("histogram.png")
    img_gray_histogram = ImageTk.PhotoImage(Image.open("histogram.png").convert('L'))
    imLabel_left = tk.Label(bottom_frame, image = new_img_gray).pack(side = tk.LEFT)
    imLabel_right = tk.Label(bottom_frame, image = img_gray_histogram).pack(side = tk.RIGHT)
    root.mainloop()
    
new_button = tk.Button(top_frame, text = '新增圖片', fg = 'black', command = new_image).pack(side = tk.LEFT)    
gray_button = tk.Button(top_frame, text = '灰階圖片', fg = 'black', command = gray_image).pack(side = tk.LEFT)
histogram_button = tk.Button(top_frame, text = '灰階直方圖', fg = 'black', command = set_histogram).pack(side = tk.LEFT)
file_path = None
new_img = None
new_img_gray = None
root.mainloop()
