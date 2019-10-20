from website import *
from requests import get
from flask import Flask, request, render_template
from telethon import functions, types, events, sync, TelegramClient
from pymongo import MongoClient
from telethon.tl.functions.users import GetFullUserRequest
from random import randrange
from imgurpython import ImgurClient
from PIL import Image
from io import BytesIO
import asyncio
import sqlite3
import socket
import constant
import collections

COLORS = [("BLUE", (255, 0, 0, 255)), ("GOLDEN", (218, 165, 32, 255)), ("LIME GREEN", (50, 205, 50, 255)),
          ("DARK ORCHID", (153, 50, 204, 255)), ("CHOCOLATE", (210, 105, 30, 255)),
          ("LIGHT STEEL BLUE", (176, 196, 222, 255)), ("NAVY", (0, 0, 128, 255)), ("PURPLE", (128, 0, 128, 255)),
          ("GRAY", (128, 128, 128, 255)), ("MAGENTA", (255, 0, 255, 255)), ("CYAN", (0, 255, 255, 255)),
          ("CORNFLOWERBLUE", (100, 149, 237, 255)), ("INDIGO", (75, 0, 130, 255)), ("GREENYELLOW", (173, 255, 47, 255)),
          ("MISTYROSE", (255, 228, 225, 255)), ("NAVAJOWHITE", (255, 222, 173, 255)),
          ("HONEYDEW", (240, 255, 240, 255)),
          ("LAVENDERBLUSH", (255, 240, 245, 255)), ("BLUEVIOLET", (138, 43, 226, 255)), ("CRIMSON", (220, 20, 60, 255)),
          ("PALEVIOLETRED", (219, 112, 147, 255)), ("FIREBRICK", (178, 34, 34, 255)), ("SALMON", (250, 128, 114, 255)),
          ("GOLD", (255, 215, 0, 255)), ("HOTPINK", (255, 105, 180, 255)), ("DEEPSKYBLUE", (0, 191, 255, 255))]

app = Flask(__name__)
users = ""
tCli = ""
iCli = ""
mCli = ""
me = ""


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


async def getUsers(client):
    res = []
    contacts = await client(functions.contacts.GetContactsRequest(hash=0))
    for i in contacts.users:
        res.append(i)
    return res


##TODO upgrade :D
def searchUsername(fname, users):
    for i in users:
        if fname == i.first_name:
            return i


async def allDialogs(client):
    res = []
    async for dialog in client.iter_dialogs():
        res.append('{:>14}: {}'.format(dialog.id, dialog.title))
    return res
def getcolors():
    return COLORS

def upload_img(client, pathImg):
    image = client.upload_from_path(pathImg)
    return image


def get_img(url, name):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.save(name + ".png", "PNG")
    return img


def get_imgCli():
    CLIENT_ID = 'e16b30a76cbed68'
    CLIENT_SECRET = '8796078f422ceac6352c97ed8ffc33c3c08a4665'
    client = ImgurClient(CLIENT_ID, CLIENT_SECRET)
    return client


def get_mongoDoc():
    client = MongoClient("mongodb+srv://Telerol:MONOPOLy3@teleroldb-jvhhg.mongodb.net/test?retryWrites=true&w=majority")
    db = client["Telerol"]
    collection = db["chats"]
    return collection


async def connect():
    api_id = 94575
    api_hash = 'a3406de8d171bb422bb6ddf3bbd800e2'
    ipPub = get('https://api.ipify.org').text
    ipPriv = get_ip()
    ip = "Telerol: " + ipPriv + " " + ipPub
    tClient = TelegramClient(ip, api_id, api_hash)
    await tClient.start()
    mClient = get_mongoDoc()
    iClient = get_imgCli()
    return tClient, mClient, iClient


def createGroup(tClient, mClient, users, name, me):
    admin = me
    colours = COLORS
    value = randrange(len(colours))
    idTofName = {}
    idToColor = {}
    idTofName[str(admin.id)] = admin.first_name
    idToColor[str(admin.id)] = colours[value]
    colours.remove(colours[value])
    for user in users:
        idTofName[str(user.id)] = user.first_name
        value = randrange(len(colours))
        idToColor[str(user.id)] = colours[value]
        colours.remove(colours[value])
    idToNickname = idTofName
    # TODO idToPhoto
    result = tClient(functions.messages.CreateChatRequest(users=users, title=name))
    '''
    idChat = str(result.chats[0].id)
    dic = {}
    dic["idChat"] = idChat
    dic["idTofName"] = idTofName
    dic["idToNickname"] = idTofName
    dic["idToColor"] = idToColor
    mClient.insert_one(dic)
    return result, mClient.find_one({"idChat": str(idChat)})
    '''

async def main():
    '''
    ip= "149.154.167.40"
    api_id = 94575
    api_hash = 'a3406de8d171bb422bb6ddf3bbd800e2'
    tClient = TelegramClient(None, api_id, api_hash)
    tClient.session.set_dc(2, ip , 80)
    await tClient.start(phone="9996624545", code_callback=lambda : "22222")
    '''

    await main_web()


if __name__ == "__main__":
    start()
