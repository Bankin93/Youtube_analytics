import os
import json
import datetime
import isodate
from abc import ABC, abstractmethod
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
        self.subscriber_count = int(self.channel['items'][0]['statistics']['subscriberCount'])  # количество подписчиков
        self.video_count = int(self.channel['items'][0]['statistics']['videoCount'])  # количество видео
        self.view_count = int(self.channel['items'][0]['statistics']['viewCount'])  # общее количество просмотров

    def __repr__(self):
        return f"{self.__class__.__name__}('{self._channel_id}')"

    def __str__(self):
        return f'YouTube-канал: {self.channel_title}'

    def __add__(self, other) -> int:
        """Сложение количества подписчиков каналов"""
        if isinstance(other, Youtube):
            return self.subscriber_count + other.subscriber_count

    def __gt__(self, other) -> bool:
        """Сравнение количества подписчиков каналов на больше/меньше"""
        if isinstance(other, Youtube):
            return self.subscriber_count > other.subscriber_count

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


class Video:
    """Базовый класс Видео"""
    def __init__(self, video_id):
        self._video_id = video_id

        youtube = Youtube.get_service()
        self.video = youtube.videos().list(id=video_id, part='snippet,statistics').execute()  # инфо о видео

        # Инициализация дополнительных атрибутов класса
        self.video_title = self.video['items'][0]['snippet']['title']  # название видео
        self.video_views = int(self.video['items'][0]['statistics']['viewCount'])  # количество просмотров
        self.video_likes = int(self.video['items'][0]['statistics']['likeCount'])  # количество лайков

    def __repr__(self):
        return f"{self.__class__.__name__}('{self._video_id}')"

    def __str__(self):
        return f'{self.video_title}'

    def print_info_v(self):
        """ Выводим информацию о видео на консоль"""
        print(json.dumps(self.video, indent=2, ensure_ascii=False))

    @property
    def video_id(self) -> str:
        """Возвращает id видео"""
        return self.video_id


class PLVideo(Video):
    """Класс плэйлист видео, наследуемый класса Video"""
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

        youtube = Youtube.get_service()
        self.playlist = youtube.playlists().list(id=self.playlist_id, part='snippet').execute()  # инфо о плэйлисте

        # Инициализация дополнительного атрибута
        self.playlist_title = self.playlist['items'][0]['snippet']['title']  # название плэйлиста

    def __repr__(self):
        return f"{self.__class__.__name__}('{self._video_id}', '{self.playlist_id}')"

    def __str__(self):
        return f"{super().__str__()} ({self.playlist_title})"

    def print_info_pl(self):
        """Выводим информацию о плэйлисте в консоль"""
        print(json.dumps(self.playlist, indent=2, ensure_ascii=False))


class MixinLog(ABC):
    """Абстрактный класс миксин, содержайщий абстрактные методы"""

    @abstractmethod
    def playlist_title(self) -> str:
        pass

    @abstractmethod
    def playlist_url(self) -> str:
        pass

    @abstractmethod
    def total_duration(self):
        pass

    @abstractmethod
    def show_best_video(self):
        pass


class PlayList(MixinLog):
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id

        youtube = Youtube.get_service()
        self.playlist = youtube.playlists().list(id=self.playlist_id, part='snippet').execute()  # инфо о плэйлисте
        self.playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id, part='contentDetails',
                                                            maxResults=50).execute()  # инфо о видео в плэйлисте

        # Доп атрибуты: названия и url плэйлиста
        self._playlist_title = self.playlist['items'][0]['snippet']['title']
        self._playlist_url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    @property
    def playlist_title(self) -> str:
        """Название плэйлиста"""
        return self._playlist_title

    @property
    def playlist_url(self) -> str:
        """Ссылка на плэйлист"""
        return self._playlist_url

    def print_info_playlist_videos(self):
        """Выводим информацию о видео в плэйлисте в консоль"""
        print(json.dumps(self.playlist_videos, indent=2, ensure_ascii=False))

    @property
    def total_duration(self) -> datetime.timedelta:
        """подсчет суммарной длительности плейлиста"""

        # получаем все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]

        youtube = Youtube.get_service()
        video_response = youtube.videos().list(part='contentDetails,statistics', id=','.join(video_ids)).execute()

        total_duration = datetime.timedelta()

        for video in video_response['items']:
            # Длительности YouTube-видео представлены в ISO 8601 формате
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration

        return total_duration

    def show_best_video(self) -> str:
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        youtube = Youtube.get_service()
        video_response = youtube.videos().list(part='snippet,statistics', id=','.join(video_ids)).execute()

        best_video = None
        max_likes = 0
        for video in video_response['items']:
            if isinstance(int(video['statistics']['likeCount']), int):
                if int(video['statistics']['likeCount']) > max_likes:
                    best_video = video
                    max_likes = int(video['statistics']['likeCount'])
        return f'https://youtu.be/{best_video["id"]}'
