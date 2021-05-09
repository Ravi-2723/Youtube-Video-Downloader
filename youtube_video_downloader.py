from tkinter import *
from tkinter import filedialog as fd
import tkinter.messagebox as msgbox
from pytube import YouTube
import os
from _thread import *

def download_func():
    link = link_value.get()
    file_name = file_name_value.get()

    if link != '':
        link_checker(link, file_name)
    else:
        msgbox.showerror('Error', 'Please Enter a link')
        return

def link_checker(link, file_name):
    try:
        con = YouTube(link)
    except:
        msgbox.showerror('Error', 'Enter a valid link')

    start_new_thread(downloader, (con, file_name))

def downloader(con, file_name):
    video = con.streams.get_by_itag(137)
    audio = con.streams.get_by_itag(140)
    
    if path:
        audio_data = audio.download(output_path=path)
    else:
        audio_data = audio.download()
    if file_name != '':
        base, _ = os.path.split(audio_data)
        audio_data_new = base + '/' + file_name + '.mp3'
        os.rename(audio_data, audio_data_new)
    else:
        base, _ = os.path.splitext(audio_data)
        audio_data_new = base + '.mp3'
        os.rename(audio_data, audio_data_new)
    if path:
        video_data = video.download(output_path=path)
    else:
        video_data = video.download()
    if file_name != '':
        base, _ = os.path.split(video_data)
        video_data_new = base + '/' + file_name + '.mp4'
        os.rename(video_data, video_data_new)

    msgbox.showinfo('Notification', 'Downloaded')
    
def file_sel_func():
    global path
    path = fd.askdirectory()

surface = Tk()
surface.geometry('200x100')
surface.title('Youtube Video Downloader')

link_value = StringVar()
file_name_value = StringVar()
path = None

link_label = Label(surface, text='Link').grid(row=0, column=0)
file_name_label = Label(surface, text='File Name').grid(row=1, column=0)

link_entry = Entry(surface, textvariable=link_value).grid(row=0, column=1)
file_name_entry = Entry(surface, textvariable=file_name_value).grid(row=1, column=1)

file_selector = Button(surface, text='File', command=file_sel_func).grid(row=2, column=1)
download_button = Button(surface, text='Download', command=download_func).grid(row=3, column=1)

surface.mainloop()
