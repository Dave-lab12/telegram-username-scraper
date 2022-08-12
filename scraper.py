'''Program to scrape all the members from a given Telegram group and store them in a CSV file.'''

# Importing libraries
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import json
import sys
# Enter your own telegram api id and hash. You can get them by logging in with your phone number in the website: https://my.telegram.org/auth

# You can get detailed information in this page: https://core.telegram.org/api/obtaining_api_id


api_id = input("Enter your api id: ")
api_hash = input("Enter your api hash: ")
phone = input(
    "Enter your phone number (in international format(i.e. with country code)): ")



print(api_id, api_hash, phone)

client = TelegramClient(phone, api_id, api_hash)

# If you don't have a active session it will create one for you.
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input(
        'Enter the code (recieved in your telegram app): '))

# You can increase/decrease chunk size according to your own need.

chats = []
last_date = None
chunk_size = 2000
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

# It will show you all the groups in which you are a member.
print('Choose a group to scrape members from:')
i = 0
for g in groups:
    print(str(i) + '- ' + g.title)
    i += 1

g_index = input("Enter a Number: ")
target_group = groups[int(g_index)]

print('Fetching Members...')
all_participants = []
all_participants = client.get_participants(target_group)

print('Saving In file...')
membersCollection = []
for index, user in enumerate(all_participants):
    if user.username:
        membersCollection.append({"firstName": user.first_name, "lastName": user.last_name,
                                  "username": user.username, "groupTitle": target_group.title, "groupId": target_group.id})

with open("members.json", 'w', encoding='utf-8') as jsonf:
    jsonString = json.dumps(membersCollection, indent=4)
    jsonf.write(jsonString)


print('Members scraped successfully.')
