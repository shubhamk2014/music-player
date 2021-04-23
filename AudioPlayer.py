from tkinter import *
from PIL import Image, ImageTk
from tkinter.ttk import Progressbar
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilenames
import os
from pygame import mixer

# initialization of pygame
mixer.init()
root = Tk()
root.title("Audio Player")
root.geometry("500x400")
root.minsize(500, 400)


# music loading and creating playlist
interpt = 0


def openfile(event=None):
    global interpt
    global music_files, current_fileInd
    music_files = askopenfilenames(initialdir="E:\\Playlists", defaultextension=".mp3", filetypes=[
                                   ("alltyes", "*.*"), ("musicfiles", "*.mp3")])
    # print(music_files)
    current_fileInd = len(music_files)-1
    mixer.music.load(music_files[current_fileInd])
    mixer.music.play(loops=0)
    play_btn.config(text="Pause")
    interpt = 1


# function for next song
def next():
    global current_fileInd, interpt
    current_fileInd = (current_fileInd - 1) % len(music_files)
    print(music_files[current_fileInd])
    mixer.music.load(music_files[current_fileInd])
    mixer.music.play()
    play_btn.config(text="Pause")
    interpt = 1


# function for previous song
def prev():
    global current_fileInd, interpt
    current_fileInd = (current_fileInd + 1) % len(music_files)
    print(music_files[current_fileInd])
    mixer.music.load(music_files[current_fileInd])
    mixer.music.play()
    play_btn.config(text="Pause")
    interpt = 1


def play_pause():
    global interpt
    if interpt == 0:
        play()
        interpt = 1
        # print("1")

    elif interpt == 1:
        pause()
        interpt = 2
        # print("2")

    elif interpt > 1:
        resume()
        interpt = 1
        # print("3")


def play():
    global interpt
    mixer.music.play()
    play_btn.config(text="Pause")
    interpt = 1


def pause():
    global interpt
    mixer.music.pause()
    play_btn.config(text="Resume")
    interpt = 2


def resume():
    global interpt
    mixer.music.unpause()
    play_btn.config(text="Pause")
    interpt = 1


i = 0


def replay():
    pass


def shuffle():
    pass


def volume(vol):
    volum = int(vol)/100
    mixer.music.set_volume(volum)
    volum = volum*100
    set_img(volum)


def set_img(volum):
    global vol_image
    global path
    if volum == 0:
        path = "imgs\\mute.png"
        # print("1")
    elif volum > 0 and volum < 35:
        path = "imgs\\lVol.png"
        # print("2")
    elif volum > 35 and volum < 75:
        path = "imgs\\medVol.png"
        # print("3")
    else:
        path = "imgs\\fVol.png"
        # print("4")
    vol_image = ImageTk.PhotoImage(Image.open(
        path).resize((20, 20), Image.ANTIALIAS))
    vol_btn.config(image=vol_image)
    # print("5")


def volUp():
    inp = scale.get()
    if inp <= 90:
        inp = int(inp)+10
        scale.set(inp)


def volDown():
    inp = scale.get()
    if inp >= 10:
        inp = int(inp)-10
        scale.set(inp)


def mute_unmute():
    pass


def about():

    f = open("aboutMessege.txt")
    showinfo(title='Audio Player', message=f.read())


menubar = Menu(root)

# filemenu
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(
    label="Open", accelerator="Ctrl+O", command=openfile)
filemenu.bind_all("<Control-o>", openfile)
filemenu.add_separator()
filemenu.add_command(
    label="Exit", accelerator="Alt+F4", command=root.quit)
# filemenu.bind_all("<Alt-F4>", openfile)

menubar.add_cascade(label="File", menu=filemenu)

# playmenu

playmenu = Menu(menubar, tearoff=0)
playmenu.add_command(label="Play", accelerator="F5",
                     command=play)
# filemenu.bind_all("<F5>", play)
playmenu.add_command(label="Pause", accelerator="F7", command=pause)
playmenu.add_command(label="Resume", accelerator="F7", command=resume)
playmenu.add_separator()
playmenu.add_command(label="Next", accelerator="F6", command=next)
playmenu.add_command(label="Previous", accelerator="F4", command=prev)
playmenu.add_separator()
playmenu.add_command(label="Replay", accelerator="F4", command=replay)
playmenu.add_command(label="Shuffle", accelerator="F4", command=shuffle)
playmenu.add_separator()
playmenu.add_command(label="Volume Up", accelerator="F3",
                     command=volUp)
playmenu.add_command(label="Volume Down", accelerator="F2",
                     command=volDown)
menubar.add_cascade(label="Play", menu=playmenu)

# Helpmenu

Helpmenu = Menu(menubar, tearoff=0)
Helpmenu.add_command(label="About", accelerator="F10", command=about)

menubar.add_cascade(label="Help", menu=Helpmenu)


root.config(menu=menubar)


filename = "imgs\\music.jpg"

frame1 = Frame(root, width=550, height=300)

img = ImageTk.PhotoImage(Image.open(filename))
img_lbl = Label(frame1, image=img).pack(expand=TRUE, fill=BOTH)

frame1.pack(expand=TRUE, fill=BOTH)

# frame2 is for song progress bar
frame2 = Frame(root, width=550, height=5)
progressbar1 = Progressbar(
    frame2, max=100, mode="determinate").pack(fill=X, padx=10)
frame2.pack(expand=TRUE, fill=X)

# can_wid is for all btns
can_wid = Canvas(frame2, width=550, height=37)
can_wid.pack()

# rewind_btn replaying song
rewind_btn = Button(can_wid, text="Rewind",
                    font="lucida 10 bold", bg="green", fg="white")
rewind_btn.pack(side=LEFT, padx=5, pady=10)

# button for previous song
prev_btn = Button(can_wid, text="<<", font="lucida 10 bold",
                  bg="green", fg="white", command=prev)
prev_btn.pack(side=LEFT, padx=5, pady=10)

# play btn
play_btn = Button(can_wid, text="Play", font="lucida 13 bold",
                  bg="green", fg="white", command=play_pause)
play_btn.pack(side=LEFT, ipadx=5, ipady=5, padx=5, pady=10)

# button for next song
nxt_btn = Button(can_wid, text=">>", font="lucida 10 bold", bg="green", fg="white", command=next).pack(
    side=LEFT, padx=5, pady=10)
# shuffle_btn
shuffle_btn = Button(can_wid, text="Shuffle",
                     font="lucida 10 bold", bg="green", fg="white")
shuffle_btn.pack(side=LEFT, padx=5, pady=10)

# volume button and condition for different volume
vol_image = ImageTk.PhotoImage(Image.open(
    "imgs\\mute.png").resize((20, 20), Image.ANTIALIAS))
vol_btn = Button(can_wid, text="vol_btn", image=vol_image, bg="green")
vol_btn.pack(side=LEFT, padx=5)
vol_btn.bind("<Button-1>", mute_unmute)
# volume progessbar

scale = Scale(can_wid, from_=0, to=100,
              orient=HORIZONTAL, command=volume, bg="green", showvalue=0, width=10)
scale.pack(side=LEFT)
scale.set(25)

root.mainloop()
