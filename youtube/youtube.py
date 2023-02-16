import os
import json

from googleapiclient.discovery import build


class Youtube:
    """Базовый класс, для работы с API YouTube"""
    def __init__(self, channel_id):
        self.channel_id = channel_id

        api_key: str = os.environ.get('YOUTUBE_API_KEY')  # Получаем ключ API из переменной окружения

        youtube = build('youtube', 'v3', developerKey=api_key)  # сервис youtube

        self.channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()  # инфо о канале

    def print_info(self):
        """ Выводим информацию о канале на консоль"""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))
