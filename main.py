from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from decouple import config
from database import DataBase
from request import Request
from pyromod import listen
# config your api id, api hash and your bot token here 
app = Client(
    "git",
    api_id = config("API_ID"),
    api_hash = config("API_HASH"),
    bot_token = config("TOKEN"))

db = DataBase()
re = Request()

@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    '''
        response to /start command
    '''
    #if user is authenticated
    if (db.authenticate(user_id=message.from_user.id)):
        await message.reply(f""" Hello [{message.from_user.first_name}](tg://user?id={message.from_user.id}).
        Welcome back.
                            """,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(
                        "Logout", 
                        callback_data = "logout-request"
                    )
                    ],
                ]
            )
        )
    else:
        await message.reply(f""" Hello [{message.from_user.first_name}](tg://user?id={message.from_user.id}).
        Welcome to todo bot.
        you are not authenticated, please register/login to our website .
                            """,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(
                    "Register", 
                    callback_data = "register-request"
                ),
                InlineKeyboardButton("Login",
                    callback_data = "login-request",
                )
                ],
            ]
        )
    )




@app.on_callback_query(filters.regex("^login-request$"))
async def callback(c, q):
    '''
        Login user to website and add to db
    '''

    message_id = q.message.chat.id

    await q.edit_message_text("Send me your username")
    username = await app.listen(message_id, filters=filters.text, timeout=120)
    await app.send_message(message_id, "Now send me your Token")
    token = await app.listen(message_id, filters=filters.text, timeout=120)
    # send request
    msg = await app.send_message(message_id, "Request sent")
    if re.Login(username.text, token.text, message_id):
        db.token(user_id=message_id, token=token.text)
        await msg.edit("you are now logged in")
    else:
        await msg.edit("Sth went wrong, token or username is invalid.")
    

@app.on_callback_query(filters.regex("^register-request$"))
async def callback(c, q):
    '''
        Register user to website and add to db
    '''
    message_id = q.message.chat.id
    await q.edit_message_text("Tell me your first name")
    first_name = await app.listen(message_id, filters=filters.text, timeout=120)

    await app.send_message(message_id, "Tell me your last name")
    last_name = await app.listen(message_id, filters=filters.text, timeout=120)

    await app.send_message(message_id, "tell me your password (must contain numbers and letters")
    password = await app.listen(message_id, filters=filters.text, timeout=120)

    if (request:= re.Register(first_name.text, last_name.text,message_id , password.text)):
        db.token(user_id=message_id, token=request[1])
        await app.send_message(message_id, f"""You are now registered 
                                            your username: `{request[2]}`
                                            Your token: |{request[1]}| (keep it safe)"""
                                            )
    else:
        await app.send_message(message_id, f"sth went wrong... \n please try again later")



@app.on_callback_query(filters.regex("^logout-request$"))
async def callback(c, q):
    '''
        Logout user from website and remove token from db
    '''

    message_id = q.message.chat.id

    await q.edit_message_text("Send me your username")
    username = await app.listen(message_id, filters=filters.text, timeout=120)
    await app.send_message(message_id, "Now send me your Token")
    token = await app.listen(message_id, filters=filters.text, timeout=120)
    # send request
    msg = await app.send_message(message_id, "Request sent")
    if re.Logout(username.text, token.text, message_id):
        db.logout(user_id=message_id)
        await msg.edit("you are now logged out")
    else:
        await msg.edit("Sth went wrong, token or username is invalid.")


app.run()