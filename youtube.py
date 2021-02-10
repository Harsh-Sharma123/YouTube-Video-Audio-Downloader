from tkinter import *
from tkinter import ttk
from pytube import *
from PIL import Image, ImageTk
import requests
import io
from tkinter.messagebox import showinfo
# import cv2

# Global variables
size_in_bytes = 0
img = 0

# =============================================== Functions=========================================== 

def search():
    global img
    url = file_url.get()
    if url=="":
        msg_label.config(text="Video URL Empty", bg="red")
    else:    
        yt = YouTube(url)
        video_title = yt.title[:60]

        # Conver thumbnail url into image
        video_thumbnail = yt.thumbnail_url
        response = requests.get(video_thumbnail)
        img_byte = io.BytesIO(response.content)
        img = Image.open(img_byte)
        img = img.resize((210,205), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        descrip = yt.description[:230]

        # Download size of the files
        if string_var.get()=="Video": 
            select_file = yt.streams.filter(progressive=True).first()
        if string_var.get()=="Audio":
            select_file = yt.streams.filter(only_audio=True).first()

        global size_in_bytes
        size_in_bytes = select_file.filesize    
        max_size = size_in_bytes/1024000
        size_mb = str(round(max_size,2))+"MB"

        # Updating the labels
        title.config(text=video_title)
        textarea.delete(1.0, END)
        textarea.insert(END, descrip)
        video_image.config(image=img)
        # video_image.config(bg="green")
        lbl_size.config(text=f"Total Size : {size_mb}")
        download_btn.config(state=NORMAL)
        msg_label.config(text="Search Completed", bg="black")

def progress(streams, chunk, bytes_remaining):
    percentage = (float(abs(bytes_remaining-size_in_bytes)/size_in_bytes))*float(100)
    prog['value'] = percentage
    prog.update()
    lbl_percent.config(text=f"Downloading : {str(round(percentage, 2))}%")
    if round(percentage, 2) == 100:
        msg_label.config(text="Download Completed Successfully.", bg="green")


def download():
    search()
    url = file_url.get()
    yt = YouTube(url, on_progress_callback=progress)
    video_file = yt.streams.filter(progressive=True).first()
    audio_file = yt.streams.filter(only_audio=True).first()
    if string_var.get()=="Video":
        video_file.download("./video")
        showinfo("Download SuccessFull", "Your file have been downloaded successfullly.")
    elif string_var.get()=="Audio":
        audio_file.download("./audio")
        showinfo("Download SuccessFull", "Your file have been downloaded successfullly.")

def clear():
    title.config(text="Video Title")
    textarea.delete(1.0, END)
    prog['value'] = 0
    string_var.set("Video")
    file_url.set("")
    download_btn.config(state=DISABLED)
    msg_label.config(text="No Error", bg="black")
    video_image.config(image="")
    lbl_percent.config(text="Downaloding : 0 %")
    lbl_size.config(text="Total Size : 0 MB")


# =========================================Root and the GUI Window==================================================

root = Tk()
root.title("YouTube Downloader")
root.geometry("560x510+300+50")
root.resizable(False, False)
root.config(bg="white")

# Title
title = Label(root, text="YouTube Downloader || Developed By Harsh Sharma", font="Helvetica 12 bold", bg="black", fg="white").pack(side=TOP, fill=X)

# URL Entry Field
url_label = Label(root, text="Video URL", font="Helvetica 14 ", bg="white").place(x=30, y=50)
file_url = StringVar()
url_entry = Entry(root, textvariable=file_url, bg="lightyellow", font="Helvetica 14").place(x=180,y=50, width=350)

# File Type Radio Buttons
file_type = Label(root, text="File Type", font="Helvetica 14", bg="white").place(x=30, y=95)
string_var = StringVar()
string_var.set("Video")
video_radio = Radiobutton(root, text="Video",variable=string_var, value="Video", font="Helvetica 13", bg="White").place(x=180, y=95)
audio_radio = Radiobutton(root, text="Audio",variable=string_var, value="Audio", font="Helvetica 13", bg="White").place(x=280, y=95)

# Search Button
btn = Button(root, text="Search", font="Helvetica 14", bg="skyblue", command=search).place(x=420, y=90, height=30, width=110)

# Frame Begins
frame1 = Frame(root, relief=RIDGE, bg="yellow")
frame1.place(x=20, y=135, height=300, width=520)

# Frame title =========== Youtube Video Title
title = Label(frame1, text="Video Title", font="Helvetica 11 bold", bg="black", fg="white")
title.place(x=0, y=0, relwidth=1)

# Youtube Video Thumbnail Image
video_image = Label(frame1)
video_image.place(x=10, y=30, height=205, width=210)

# Description 
description = Label(frame1, text="Description", font="Helvetica 12 bold",bg="yellow", anchor="w").place(x=240, y=30, width=265)
textarea = Text(frame1, font="Helvetica 12", bg="lightyellow", relief=RIDGE)
textarea.place(x=240, y=55, height=180, width=265)

# File Size and Download Percentage Meter
lbl_size = Label(frame1, text="Total Size : 0 MB", font="Helvetica 11", bg="white")
lbl_size.place(x=10, y=252)
lbl_percent = Label(frame1, text="Downloading : 0%", font="Helvetica 11", bg="white")
lbl_percent.place(x=155, y=252)

# Clear and Download Buttons
clear_btn = Button(frame1, text="Clear", font="Helvetica 14", bg="grey",command=clear)
clear_btn.place(x=310, y=250, height=25, width=80)
download_btn = Button(frame1, text="Download", font="Helvetica 14", bg="green", command=download)
download_btn.place(x=400, y=250, height=25, width=110)

# Progress Bar
prog = ttk.Progressbar(root, orient=HORIZONTAL, length=520, mode="determinate")
prog.place(x=20, y=450)

msg_label = Label(root, text="Error Messages", font="Helvetica 12", bg="black", fg="white")
msg_label.place(x=20, y=480, width=520)

root.mainloop()