from asyncClient import *
from imageF import *
from telethon import *
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from async_timeout import timeout
from quart import Quart, request, render_template, redirect, url_for
import asyncio
import json
import urllib.parse
import ast
from dice import diceThrow
from os import listdir
app = Quart(__name__)
mClient = get_mongoDoc()
iClient = get_imgCli()
sessions = {}
tClient = ""
me = ""
def nullToStr(word):
    if word == None:
        return ""
    else:
        return str(word)

@app.route("/welcome" , methods=['GET, POST'])
def welcome():
    ip = request.remote_addr
    things = sessions[ip]

    if request.method == 'POST':
        return redirect(url_for('me'))




@app.route("/nono", methods=['GET', 'POST'])
def conn():
    ip = request.remote_addr
    if os.path.exists(ip+".session"):
        redirect(url_for('welcome'))
    if request.method == 'GET':
        return render_template('login.html')
    else:
        values = request.form
        if values['part'] == "2":
            telf = values['telf']
            loop = asyncio.new_event_loop()
            loop.run_until_complete(startTele(ip, telf, loop))
            return render_template('login.html', part="2", )
        else:
            codigo = values['codigo']
            global sessions
            loop = sessions[ip][2]
            loop.run_until_complete(sign_in_tele(ip, codigo))
            return redirect(url_for('welcome'))

async def sign_in_tele(ip, codigo):
    global sessions
    telf, client, loop = sessions[ip]
    me = await client.sign_in(telf, codigo)
    await client.start()
    un = me.username
    sessions[ip] = (telf, client, loop, un)
async def startTele(ip, telf, loop):
    global sessions
    tclient = TelegramClient(str(ip), 94575, 'a3406de8d171bb422bb6ddf3bbd800e2')
    await tclient.connect()
    if not await tclient.is_user_authorized():
        await tclient.send_code_request(telf, force_sms=False)
        #await tclient.send_code_request(telf, force_sms=True)
    sessions[ip]= (telf, tclient, loop)
@app.route("/create-group", methods=['GET', 'POST'])
def static_page():
    args = []
    global users
    for i in users:
        args.append((str(i.id), i.first_name, nullToStr(i.last_name), i.phone))

    if request.method == 'POST':
        values = request.form
        if (values['desc'] == "Desconectar"):
            users = []
            loop = asyncio.new_event_loop()
            loop.run_until_complete(disconn(request.remote_addr))
            loop.close()
        else:
            loop = asyncio.new_event_loop()
            loop.run_until_complete(formatChat(values))
            loop.close()
        return render_template('contacts.html', lenUsers=len(users), user=args)
    else:

        return render_template('contacts.html', lenUsers=len(users), user=args)


async def disconn(ip):
    global sessions
    clients = sessions[ip]
    if ip in sessions: del sessions[ip]
    await clients[1].log_out()


async def formatChat(values):

    global client
    users = await getUsers(client[0])
    clients = await  connect()
    me = await clients[0].get_me()
    imgurC = clients[2]

    us = []
    us.append(me)
    nombre = ""
    for i in values:
        if i == "gname":
            nombre = values[i]
        else:
            us.append(users[int(i)])
    colours = getcolors()
    idTofName = {}
    idToColor = {}
    idToPhoto = {}
    for user in us:
        idTofName[str(user.id)] = user.first_name
        value = randrange(len(colours))
        idToColor[str(user.id)] = colours[value]

        createDefaultProfilePhoto(colours[value])
        link = upload_img(imgurC, "profile-photos/" + colours[value][0] + ".png")
        colours.remove(colours[value])
        idToPhoto[str(user.id)] = link['link']
    result = await clients[0](functions.messages.CreateChatRequest(users=us, title=nombre))
    idChat = str(result.chats[0].id)
    dic = {"idChat": idChat, "idTofName": idTofName, "idToNickname": idTofName, "idToColor": idToColor,
           "idToPhoto": idToPhoto}
    clients[1].insert_one(dic)


async def clientAndUsers():
    client = await connect()
    users = await getUsers(client[0])
    return client, users


@app.route("/", methods=["GET", "POST"])
async def mainPage():
    '''
    global tClient, mClient
    ip = "149.154.167.40"
    api_id = 94575
    api_hash = 'a3406de8d171bb422bb6ddf3bbd800e2'
    tClient = TelegramClient("Espain", api_id, api_hash)
    tClient.session.set_dc(2, ip, 80)
    await tClient.start(phone="9996624545", code_callback=lambda: "22222")

    await tClient.connect()
    me = await  tClient.get_me()
    query = {"idTofName." + str(me.id): str(me.first_name)}
    allChats = mClient.find(query)
    chats = []
    for i in allChats:
        ids = i['_id']
        keys = i['idTofName'].keys()
        c = await tClient.get_entity(ids)
        print(c)
        userInfo = {}
        for j in keys:
            userInfo[j] = (i['idTofName'][j], i['idToNickname'][j], i['idToColor'][j], i['idToPhoto'][j])
            chat = [ids, userInfo]
        chats.append(chat)

'''
    if request.method == 'GET':
        return await render_template('main.html' )
    else:
        api_id = 94575
        api_hash = 'a3406de8d171bb422bb6ddf3bbd800e2'
        tClient = TelegramClient("n", api_id, api_hash)
        await tClient.connect()



        async with timeout(app.config['BODY_TIMEOUT']):
            async for data in request.body:
                data = data.decode('utf-8')
                data = data.replace("\n", "LD7ko0MdqFUQFjVGw2tF")
                data = ast.literal_eval(data)
                data['data']=data['data'].replace("LD7ko0MdqFUQFjVGw2tF", "\n")
                evals = data['data'].find("/d(")
                while evals >= 0:
                    startPos =data['data'].find("/d(")
                    endPos = data['data'].find(")",startPos)
                    dice = data['data'][startPos+3:endPos]
                    result = diceThrow(dice)
                    data['data'] = data['data'][:startPos]+"(["+dice+"] = "+str(result[0])+")"+ data['data'][endPos+1:]
                    evals = data['data'][endPos+1:].find("/d(")

        await tClient.send_message("me", data['data'])
        return {}
def main_web():
    app.run( )
'''
    test = os.listdir()
    for item in test:
        if item.endswith(".session"):
            os.remove(item)
'''


