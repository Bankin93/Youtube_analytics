import json
import datetime
import isodate
from abc import ABC, abstractmethod

from youtube.mixin import Mixin


class Youtube(Mixin):
    """Базовый класс, для работы с API YouTube"""
    def __init__(self, channel_id):
        super().__init__()

        self.channel = self.get_channel_info(channel_id)  # Получение информации о канале

        # Инициализация атрибутов класса
        self._channel_id = channel_id  # ID канала
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
        print(super().print_info(self.channel))

    @property
    def channel_id(self) -> str:
        """возвращает id канала"""
        return self._channel_id

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


class Video(Mixin):
    """Базовый класс Видео"""
    def __init__(self, video_id):
        super().__init__()
        try:
            self._video_id = video_id
            self.video = self.get_video_info(video_id)  # получение информации о видео

            # Инициализация дополнительных атрибутов класса
            self.video_title = self.video['items'][0]['snippet']['title']  # название видео
            self.video_views = int(self.video['items'][0]['statistics']['viewCount'])  # количество просмотров
            self.video_likes = int(self.video['items'][0]['statistics']['likeCount'])  # количество лайков

        except IndexError:
            self.video_title = None
            self.video_views = None
            self.video_likes = None

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
        self.playlist = self.get_playlist_info(playlist_id)  # получение информации о плэйлисте

        # Инициализация дополнительного атрибута
        self.playlist_title = self.playlist['items'][0]['snippet']['title']  # название плэйлиста

    def __repr__(self):
        return f"{self.__class__.__name__}('{self._video_id}', '{self.playlist_id}')"

    def __str__(self):
        return f"{super().__str__()} ({self.playlist_title})"

    def print_info_pl(self):
        """Выводим информацию о плэйлисте в консоль"""
        print(json.dumps(self.playlist, indent=2, ensure_ascii=False))


class AbstractLog(ABC):
    """Абстрактный класс AbstractLog, содержайщий абстрактные методы"""

    @abstractmethod
    def playlist_title(self) -> str:
        pass

    @abstractmethod
    def playlist_url(self) -> str:
        pass

    @abstractmethod
    def total_duration(self) -> datetime.timedelta:
        pass

    @abstractmethod
    def show_best_video(self) -> str:
        pass


class PlayList(AbstractLog, Mixin):
    """Класс плэйлист, наследуемый от класс AbstractLog и Mixin"""
    def __init__(self, playlist_id):
        super().__init__()
        self.playlist_id = playlist_id

        self.playlist = self.get_playlist_info(playlist_id)  # получение информации о плэйлисте
        self.playlist_videos = self.get_playlist_videos(playlist_id)  # список видео
        self.video_ids = self.get_video_ids(playlist_id)  # список видео ID
        self.video_response = self.get_video_info_by_id(self.video_ids)  # получение информации о видео

        # Доп атрибуты: названия и url плэйлиста
        self._playlist_title = self.playlist['items'][0]['snippet']['title']  # название плэйлиста
        self._playlist_url = f'https://www.youtube.com/playlist?list={self.playlist_id}'  # ссылка на плэйлист

    @property
    def playlist_title(self) -> str:
        """Название плэйлиста"""
        return self._playlist_title

    @property
    def playlist_url(self) -> str:
        """Ссылка на плэйлист"""
        return self._playlist_url

    def print_info_playlist_videos(self) -> json:
        """Выводим информацию о видео в плэйлисте в консоль"""
        print(json.dumps(self.playlist_videos, indent=2, ensure_ascii=False))

    @property
    def total_duration(self) -> datetime.timedelta:
        """подсчет суммарной длительности плейлиста"""
        total_duration = datetime.timedelta()

        for video in self.video_response['items']:
            # Длительности YouTube-видео представлены в ISO 8601 формате
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration

        return total_duration

    def show_best_video(self) -> str:
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""

        best_video = None
        max_likes = 0
        for video in self.video_response['items']:
            if isinstance(int(video['statistics']['likeCount']), int):
                if int(video['statistics']['likeCount']) > max_likes:
                    best_video = video
                    max_likes = int(video['statistics']['likeCount'])
        return f'https://youtu.be/{best_video["id"]}'
