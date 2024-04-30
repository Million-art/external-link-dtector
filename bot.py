import re
import requests
import time

# Replace with your actual bot token
TOKEN = '7127819217:AAFmQVxcitAFBmdi7FJxhAbq4fKmOwIDx-w'
CHANNEL_USERNAME = '@inbivili'  # Replace with the channel username

def has_youtube_link(text):
    youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    return re.search(youtube_regex, text)

def check_last_post():
    try:
        response = requests.get(f'https://api.telegram.org/bot{TOKEN}/getUpdates', params={'limit': 1, 'offset': -1})
        data = response.json()
        if data.get('ok'):
            update = data.get('result', [])[0]
            message = update.get('message')
            if message and message.get('chat') and message['chat'].get('type') == 'channel' and message['chat']['username'] == CHANNEL_USERNAME:
                entities = message.get('entities', [])
                for entity in entities:
                    if entity.get('type') == 'text_link':
                        if has_youtube_link(entity['url']):
                            message_id = message['message_id']
                            chat_id = message['chat']['id']
                            requests.post(f'https://api.telegram.org/bot{TOKEN}/deleteMessage', params={'chat_id': chat_id, 'message_id': message_id})
                            break
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    while True:
        check_last_post()
        # Sleep for a few seconds before checking for the latest post again
        time.sleep(5)

if __name__ == '__main__':
    main()
