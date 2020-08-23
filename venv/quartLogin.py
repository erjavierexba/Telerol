
import base64
import os
import hypercorn.asyncio
from quart import Quart, render_template_string, url_for, request, redirect
from hypercorn.config import Config
import asyncio
from telethon import TelegramClient, utils, functions, types
from pymongo import MongoClient
from imgurpython import ImgurClient


def get_env(name, message):
    if name in os.environ:
        return os.environ[name]
    return input(message)


modoONLINE = False

BASE_TEMPLATE = '''<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
        <meta name="viewport" content="width=device-width, height=device-height, user-scalable=no">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/axios/0.19.2/axios.min.js" integrity="sha256-T/f7Sju1ZfNNfBh7skWn0idlCBcI3RwdLSS4/I7NQKQ=" crossorigin="anonymous"></script>
        <style>
            #overlay {
                position: fixed;
                display: none;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-color: rgba(0,0,0,0.5);
                z-index: 2;
                cursor: pointer;
            }
            .button:hover {
                filter: invert(81%) sepia(54%) saturate(169%) hue-rotate(157deg) brightness(96%) contrast(87%);
            }
            #overlay2 {
                position: fixed;
                display: none;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-color: rgba(0,0,0,0.5);
                z-index: 2;
                cursor: pointer;
            }
            body {
                background-color: lightblue;
                height:100%;
                overflow:hidden;
            }
            h1 {
                color: white;
                text-align: center;
            }
            p {
                font-family: verdana;
                font-size: 18px;
                margin: 0px;
            }
            .grid-container {
                display: grid;
                grid-template-columns: auto auto auto;
                padding: 10px;
            }
            ::-webkit-scrollbar {
                width: 12px;
            }
            ::-webkit-scrollbar-track {
                -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
                border-radius: 10px;
            }
            ::-webkit-scrollbar-thumb {
                border-radius: 10px;
                -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.8);
            }
            .grid-item {
                padding: 10px;
                font-size: 18px;
                text-align: center;
                vertical-align: center;
            }
            .grid-item-2pos {
                padding: 10px;
                font-size: 18px;
                text-align: center;
                vertical-align: center;
                grid-column: 2 / 4;
            }
            .grid-container-3 {
                display: grid;
                grid-template-columns: calc(100% / 3) calc(100% / 3) calc(100% / 3);
                grid-template-rows: calc(100%);
                overflow:hidden;
            }
            .grid-container-7 {
                display: grid;
                grid-template-columns: 10% 25% 10% 10% 10% 25% 10%;
                grid-template-rows: calc(100%);
                overflow:hidden;
            }
            .grid-container-icon {
                display: grid;
                grid-template-columns: 28% 36% 36%;
                grid-template-rows: calc(100%);
                overflow:hidden;
            }
            .grid-item-7 {
                font-size: 10px;
                text-align: center;
                vertical-align: text-top;
            }
            .grid-item-3 {
                font-size: 10px;
                text-align: center;
                vertical-align: text-top;
            }
            .grid-container-menu {
                display: grid;
                grid-template-columns: calc(100% / 5) calc(100% / 2.5) calc(100% / 2.5);
                grid-template-rows: 62em;
                overflow:hidden;
            }
            .grid-container-25-75 {
                display: grid;
                grid-template-columns: calc(25%) calc(75%) calc(100%); 
                overflow:hidden;
            }
            .grid-item-menu {
                font-size: 10px;
                text-align: center;
                vertical-align: text-top;
            }
            .grid-container-col1{
                height:100%;
                display: grid;
                grid-template-rows: calc(10%) calc(88%);
                grid-template-columns: 100%;
                grid-row-gap: 5px;
                overflow:hidden;
            }
            .grid-container-col2{
                height:100%;
                display: grid;
                grid-template-rows: calc(88%) calc(10%);
                grid-template-columns: 100%;
                grid-row-gap: 5px;
                overflow:hidden;
            }
            .grid-container-half{
                height:100%;
                width:50%;
                display: grid;
                grid-template-rows: calc(40%) calc(40%);
                grid-template-columns: 100%;
                grid-row-gap: 5px;
                overflow:hidden;
            }
            .grid-container-col3{
                height:100%;
                display: grid;
                grid-template-rows: calc(73%) calc(25%);
                grid-template-columns:  calc(73%) calc(25%);
                grid-row-gap: 5px;
                grid-column-gap: 5px;
                overflow:hidden;
            }
            .grid-item {
                font-size: 10px;
                text-align: center;
                vertical-align: text-top;
                height:100%;
            }
            .smallFont{
                font-size: 12px;
            }
            .header {
                background-color: white;
            }
            .half {
                width: 50%;
                height: 50%;
            }
            .vcentered{
                position: relative;
                top: 50%;
                transform: translateY(-50%);
            }
            .vcentrable{
                position:relative;
                height:100%;
                width:100%;
            }
            .max-height{
                height:100%;
            }
            .max-height2{
                height:97%;
            }
            input[type="color"] {
                -webkit-appearance: none;
                border: none;
                padding: 0;
                margin:0;
            }
            input[type="color"]::-webkit-color-swatch-wrapper {
                padding: 0;
                margin:0;
            }
            input[type="color"]::-webkit-color-swatch {
                border: none;
                padding: 0;
                margin:0;
            }
            .center {
                display: block;
                margin-left: auto;
                margin-right: auto;
                transform: translateY(50%);
                height:50%;
            }
            .bordered{
                border-style: outset;
            }
            .centered-white{
                background-color: rgba(255,255,255,1);
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translateX(-50%) translateY(-50%);
            }
        </style>
        <script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
        <script>
            function getRandomColor() {
                var letters = '0123456789ABCDEF';
                var color = '#';
                for (var i = 0; i < 6; i++) {
                    color += letters[Math.floor(Math.random() * 16)];
                }
                return color;
            }  
            function stringToHTML(str){
                var parser = new DOMParser();
                console.log(new DOMParser().parseFromString(str, 'text/html'));
                var doc = parser.parseFromString(str, 'text/html');
                return doc;
            }
            function deleteChat( chat){
                console.log('chat',chat)
                let varDel = 'chat_'+chat;
                let element = document.getElementById(varDel);
                element.parentNode.removeChild(element);
            }
            function myFunction( y ) {
                console.log(y)
                var reg = /^\d+$/;
                if(y == "Crear grupo"){
                    document.getElementById('menu').style.display = "none";
                    document.getElementById('crear_grupo').style.display = "block";
                }
                if(reg.test(y) && (document.getElementById('crear_grupo').style.display == "block") && (document.getElementById('chat_'+y)==null) ){
                    console.log("La id es " + y);
                    let id = document.getElementById('amigo_'+y).innerText;
                    let otros_datos = document.getElementById('amigo_otros_datos_'+y).innerText;
                    console.log("id", id, otros_datos);
                    var res = stringToHTML("<div id='chat_"+y+"' class='grid-container-3' style='width:100%;background-color:white;border:1px solid black;height:12%'> <div class='grid-item-3 vcentrable'><p class='vcentered'>"+id+"</p></div><div class='grid-container-25-75 grid-item-3'> <input class='grid-item' name='amigo_color_"+y+"' type='color' value='"+getRandomColor()+"'/> <input style='font-size: 14px;'  class='grid-item-' type='text' name='amigo_nickname_"+y+"' value="+id+"></input> </div> <input class='grid-item-3' type='text' style='display:none;' name='amigo_n_"+y+"' value="+y+"></input><div class='grid-item-3 vcentrable'><img class='vcentered button' onClick='deleteChat("+y+")' style='width:20px;height:20px;' src='/static/minusSimbol.png'></div>  </div>");
                    let divChild = res.getElementById('chat_'+y);
                    document.getElementById('new_usuarios').appendChild(divChild);
                }
            }
            function on( s ) {
                document.getElementById(s).style.display = "block";
            }
            function off( s ) {
                document.getElementById(s).style.display = "none";
            }
            function onClickAway(e) {
                e = e || window.event;
                var target = e.target || e.srcElement;
                if(target.id == "overlay"){
                    document.getElementById('menu').style.display = "block";
                    document.getElementById('crear_grupo').style.display = "block";
                    document.getElementById("overlay").style.display = "none";
                }
            }
        </script>
        <script  type="text/javascript">
            function readURL(input) {
                console.log("read URL ok",input.files && input.files[0],input.files, input.files[0]);
                if (input.files && input.files[0]) {
                    var reader = new FileReader();
                    reader.onload = function (e) {
                        $('#blah').attr('src', e.target.result);
                    }

                    reader.readAsDataURL(input.files[0]);
                }
            }
        </script>
        <meta charset='UTF-8'>
        <title>Telerol</title>
    </head>
    <body>
        <div id="overlay" onclick="onClickAway(event)">
            <div class="w3-card centered-white">
                <div style="width:80em;height:40em;">
                    <div class="grid-item-menu grid-container-3" style="padding:10px;height:100%;">
                        <div class="grid-item-3 max-height2" style="padding:5px;background-color: ghostwhite; overflow-y: scroll;">
                            {{ friends | safe }}
                        </div>
                        <div id="menu" class="grid-item-3 max-height2" style="width: 100%; background-color: ghostwhite; grid-column : 2 / 4">
                            <div class="vcentrable" style="height:35%;">
                                <div class="vcentered">
                                    <button style="background-color:white;margin:5px;width:95%; height:100px;" onclick="myFunction('Crear grupo')">
                                        <div style="background-color:white;margin:5px;">
                                            <div class="grid-item grid-container-icon" style="height:100%">
                                                <div class="grid-item-3 " style="margin:0px; grid-column: 1 / 4;">
                                                    <div class="grid-container-half vcentrable">
                                                        <span class="grid-item vcentered">
                                                            <p style="font-size:16px;">Crear grupo</p>
                                                        </span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </button>
                                </div>
                            </div>
                            <div class="vcentrable" style="height:35%;">
                                <div class="centrered">
                                    <button style="background-color:white;margin:5px;width:95%; height:100px;" onclick="myFunction('Agregar persona')">
                                        <div style="background-color:white;margin:5px;">
                                            <div class="grid-item grid-container-icon" style="height:100%">
                                                <div class="grid-item-3 " style="margin:0px; grid-column: 1 / 4;">
                                                    <div class="grid-container-half vcentrable">
                                                        <span class="grid-item vcentered">
                                                            <p style="font-size:16px;">Agregar persona</p>
                                                        </span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </button>
                                </div>
                            </div>
                            <div class="vcentrable" style="height:30%;">
                                <div  class="vcentered">
                                    <div class="grid-container-7">
                                        <div class="grid-item-7" style="grid-column: 2 / 3; background-color:#ffcccc;">
                                            <button style="background-color:#ffd2d2;margin:5px;width:95%; height:80px;" onclick="myFunction('Borrar grupo')">
                                                <div style="background-color:#ffd2d2;margin:5px;">
                                                    <div class="grid-item grid-container-icon" style="height:100%">
                                                        <div class="grid-item-3 " style="margin:0px; grid-column: 1 / 4;">
                                                            <div class="grid-container-half vcentrable">
                                                                <span class="grid-item vcentered">
                                                                    <p style="font-size:16px;">Borrar grupo</p>
                                                                </span>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </button>
                                        </div>
                                        <div class="grid-item-7" style="grid-column: 4 / 5;"></div>
                                        <div class="grid-item-7" style="grid-column: 6 / 7; background-color:#ffcccc;">
                                            <button style="background-color:#ffd2d2;margin:5px;width:95%; height:80px;" onclick="myFunction('Borrar persona')">
                                                <div style="background-color:#ffd2d2;margin:5px;">
                                                    <div class="grid-item grid-container-icon" style="height:100%">
                                                        <div class="grid-item-3 " style="margin:0px; grid-column: 1 / 4;">
                                                            <div class="grid-container-half vcentrable">
                                                                <span class="grid-item vcentered">
                                                                    <p style="font-size:16px;">Borrar persona</p>
                                                                </span>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div id="crear_grupo" class="grid-item-3 max-height2" style="display:none; grid-column : 2 / 4">
                            <div class="vcentrable" style="height:50%">
                                <div class="vcentered">
                                    <div style="background-color:white;margin:5px;" >
                                        <div class="grid-container-half vcentrable">
                                            <span class="grid-item vcentered">
                                                <p style="font-size:26px;">CREAR GRUPO</p>
                                            </span>
                                        </div>
                                        <div class="grid-container-half vcentrable">
                                            <div class="grid-container vcentered">
                                                <div class="grid-item">
                                                    <p style="font-size:16px;">Nombre del grupo</p>
                                                    <input name="nombre_grupo" style="font-size:16px;"></input>
                                                </div>
                                                <div class="grid-item">
                                                    <p style="font-size:16px;">Nombre del grupo</p>
                                                    <input name="foto_grupo" onchange="readURL(this)" id="foto_grupo" type="file"></input>
                                                </div>
                                                <div class="grid-item">
                                                    <img style="height:40px;width:40px;" id="blah" src="#" alt="Sin imagen seleccionada" />
                                                </div>
                                            </div>
                                        </div>
                                        <div class="grid-container-half vcentrable">
                                            <div class="grid-item vcentered">
                                                <p style="font-size:16px;">Pincha en los usuarios que quieres agregar</p> 
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="vcentrable" id="new_usuarios" style="height:40%; overflow-y: scroll;">
                                <div class='grid-container-3' style='width:100%;background-color:white;'>
                                    <div class='grid-item-3 vcentrable' style='border:1px solid black;font-weight: bold;'>
                                        <p class='vcentered'>USUARIO</p>
                                    </div>
                                    <div class='grid-item-3 vcentrable' style='border:1px solid black;font-weight: bold;'>
                                        <p class='vcentered'>COLOR/NICKNAME</p>
                                    </div>
                                    <div class='grid-item-3 vcentrable' style='border:1px solid black;font-weight: bold;'>
                                        <p class='vcentered'>ELIMINAR DEL GRUPO</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div id="overlay2" onclick="off('overlay2')">
            <div id="text">Overlay Text 2 :D</div>
        </div>
        {{ content | safe }}
    </body>
</html>
'''

PHONE_FORM = '''
<form action='/' method='post'>
    <div style="position: absolute; top: 50%;left: 50%;transform: translateX(-50%) translateY(-50%);background-color:white;">
        <div style="margin:20px;">
            <div style="margin:20px;">
                <div class="grid-container" style="vertical-align:center;">
                    <div class="grid-item"></div>
                    <div class="grid-item"><img src="https://i.ibb.co/hgn7tq7/Logo.png" align="middle" /></div>
                    <div class="grid-item"></div>
                </div>
            </div>
            <div style="margin:20px;">
                <div class="grid-container" style="vertical-align:center;">
                    <div class="grid-item"><p>Teléfono (formato internacional): </p></div>
                    <div class="grid-item"><input name='phone' class='w3-white' type='text' placeholder='+34600000000'></div>
                </div>
            </div>
            <div style="margin:20px;">
                <div class="grid-container" style="vertical-align:center;">
                    <div class="grid-item"><p>¿No eres un usuario?</p></div>
                    <div class="grid-item"><a href="https://web.telegram.org/#/loginuser">¡Registrate!</a></div>
                    <div class="grid-item"><input type='submit'></div>
                </div>
            </div>
            <div style="margin:20px;">
                <p  class="smallFont">
                    Al pulsar en "¡Registrate!" te enviaremos a crearte una cuenta de Telegram, cuando la hayas creado, ya podrás loguearte aquí.
                </p>
            </div>
        </div>
    </div>
</form>
'''

CODE_FORM = '''
<form action='/' method='post'>
    <div style="position: absolute; top: 50%;left: 50%;transform: translateX(-50%) translateY(-50%);background-color:white;">
        <div style="margin:20px;">
            <div style="margin:20px;">
                <div class="grid-container" style="vertical-align:center;">
                    <div class="grid-item"></div>
                    <div class="grid-item"><img src="https://i.ibb.co/hgn7tq7/Logo.png" align="middle" /></div>
                    <div class="grid-item"></div>
                </div>
            </div>
            <div style="margin:20px;">
                <div class="grid-container" style="vertical-align:center;">
                    <div class="grid-item"><p style="margin:10px;">Telegram code:</p></div>
                    <div class="grid-item"><input style="margin:10px;" name='code' type='text' placeholder='12345'></div>
                    <div class="grid-item"><input style="margin:10px;" type='submit'></div>
                </div>
            </div>
        </div>
    </div>
</form>
'''

MENU_FORM = '''
<div class="grid-container-3 header">
    <div class="grid-item-3">
        <div class="grid-container-3 vcentrable">
            <div class='grid-item-3 vcentrable'>
                <input type='button' class='w3-btn w3-white vcentered bordered' value='Configuración'>
            </div>
            <div class='grid-item-3'></div>
            <div class='grid-item-3'></div>
        </div>
    </div>
    <img class="grid-item-3 center" src="https://i.ibb.co/hgn7tq7/Logo.png"/>
    <div class="grid-item">
        <div class="grid-container-3 vcentrable">
            <div class='grid-item-3'></div>
            <div class='grid-item-3'></div>
            <form action='/disconnect' class='grid-item-3 vcentrable' method='post'>
                <button class='w3-btn w3-white vcentered bordered'>
                    Desconectar
                </button>
            </form>
        </div>
    </div>
</div>
<div class="grid-container-menu">
    <div class="grid-item-menu" style="padding:10px;">
        <div class="w3-panel w3-white w3-round-xlarge max-height">
            <div class="grid-container-col1" style="padding:5px;">
                <div class="grid-item grid-container-icon" style="padding:5px;">
                    <div class="grid-item-3" style="margin:5px;">
                        <img
                            src="https://lh3.googleusercontent.com/c3Ht55yqQwrA5ICTdFwPUzOJVV1aE95mLq1atMIXOM4ksF4a_EmKBzuSpM9Yt8lAzenv7Bv6sHsUtJIs5E7eR2o4OPqQ1s-XD06NrSvY8DNDsfYkwkstoeUdd9PspKVzPyFx1SQLq-VwI5jT_rZpOV3jJHm9qCfupKHgFXxk8j3Wbv1mcQfxNLxNZAjs0dZmuV4sQM1VWamGmeuKFgoMObnUILSHKWQKorxZKkCNG--i5GeEd6AWTcXqtzqAUWs0GNnbPXuc4ToYE7nh0B4jzzVLL6TX54eL90NbM701BqOtu5pu5UCvipirJO-cIqVMw05GGJMpt-7KL7k1WMUkCihzzJaEEaaodwlf5ngNB7vxXSqrC1SSRHeksbY084iI9ZYGK_gLpUb5z1c9YOfOt9miRjtfbAXY3yvk_gTGVvOBgcpOnshNrzuJnI-jPT1KvzeZZiD7BG_q9uN6j1qKkE2SJteJCnIDKRnSyTcl4EEPzFqqN9ILW-BbGXUMZX5JPxQk47NioiB4UqU_90qoyIQrKG0l04JwVkdyuC9FiSP9zX1XvXjQmoZNQsCZF0K8L-b7r-BSxiOH0Dad-VsH6feFebb5WQsHpfcn756uZr59jMS0t3IH3U7lbhr5YQM-dYjw8fARbGclPe23zwlZyOLvkaFmQCnp_L6WaMvAARnhwwF85FZLoA9hkyOocA=w671-h604-no"
                            style="height:100%;width:100%;"
                        >
                    </div>
                    <div class="grid-item-3 " style="margin:5px; grid-column: 2 / 4;">
                        <div class="grid-container-half vcentrable">
                            <span class="grid-item vcentered">
                                <p style="font-size:14px;width:80%;float:left;">{name}</p>
                                <button class="btn" style="float:left;" onclick="on('overlay')">
                                    <img src="https://image.flaticon.com/icons/svg/747/747376.svg" style="height:16px; width:16px;" alt="Error"/>
                                </button>
                            </span>
                            <span class="grid-item vcentered">
                                <p style="font-size:14px;width:80%;float:left;">{nickname}</p>
                                <button class="btn" style="float:left;" onclick="on('overlay2')">
                                    <img src="https://image.flaticon.com/icons/svg/2567/2567326.svg" style="height:16px; width:16px;" alt="Error"/>
                                </button>
                            </span>
                        </div>
                    </div>
                </div>
                <div class="grid-item" style="padding:5px;background-color: ghostwhite; overflow-y: scroll;">
                    {chats}
                </div>
            </div>
        </div>
    </div>
    <div class="grid-item-menu" style="padding:10px;">
        <div class="w3-panel w3-white w3-round-xlarge max-height">
            <div class="grid-container-col2" style="padding:5px;">
                <div class="grid-item" style="padding:5px;background-color: lightblue;">

                </div>
                <div class="grid-item" style="padding:5px;background-color: lightblue;">

                </div>
            </div>
        </div>
    </div>
    <div class="grid-item-menu" style="padding:10px;">
        <div class="w3-panel w3-white w3-round-xlarge max-height">
            <div class="grid-container-col3" style="padding:5px;">
                <div class="grid-item" style="padding:5px;background-color: lightblue;">

                </div>
                <div class="grid-item" style="padding:5px;background-color: lightblue;">

                </div>
                <div class="grid-item" style="padding:5px;background-color: lightblue;">

                </div>
                <div class="grid-item" style="padding:5px;background-color: lightblue;">

                </div>
            </div>
        </div>
    </div>
</div>
'''
# Session name, API ID and hash to use; loaded from environmental variables
SESSION = os.environ.get('TG_SESSION', 'quart')
API_ID = 94575
API_HASH = 'a3406de8d171bb422bb6ddf3bbd800e2'

# Telethon client
client = TelegramClient(None, API_ID, API_HASH)
phone = None

arrayClients = {}

# Quart app
app = Quart(__name__)
app.secret_key = 'a3406de8d171bb422bb6ddf3bbd800e2a3406de8d171bb422bb6ddf3bbd800e2'


# Helper method to format messages nicely
async def format_message(message):
    if message.photo:
        content = '<img src="data:image/png;base64,{}" alt="{}" />'.format(
            base64.b64encode(await message.download_media(bytes)).decode(),
            message.raw_text
        )
    else:
        # client.parse_mode = 'html', so bold etc. will work!
        content = (message.text or '(action message)').replace('\n', '<br>')

    return '<p><strong>{}</strong>: {}<sub>{}</sub></p>'.format(
        utils.get_display_name(message.sender),
        content,
        message.date
    )


# Connect the client before we start serving with Quart
@app.before_serving
async def startup():
    await client.connect()


# After we're done serving (near shutdown), clean up the client
@app.after_serving
async def cleanup():
    await client.disconnect()


@app.route('/disconnect', methods=['GET', 'POST'])
async def disconnect():
    ip = request.remote_addr
    ip = ip.replace('.', '_')
    global arrayClients
    await arrayClients[ip].log_out()
    del arrayClients[ip+'telf']
    del arrayClients[ip]
    return redirect('/')


@app.route('/', methods=['GET', 'POST'])
async def root():
    ip = request.remote_addr
    ip = ip.replace('.', '_')
    global arrayClients
    if ip in arrayClients:
        print('¡everything Wut!')
    else:
        arrayClients[ip] = TelegramClient(ip, API_ID, API_HASH)
        arrayClients[ip+'telf'] = None
    if arrayClients[ip].is_connected() == False:
        await arrayClients[ip].connect()
    form = await request.form
    if 'phone' in form:
        arrayClients[ip+'telf'] = form['phone']
        await arrayClients[ip].send_code_request(arrayClients[ip+'telf'])
    if 'code' in form:
        await arrayClients[ip].sign_in(code=form['code'])
    if await arrayClients[ip].is_user_authorized():
        ch = ''
        mongo = get_mongoDoc()
        amigos = ''''''
        for friend in (await arrayClients[ip](functions.contacts.GetContactsRequest(hash=0))).users:
            if(friend.mutual_contact is True):
                amigos = amigos + '''<button style="background-color:white;margin:5px;width:95%; height:100px;" onclick="myFunction({id})">
                        <div style="background-color:white;margin:5px;">
                            <div class="grid-item grid-container-icon" style="height:100%">
                                <div class="grid-item-3 " style="margin:0px; grid-column: 1 / 4;">
                                    <div class="grid-container-half vcentrable">
                                        <span class="grid-item vcentered">
                                            <p id="amigo_{id}" style="font-size:16px;">{fn}</p>
                                            <p id="amigo_otros_datos_{id}"style="font-size:12px;color:grey;">Nick: {us}  Tlf: {telf}</p>
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </button>
                '''.format(id=friend.id, fn=friend.first_name, us=friend.username, telf=friend.phone)
        me = await arrayClients[ip].get_me()
        for dialog in await arrayClients[ip].get_dialogs():
            chatMongo = mongo.find_one({"idChat": str(dialog.entity.id)})
            if chatMongo is not None:
                ch = ch + '''
                    <button style="background-color:white;margin:5px;width:95%; height:100px;" onclick="myFunction({id})">
                        <div style="background-color:white;margin:5px;">
                            <div class="grid-item grid-container-icon" style="height:100%">
                                <div class="grid-item-3" style="margin:5px;">
                                    <img src={photo} style="height:100%;width:100%;" >
                                </div>
                                <div class="grid-item-3 " style="margin:0px; grid-column: 2 / 4;">
                                    <div class="grid-container-half vcentrable">
                                        <span class="grid-item vcentered">
                                            <p style="font-size:16px;">{name}</p>
                                            <p style="font-size:12px;color:grey;">Nick: {nickname}</p>
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </button>
                '''.format(
                    name=dialog.name,
                    photo=chatMongo['idToPhoto'][str(me.id)],
                    id=str(dialog.entity.id),
                    nickname=chatMongo['idToNickname'][str(me.id)]
                )
        return await render_template_string(BASE_TEMPLATE, friends=amigos, content=MENU_FORM.format(nickname=me.first_name, name='@'+me.username, chats=ch))

    # Ask for the phone if we don't know it yet
    if arrayClients[ip+'telf'] is None:
        return await render_template_string(BASE_TEMPLATE, content=PHONE_FORM)

    return await render_template_string(BASE_TEMPLATE, content=CODE_FORM)


def get_imgCli():
    CLIENT_ID = 'e16b30a76cbed68'
    CLIENT_SECRET = '8796078f422ceac6352c97ed8ffc33c3c08a4665'
    client = ImgurClient(CLIENT_ID, CLIENT_SECRET)
    return client


def get_mongoDoc():
    client = MongoClient(
        "mongodb+srv://Telerol:MONOPOLy3@teleroldb-jvhhg.mongodb.net/test?retryWrites=true&w=majority")["Telerol"]["chats"]
    return client


async def main():
    if modoONLINE == True:
        # web: telerol.ddns.net
        config = Config()
        config.bind = ["192.168.1.39:5000"]
        await hypercorn.asyncio.serve(app, config)
    else:
        await hypercorn.asyncio.serve(app, hypercorn.Config())

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
