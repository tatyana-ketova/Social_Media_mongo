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

host = 'localhost'
port = 27017

database_name = 'social_media'


client = pymongo.MongoClient(host, port)

database = client[database_name]
users_collection = database["users"]
posts_collection = database["posts"]


def user_registration(username, email, password):
    data = {"username": username, "email": email, "password": password, "followers": []}
    insert_result = users_collection.insert_one(data)
    print("{}, you are registered successfully!!!!".format(username))


def user_login(username, password):
    users = users_collection.find_one(username, password)
    if users == {}:
        print('there is no user {} or password not right')
        return 0
    else:
        print('You, {}, are login in successfully'.format(username))
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
    print("{} add your list {}".format(followers, user_in))


def unfollow_user(user_in, unfollowers):
    user_document = users_collection.find_one({"username": user_in})
    if "followers" in user_document:
        followers_list = user_document.get("followers", [])
    else:
        followers_list = []
    if unfollowers in followers_list:
        followers_list.remove(unfollowers)
        users_collection.update_one(
            {"username": user_in},
            {"$set": {"followers": followers_list}}
        )
        print("{} deleted from your list {}".format(unfollowers,user_in))
    else:
        print("{}, you don't have {} in your followers".format(user_in,unfollowers))

def user_exist(username):
    existing_user = users_collection.find_one({"username": username})
    return existing_user

def show_favorite(username):
    x = 0
    user_document = users_collection.find_one({"username": username})
    followers_list = user_document.get("followers", [])
    for follower in followers_list:
        follower_posts = posts_collection.find({"username": follower})
        for post in follower_posts:
            print("post of {}:".format(follower))
            print(post["message"])
            x = 1
    if x == 0:
        print("{}, you has 0 messages from users".format(username))




main_user = " "
login_answer = " "
start_answer = input("Are you registered on our media? Y/N ")
if start_answer == "Y":
    login_answer = input("Do you want to login in? Y/N ")
else:
    regist_answer = input("Do you want to registered? Y/N ")
    if regist_answer == "Y":
        username = input("Write your login ")
        email = input("Write your email ")
        password = input("Write your password ")
        user_registration(username, email, password)
        login_answer = input("Do you want to login in? Y/N ")
    else:
        print("May be nex time ...")

if login_answer == "Y":
    username = input("Write your login ")
    password = input("Write your password ")
    main_user = user_login(username, password)
    n = 1
    if main_user != 0:
        while n != 0:
            do_answer = input("What do you want to do? W - write message; F -follow users, U - unfollow users, V - view messages from users, E - exit W/F/U/V/E ")
            if do_answer == "W":
                message = input("Write your message {}".format(main_user))
                post_messages(main_user, message)
            if do_answer == "F":
                answer_users = input("Which user do you want to follow? ")
                if user_exist(answer_users) is not None:
                    follow_user(main_user, answer_users)
                    n = 1
                else:
                    print("We dont have that user in our media")
                    n = 1
            if do_answer == "U":
                unfollow_us = input("Which user do you want to unfollow? ")
                if user_exist(unfollow_us) is not None:
                    unfollow_user(main_user, unfollow_us)
                    n = 1
                else:
                    print("We dont have {} user in our media".format(unfollow_us))
                    n = 1
            if do_answer == "V":
                show_favorite(main_user)
            if do_answer == "E":
                n = 0
                print("Good buy {}".format(main_user))

else:
    print("Good buy")

'''
#print all users

cursor = users_collection.find({})

for document in cursor:
    print(document)
'''
client.close()


