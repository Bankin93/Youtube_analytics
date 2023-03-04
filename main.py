from pprint import pprint

from youtube.youtube import Youtube, Video, PLVideo, PlayList

#channel = Youtube('UCMCgOm8GZkHp8zJ6l7_hIuA')  # Вдудь
#channel_1 = Youtube('UC1eFXmJNkjITxPFWTy6RsWg')  # Редакция
#channel.print_info()
# print(channel.channel_title)
# print(channel.video_count)
# print(channel.channel_link)
# # channel.channel_id = 'Новое название'  # менять не можем
# print(channel.channel_id)
# print(Youtube.get_service())
# channel.to_json('channel.json')
# print(channel)
# print(channel_1)
# print(channel > channel_1)
# print(channel < channel_1)
# print(channel + channel_1)

# video1 = Video('9lO06Zxhu88')
# video1.print_info_v()
# print(video1)
#
# video2 = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
# video2.print_info_pl()
# print(video2)

pl = PlayList('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')

print(pl.playlist_title)
print(pl.playlist_url)

duration = pl.total_duration
print(duration)
print(type(duration))
print(duration.total_seconds())
print(pl.show_best_video())
