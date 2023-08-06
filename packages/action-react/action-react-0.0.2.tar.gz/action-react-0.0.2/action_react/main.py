import configparser

from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.types import PeerChannel

CATEGORY = "H"
FILENAME = "config.ini"


def read_configs(file_name):
    config = configparser.ConfigParser()
    config.read(file_name)
    api_id = config["Telegram"]["api_id"]
    api_hash = str(config["Telegram"]["api_hash"])
    phone = config["Telegram"]["phone"]
    username = config["Telegram"]["username"]
    target_date = datetime.strptime(config["General"]["target-date"], "%m/%d/%Y").date()
    cities = config["General"]["cities"].split(", ")
    return api_id, api_hash, phone, username, target_date, cities


def get_target_channel():
    listening_channel = input("enter entity (telegram URL or entity id) to listen to: ")
    if listening_channel.isdigit():
        return PeerChannel(int(listening_channel))
    return listening_channel


def connect_to_telegram(username, api_id, api_hash, phone):
    client = TelegramClient(username, api_id, api_hash)
    client.start()
    return client


def check_message(message, target_date, cities):
    try:
        colon_list = message.split(":")
        message_list = [" ".join(colon_list[0].split()[:-1])] + [colon_list[0].split()[-1]] + colon_list[1].split()
        if message_list[1] == CATEGORY:
            city = message_list[0]
            date = message_list[-1]
            if len(date.split("/")) == 2:
                date = "2023/" + date
            date = datetime.strptime(date, "%Y/%m/%d").date()
            if date < target_date and city.lower() in cities:
                return True, (date, city)
        return False, None
    except Exception as e:
        print(f"error {e}")
        return False, None


def main(api_id, api_hash, phone, username, target_date, cities):
    listening_channel = get_target_channel()
    client = connect_to_telegram(username, api_id, api_hash, phone)

    @client.on(events.NewMessage(chats=listening_channel))
    async def listener(event):
        message = event.message.message
        print("received message:\n" + message)
        is_good, info = check_message(message, target_date, cities)
        if is_good:
            date, city = info
            print(f"found a good appointment in {city} on {date} ")

    with client:
        client.run_until_disconnected()


if __name__ == "__main__":
    api_id, api_hash, phone, username, target_date, cities = read_configs(FILENAME)
    main(api_id, api_hash, phone, username, target_date, cities)
