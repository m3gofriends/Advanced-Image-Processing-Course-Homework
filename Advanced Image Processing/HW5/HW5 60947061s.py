#張哲銘 60947061s
import tkinter as tk
from tkinter import filedialog
from tkinter.simpledialog import askinteger
from PIL import Image,ImageTk
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
root.geometry(str(screen_width)+'x'+str(screen_height))

top_frame = tk.Frame(root)
top_frame.pack()

scrollbar = tk.Scrollbar(root)
canvas = tk.Canvas(root, yscrollcommand=scrollbar.set)
scrollbar.config(command=canvas.yview)
scrollbar.pack(side=tk.LEFT, fill=tk.Y)
bottom=tk.Frame(canvas)
canvas.pack(fill="both", expand=True)
canvas.create_window(0,0,window=bottom, anchor='nw')

bottom_frame = tk.Frame(bottom)
bottom_frame.pack()

bottom_frame_2 = tk.Frame(bottom)
bottom_frame_2.pack()

tk.Label(bottom_frame_2,width=screen_height//4).pack()

def new_image():
    for widget in bottom_frame.winfo_children():
        widget.destroy()
    for widget in bottom_frame_2.winfo_children():
        widget.destroy()
    plt.clf()
    canvas.config(scrollregion=(0,0,0,0))
    global file_path, img_gray, new_img, new_img_gray, img_gray_histogram, flag
    resized = False
    file_path = filedialog.askopenfilename()
    try:
        img=Image.open(file_path)
    except:
        root.mainloop()    
    img_message = img.format+' '+str(img.size)
    img_width, img_height = img.size
    if img_width > screen_width/2 or img_height > screen_height/2:
        resized = True
        if img_width > img_height:
            img = img.resize((int(img_width*(screen_width/img_width)/2), int(img_height*(screen_width/img_width)/2)))
        else:
            img = img.resize((int(img_width*(screen_height/img_width)/2), int(img_height*(screen_height/img_width)/2)))
    img_gray = img.convert('L')
    new_img=ImageTk.PhotoImage(img)
    new_img_gray=ImageTk.PhotoImage(img_gray)
    tk.Label(bottom_frame,image=new_img).pack()
    if resized:
        tk.messagebox.showinfo('圖片資訊', img_message+"\n重新縮放尺寸")
    else:
        tk.messagebox.showinfo('圖片資訊', img_message+"\n圖片大小未改變")
    flag = True
    plt.hist(np.array(Image.open(file_path).convert('L')).ravel(), 256, [0, 256])
    plt.savefig("histogram.png")
    img_gray_histogram = ImageTk.PhotoImage(Image.open("histogram.png").convert('L'))
    os.remove("histogram.png")
    root.mainloop()

def gray_image():
    for widget in bottom_frame.winfo_children():
        widget.destroy()
    for widget in bottom_frame_2.winfo_children():
        widget.destroy()
    canvas.config(scrollregion=(0,0,0,0))
    global new_img, new_img_gray, flag
    if flag == False:
        tk.messagebox.showinfo("操作錯誤", "請先新增圖片")
        root.mainloop()
    tk.Label(bottom_frame,image=new_img).pack(side=tk.LEFT)
    tk.Label(bottom_frame,image=new_img_gray).pack(side=tk.RIGHT)
    root.mainloop()

def set_histogram():
    for widget in bottom_frame.winfo_children():
        widget.destroy()
    for widget in bottom_frame_2.winfo_children():
        widget.destroy()
    canvas.config(scrollregion=(0,0,0,0))
    global file_path, new_img_gray, img_gray_histogram, flag
    if flag == False:
        tk.messagebox.showinfo("操作錯誤", "請先新增圖片")
        root.mainloop()   
    tk.Label(bottom_frame,image=new_img_gray).pack(side=tk.LEFT)
    tk.Label(bottom_frame,image=img_gray_histogram).pack(side=tk.RIGHT)
    root.mainloop()

def AWGN():
    for widget in bottom_frame.winfo_children():
        widget.destroy()
    for widget in bottom_frame_2.winfo_children():
        widget.destroy()
    plt.clf()
    canvas.config(scrollregion=(0,0,0,0))
    global img_gray, flag
    if flag == False:
        tk.messagebox.showinfo("操作錯誤", "請先新增圖片")
        root.mainloop()
    AWGN_img=np.array(img_gray)
    rows,cols=AWGN_img.shape
    n = askinteger("輸入整數", "輸入雜訊值\nGray-level range(0~255)")
    if n == None:
        root.mainloop()
    for i in range(rows):
        for j in range(0, cols-1, 2):
            r1 = random.random()
            r2 = random.random()
            z1 = n*math.cos(2*math.pi*r2)*math.sqrt(-2*np.log(r1))
            z2 = n*math.sin(2*math.pi*r2)*math.sqrt(-2*np.log(r1))
            AWGN_img[i,j] = AWGN_img[i,j] + z1
            if(AWGN_img[i,j] < 0):
                AWGN_img[i,j] = 0
            elif(AWGN_img[i,j] > 255):
                AWGN_img[i,j] = 255
            else:
                pass
            AWGN_img[i,j+1] = AWGN_img[i,j+1] + z2
            if(AWGN_img[i,j+1] < 0):
                AWGN_img[i,j+1] = 0
            elif(AWGN_img[i,j+1] > 255):
                AWGN_img[i,j+1] = 255
            else:
                pass
    misc.imsave("AWGN.png", AWGN_img)
    AWGN_histogram_img=np.array(Image.open("AWGN.png"))
    plt.hist(AWGN_histogram_img.ravel(), 256, [0, 256])
    plt.savefig("histogram.png")
    AWGN_img = ImageTk.PhotoImage(Image.open("AWGN.png"))
    AWGN_histogram = ImageTk.PhotoImage(Image.open("histogram.png").convert('L'))
    tk.Label(bottom_frame,image=AWGN_img).pack(side=tk.LEFT)
    tk.Label(bottom_frame,image=AWGN_histogram).pack(side=tk.RIGHT)
    os.remove("AWGN.png")
    os.remove("histogram.png")
    root.mainloop()

def DWT():
    for widget in bottom_frame.winfo_children():
        widget.destroy()
    for widget in bottom_frame_2.winfo_children():
        widget.destroy()
    canvas.config(scrollregion=(0,0,0,0))
    global img_gray, new_img_gray, flag
    if flag == False:
        tk.messagebox.showinfo("操作錯誤", "請先新增圖片")
        root.mainloop()
    DWT_img=np.array(img_gray, 'float')
    rows,cols=DWT_img.shape
    if rows%2 == 1 or cols %2 == 1:
        tk.messagebox.showinfo("操作錯誤", "圖片長寬 : ("+ str(rows) + ", " + str(cols) + ")\n不全為偶數")
        root.mainloop()
    n = askinteger("輸入整數", "輸入小波轉換層數")
    if n == None:
        root.mainloop()
    DWT_output = np.zeros((rows,cols), 'float')
    for levels in range(n):
        for i in range(0, rows, 2):
            for j in range(0, cols, 2):
                DWT_output[0+i//2, 0+j//2] = (DWT_img[i, j] + DWT_img[i, j+1] + DWT_img[i+1, j] + DWT_img[i+1, j+1]) / 4 #LL
                DWT_output[0+i//2, cols//2+j//2] = (DWT_img[i, j] - DWT_img[i, j+1] + DWT_img[i+1, j] - DWT_img[i+1, j+1]) / 4 #LH
                DWT_output[rows//2+i//2, 0+j//2] = (DWT_img[i, j] + DWT_img[i, j+1] - DWT_img[i+1, j] - DWT_img[i+1, j+1]) / 4 #HL
                DWT_output[rows//2+i//2, cols//2+j//2] = (DWT_img[i, j] - DWT_img[i, j+1] - DWT_img[i+1, j] + DWT_img[i+1, j+1]) / 4 #HH
        DWT_img[:rows, :cols] = DWT_output[:rows, :cols]
        rows = rows // 2
        cols = cols // 2
    misc.imsave("DWT.png", DWT_img)
    DWT_img = ImageTk.PhotoImage(Image.open("DWT.png"))
    tk.Label(bottom_frame,image=new_img_gray).pack(side=tk.LEFT)
    tk.Label(bottom_frame,image=DWT_img).pack(side=tk.RIGHT)
    os.remove("DWT.png")
    root.mainloop()

def histogram_qualization():
    for widget in bottom_frame.winfo_children():
        widget.destroy()
    for widget in bottom_frame_2.winfo_children():
        widget.destroy()
    plt.clf()
    global img_gray, new_img_gray, img_gray_histogram, flag
    if flag == False:
        tk.messagebox.showinfo("操作錯誤", "請先新增圖片")
        root.mainloop()
    HQ_img=np.array(img_gray)
    rows,cols=HQ_img.shape
    H = np.zeros(256, int)
    Hc = np.zeros(256, int)
    T = np.zeros(256, int)
    for i in range(rows):
        for j in range(cols):
            H[HQ_img[i][j]] = H[HQ_img[i][j]] + 1
    g_min = np.nonzero(H)[0][0]
    for i in range(1, 256):
        Hc[i] = Hc[i-1] + H[i]
    H_min = Hc[g_min]
    try:
        for i in range(256):
            T[i] = round(((Hc[i]-H_min)*255)/((cols*rows)-H_min))
    except:
        tk.messagebox.showinfo("計算錯誤", "分母為0")
        root.mainloop()
    for i in range(rows):
        for j in range(cols):
            HQ_img[i][j] = T[HQ_img[i][j]]
    misc.imsave("HQ.png", HQ_img)
    HQ_img = ImageTk.PhotoImage(Image.open("HQ.png"))
    plt.hist(np.array(Image.open("HQ.png")).ravel(), 256, [0, 256])
    plt.savefig("histogram.png")
    HQ_histogram = ImageTk.PhotoImage(Image.open("histogram.png").convert('L'))
    imLabel_left=tk.Label(bottom_frame,image=new_img_gray).pack(side=tk.LEFT)
    imLabel_right=tk.Label(bottom_frame,image=HQ_img).pack(side=tk.RIGHT)
    tk.Label(bottom_frame_2,image=img_gray_histogram).pack(side=tk.LEFT)
    tk.Label(bottom_frame_2,image=HQ_histogram).pack(side=tk.RIGHT)
    root.update()
    canvas.config(scrollregion=canvas.bbox("all"))
    os.remove("HQ.png")
    os.remove("histogram.png") 
    root.mainloop()

new_button = tk.Button(top_frame, text='新增圖片', fg='black', command=new_image).pack(side=tk.LEFT)    
gray_button = tk.Button(top_frame, text='灰階圖片', fg='black', command=gray_image).pack(side=tk.LEFT)
histogram_button = tk.Button(top_frame, text='灰階直方圖', fg='black', command=set_histogram).pack(side=tk.LEFT)
noise_button = tk.Button(top_frame, text='加性高斯白雜訊', fg='black', command=AWGN).pack(side=tk.LEFT)
DWT_button = tk.Button(top_frame, text='離散小波轉換', fg='black', command=DWT).pack(side=tk.LEFT)
histogram_qualization_button = tk.Button(top_frame, text='直方圖均衡化', fg='black', command=histogram_qualization).pack(side=tk.LEFT)
file_path = None
img_gray = None
new_img = None
new_img_gray = None
img_gray_histogram = None
flag = False
root.mainloop()
