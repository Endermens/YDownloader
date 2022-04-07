import tkinter as gui
from tkinter import ttk, filedialog, PhotoImage
from pytube import YouTube
import os, sys
import re
import requests
from io import BytesIO
import base64
from img_to_exe import tk_icon, pakage_icon
from PIL import Image, ImageTk


class YDownloader:
    """ YouTube Video Dowloader """
    def __init__(self):
        self.__window = gui.Tk()
        self.attempts = 0
        self.filename = (f"{os.environ['USERPROFILE']}\\Downloads")
        self.scren_setup()

    def __exe_file_pass(self, icon_id, icon_name):
        """dont touch me!"""
        icondata= base64.b64decode(icon_id)
        tempFile= icon_name
        iconfile= open(tempFile,"wb")
        iconfile.write(icondata)
        iconfile.close()
        return tempFile

    def scren_setup(self):
        self.__window.title('YouTube Video Downloader')
        self.__window.wm_iconbitmap(self.__exe_file_pass(tk_icon, "128.ico"))
        os.remove("128.ico")
        self.__window.geometry('800x600')
        self.__window.maxsize(1920,1080)
        self.__window.minsize(800, 640)
        self.__programm_interface()
        self.__window .mainloop()


    def __programm_interface(self):
        self.heard = gui.Frame(master = self.__window, bg = '#708090')
        self.greeting = gui.Label(master = self.heard, font='Arial 14', text='Вставьте ссылку на видео', bg = '#708090', fg = '#F8F8FF')
        self.greeting.pack(side="top")
        self.video_shref = gui.Entry(text="aboba", master = self.heard, font='Arial 12', width=60)
        self.video_shref.pack(side="left", anchor="e", expand=True)
        folder_img = PhotoImage(file = self.__exe_file_pass(pakage_icon, "video16.png"))
        os.remove("video16.png")
        self.pass_folder = gui.Button(master = self.heard, image = folder_img, command=self.folder_pass)
        self.pass_folder.image = folder_img
        self.pass_folder.pack(side="left", anchor="w", expand=True, padx=8)
        self.heard.pack(fill=gui.X, side=gui.TOP)

        self.body = gui.Frame(master = self.__window, height = 40, bg = '#708090')
        self.download_button = gui.Button(master = self.body, text='скачать', width=16, height= 2, font='Arial 18', bg="#FF6347", fg="#F8F8FF", command=self.get_shref).pack(side="left", anchor="e", expand=True, pady=5)
        self.var = gui.IntVar()
        self.var.set(1)
        self.mp3 = gui.Radiobutton(master = self.body, font='Arial 14', text="mp3", variable=self.var, value=0, bg='#708090', fg="#FFFFFF", activebackground="#708090", activeforeground="red", selectcolor="#708090")
        self.mp4 = gui.Radiobutton(master = self.body, font='Arial 14', text="mp4", variable=self.var, value=1, bg='#708090', fg="#FFFFFF", activebackground="#708090", activeforeground="red", selectcolor="#708090")
        self.mp3.pack(side="top", anchor="w",  expand=True)
        self.mp4.pack(side="left", anchor="w",  expand=True)
        self.body.pack(fill=gui.X, side=gui.TOP)

        self.foot = gui.Frame(master = self.__window, height = 600, bg = '#708090')
        self.foot.pack(fill=gui.BOTH, side=gui.TOP, expand=True)


    def get_shref(self):
        video_url = (self.video_shref.get())
        result1 = re.match(r'https://www.youtube.com', video_url)
        result2 = re.match(r'https://youtu.be', video_url)
        if result1 or result2 is not None:
            obj = YouTube(video_url)
            if self.var.get() == 1:
                print("var:1")
                self.image_preview(obj)
                self.video_download(obj)
            else:
                print("var:0")
                obj_mp3 = YouTube(video_url).streams.filter(only_audio=True).first()
                self.image_preview(obj)
                self.audio_download(obj_mp3)


    def folder_pass(self):
        """get folder path"""
        folder_path = gui.StringVar()
        self.filename = filedialog.askdirectory()
        folder_path.set(self.filename)
        print(self.filename)


    def image_preview(self, img_obj):
        """ imege preview """
        link = (img_obj.thumbnail_url)
        img_shref = requests.get(link)

        if self.attempts == 0:
            url_image = ImageTk.PhotoImage(Image.open(BytesIO(img_shref.content)))
            self.img = gui.Label(master = self.foot, image = url_image)
            self.img.configure(image=url_image)
            self.img.image = url_image
            self.img.pack(pady=10)
        else:
            url_image1 = ImageTk.PhotoImage(Image.open(BytesIO(img_shref.content)))
            self.img.configure(image=url_image1)
            self.img.image = url_image1


    def audio_download(self, audio_obj):
        """download audio"""
        self.greeting['text'] = 'Идёт загрузка аудио'
        stream = audio_obj
        self.__user_dowlnoad = (f"{os.environ['USERPROFILE']}\\Downloads")
        if self.__user_dowlnoad != self.filename:
            self.__user_dowlnoad = self.filename
        downloaded_audio = stream.download(self.__user_dowlnoad)
        base, ext = os.path.splitext(downloaded_audio)
        new_file = base + '.mp3'
        try:
            os.rename(downloaded_audio, new_file)
        except FileExistsError:
            os.remove(downloaded_audio)
        print(new_file)
        self.greeting['text'] = 'Вставьте ссылку на видео!'
        self.attempts += 1


    def video_download(self, video_obj):
        """ download video """
        self.greeting['text'] = 'Идёт загрузка видео'
        stream = video_obj.streams.get_highest_resolution()
        self.__user_dowlnoad = (f"{os.environ['USERPROFILE']}\\Downloads")
        if self.__user_dowlnoad != self.filename:
            self.__user_dowlnoad = self.filename
        stream.download(self.__user_dowlnoad)
        self.greeting['text'] = 'Вставьте ссылку на видео!'
        self.attempts += 1

if __name__ == '__main__':
    main = YDownloader()
    main
