#張哲銘 60947061s
import tkinter as tk
from tkinter import filedialog
from PIL import Image,ImageTk

root = tk.Tk()
root.title('AIP 60947061s')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(str(screen_width)+'x'+str(screen_height))

top_frame = tk.Frame(root)
top_frame.pack()

bottom_frame = tk.Frame(root)
bottom_frame.pack()

def set_image():
    try:
        for widget in bottom_frame.winfo_children():
            widget.destroy()
    except:
        pass    
    file_path = filedialog.askopenfilename()
    im=Image.open(file_path)
    print (im.format)
    print (im.size)
    img_width, img_height = im.size
    if img_width > screen_width/2 or img_height > screen_height/2:
        if img_width > img_height:
            im = im.resize((int(img_width*(screen_width/img_width)/2), int(img_height*(screen_width/img_width)/2)))
        else:
            im = im.resize((int(img_width*(screen_height/img_width)/2), int(img_height*(screen_height/img_width)/2)))
    img=ImageTk.PhotoImage(im)
    imLabel_left=tk.Label(bottom_frame,image=img).pack(side=tk.LEFT)
    imLabel_right=tk.Label(bottom_frame,image=img).pack(side=tk.RIGHT)
    root.mainloop()

add_button = tk.Button(top_frame, text='新增圖片', fg='black', command=set_image)
add_button.pack()

root.mainloop()
