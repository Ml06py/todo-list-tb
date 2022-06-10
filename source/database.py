import sqlite3

class DataBase():
    def __init__(self):
        self.connect = sqlite3.connect("source/database.db")
        self.cur = self.connect.cursor()

    def authenticate(self, user_id):
        '''
            Check if user exist on db, if not it will be added to db
        '''
        #Search for user
        result = self.cur.execute("SELECT userid, auth FROM users where userid = (?)", (user_id,)).fetchall()

        #if user does not exist, this func will add them to db
        if not result:
            self.cur.execute("INSERT INTO users (userid, auth) VALUES (?,?)", (user_id, "f",))
            self.connect.commit()
            return False

        else:
            return result[0][1] == 't'

    def token(self, user_id, token):
        '''
            This func add user token to db
        '''
        self.cur.execute("UPDATE users SET usertoken = (?), auth = (?) where userid = (?)", (token, "t", user_id,))
        self.connect.commit()
    def logout(self, user_id):
        '''
            Log out a user (set status 'n' and remove his token)
        '''
        self.cur.execute("UPDATE users SET usertoken = NULL , auth = (?) where userid = (?)", ("f", user_id,))
        self.connect.commit()


    def info(self, user_id):
        '''
            Return users token
        '''
        user = self.cur.execute("SELECT userid, usertoken FROM users where userid = (?)", (user_id,))
        result = [i for i in user]
        if result != []:
            return result[0][1]
        else:
            return False

