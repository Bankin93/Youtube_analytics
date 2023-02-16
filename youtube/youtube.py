import os
import json

from googleapiclient.discovery import build


class Youtube:
    def __init__(self, channel_id):
        self.channel_id = channel_id

        #Получаем ключ API из переменной окружения
        api_key: str = os.environ.get('YOUTUBE_API_KEY')
        #сервис youtube
        youtube = build('youtube', 'v3', developerKey=api_key)
        #Получаем информацию о канале
        self.channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

# channel_id = 'UCMCgOm8GZkHp8zJ6l7_hIuA'  # вДудь

    def print_info(self):
        """ Выводим информацию о канале на консоль"""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))


vdud = Youtube('UCMCgOm8GZkHp8zJ6l7_hIuA')
vdud.print_info()

