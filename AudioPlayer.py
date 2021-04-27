from tkinter import Tk, Menu, Label, Button, Canvas, Frame, Scale, HORIZONTAL, TRUE, LEFT, BOTH, X, StringVar
from tkinter.ttk import Scale as s
from PIL import Image, ImageTk
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilenames
from pygame import mixer
from random import randint
from mutagen.mp3 import MP3
from time import strftime, gmtime


# initialization of pygame
mixer.init()
root = Tk()
root.title("Audio Player")
root.geometry("530x430")
root.minsize(530, 430)


# music loading
interpt = 0


def openfile(event=None):
    global music_files, current_fileInd, interpt
    music_files = askopenfilenames(initialdir="E:\\Playlists", defaultextension=".mp3", filetypes=[
                                   ("alltyes", "*.*"), ("musicfiles", "*.mp3")])

    current_fileInd = len(music_files)-1
    playMusic()


def playMusic():
    global music_files, interpt, current_fileInd
    # print(current_fileInd)

    mixer.music.load(music_files[current_fileInd])
    mixer.music.play()

    play_btn.config(text="Pause")
    interpt = 1
    duration()


# function for next song
def next():
    global current_fileInd, interpt
    # print(current_fileInd)

    current_fileInd = (current_fileInd + 1) % len(music_files)
    # print(music_files[current_fileInd])
    mixer.music.load(music_files[current_fileInd])
    mixer.music.play()
    play_btn.config(text="Pause")
    interpt = 0


# function for previous song
def prev():
    global current_fileInd, interpt
    # print(current_fileInd)

    current_fileInd = (current_fileInd - 1) % len(music_files)
    # print(music_files[current_fileInd])
    mixer.music.load(music_files[current_fileInd])
    mixer.music.play()
    play_btn.config(text="Pause")
    interpt = 1

# assigning play and pause to funtionalities to same btn


def play_pause():
    global interpt
    if interpt == 0:
        playMusic()

    elif interpt == 1:
        pause()
        interpt = 2
        # print("2")

    elif interpt > 1:
        resume()
        interpt = 1
        # print("3")

# function to play music


def play():
    global interpt
    mixer.music.play()
    play_btn.config(text="Pause")

    interpt = 1

# function to pause music


def pause():
    global interpt
    mixer.music.pause()
    play_btn.config(text="Resume")
    interpt = 2

# function to resume music


def resume():
    global interpt
    mixer.music.unpause()
    play_btn.config(text="Pause")
    interpt = 1

# function to replay music


def replay():
    play()

# function to shuffle music


def shuffle():
    global music_files, current_fileInd
    try:

        current_fileInd = randint(0, len(music_files)-1)
        # print(current_fileInd)
        audio_f = music_files[current_fileInd]
        mixer.music.load(audio_f)
        mixer.music.play()
    except Exception:
        pass

# function to control volume


def volume(vol):
    volum = int(vol)/100
    print(vol)
    mixer.music.set_volume(volum)
    volum = volum*100
    set_img(volum)

# function to set image on volume btn


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

# function to increase the playback volume


def volUp():
    inp = scale.get()
    if inp <= 90:
        inp = int(inp)+10
        scale.set(inp)

# function to decrease the playback volume


def volDown():
    inp = scale.get()
    if inp >= 10:
        inp = int(inp)-10
        scale.set(inp)


# function to mute unmute the song
muted = 0


def mute_unmute(event):
    global muted, vol_image, path
    if muted:
        scale.set(80)
        path = "imgs\\fVol.png"
        vol_image = ImageTk.PhotoImage(Image.open(
            path).resize((20, 20), Image.ANTIALIAS))
        vol_btn.config(image=vol_image)
        muted = 0
    else:
        scale.set(0)
        path = "imgs\\mute.png"
        vol_image = ImageTk.PhotoImage(Image.open(
            path).resize((20, 20), Image.ANTIALIAS))
        vol_btn.config(image=vol_image)
        muted = 1

# function to showinfo about player


def about():
    showinfo(title='Audio Player',
             message="This is the 'Audio Player' by creator 'Shubham Kumbhar'")


# function for moving songProgress in case we want to forward the song
def set_song_pos(pos):
    slider_pos = pos.widget.get()
    mixer.music.set_pos(slider_pos)


# function for song lenth and song current position


def duration():
    # global declaration of variables we need in this function
    global music_files, current_fileInd, current_pos
    # get_pos returns time in millisec ,converting it to sec by dvidin with 1000
    current_pos = mixer.music.get_pos()/1000
    # converting time in the sec into format %M:%S
    converted_pos = strftime("%M:%S", gmtime(current_pos))
    # updating label with converted time
    dur_lbl.config(text=converted_pos)
    songProgress.set(current_pos)
    # for getting the position of the song every sec run the function every sec
    dur_lbl.after(1000, duration)

    # audio file of which we want to find the length
    audio_f = music_files[current_fileInd]
    current_audio = MP3(audio_f)
    audio_len = current_audio.info.length
    # converting in sec audio lenth to format %m:%s
    converted_audio_len = strftime("%M:%S", gmtime(audio_len))
    # finally updating songlen_lbl
    songlen_lbl.config(text=converted_audio_len)
    songProgress.config(to=audio_len)
    print(f"current={current_pos}")


menubar = Menu(root)

# filemenu
filemenu = Menu(menubar, tearoff=0)

filemenu.add_command(label="Open", accelerator="Ctrl+O", command=openfile)
filemenu.bind_all("<Control-o>", openfile)
filemenu.add_separator()
filemenu.add_command(label="Exit", accelerator="Alt+F4", command=root.quit)

menubar.add_cascade(label="File", menu=filemenu)

# playmenu

playmenu = Menu(menubar, tearoff=0)

playmenu.add_command(label="Play", accelerator="F5", command=play)
playmenu.add_command(label="Pause", accelerator="F7", command=pause)
playmenu.add_command(label="Resume", accelerator="F7", command=resume)
playmenu.add_separator()
playmenu.add_command(label="Next", accelerator="F6", command=next)
playmenu.add_command(label="Previous", accelerator="F4", command=prev)
playmenu.add_separator()
playmenu.add_command(label="Replay", accelerator="F4", command=replay)
playmenu.add_command(label="Shuffle", accelerator="F4", command=shuffle)
playmenu.add_separator()
playmenu.add_command(label="Volume Up", accelerator="F3", command=volUp)
playmenu.add_command(label="Volume Down", accelerator="F2", command=volDown)

menubar.add_cascade(label="Play", menu=playmenu)

# Helpmenu

Helpmenu = Menu(menubar, tearoff=0)
Helpmenu.add_command(label="About", accelerator="F10", command=about)

menubar.add_cascade(label="Help", menu=Helpmenu)


root.config(menu=menubar)


frame1 = Frame(root, width=550, height=300)

filename = "imgs\\music.jpg"
img = ImageTk.PhotoImage(Image.open(filename))
Label(frame1, image=img).pack(expand=TRUE, fill=BOTH)
frame1.pack(expand=TRUE, fill=BOTH)

# frame2 is for song progress bar
frame2 = Frame(root, width=550, height=5)

# dur_lbl gives the current position of song i.e. howmuch song is played
dur_lbl = Label(frame2, text="00:00", bg="gray")
dur_lbl.pack(side=LEFT, padx=10, ipadx=10, ipady=5)

songProgress = s(frame2, from_=0, to=100,
                 orient=HORIZONTAL, length=300, value=0)
songProgress.pack(side=LEFT)
songProgress.bind("<ButtonRelease>", set_song_pos)

songlen_lbl = Label(frame2, text="00:00", bg="gray")
songlen_lbl.pack(side=LEFT, padx=10, ipadx=10, ipady=5)

frame2.pack(expand=TRUE)

# can_wid is for all btns
can_wid = Canvas(root, width=550, height=37, bg="gray",
                 borderwidth=5, relief="raised", highlightbackground="green")
can_wid.pack()

# rewind_btn replaying song
replay_btn = Button(can_wid, text="Replay", font="lucida 10 bold",
                    bg="green", fg="white", command=replay)
replay_btn.pack(side=LEFT, padx=10, pady=10)

# button for previous song
prev_btn = Button(can_wid, text="<<", font="lucida 10 bold",
                  bg="green", fg="white", command=prev)
prev_btn.pack(side=LEFT, padx=10, pady=10)

# play btn
play_btn = Button(can_wid, text="Play", font="lucida 13 bold",
                  bg="green", fg="white", command=play_pause)
play_btn.pack(side=LEFT, ipadx=5, ipady=5, padx=10, pady=10)

# button for next song
Button(can_wid, text=">>", font="lucida 10 bold", bg="green",
       fg="white", command=next).pack(side=LEFT, padx=10, pady=10)
# shuffle_btn
shuffle_btn = Button(can_wid, text="Shuffle", font="lucida 10 bold",
                     bg="green", fg="white", command=shuffle)
shuffle_btn.pack(side=LEFT, padx=10, pady=10)

# volume button and condition for different volume
vol_image = ImageTk.PhotoImage(Image.open(
    "imgs\\mute.png").resize((20, 20), Image.ANTIALIAS))
vol_btn = Button(can_wid, text="vol_btn", image=vol_image, bg="green")
vol_btn.pack(side=LEFT, padx=10)
vol_btn.bind("<Button-1>", mute_unmute)
# volume progessbar

scale = Scale(can_wid, from_=0, to=100, orient=HORIZONTAL,
              command=volume, bg="green", showvalue=0, width=10)
scale.pack(side=LEFT, padx=10)
scale.set(80)

root.mainloop()
