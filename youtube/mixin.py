import os
import json
from googleapiclient.discovery import build


class Mixin:

    api_key: str = os.environ.get('YOUTUBE_API_KEY')  # Получаем ключ API из переменной окружения
    youtube = build('youtube', 'v3', developerKey=api_key)  # сервис youtube

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self):
        super().__init__()

    @staticmethod
    def print_info(value: dict) -> json:
        """ Выводим информацию в формате Json на консоль"""
        print(json.dumps(value, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с API ютуба"""
        return cls.youtube

    @classmethod
    def get_channel_info(cls, channel_id: str) -> dict:
        """Возвращает информацию о канале"""
        channel = cls.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        return channel

    @classmethod
    def get_video_info(cls, video_id: str) -> dict:
        """Возвращает информацию о видео"""
        video = cls.youtube.videos().list(id=video_id, part='snippet,statistics').execute()
        return video

    @classmethod
    def get_playlist_info(cls, playlist_id: str) -> dict:
        """Возвращает информацию о плейлисте"""
        playlist = cls.youtube.playlists().list(id=playlist_id, part='snippet').execute()
        return playlist

    @classmethod
    def get_playlist_videos(cls, playlist_id: str) -> list:
        """Возвращает информацию о видео в плейлисте"""
        playlist_videos = cls.youtube.playlistItems().list(playlistId=playlist_id, part='contentDetails',
                                                           maxResults=50).execute()
        return playlist_videos

    @classmethod
    def get_video_ids(cls, playlist_id: str) -> list:
        """Возвращает список видео в плейлисте"""
        playlist_videos = cls.youtube.playlistItems().list(playlistId=playlist_id, part='contentDetails',
                                                           maxResults=50).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        return video_ids

    @classmethod
    def get_video_info_by_id(cls, video_ids: list[str]) -> dict:
        """Возвращает информацию о видео по ID"""
        video_response = cls.youtube.videos().list(part='contentDetails,snippet,statistics',
                                                   id=','.join(video_ids)).execute()
        return video_response
