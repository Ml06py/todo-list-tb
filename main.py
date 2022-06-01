from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from decouple import config
from database import DataBase

# config your api id, api hash and your bot token here 
app = Client(
    "git",
    api_id = config("API_ID"),
    api_hash = config("API_HASH"),
    bot_token = config("TOKEN"))

db = DataBase()


@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    '''
        response to /start command
    '''
    #if user is authenticated
    if (a := db.authenticate(user_id=message.from_user.id)):
        await message.reply(f""" Hello [{message.from_user.first_name}](tg://user?id={message.from_user.id}).
        Welcome back.
                            """)
    else:
        await message.reply(f""" Hello [{message.from_user.first_name}](tg://user?id={message.from_user.id}).
        Welcome to todo bot.
        you are not authenticated, please register/login to our website .
                            """,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Register", "pyrogram"),
                InlineKeyboardButton("Login", "pyrogram")],
            ]
        )
    )
        



app.run()