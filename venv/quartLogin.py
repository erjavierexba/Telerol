
import base64
import os

import hypercorn.asyncio
from quart import Quart, render_template_string, request, redirect

from telethon import TelegramClient, utils


def get_env(name, message):
    if name in os.environ:
        return os.environ[name]
    return input(message)


BASE_TEMPLATE = '''
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/axios/0.19.2/axios.min.js" integrity="sha256-T/f7Sju1ZfNNfBh7skWn0idlCBcI3RwdLSS4/I7NQKQ=" crossorigin="anonymous"></script>
        <style>
            body {
                background-color: lightblue;
            }
            h1 {
                color: white;
                text-align: center;
            }
            p {
                font-family: verdana;
                font-size: 20px;
            }
            .grid-container {
                display: grid;
                grid-template-columns: auto auto auto;
                padding: 10px;
            }
            .grid-item {
                padding: 20px;
                font-size: 30px;
                text-align: center;
            }
        </style>
        <meta charset='UTF-8'>
        <title>Telerol</title>
    </head>
    <body>
        {{ content | safe }}
    <script>
        function desconectar() {
            axios.get('/disconnect');
            console.log('ejemplo');
        }
    </script>
    </body>
</html>
'''

PHONE_FORM = '''
<form action='/' method='post'>
    Phone (international format): <input name='phone' class='w3-white' type='text' placeholder='+34600000000'>
    <input type='submit'>
</form>
'''

CODE_FORM = '''
<form action='/' method='post'>
    Telegram code: <input name='code' type='text' placeholder='70707'>
    <input type='submit'>
</form>
'''

# Session name, API ID and hash to use; loaded from environmental variables
SESSION = os.environ.get('TG_SESSION', 'quart')
API_ID = 94575
API_HASH = 'a3406de8d171bb422bb6ddf3bbd800e2'

# Telethon client
client = TelegramClient('quartLogin', API_ID, API_HASH)
client.parse_mode = 'html'  # <- Render things nicely
phone = None

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
    await client.log_out()
    global phone
    phone = None
    return redirect('/')


@app.route('/', methods=['GET', 'POST'])
async def root():
    # We want to update the global phone variable to remember it
    global phone
    if client.is_connected() == False:
        await client.connect()
    # Check form parameters (phone/code)
    form = await request.form
    if 'phone' in form:
        phone = form['phone']
        await client.send_code_request(phone)

    if 'code' in form:
        await client.sign_in(code=form['code'])

    # If we're logged in, show them some messages from their first dialog
    if await client.is_user_authorized():
        # They are logged in, show them some messages from their first dialog
        dialog = (await client.get_dialogs())[0]
        result = '<span class="grid-container">'
        result += '<div class="grid-item"><h2>{}</h2>'.format(
            dialog.title) + '</div>'
        result += """
        <form action='/disconnect' method='post'>
            <div class='grid-item'>
                <input type='submit' class='w3-btn w3-white' value='Desconectar'>
            </div>
        </form>
        """
        result += '</span>'

        async for m in client.iter_messages(dialog, 10):
            result += await(format_message(m))

        return await render_template_string(BASE_TEMPLATE, content=result)

    # Ask for the phone if we don't know it yet
    if phone is None:
        return await render_template_string(BASE_TEMPLATE, content=PHONE_FORM)

    return await render_template_string(BASE_TEMPLATE, content=CODE_FORM)


async def main():
    await hypercorn.asyncio.serve(app, hypercorn.Config())

if __name__ == '__main__':
    client.loop.run_until_complete(main())
