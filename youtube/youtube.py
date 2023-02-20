import os
import json

from googleapiclient.discovery import build


class Youtube:
    """Базовый класс, для работы с API YouTube"""
    def __init__(self, channel_id):
        self._channel_id = channel_id

        api_key: str = os.environ.get('YOUTUBE_API_KEY')  # Получаем ключ API из переменной окружения
        youtube = build('youtube', 'v3', developerKey=api_key)  # сервис youtube
        self.channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()  # инфо о канале

        # Инициализация атрибутов класса
        self._channel_id = self.channel['items'][0]['id']  # id канала
        self.channel_title = self.channel['items'][0]['snippet']['title']  # название канала
        self.channel_description = self.channel['items'][0]['snippet']['description']  # описание канала
        self.channel_link = 'https://www.youtube.com/channel/' + self.channel_id  # ссылка на канал
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']  # количество подписчиков
        self.video_count = self.channel['items'][0]['statistics']['videoCount']  # количество видео
        self.view_count = self.channel['items'][0]['statistics']['viewCount']  # общее количество просмотров

    def print_info(self):
        """ Выводим информацию о канале на консоль"""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self) -> str:
        """возвращает id канала"""
        return self._channel_id

    @staticmethod
    def get_service():
        """возвращает объект для работы с API ютуба"""
        api_key: str = os.environ.get('YOUTUBE_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, filename) -> None:
        """сохраняет информацию по каналу, хранящуюся в атрибутах экземпляра класса Youtube, в json-файл"""
        with open(filename, "w", encoding='utf-8') as file:
            json.dump({
                "channel_id": self._channel_id,
                "channel_title": self.channel_title,
                "channel_description": self.channel_description,
                "channel_link": self.channel_link,
                "subscriber_count": self.subscriber_count,
                "video_count": self.video_count,
                "view_count": self.view_count
            }, file, indent=2, ensure_ascii=False)
