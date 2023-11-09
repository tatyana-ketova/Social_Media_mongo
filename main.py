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

# MongoDB connection details
host = 'localhost'  # MongoDB server address
port = 27017  # MongoDB server port

database_name = 'social_media'  # Name of the database you want to connect to

# Create a connection to the MongoDB server
client = pymongo.MongoClient(host, port)

database = client[database_name]
users_collection = database["users"]
posts_collection = database["posts"]


def user_registration(username, email, password):
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


def post_messages(main_user, message):
    data = {"username": main_user, "message": message}

    if data == {}:
        print('there is no message')
    else:
        insert_result = posts_collection.insert_one(data)
        print('You {} wrote post successfully'.format(main_user))

def follow_user(user_in, followers):

    user_document = users_collection.find_one({"username": user_in})
    if "followers" in user_document:
        followers_list = user_document.get("followers", [])
    else:
        followers_list = []
    followers_list.append(followers)
    users_collection.update_one(
        {"username": user_in},
        {"$set": {"followers": followers_list}}
    )




def unfollow_user():
    pass

def user_exist(username):
    existing_user = users_collection.find_one({"username": username})
    return existing_user


main_user = " "
regist_answer = input("Do you want to registered? Y/N")
if regist_answer == "Y":
    username = input("Write your login")
    email = input("Write your email")
    password = input("Write your password")
    user_registration(username, email, password)
elif regist_answer == "N":
    print("Good buy")

login_answer = input("Do you want to login in? Y/N")
if login_answer == "Y":
    username = input("Write your login")
    password = input("Write your password")
    main_user = user_login(username, password)
elif login_answer == "N":
    print("Good buy")

post_answer = input("Do you want to write message? Y/N")
if post_answer == "Y":
    if main_user != " ":
        message = input("Write your message {}".format(main_user))
        post_messages(main_user,message)

elif post_answer == "N":
    print("Good buy")

follow_answer1 = input("Do you want to follow users? Y/N")

if follow_answer1 == "Y":
    follow_answer2 = input("Which user do you want to follow?")
    if user_exist(follow_answer2) is not None:
        follow_user(main_user, follow_answer2)
    else:
        print("We dont have that user in our media")

if follow_answer1 == "N":
    print('Thank you')



print("Posts")
tasks = posts_collection.find()
for task in tasks:
    print(task)
print("Users")
tasks = users_collection.find()
for task in tasks:
    print(task)
client.close()

"""
query = {'_id': ObjectId('654cce8dca701b31c7660f52')}
new_values = {"$set": {"followers": ['tatyana_ost']}}
users_collection.update_one(query, new_values)
"""
