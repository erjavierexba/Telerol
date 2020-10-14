
import base64
import os
import hypercorn.asyncio
from quart import Quart, render_template_string, url_for, request, redirect, jsonify
from hypercorn.config import Config
from pathlib import Path
import asyncio
from telethon import TelegramClient, utils, functions, types, events
from pymongo import MongoClient
from imgurpython import ImgurClient
from PIL import Image
from io import BytesIO
import numpy as np
from datetime import datetime
from dice import diceThrow, printMem
from imageF import createToken
def get_env(name, message):
    if name in os.environ:
        return os.environ[name]
    return input(message)


modoONLINE = False

modoSoloTexto = False

BASE_TEMPLATE = '''<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
        <meta name="viewport" content="width=device-width, height=device-height, user-scalable=no">
        <style>
            .dropup:hover .dropup-content {
                display: block;
            }
            .dropup-content {
                display: none;
                position: absolute;
                bottom: 30px;
                width:375%;
                height:125%
                z-index: 3;
            }
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
            #diceCalculator {
                position: fixed;
                display: none;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-color: rgba(0,0,0,0.5);
                z-index: 60;
                cursor: pointer;
            }
            #editPerfil {
                position: fixed;
                display: none;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-color: rgba(0,0,0,0.5);
                z-index: 60;
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
            .grid-container-message-input {
                display: grid;
                grid-template-columns: 20% 62% 18%;
                padding: 2px;
                vertical-align: middle;
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
            .grid-container-submenu-sender {
                display: grid;
                grid-template-columns: 1fr 1fr;
                grid-template-rows: 1fr 1fr;
                gap: 1px 1px;
                grid-template-areas:
                    "btnSubMenu1 btnSubMenu2"
                    "btnSubMenu3 btnSubMenu4";
            }
            .btnSubMenu1 { grid-area: btnSubMenu1; }
            .btnSubMenu2 { grid-area: btnSubMenu2; }
            .btnSubMenu3 { grid-area: btnSubMenu3; }
            .btnSubMenu4 { grid-area: btnSubMenu4; }
            .grid-item {
                padding: 10px;
                font-size: 18px;
                text-align: center;
                vertical-align: center;
            }
            .grid-item-chat {
                padding: 2px;
                font-size: 16px;
                text-align: left;
                vertical-align: center;
            }
            .grid-item-chat-2 {
                padding: 2px;
                font-size: 16px;
                text-align: right;
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
            .grid-container-message {
                display: grid;
                grid-template-columns: 91% 9%;
                grid-template-rows: calc(100%);
            }
            .grid-container-message-2 {
                display: grid;
                grid-template-columns: 9%  91% ;
                grid-template-rows: calc(100%);
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
                grid-template-rows: calc(87%) calc(10%);
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
            .chat_header{
                width:100%;
                height:10%;
                display: grid;
                grid-template-rows: calc(20%) calc(70%) calc(10%);
                border-bottom: 1px solid black;
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
            .tooltip {
                position: relative;
                display: inline-block;
                border-bottom: 1px dotted black;
            }
            .tooltip .tooltiptext {
                visibility: hidden;
                width: 120px;
                background-color: black;
                color: #fff;
                text-align: center;
                border-radius: 6px;
                padding: 5px 0;
                position: absolute;
                z-index: 1;
            }
            .tooltip:hover .tooltiptext {
                visibility: visible;
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
        <script>
            function post(path, params, method='post') {
                const form = document.createElement('form');
                form.method = method;
                form.action = path;
                for (const key in params) {
                    if (params.hasOwnProperty(key)) {
                    const hiddenField = document.createElement('input');
                    hiddenField.type = 'hidden';
                    hiddenField.name = key;
                    hiddenField.value = params[key];
                    form.appendChild(hiddenField);
                    }
                }
                document.body.appendChild(form);
                form.submit();
            }
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
            function sendDiceMessage( id ){
                let bod = {
                    'id':id,
                    'plusminusd4':document.getElementById("plusminusd4").value,
                    'd4':document.getElementById("d4").value,
                    'plusminusd6':document.getElementById("plusminusd6").value,
                    'd6':document.getElementById("d6").value,
                    'plusminusd8':document.getElementById("plusminusd8").value,
                    'd8':document.getElementById("d8").value,
                    'plusminusd10':document.getElementById("plusminusd10").value,
                    'd10':document.getElementById("d10").value,
                    'plusminusd12':document.getElementById("plusminusd12").value,
                    'd12':document.getElementById("d12").value,
                    'plusminusd20':document.getElementById("plusminusd20").value,
                    'd20':document.getElementById("d20").value,
                    'plusminusd100':document.getElementById("plusminusd100").value,
                    'd100':document.getElementById("d100").value,
                    'plusminuscustom':document.getElementById("plusminuscustom").value,
                    'dCustom':document.getElementById("dCustom").value,
                    'dCustomSize':document.getElementById("dCustomSize").value,
                    'mod':document.getElementById("mod").value,
                }
                let res = '';
                if(parseInt(bod['d4'])>0) res = res + bod['plusminusd4']+bod['d4']+"d4";
                if(parseInt(bod['d6'])>0) res = res + bod['plusminusd6']+bod['d6']+"d6";
                if(parseInt(bod['d8'])>0) res = res + bod['plusminusd8']+bod['d8']+"d8";
                if(parseInt(bod['d10'])>0) res = res + bod['plusminusd10']+bod['d10']+"d10";
                if(parseInt(bod['d12'])>0) res = res + bod['plusminusd12']+bod['d12']+"d12";
                if(parseInt(bod['d20'])>0) res = res + bod['plusminusd20']+bod['d20']+"d20";
                if(parseInt(bod['d100'])>0) res = res + bod['plusminusd100']+bod['d100']+"d100";
                if(parseInt(bod['dCustom'])>0 && parseInt(bod['dCustomSize'])>0) res = res + bod['plusminuscustom']+bod['dCustom']+"d"+bod['dCustomSize'];
                if(parseInt(bod['mod']) >= 0) res = res + "+" +bod['mod'];
                else res = res  +bod['mod'];
                axios.post('/sendDiceMessage',{idChat:id,data:res})
                        .then(function (response) {
                            console.log(response.data);
                            document.getElementById("plusminusd4").value = "+";
                            document.getElementById("d4").value = "0";
                            document.getElementById("plusminusd6").value= "+";
                            document.getElementById("d6").value = "0";
                            document.getElementById("plusminusd8").value= "+";
                            document.getElementById("d8").value = "0";
                            document.getElementById("plusminusd10").value= "+";
                            document.getElementById("d10").value = "0";
                            document.getElementById("plusminusd12").value= "+";
                            document.getElementById("d12").value = "0";
                            document.getElementById("plusminusd20").value= "+";
                            document.getElementById("d20").value = "0";
                            document.getElementById("plusminusd100").value= "+";
                            document.getElementById("d100").value = "0";
                            document.getElementById("plusminuscustom").value= "+";
                            document.getElementById("dCustom").value = "0";
                            document.getElementById("dCustomSize").value = "0";
                            document.getElementById("mod").value = "0";
                            document.getElementById("diceCalculator").style.display = "none";
                        });
            }
            function deleteChat( chat){
                let varDel = 'chat_'+chat;
                let element = document.getElementById(varDel);
                element.parentNode.removeChild(element);
            }
            function myFunction( y ) {
                console.log(y)
                var reg = /^\d+$/;
                if(y == "Crear grupo"){
                    off('menu');
                    on('crear_grupo');
                    document.getElementById('mi_color').value = getRandomColor();
                    if(document.getElementById('mi_nickname').value=='') document.getElementById('mi_nickname').value = getRandomNombre();
                }
                if( y == 'backToMenu'){
                    on('menu');
                    off('crear_grupo');
                }
                if(reg.test(y) && (document.getElementById('crear_grupo').style.display == "block") && (document.getElementById('chat_'+y)==null) ){
                    console.log("La id es " + y);
                    let id = document.getElementById('amigo_'+y).innerText;
                    let otros_datos = document.getElementById('amigo_otros_datos_'+y).innerText;
                    console.log("id", id, otros_datos);
                    var res = stringToHTML("<div id='chat_"+y+"' class='grid-container-3' style='width:100%;background-color:white;border:1px solid black;height:12%'> <div class='grid-item-3 vcentrable'><p class='vcentered'>"+id+"</p></div><div class='grid-container-25-75 grid-item-3'> <input class='grid-item' name='amigo_color_"+y+"' type='color' value='"+getRandomColor()+"'/> <input style='font-size: 14px;text-align: center;'  class='grid-item-' type='text' name='amigo_nickname_"+y+"' value='"+getRandomNombre()+"'></input> </div> <input class='grid-item-3' type='text' style='display:none;' name='amigo_n_"+y+"' value="+y+"></input><div class='grid-item-3 vcentrable'><img class='vcentered button' onClick='deleteChat("+y+")' style='width:20px;height:20px;' src='/static/minusSimbol.png'></div>  </div>");
                    let divChild = res.getElementById('chat_'+y);
                    document.getElementById('new_usuarios').appendChild(divChild);
                }
            }
            function on( s ) {
                document.getElementById(s).style.display = "block";
            }
            function getRandomNombre(){
                let fname = [ 'Agapetus', 'Aimon', 'Beltran', 'Berto', 'Bronco', 'Cipriano', 'Cisco', 'Cortez', 'Cruz', 'Cuba', 'Dario', 'Desiderio', 'Diego', 'Dimos', 'Fanuco', 'Federico', 'Fraco','Francisco', 'Frisco', 'Gervasio', 'Gig', 'Gonzalo', 'Guido', 'Guillermo', 'Hernan', 'Hilario', 'Ignado', 'Isidro', 'Jaguar', 'Jair', 'Javier', 'Jerrold', 'Juan', 'Kiki','Larenzo', 'Lisandro', 'Loredo', 'Lorenzo', 'Macario', 'Malvolio', 'Manuel', 'Marjun', 'Montana', 'Montego', 'Montel', 'Montenegro', 'Nasario', 'Nemesio', 'Neper','Neron', 'Adalia', 'Aidia', 'Alva', 'Aureliano', 'Belinda', 'Bettina', 'Carey', 'Carlotta', 'Coco', 'Damita', 'Delfina', 'Duenna', 'Dulcie', 'Elvira', 'Enriqua', 'Esmerelda', 'Esperanza', 'Fe', 'Fonda', 'Fridam', 'Friera', 'Gitana', 'Gotzone', 'Guadalupe', 'Hermosa', 'Ines', 'Isabel', 'Itzel', 'Jade', 'Jardena', 'Julitta', 'Kesare', 'Kiki', 'Lacienegam', 'Ladonna', 'Landrada', 'Lela','Lenora', 'Leya', 'Liani', 'Linda', 'Lluvia', 'Lola', 'Lolita', 'Luisa', 'Lujuana', 'Lupita', 'Lux', 'Luz', 'Madeira', 'Pagination'];
                let lname = ['Dawnmight', 'Casktalon', 'Phoenixbleeder', 'Springwing', 'Crystalweaver', 'Whitmantle', 'Nosehand', 'Brightbluff', 'Wildkeep', 'Saursky', 'Terrawhisk', 'Soliddoom', 'Rosehorn', 'Highfall', 'Emberwind', 'Wyvernmark', 'Blackspell', 'Chestdoom', 'Windflame', 'Crestfang', 'Sugnes', 'Roffilles', 'Vassetillon', 'Polannes', 'Ronchechanteau', 'Béchadras', 'Albillon', 'Estielon', 'Bonnemeur', 'Machegner', 'Chamirel', 'Béchallane', 'Beleveron', 'Ligninton', 'Caffazin', 'Croileilles', 'Choinie', 'Abaffet', 'Polathier', 'Ronchezac'];
                return  (fname[Math.floor(Math.random() * fname.length)]+" "+lname[Math.floor(Math.random() * lname.length)]);
            }
            function off( s ) {
                document.getElementById(s).style.display = "none";
            }
            function onClickAway(e) {
                e = e || window.event;
                var target = e.target || e.srcElement;
                if(target.id == "overlay"){
                    document.getElementById('menu').style.display = "block";
                    document.getElementById('crear_grupo').style.display = "none";
                    document.getElementById("overlay").style.display = "none";
                }
            }
            function onClickAwayDice(e) {
                e = e || window.event;
                var target = e.target || e.srcElement;
                if(target.id == "diceCalculator"){
                    document.getElementById("diceCalculator").style.display = "none";
                }
            }
            function onClickAwayEditPerfil(e) {
                e = e || window.event;
                var target = e.target || e.srcElement;
                if(target.id == "editPerfil"){
                    document.getElementById("editPerfil").style.display = "none";
                }
            }
            function send(params){
                post('/',params);
            }
            function leeChat(id){
                send({'id':id, 'post_method':'leer_grupo'})
            }
        </script>
        <script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
        <script  type="text/javascript">
        
            function readURLPerfil(input) {
                if (input.files && input.files[0]) {
                    var reader = new FileReader();
                    reader.onload = function (e) {
                        $('#foto-perfil-src').attr('src', e.target.result);
                        $('#foto-perfil-edit').attr('value', e.target.result);
                    }
                    reader.readAsDataURL(input.files[0]);
                }
            }

            function editProfile(id) {
                if(document.getElementById("foto-perfil-edit").files[0]){
                    var reader = new FileReader();
                    reader.onload = function (e) {
                        let data = {
                            idChat:id,
                            photo : e.target.result,
                            color : document.getElementById("foto-perfil-edit-color").value,
                            nickname : document.getElementById("foto-perfil-edit-nickname").value
                        }
                        console.log(data);
                        axios.post('/editProfile',data)
                                    .then(function (response) {
                                        console.log(response.data);
                                    });
                    }
                    reader.readAsDataURL(document.getElementById("foto-perfil-edit").files[0]);
                }else{
                     let data = {
                            idChat:id,
                            photo : '',
                            color : document.getElementById("foto-perfil-edit-color").value,
                            nickname : document.getElementById("foto-perfil-edit-nickname").value
                        }
                        console.log(data);
                        axios.post('/editProfile',data)
                                    .then(function (response) {
                                        console.log(response.data);
                                    });
                }
            }

            function readURL(input) {
                if (input.files && input.files[0]) {
                    var reader = new FileReader();
                    reader.onload = function (e) {
                        $('#blah').attr('src', e.target.result);
                        $('#foto_grupo_str').attr('value', e.target.result);
                    }
                    reader.readAsDataURL(input.files[0]);
                }
            } 
            function sendImage(id, input) {
                console.log(id,input)
                if (input.files && input.files[0]) {
                    var reader = new FileReader();
                    reader.onload = function (e) {
                        axios.post('/sendImage',{idChat:id, data:reader.result})
                            .then(function (response) {
                                console.log(response.data);
                            });
                    }
                    reader.readAsDataURL(input.files[0]);
                }
            }
            function createToken(id, input) {
                console.log(id,input)
                if (input.files && input.files[0]) {
                    var reader = new FileReader();
                    reader.onload = function (e) {
                        axios.post('/createToken',{idChat:id, data:reader.result})
                            .then(function (response) {
                                console.log(response.data);
                            });
                    }
                    reader.readAsDataURL(input.files[0]);
                }
            }
            function onTextChange() {
                var key = window.event.keyCode;
                if (key === 13 && !window.event.shiftKey) {
                    document.getElementById("sendAMessage").submit();
                }
            }
        </script>
        <script type="text/javascript">
            var charging = false;
            setInterval(function(){
                if( document.getElementById("idChatActual") ){
                let idChat = document.getElementById("idChatActual").value;
                let maxId = document.getElementById("idChatActualMaxId").value;
                if(!charging){
                    axios.post('/updater',{idChat, maxId})
                        .then(function (response) {
                            let res = response.data
                            console.log(res);
                            res['mongoDoc']['users'].forEach(user=>{
                                let divsUser = document.getElementsByName('mes_from_'+String(user))
                                let nicknameUser = document.getElementsByName('mes_from_'+String(user)+'_nickname')
                                let photoUser = document.getElementsByName('mes_from_'+String(user)+'_photo')
                                let profilePhoto = document.getElementById("photo_"+String(user)+"_textarea")
                                console.log(profilePhoto)
                                if(profilePhoto){
                                    profilePhoto.src = res['mongoDoc'][String(user)]['photo']
                                }
                                divsUser.forEach((element,index)=>{
                                    divsUser[index].style.border = "3px solid "+ res['mongoDoc'][String(user)]['color']
                                    nicknameUser[index].innerHTML = res['mongoDoc'][String(user)]['nickname']
                                    nicknameUser[index].style.color = res['mongoDoc'][String(user)]['color']
                                    photoUser[index].src = res['mongoDoc'][String(user)]['photo']
                                })
                            });
                            if(res['newData']){
                                charging=true;
                                console.log("Actualizando datos de lectura")
                                res['messages'].forEach((elem,index)=>{
                                    console.log(elem,index)
                                    let newMes =  document.createElement("div");
                                    newMes.style.padding= "2px";
                                    newMes.style.display= "grid";
                                    if(elem['mine']){
                                        newMes.style.gridTemplateColumns = "calc(10%) calc(90%)";
                                        let innerNewMessage =  document.createElement("div");
                                        innerNewMessage.name = 'mes_from_'+String(elem['fromId']);
                                        innerNewMessage.className = 'w3-round';
                                        innerNewMessage.style.backgroundColor= 'white';
                                        innerNewMessage.style.border= '3px solid '+res['mongoDoc'][String(elem['fromId'])]['color'];
                                        innerNewMessage.style.gridColumn= ' 2 / 3 ';
                                        
                                        let inner2NewMessage =  document.createElement("div");
                                        inner2NewMessage.className = 'grid-item-chat-2 grid-container-message';
                                        

                                        let innerNewMessageNicK =  document.createElement("div");
                                        innerNewMessageNicK.className = 'grid-item-3';
                                        innerNewMessageNicK.style.margin = '0px';
                                        
                                        //Generamos el nickname
                                        
                                        let nickname =  document.createElement("p");
                                        nickname.name = 'mes_from_'+String(elem['fromId'])+'_nickname';
                                        nickname.innerHTML = res['mongoDoc'][String(elem['fromId'])]['nickname']
                                        nickname.style.paddingTop = '5px';
                                        nickname.style.fontSize = '18px';
                                        nickname.style.color = res['mongoDoc'][String(elem['fromId'])]['color'];
                                        nickname.style.textAlign = 'right';
                                        nickname.style.fontWeight = 'bold';
                                        innerNewMessageNicK.appendChild(nickname)
                                        
                                        //Generamos el message

                                        if(elem['type']=='image'){
                                            console.log('generando imagen');
                                            let image = document.createElement("img");
                                            image.style.width='80%';
                                            image.style.height='auto';
                                            image.alt = "Red dot";
                                            image.src = elem['src'];
                                            innerNewMessageNicK.appendChild(image)
                                        }else if(elem['type']=='audio'){
                                            console.log('generando audio');
                                            let au = document.createElement("audio");
                                            au.controls = "controls";
                                            au.autobuffer = "autobuffer";
                                            let sr = document.createElement("source");
                                            sr.src = elem['src'];
                                            au.appendChild(sr);
                                            innerNewMessageNicK.appendChild(au)
                                        }else if(elem['type']=='video'){
                                            console.log('generando video');
                                            let vid = document.createElement("video");
                                            vid.controls = "controls";
                                            vid.style.width='80%';
                                            vid.style.height='auto';
                                            let sr = document.createElement("source");
                                            sr.src = elem['src'];
                                            sr.type = elem['videoType']
                                            vid.appendChild(sr);
                                            innerNewMessageNicK.appendChild(vid)
                                        }else{
                                            console.log('generando texto');
                                            let txt = document.createElement("p");
                                            txt.style.padding = "5px";
                                            txt.style.fontSize= "14px";
                                            txt.style.textAlign = elem['align'];
                                            txt.style.overflowWrap = "break-word";
                                            txt.innerHTML = elem['message'];
                                            innerNewMessageNicK.appendChild(txt)
                                        }
                                        inner2NewMessage.appendChild(innerNewMessageNicK);
                                        
                                        let divProfilePhoto =  document.createElement("div");
                                        divProfilePhoto.className = 'grid-item-3';
                                        divProfilePhoto.style.padding = '5px';
                                        let profileImg =  document.createElement("img");
                                        profileImg.style.height = '45px';
                                        profileImg.style.width = '45px';
                                        profileImg.name = "mes_from_"+String(elem['fromId']) +"_photo";
                                        profileImg.src = res['mongoDoc'][String(elem['fromId'])]['photo'];
                                        divProfilePhoto.appendChild(profileImg);
                                        inner2NewMessage.appendChild(divProfilePhoto);
                                        innerNewMessage.appendChild(inner2NewMessage);
                                        newMes.appendChild(innerNewMessage);
                                    }else{
                                        newMes.style.gridTemplateColumns = "calc(90%) calc(10%)";
                                        let innerNewMessage =  document.createElement("div");
                                        innerNewMessage.name = 'mes_from_'+String(elem['fromId']);
                                        innerNewMessage.className = 'w3-round';
                                        innerNewMessage.style.backgroundColor= 'white';
                                        innerNewMessage.style.border= '3px solid '+res['mongoDoc'][String(elem['fromId'])]['color'];
                                        innerNewMessage.style.gridColumn= ' 1 / 2 ';
                                        
                                        let inner2NewMessage =  document.createElement("div");
                                        inner2NewMessage.className = 'grid-item-chat grid-container-message-2';
                                        
                                        let divProfilePhoto =  document.createElement("div");
                                        divProfilePhoto.className = 'grid-item-3';
                                        divProfilePhoto.style.padding = '5px';
                                        let profileImg =  document.createElement("img");
                                        profileImg.style.height = '45px';
                                        profileImg.style.width = '45px';
                                        profileImg.name = "mes_from_"+String(elem['fromId']) +"_photo";
                                        profileImg.src = res['mongoDoc'][String(elem['fromId'])]['photo'];
                                        divProfilePhoto.appendChild(profileImg);
                                        inner2NewMessage.appendChild(divProfilePhoto);

                                        let innerNewMessageNicK =  document.createElement("div");
                                        innerNewMessageNicK.className = 'grid-item-3';
                                        innerNewMessageNicK.style.margin = '0px';
                                        
                                        //Generamos el nickname
                                        
                                        let nickname =  document.createElement("p");
                                        nickname.name = 'mes_from_'+String(elem['fromId'])+'_nickname';
                                        nickname.innerHTML = res['mongoDoc'][String(elem['fromId'])]['nickname']
                                        nickname.style.paddingTop = '5px';
                                        nickname.style.fontSize = '18px';
                                        nickname.style.color = res['mongoDoc'][String(elem['fromId'])]['color'];
                                        nickname.style.textAlign = 'left';
                                        nickname.style.fontWeight = 'bold';
                                        innerNewMessageNicK.appendChild(nickname)
                                        
                                        //Generamos el message

                                        if(elem['type']=='image'){
                                            console.log('generando imagen');
                                            let image = document.createElement("img");
                                            image.style.width='80%';
                                            image.style.height='auto';
                                            image.alt = "Red dot";
                                            image.src = elem['src'];
                                            innerNewMessageNicK.appendChild(image)
                                        }else if(elem['type']=='audio'){
                                            console.log('generando audio');
                                            let au = document.createElement("audio");
                                            au.controls = "controls";
                                            au.autobuffer = "autobuffer";
                                            let sr = document.createElement("source");
                                            sr.src = elem['src'];
                                            au.appendChild(sr);
                                            innerNewMessageNicK.appendChild(au)
                                        }else if(elem['type']=='video'){
                                            console.log('generando video');
                                            let vid = document.createElement("video");
                                            vid.controls = "controls";
                                            vid.style.width='80%';
                                            vid.style.height='auto';
                                            let sr = document.createElement("source");
                                            sr.src = elem['src'];
                                            sr.type = elem['videoType']
                                            vid.appendChild(sr);
                                            innerNewMessageNicK.appendChild(vid)
                                        }else{
                                            console.log('generando texto');
                                            let txt = document.createElement("p");
                                            txt.style.padding = "5px";
                                            txt.style.fontSize= "14px";
                                            txt.style.textAlign = elem['align'];
                                            txt.style.overflowWrap = "break-word";
                                            txt.innerHTML = elem['message'];
                                            innerNewMessageNicK.appendChild(txt)
                                        }
                                        inner2NewMessage.appendChild(innerNewMessageNicK);
                                        
                                        
                                        innerNewMessage.appendChild(inner2NewMessage);
                                        newMes.appendChild(innerNewMessage);
                                    }
                                    let chats = document.getElementById('messages_chat_group_limit')
                                    chats.insertBefore(newMes, chats.firstChild);
                                })
                                charging=false;
                            }
                            document.getElementById("idChatActual").value = String(res['idChat']);
                            document.getElementById("idChatActualMaxId").value = String(res['maxId']);
                        });

                }
            }
            }, 4000);
        </script>
        <script type="text/javascript">
            let recorder = null;
            let isRecording = false;
            let streamAudio = null;
            function recorderController(id){
                console.log('Recorder val',recorder)
                if(!isRecording){
                    document.getElementById('recorderImg').src = '/static/microStop.png'
                    startRecording();
                    isRecording = true
                }else{
                    document.getElementById('recorderImg').src = '/static/micro.png'
                    stopRecording(id)
                    isRecording = false
                }
            }
            function startRecording(){
                 navigator.mediaDevices.getUserMedia({ audio: true }).then(stream=> {
                    streamAudio = stream
                    recorder = new MediaRecorder(streamAudio, {
                        type: 'audio/ogg; codecs=opus'
                    });
                    recorder.start();
                });
            }
            function stopRecording(id){
                recorder.stop();
                recorder.ondataavailable = (e) => {
                    let reader = new FileReader()
                    reader.onloadend = () => {
                        axios.post('/sendAudio',{idChat:id,data:reader.result})
                        .then(function (response) {
                            // handle success
                            console.log(response.data);
                        });
                    }
                    reader.readAsDataURL(e.data);
                }
                recorder = null;
                streamAudio.getTracks().forEach(track => track.stop());
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
                        <form action='/' method=POST  class="grid-item-3 max-height2" id="crear_grupo" style="display:none; grid-column : 2 / 4">
                            <input name='post_method' value='crear_grupo' style='display:none;'/>
                            <input id='foto_grupo_str' name='foto_grupo_str' value='' style='display:none;'/>
                            <div class="vcentrable" style="height:40%">
                                <div class="vcentered">
                                    <div style="background-color:white;margin:5px;" >
                                        <div class="grid-container-half vcentrable">
                                            <span class="grid-item vcentered">
                                                <img class='button' onclick='myFunction("backToMenu")' style='width:20px;height:20px;float:left' src='/static/leftArrow.png'>
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
                                                    <p style="font-size:16px;">Foto del grupo</p>
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
                            <div class="vcentrable" id="new_usuarios" style="height:50%; overflow-y: scroll;">
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
                                <div class='grid-container-3' style='width:100%;background-color:white;border:1px solid black;height:12%'>
                                    <div class='grid-item-3 vcentrable'>
                                        <p class='vcentered'>Usted</p>
                                    </div>
                                    <div class='grid-container-25-75 grid-item-3'>
                                        <input class='grid-item' name='mi_color' id='mi_color' type='color'/>
                                        <input style='font-size: 14px;text-align: center;'  class='grid-item-3' type='text' name='mi_nickname' id='mi_nickname' value=''></input> 
                                    </div>
                                    <div class='grid-item-3 vcentrable'>
                                        <p class='vcentered'></p>
                                    </div>
                                </div>
                            </div>
                            <div class="vcentrable"  style="height:10%;">
                                <input type='submit'/>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
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
            {messages}
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

@app.route('/updater', methods=['POST'])
async def updater():
    data = await request.json
    ip = request.remote_addr
    ip = ip.replace('.', '_')
    global arrayClients
    me = await arrayClients[ip].get_me()
    idChat = int(data['idChat'])
    minId = int(data['maxId'])
    messages = []
    res ={'maxId':data['maxId']}
    i = -1
    newData=False
    result = await arrayClients[ip].get_messages(idChat, min_id=minId, reverse=False)
    for mes2 in result:
        newData = True
        messages.append({})
        i = i+1
        mes = mes2.to_dict()
        if mes['id']>int(data['maxId']):
            res['maxId'] = str(mes['id'])
        if mes['_'] == "Message":
            messages[i] = {
                'message':mes['message'].replace('\n','<br/>'),
                'align':'right' if mes['from_id'] == me.id else 'left',
                'type':'text',
                'mine':  mes['from_id'] == me.id,
                'fromId':mes['from_id']
                }
            global modoSoloTexto
            if mes['media'] is not None and not modoSoloTexto:
                if mes['media']['_'] == 'MessageMediaPhoto':
                    path = 'static/imgToFrontend/'+ str(mes['media']['photo']['id'])  +'.png'
                    if not os.path.exists(path):
                       img = await arrayClients[ip].download_media(mes2, file=path)
                       messages[i]={
                           'type':'image',
                           'src': img,
                           'mine':  mes['from_id'] == me.id,
                           'fromId':mes['from_id']
                           }
                    else:
                        messages[i]={
                           'type':'image',
                           'src': path,
                           'mine':  mes['from_id'] == me.id,
                            'fromId':mes['from_id']
                           }
                else:
                    t = mes['media']['document']['mime_type']
                    if 'audio' in t:
                        path = 'static/audToFrontend/'+ str(mes['media']['document']['id'])  +'.'+t.split('/')[1]
                        if not os.path.exists(path):
                            audio = await arrayClients[ip].download_media(mes2, file=path)
                            messages[i]={
                            'type':'audio',
                            'src': audio,
                            'mine':  mes['from_id'] == me.id,
                            'fromId':mes['from_id']
                            }
                        else:
                            messages[i]={
                            'type':'audio',
                            'src': path,
                            'mine':  mes['from_id'] == me.id,
                            'fromId':mes['from_id']
                            }
                    if 'video' in t:
                        path = 'static/vidsToFrontend/'+ str(mes['media']['document']['id'])  +'.'+t.split('/')[1]
                        if not os.path.exists(path):
                            video = await arrayClients[ip].download_media(mes2, file=path )
                            messages[i]={
                            'type':'video',
                            'videoType':'video/'+ t.split('/')[1],
                            'src': video,
                            'mine':  mes['from_id'] == me.id,
                            'fromId':mes['from_id']
                            }
                        else:
                            messages[i]={
                            'type':'video',
                            'videoType':'video/'+ t.split('/')[1],
                            'src': path,
                            'mine':  mes['from_id'] == me.id,
                            'fromId':mes['from_id']
                            }
    res['messages'] = messages
    res['idChat'] = idChat
    res['myId'] = str(me.id)
    m = get_mongoDoc()
    mongo = m.find_one({'idChat':str(idChat)})
    mongo.pop('_id',None)
    res['mongoDoc'] = mongo
    res['newData'] = newData
    res['notificationsChat']=[]
    for dialog in await arrayClients[ip].get_dialogs():
        chatMongo = m.find_one({"idChat": str(dialog.entity.id)})
        if chatMongo is not None:
            dia ='inline-block' if dialog.unread_count>0 else 'none'
            res['notificationsChat'].append({
                'id':"notificaciones_"+str(dialog.entity.id),
                'not': str(dialog.unread_count),
                'display':dia
                })
    return jsonify(res)

@app.route('/sendDiceMessage', methods=['POST'])
async def sendDiceMessage():
    data = await request.json
    ip = request.remote_addr
    ip = ip.replace('.', '_')
    global arrayClients
    sum, memory = diceThrow(data['data'])
    await arrayClients[ip].send_message(int(data['idChat']), 'Sumatorio: '+str(sum)+'\nMemoria: ('+printMem(memory)+')', parse_mode='html')
    return {'beta':'de mis tetas'}

@app.route('/createToken', methods=['POST'])
async def createTokenNormal():
    data = await request.json 
    ip = request.remote_addr
    ip = ip.replace('.', '_')
    global arrayClients
    idChat = int(data['idChat'])
    tipo= data['data'].split('base64,')[0].split('data:')[1].split(';')[0]
    fileData= data['data'].split('base64,')[1]
    data = base64.b64decode(fileData)
    me = await arrayClients[ip].get_me()
    mongo = get_mongoDoc()
    chatMongo = mongo.find_one({"idChat": str(idChat)})
    if me.id == chatMongo['master']:
        print("Im the master, bitch")
        Path("static/groups/"+str(idChat)+"/master").mkdir(parents=True, exist_ok=True)
        p = 'static/groups/'+str(idChat)+"/master/imgTokenPersonal."+tipo.split('/')[1]
        tempFile = open(p,'wb')
        tempFile.write(data)
        tempFile.close()
        h = chatMongo[str(me.id)]['color'].lstrip('#')
        c = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        token = createToken(1000, c, 0.9, (255,255,255,255),0.8, p)
        token.save('static/groups/'+str(idChat)+"/master/tokenPersonal."+tipo.split('/')[1])
    else:
        Path("static/groups/"+str(idChat)+"/"+str(me.id)).mkdir(parents=True, exist_ok=True)
        p = 'static/groups/'+str(idChat)+"/master/token."+tipo.split('/')[1]
        tempFile = open(p,'wb')
        tempFile.write(data)
        tempFile.close()
        h = chatMongo[str(me.id)]['color']
        c = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        token = createToken(600, c, 0.8, (255,255,255,255),0.9, p)
    return {'beta':'de mis tetas'}

@app.route('/editProfile', methods=['POST'])
async def editProfile():
    data = await request.json 
    ip = request.remote_addr
    ip = ip.replace('.', '_')
    global arrayClients
    idChat = int(data['idChat'])
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y-%H-%M-%S-%f")
    if data['photo'] is not '':
        tipo= data['photo'].split('base64,')[0].split('data:')[1].split(';')[0]
        fileData= data['photo'].split('base64,')[1]
        data = base64.b64decode(fileData)
        me = await arrayClients[ip].get_me()
        me = me.id
        path = 'static/groups/'+str(idChat)+"/"+str(me)+timestampStr+"."+tipo.split('/')[1]
        tempFile = open(path,'wb')
        tempFile.write(data)
        tempFile.close()
        info= await request.json
        mongoChat = get_mongoDoc()
        chatMongo = mongoChat.find_one({"idChat": str(info['idChat'])})
        chatMongo[str(me)]={'photo':path, 'nickname':info['nickname'], 'color':info['color']}
        mongoChat.replace_one({"idChat": str(idChat)}, chatMongo)
    else:
        info= await request.json
        mongoChat = get_mongoDoc()
        me = await arrayClients[ip].get_me()
        me = me.id
        chatMongo = mongoChat.find_one({"idChat": str(info['idChat'])})
        chatMongo[str(me)]={'photo':chatMongo[str(me)]['photo'], 'nickname':info['nickname'], 'color':info['color']}
        mongoChat.replace_one({"idChat": str(idChat)}, chatMongo)
    return {'beta':'de mis tetas'}
    
@app.route('/sendImage', methods=['POST'])
async def sendImage():
    data = await request.json 
    ip = request.remote_addr
    ip = ip.replace('.', '_')
    global arrayClients
    idChat = int(data['idChat'])
    tipo= data['data'].split('base64,')[0].split('data:')[1].split(';')[0]
    fileData= data['data'].split('base64,')[1]
    data = base64.b64decode(fileData)
    print(tipo.split('/')[0])
    if tipo.split('/')[0] == 'video':
        tempFile = open('auxVideos/'+str(idChat)+"."+tipo.split('/')[1],'wb')
        tempFile.write(data)
        tempFile.close()
        await arrayClients[ip].send_file(idChat, 'auxVideos/'+str(idChat)+"."+tipo.split('/')[1])
    elif tipo.split('/')[0] == 'image':
        tempFile = open('auxImages/'+str(idChat)+"."+tipo.split('/')[1],'wb')
        tempFile.write(data)
        tempFile.close()
        await arrayClients[ip].send_file(idChat, 'auxImages/'+str(idChat)+"."+tipo.split('/')[1])
    return {'beta':'de mis tetas'}

@app.route('/sendAudio', methods=['POST'])
async def sendAudio():
    data = await request.json 
    ip = request.remote_addr
    ip = ip.replace('.', '_')
    global arrayClients
    idChat = int(data['idChat'])
    data = data['data'].split('audio/webm;codecs=opus;base64,')[1]
    data += "=" * ((4 - len(data) % 4) % 4)
    audio = base64.b64decode(data)
    tempFile = open('auxAudios/'+str(idChat)+".ogg",'wb')
    tempFile.write(audio)
    tempFile.close()
    await arrayClients[ip].send_file(idChat, 'auxAudios/'+str(idChat)+".ogg", voice_note=True)
    return {'beta':'de mis tetas'}



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
    if ip not in arrayClients:
        arrayClients[ip] = TelegramClient(ip, API_ID, API_HASH)
        arrayClients[ip+'telf'] = None
    if not arrayClients[ip].is_connected():
        await arrayClients[ip].connect()
    form = await request.form
    if request.method == 'GET':
        for callback in arrayClients[ip].list_event_handlers():
            name = str(str(callback[0]).split(' at 0x')[0]).split('function ')[1]
    if 'phone' in form:
        arrayClients[ip+'telf'] = form['phone']
        await arrayClients[ip].send_code_request(arrayClients[ip+'telf'])
    if 'code' in form:
        await arrayClients[ip].sign_in(code=form['code'])
    if await arrayClients[ip].is_user_authorized():
        me = await arrayClients[ip].get_me()
        ch = ''
        mongo = get_mongoDoc()
        amigos = ''''''
        messages= '''
                <div style="background-color:white;width:100%;height:100%;">
                    <div class="chat_header">
                    </div>
                </div>
                '''
        if 'post_method' in form:
            reload =  False
            if form['post_method'] == 'enviar_mensaje':
                if form['TextToSend'] is not '':
                    print(form['TextToSend'])
                    await arrayClients[ip].send_message(int(form['id']), form['TextToSend'])
                reload = True
            if form['post_method'] == 'leer_grupo' or reload:
                result = await arrayClients[ip].get_messages(int(form['id']),limit=40,reverse=False)
                chat = await arrayClients[ip].get_entity(int(form['id']))
                chatMongo = mongo.find_one({"idChat": form['id']})
                messages= '''<div style="background-color:white;padding:8px; width:100%;height:100%;">
                        <div class="chat_header">
                            <img src={photo} alt="error" style="height:60px;width:60px;padding-top: 5px;padding-bottom: 5px;">
                            <div >
                                <input type='button' class='w3-btn w3-white' style="font-size:20px;" value={name}>
                            </div>
                        </div>
                        <div id='messages_chat_group_limit' style="height:78%;overflow-y: scroll;display: flex;flex-direction: column-reverse; border-bottom:2px solid black;">
                        '''.format(
                            photo= chatMongo['fotoGrupo'],
                            name=chat.title
                        )
                maxid = 0
                for mes2 in result:
                    mes = mes2.to_dict()
                    await arrayClients[ip].send_read_acknowledge(int(form['id']), message=mes2)
                    m=''
                    if mes['id']>maxid:
                        maxid = mes['id']
                    if mes['_'] == "Message":
                        message = ''' <p style="padding:5px;font-size:14px;text-align: {align}; overflow-wrap: break-word;">{message}</p>'''.format(
                            message=mes['message'].replace('\n','<br/>'),
                            align='right' if mes['from_id'] == me.id else 'left')
                        global modoSoloTexto
                        if mes['media'] is not None and not modoSoloTexto:
                            if mes['media']['_'] == 'MessageMediaPhoto':
                                path = 'static/imgToFrontend/'+ str(mes['media']['photo']['id'])  +'.png'
                                if not os.path.exists(path):
                                    img = await arrayClients[ip].download_media(mes2, file=path)
                                    message = '''<img style="width:80%;height:auto;" src={src} alt="Red dot" />'''.format(src = img)
                                else:
                                    message = '''<img style="width:80%;height:auto;" src={src} alt="Red dot" />'''.format(src = path)
                            else:
                                t = mes['media']['document']['mime_type']
                                if 'audio' in t:
                                    path = 'static/audToFrontend/'+ str(mes['media']['document']['id'])  +'.'+t.split('/')[1]
                                    if not os.path.exists(path):
                                        audio = await arrayClients[ip].download_media(mes2, file=path)
                                        message = '''<audio controls="controls" autobuffer="autobuffer">
                                            <source src={src} />
                                        </audio>
                                        '''.format(src = audio )
                                    else:
                                        message = '''<audio controls="controls" autobuffer="autobuffer">
                                            <source src={src} />
                                        </audio>
                                        '''.format(src = path )
                                if 'video' in t:
                                    path = 'static/vidsToFrontend/'+ str(mes['media']['document']['id'])  +'.'+t.split('/')[1]
                                    if not os.path.exists(path):
                                        video = await arrayClients[ip].download_media(mes2, file=path )
                                        message = '''<video  controls style="width:80%;height:auto;">
                                            <source src={src} type={type} />
                                        </video>
                                        '''.format(src = video, type= 'video/'+ t.split('/')[1])
                                    else:
                                        message = '''<video  controls style="width:80%;height:auto;">
                                            <source src={src} type={type} />
                                        </video>
                                        '''.format(src = path, type= 'video/'+ t.split('/')[1])
                        if mes['from_id'] == me.id :
                            m='''<div style="padding:2px;display:grid;grid-template-columns: calc(10%) calc(90%);" >
                                <div name='mes_from_{fromID}' class="w3-round" style="background-color:white; border: 3px solid {color}; grid-column: 2 / 3;" >
                                    <div class="grid-item-chat-2 grid-container-message">
                                        <div class="grid-item-3 " style="margin:0px;">
                                            <p name='mes_from_{fromID}_nickname' style="padding-top:5px;font-size:18px;color:{color};text-align: right;font-weight:bold;">{nickname}</p>
                                           {message}
                                        </div>
                                        <div class="grid-item-3" style="padding:5px;">
                                            <img name='mes_from_{fromID}_photo' src={photo} style="height:45px;width:45px;" >
                                        </div>
                                    </div>
                                </div>
                            </div>'''.format(
                                photo = chatMongo [str(mes['from_id'])]['photo'],
                                nickname =  chatMongo [str(mes['from_id'])]['nickname'],
                                color =  chatMongo [str(mes['from_id'])]['color'],
                                message = message,
                                fromID = mes['from_id']
                            )
                        else:
                            m='''<div style="padding:2px;display:grid;grid-template-columns: calc(90%) calc(10%);" >
                                <div name='mes_from_{fromID}' class="w3-round" style="background-color:white; border: 3px solid {color}; grid-column: 1 / 2;" >
                                    <div class="grid-item-chat grid-container-message-2">
                                        <div class="grid-item-3" style="padding:5px;">
                                            <img name='mes_from_{fromID}_photo' src={photo} style="height:45px;width:45px;" >
                                        </div>
                                        <div class="grid-item-3 " style="margin:0px;">
                                            <p name='mes_from_{fromID}_nickname' style="padding-top:5px;font-size:18px;color:{color};text-align: left;font-weight:bold;">{nickname}</p>
                                           {message}
                                        </div>
                                    </div>
                                </div>
                            </div>'''.format(
                                photo = chatMongo [str(mes['from_id'])]['photo'],
                                nickname =  chatMongo [str(mes['from_id'])]['nickname'],
                                color =  chatMongo [str(mes['from_id'])]['color'],
                                message = message,
                                fromID = mes['from_id']
                            )
                    messages = messages+m
                messages= messages+'''</div>
                <div style='text-align:left;'>
                    <div id='diceCalculator' onclick='onClickAwayDice(event)'>
                        <div class="w3-card centered-white" style="text-align:center;">
                            <div style="font-size:24px;margin:20px;">
                                <select id="plusminusd4" value="+" >
                                    <option>+</option>
                                    <option>-</option>
                                </select>
                                <input type="number" min="0" oninput="validity.valid||(value='0');" max="99"  name="d4" id="d4" maxlength="2"  value="0"/>
                                <label for="d4">&nbsp;&nbsp;&nbsp;&nbsp;d4</label>
                                <br/>
                                <select id="plusminusd6" value="+" >
                                    <option>+</option>
                                    <option>-</option>
                                </select>
                                <input type="number" min="0" oninput="validity.valid||(value='0');" max="99"  name="d6" id="d6" maxlength="2"  value="0"/>
                                <label for="d6">&nbsp;&nbsp;&nbsp;&nbsp;d6</label>
                                <br/>
                                <select id="plusminusd8" value="+" >
                                    <option>+</option>
                                    <option>-</option>
                                </select>
                                <input type="number" min="0" oninput="validity.valid||(value='0');" max="99"  name="d8" id="d8" maxlength="2"  value="0"/>
                                <label for="d8">&nbsp;&nbsp;&nbsp;&nbsp;d8</label>
                                <br/>
                                <select id="plusminusd10" value="+" >
                                    <option>+</option>
                                    <option>-</option>
                                </select>
                                <input type="number" min="0" oninput="validity.valid||(value='0');" max="99"  name="d10" id="d10" maxlength="2"  value="0"/>
                                <label for="d10">&nbsp;&nbsp;d10</label>
                                <br/>
                                <select id="plusminusd12" value="+" >
                                    <option>+</option>
                                    <option>-</option>
                                </select>
                                <input type="number" min="0" oninput="validity.valid||(value='0');" max="99"  name="d12" id="d12" maxlength="2"  value="0"/>
                                <label for="d12">&nbsp;&nbsp;d12</label>
                                <br/>
                                <select id="plusminusd20" value="+" >
                                    <option>+</option>
                                    <option>-</option>
                                </select>
                                <input type="number" min="0" oninput="validity.valid||(value='0');" max="99"  name="d20" id="d20" maxlength="2"  value="0"/>
                                <label for="d20">&nbsp;&nbsp;d20</label>
                                <br/>
                                <select id="plusminusd100" value="+" >
                                    <option>+</option>
                                    <option>-</option>
                                </select>
                                <input type="number" min="0" oninput="validity.valid||(value='0');" max="99"  name="d100" id="d100" maxlength="2"  value="0"/>
                                <label for="d100">d100</label>
                                <br/>
                                <div style="margin-top:15px;">
                                    <select id="plusminuscustom" value="+" >
                                        <option>+</option>
                                        <option>-</option>
                                    </select>
                                    <input type="number" min="0" oninput="validity.valid||(value='0');" max="99"  name="dCustom" id="dCustom" maxlength="2"  value="0"/>
                                    <label for="dCustom">
                                        d<input type="number" min="0" oninput="validity.valid||(value='0');" max="999"  name="dCustomSize" id="dCustomSize" maxlength="3"  value="0"/>
                                    </label>
                                    <br/>
                                    <label for="mod">Mod</label>
                                    <input type="number" min="-999"  max="999"  name="mod" id="mod" maxlength="3"  value="0"/>
                                </div>
                                <button onclick="sendDiceMessage({id})" class="btn w3-btn w3-white" style="vertical-align: middle;">
                                    Enviar
                                </button>
                            </div>
                        </div>
                    </div>
                    <div id='editPerfil' onclick='onClickAwayEditPerfil(event)'>
                        <div class="w3-card centered-white" style="text-align:center;">
                            <div style="font-size:24px;margin:20px;">
                                <div id='foto de perfil'>
                                    <p>Foto de perfil</p>
                                    <label for="foto-perfil-edit">
                                        <img id='foto-perfil-src' class="w3-btn btn w3-white" src={photo} style="width:150px;height:width:150px;">
                                    </label>
                                    <input name="foto-perfil-edit" onchange="readURLPerfil(this)" id="foto-perfil-edit" type="file" style="display:none;"></input>
                                </div>
                                <div>
                                    <p style="margin-top:20px;">Color asignado</p>
                                    <input name="foto-perfil-color" id="foto-perfil-edit-color" type="color" value={color}></input>
                                </div>
                                <div>
                                    <p style="margin-top:20px;">Nickname</p>
                                    <input name="foto-perfil-edit-nickname" id="foto-perfil-edit-nickname" value='{nickname}'></input>
                                </div>
                                <div>
                                    <button onclick="editProfile({id})" class="btn w3-btn w3-white" style="vertical-align: middle;">
                                        Enviar
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <form id="sendAMessage" action="/" method="post">
                        <div class="grid-container-message-input">
                            <div style="grid-column: 1 / 2;text-align:center;vertical-align: middle;">
                                <img id="photo_{meId}_textarea" src={photo} style="height:auto;width:75%;" >
                            </div>
                            <input name='id' id='idChatActual' value={id} style='display:none;'/>
                            <input name='max-id' id='idChatActualMaxId' value={maxId} style='display:none;'/>
                            <input name='post_method' value='enviar_mensaje' style='display:none;'/>
                            <div style="grid-column: 2 / 3;">
                                <textarea autofocus onkeypress="onTextChange();" style='font-size:16px;resize: none;width:100%' name="TextToSend" id="TextToSend" rows="4"></textarea>
                            </div>
                            <div style="grid-column: 3 / 4;">
                                <div style="display: grid;grid-template-columns: 55% 45%;height:100%;">
                                    <div style="text-align: center;vertical-align: middle;">
                                         <button type="submit" class="btn btn-success w3-btn w3-white" style="width:100%;height:80%;vertical-align: middle;">
                                            <img  src="/static/send.png" style="width:100%;height:auto%;">
                                        </button>
                                    </div>
                                    <div style="text-align: center;vertical-align: middle;height:100%;">
                                        <button    type="button" onclick='recorderController({id})' class="btn w3-btn w3-white" style="width:100%;height:40%;vertical-align: middle;">
                                            <img id='recorderImg'  src="/static/micro.png" style="width:100%;height:auto%;">
                                        </button>
                                        <div class="dropup" style=" position: relative;display: inline-block;">
                                            <button   type="button" class="btn w3-btn w3-white" style="width:100%;height:40%;vertical-align: middle;">
                                                <img id='moreImg'  src="/static/More.png" style="width:100%;height:auto%;">
                                            </button>
                                            <div class="dropup-content w3-panel w3-white w3-round" style="margin:0px;" >
                                                <div class="grid-container-submenu-sender">
                                                    <div class="btnSubMenu1">
                                                        <label for="file-upload">
                                                            <img class="w3-btn btn w3-white" src="/static/sendFileToAChat.png" style="width:100%;height:auto%;">
                                                        </label>
                                                        <input name="send_image" id="file-upload" onchange="sendImage({id},this)" type="file" style="display:none;"></input>
                                                    </div>
                                                    <div class="btnSubMenu2">
                                                        <button    type="button" onclick='on("diceCalculator")' class="btn w3-btn w3-white" style="width:100%;height:40%;vertical-align: middle;">
                                                            <img src="/static/diceCalculator.png" style="width:100%;height:auto%;">
                                                        </button>
                                                    </div>
                                                    <div class="btnSubMenu3">
                                                        <label for="file-upload3">
                                                            <img id='moreImg' class="w3-btn btn w3-white" src="/static/CreateSheet.png" style="width:100%;height:auto%;">
                                                        </label>
                                                        <input name="send_image" id="file-upload3" onchange="createToken({id},this)" type="file" style="display:none;"></input>
                                                    </div>
                                                    <div class="btnSubMenu4">
                                                        <button  type="button" onclick='on("editPerfil")' class="btn w3-btn w3-white" style="width:100%;height:40%;vertical-align: middle;">
                                                            <img src="/static/editUser.png" style="width:100%;height:auto%;">
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
                </div>'''.format(
                    id= form['id'],
                    maxId = maxid,
                    photo= chatMongo[str(me.id)]['photo'],
                    color=  chatMongo[str(me.id)]['color'],
                    nickname= chatMongo[str(me.id)]['nickname'],
                    meId = me.id
                )
            elif form['post_method'] == 'crear_grupo':
                f = form.to_dict()
                res = [val for key, val in form.to_dict().items()
                       if 'amigo_n_' in key]
                insertion = {'users': [me.id], 'master':me.id}
                insertion[str(me.id)] = {'color': f['mi_color'], 'nickname': f['mi_nickname']}
                for i in res:
                    insertion[i] = {'color': f['amigo_color_'+i], 'nickname': f['amigo_nickname_'+i]}
                    insertion['users'].append(int(i))
                result = await arrayClients[ip](functions.messages.CreateChatRequest(
                    users=insertion['users'], title=f['nombre_grupo']))
                idChat = str(result.chats[0].id)
                os.mkdir(os.getcwd()+'/static/groups/'+idChat+'/')
                insertion['idChat'] = idChat
                insertion['fotoGrupo'] = ''
                if(f['foto_grupo_str'] != ''):
                    b64_string = form['foto_grupo_str'].split(';base64,')[1]
                    b64_string += "=" * ((4 - len(b64_string) % 4) % 4)
                    imgdata = Image.open(BytesIO(base64.b64decode(b64_string)))
                    filename = 'static/groups/'+idChat+'/fotoGrupo.'+form['foto_grupo'].split('.')[1]
                    imgdata.save(filename, (form['foto_grupo'].split('.')[1]).upper())
                    insertion['fotoGrupo'] = '/'+filename
                insertion[str(me.id)]['photo'] = createDefaultProfilePhoto(f['mi_color'],str(me.id),idChat)
                for i in res:
                    insertion[i]['photo'] = createDefaultProfilePhoto(f['amigo_color_'+i],i,idChat)
                mongo.insert_one(insertion)
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
        for dialog in await arrayClients[ip].get_dialogs():
            chatMongo = mongo.find_one({"idChat": str(dialog.entity.id)})
            if chatMongo is not None:
                dia ='inline-block' if dialog.unread_count>0 else 'none'
                ch = ch + '''
                    <button style="background-color:white;margin:5px;width:95%; height:100px;" onclick="leeChat({id})">
                        <div id="{id}" style="background-color:white;margin:5px;">
                            <div class="grid-item grid-container-icon" style="height:100%">
                                <div class="grid-item-3" style="margin:5px;">
                                    <img src={photo} style="height:100%;width:100%;" >
                                </div>
                                <div class="grid-item-3 " style="margin:0px; grid-column: 2 / 4;">
                                    <div class="grid-container-half vcentrable">
                                        <span class="grid-item vcentered">
                                            <div style="display: grid;grid-template-columns: calc(88%) calc(12%); overflow:hidden;">
                                                <span title="{name}" ><p style="font-size:16px;white-space: nowrap;overflow: hidden;text-overflow: ellipsis;">{name}</p></span>
                                                <p id="notificaciones_{id}" style="font-size:13px;color:white;background-color:lightblue; display: {style};">{notifications}</p>
                                            </div>
                                            <p style="font-size:12px;color:grey;">Nick: {nickname}</p>
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </button>
                '''.format(
                    name=dialog.name,
                    photo=chatMongo['fotoGrupo'],
                    id=str(dialog.entity.id),
                    nickname=chatMongo[str(me.id)]['nickname'],
                    notifications=dialog.unread_count,
                    style= dia
                )
        return await render_template_string(BASE_TEMPLATE, friends=amigos, content=MENU_FORM.format(nickname=me.first_name,  messages=messages, name='@'+me.username, chats=ch))

    # Ask for the phone if we don't know it yet
    if arrayClients[ip+'telf'] is None:
        return await render_template_string(BASE_TEMPLATE, content=PHONE_FORM)

    return await render_template_string(BASE_TEMPLATE, content=CODE_FORM)

def createDefaultProfilePhoto (color, id, chatId):
    im = Image.open('default.png')
    im = im.convert('RGBA')
    c = color.split('#')[1]
    c2 = tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
    data = np.array(im)
    red, green, blue, alpha = data.T
    white_areas = (red == 0) & (blue == 0) & (green == 0)
    data[..., :-1][white_areas.T] = (c2[0], c2[1], c2[2])  # Transpose back needed
    Image.fromarray(data).save("static/groups/"+chatId+"/"+id+".png","PNG")
    return "/static/groups/"+chatId+"/"+id+".png"

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
        config = Config()
        await hypercorn.asyncio.serve(app, hypercorn.Config())

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
