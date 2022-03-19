import tkinter as gui
from tkinter import ttk
from pytube import YouTube
import os
import re
import requests
from io import BytesIO
from PIL import Image, ImageTk


class YDownloader:
    """ YouTube Video Dowloader """
    def __init__(self):
        self.__window = gui.Tk()
        self.scren_setup()

    def scren_setup(self):
        self.__window.title('YouTube Video Downloader')
        self.__window.iconbitmap('128.ico')
        self.__window.geometry('800x600')
        self.__window.maxsize(1920,1080)
        self.__window.minsize(800, 640)
        self.__programm_interface()
        self.__window .mainloop()
        print("<screen setup> init end")


    def __programm_interface(self):
        self.heard = gui.Frame(master = self.__window, width = 1920,  height = 1080, bg = '#708090')
        self.greeting = gui.Label(master = self.heard, font='Arial 14', text='Вставьте ссылку на видео!', bg = '#708090', fg = '#F8F8FF')
        self.greeting.pack()
        self.video_shref = gui.Entry(master = self.heard, font='Arial 12', width=60)
        self.video_shref.pack()
        self.download_button = gui.Button(master = self.heard, text='скачать', width=16, height=2, font='Arial 18', bg="#FF6347", fg="#F8F8FF", command=self.get_shref).pack(pady=5)
        self.heard.pack(fill=gui.BOTH, side=gui.LEFT, expand=True)
        print("<programm interface> init end")


    def get_shref(self):
        video_url = (self.video_shref.get())
        result = re.match(r'https://www.youtube.com', video_url)
        if result is not None:
            obj = YouTube(video_url)
            self.image_preview(obj)
            self.video_download(obj)
        else:
            self.greeting['text'] = 'Эта ссылка не прошла проверку!'


    def image_preview(self, img_obj):
        """ imege preview """
        self.img_obj = img_obj
        self.link = (self.img_obj.thumbnail_url)
        print(self.link)
        # fix me :3 (
        self.img_shref = requests.get(self.link)
        self.url_image = ImageTk.PhotoImage(Image.open(BytesIO(self.img_shref.content)))
        self.img = gui.Label(master = self.heard, image = self.url_image)
        self.img.configure(image=self.url_image)
        self.img.image = self.url_image
        self.img.pack(pady=10)
        # )
        print("<image_preview> картинка установленна!")



    def video_download(self, video_obj):
        """ download video """
        self.greeting['text'] = 'Идёт скачивание видео.'
        stream = video_obj.streams.get_highest_resolution()
        user_dowlnoad = (f"{os.environ['USERPROFILE']}\\Downloads")
        stream.download(user_dowlnoad)
        print("<video_download> загрузка видео завершена!")
        self.greeting['text'] = 'Вставьте ссылку на видео!'

if __name__ == '__main__':
    main = YDownloader()
    main
