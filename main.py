from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
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
            reply_markup=ReplyKeyboardMarkup(
                [
                    ["tasks"],
                    ["add task", "update task"],
                    ["logout", "token"]  
                ],
                resize_keyboard=True
            )
        )
    else:
        await message.reply(f""" Hello [{message.from_user.first_name}](tg://user?id={message.from_user.id}).
        Welcome to todo bot.
        you are not authenticated, please register/login to our website .
                            """,
        reply_markup=ReplyKeyboardMarkup(
                [
                    ["login", "register"]  
                ],
                resize_keyboard=True
            )
        )




@app.on_message(filters.regex("^login$"))
async def login(c, m):
    '''
        Login user to website and add to db
    '''

    message_id = m.chat.id
    if not (db.authenticate(user_id=message_id)):
        # inputs
        await app.send_message(message_id, "Now send me your Username")
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
    else:
        await app.send_message(message_id, "You are already logged in!")
    

@app.on_message(filters.regex("^register$"))
async def register(c, m):
    '''
        Register user to website and add to db
    '''
    message_id = m.chat.id
    if not (db.authenticate(user_id=message_id)):
        # inputs 
        await app.send_message(message_id, "Tell me your first name")
        first_name = await app.listen(message_id, filters=filters.text, timeout=120)

        await app.send_message(message_id, "Tell me your last name")
        last_name = await app.listen(message_id, filters=filters.text, timeout=120)

        await app.send_message(message_id, "tell me your password (must contain numbers and letters")
        password = await app.listen(message_id, filters=filters.text, timeout=120)
        
        # send register request
        if (request:= re.Register(first_name.text, last_name.text,message_id , password.text)):
            db.token(user_id=message_id, token=request[1])
            await app.send_message(message_id, f"""You are now registered 
                                                your username: `{request[2]}`
                                                Your token: ||{request[1]}|| (keep it safe)"""
                                                )
        else:
            await app.send_message(message_id, f"sth went wrong... \n please try again later")
    else:
        await app.send_message(message_id, "You are already logged in!")


@app.on_message(filters.regex("logout"))
async def logout(c, m):
    '''
        Logout user from website and remove token from db
    '''

    message_id = m.chat.id
    if (db.authenticate(user_id=message_id)):
        await m.reply ("Send me your username")
        username = await app.listen(message_id, filters=filters.text, timeout=120)
        
        msg = await app.send_message(message_id, "Request sent")
        # get users token
        token = db.info(user_id=message_id)
        # send request
        if re.Logout(username.text, token, message_id):
            db.logout(user_id=message_id)
            await msg.edit("you are now logged out")
        else:
            await msg.edit("Sth went wrong, token or username is invalid.")
    else:
        await m.reply("You are not logged in!")


@app.on_message(filters.regex("^token$"))
async def token(c, m):
    '''
        return users token
    '''
    message_id = m.chat.id
    if (db.authenticate(user_id=message_id)):
        # get users token from db
        if (token:= db.info(user_id=message_id)):
            await m.reply(f"your token is: ||{token}||")
        else:
            "Token does not exist :|"
    else:
        await m.reply("You are not logged in!")


@app.on_message(filters.regex("^add task$"))
async def add_task(c, m):
    '''
        Add task to website db
    '''
    message_id = m.chat.id
    if (db.authenticate(user_id=message_id)):
        # inputs
        await m.reply ("give me a title for your task")
        name = await app.listen(message_id, filters=filters.text, timeout=120)
        await m.reply ("Write about 2 lines about what you want to do")
        description = await app.listen(message_id, filters=filters.text, timeout=120)
        await m.reply ("When you wanna do it? \n format-> YYYY-MM-DD HH:MM ")
        time = await app.listen(message_id, filters=filters.text, timeout=120)

        # send request to create a task
        request= re.Create(token=db.info(user_id=message_id),
                    name= name.text,
                    detail= description.text,
                    time= time.text)
        # if data was valid
        if (token:= request):
            await m.reply(f"Task saved! \nToken is ||{token[1]}||")
        else:
            await m.reply(f"Sth went wrong with your information, please correct them.")

    else:
        await m.reply("You are not logged in!")


@app.on_message(filters.regex("^update task$"))
async def update_task(c, m):
    '''
        Update your tasks status
    '''
    message_id = m.chat.id
    if (db.authenticate(user_id=message_id)):
        await m.reply ("Send me your task's token")
        task_token = await app.listen(message_id, filters=filters.text, timeout=120)
        request= re.Update(task_token=task_token.text, user_token=db.info(user_id=message_id))
        if request:
            await m.reply(f"Your task's status have changed.")
        else:
            await m.reply(f"Sth went wrong, make sure token is correct and status if unfinished.")
    else:
        await m.reply("You are not logged in!")


@app.on_message(filters.regex("^tasks$"))
async def task_option(c, m):
    '''
        Show available actions for tasks
    '''
    message_id = m.chat.id
    if (db.authenticate(user_id=message_id)):
        await app.send_message(
            message_id,
            "Select one option below",
            reply_markup=InlineKeyboardMarkup(
                [
                    [ 
                        InlineKeyboardButton( 
                            "All tasks file",
                            callback_data="task-file"
                        ),
                    ]
                ]
            )
        )

    else:
        await m.reply("You are not logged in!")


@app.on_callback_query(filters.regex("^task-file$"))
async def task_file(c, q):
    '''
        Return all tasks as a file
    '''
    message_id = q.message.chat.id

    if (db.authenticate(user_id=message_id)):
        # users token
        token = db.info(user_id=message_id)
        # send request to get users task
        request = re.List(token=token)

        # if user doesnt have any task
        if not request:
             await q.edit_message_text("You dont have any task, you can add one.")

        else:
            await q.edit_message_text("Check the file below")
            await app.send_document(message_id, request)
    else:
        await app.send_message(message_id, "You are not logged in!")



app.run()