import sys

import telethon
from telethon.tl import functions, types

# read environment variables
with open('.env', 'r') as f:
    for line in f:
        key, val = line.strip().split('=')
        globals()[key] = val

target_group = '@east_shift'
# remove `@` if specified
if target_group and target_group.startswith('@'):
    target_group = target_group.split('@')[1]


try:
    client = telethon.TelegramClient(SESSION_NAME, APP_API_ID, APP_API_HASH)
    client.start()
except Exception as e:
    print('Error while authenticating the user:\n\t%s' % e)
    sys.exit()

chats = []
if client.is_user_authorized():
    print('User is authenticated')
    try:
        chat_obj = client(functions.channels.GetChannelsRequest(
            id=[target_group]
        ))  # returns Chats obj with minimal number of data
        # chat_obj = client(functions.channels.GetFullChannelRequest(
        #     channel=target_group
        # ))  # returns ChatFull obj with much data
        print(chat_obj.stringify())
        group = chat_obj.chats[0]
    except Exception as e:
        print(e)
        sys.exit(2)

    chats = [group]
print(chats)

NEW_MESSAGES = 10_000
posts = []
for message in client.iter_messages(chats[0]):
        if message.text:
            posts.append(message.text)
        if len(posts) == NEW_MESSAGES:
            break
print(len(posts), ' from ', target_group)

import json
with open(target_group + '.json', 'w', encoding='ascii') as f:
    json.dump(posts, f)