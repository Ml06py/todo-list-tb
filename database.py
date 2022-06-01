import sqlite3

class DataBase():
    def __init__(self):
        self.connect = sqlite3.connect("database.db")
        self.cur = self.connect.cursor()

    def authenticate(self, user_id):
        '''
            Check if user exist on db, if not it will be added to db
        '''
        #Search for user
        user = self.cur.execute("SELECT userid, auth FROM users where userid = (?)", (user_id,))
        result = [i for i in user]
        #if user does not exist, this func add them to db
        if result == []:
            self.cur.execute("INSERT INTO users (userid, auth) VALUES (?,?)", (user_id, "f",))
            self.connect.commit()
            return False
        #if user is in db but he is not authenticated to website, it will return it
        elif result != [] and result[0][1] == "f":
            return False
        # if user is authenticated to website and exist in db, func will return true
        elif result != [] and result[0][1] == "t":
            return True

    