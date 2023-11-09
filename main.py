"""
In this lab, you'll create a console-based social
media application with the following features:
User Registration: Users can create an account with a username and password.
User Login: Users can log in to their accounts.
Post Messages: Logged-in users can post messages with text content.
Follow/Unfollow Users: Users can follow and unfollow other users.
View User Feed: Users can view a feed of messages from users they are following.

"""


import pymongo
from bson import ObjectId

#MongoDB connection details
host = 'localhost'  # MongoDB server address
port = 27017        # MongoDB server port

database_name = 'social_media'  # Name of the database you want to connect to


# Create a connection to the MongoDB server
client = pymongo.MongoClient(host, port)

database = client[database_name]
users_collection = database["users"]
posts_collection = database["posts"]



def user_registration(username,email,password):
    data = {"username": username, "email": email, "password": password}
    insert_result = users_collection.insert_one(data)
    print("{}, you are registered successfully!!!!".format(username))


def user_login(username, password):
    users = users_collection.find_one(username, password)
    if users == {}:
        print('there is no user {} os password not right')
    else:
        print('You {} are login in successfully'.format(username))
        return username

def post_messages():
    pass

def follow_user():
    pass

def unfollow_user():
    pass

regist_answer = input("Do you want to registered? Y/N")
if regist_answer == "Y":
    username = input ("Write your login")
    email = input("Write your email")
    password = input("Write your password")
    user_registration(username,email,password)
elif regist_answer == "N":
    print("Good buy")

login_answer = input("Do you want to login in? Y/N")
if login_answer == "Y":
    username = input("Write your login")
    password = input("Write your password")
    user_login(username, password)
elif login_answer == "N":
    print("Good buy")

print("Posts")
tasks = posts_collection.find()
for task in tasks:
        print(task)
print("Users")
tasks = users_collection.find()
for task in tasks:
        print(task)
client.close()
