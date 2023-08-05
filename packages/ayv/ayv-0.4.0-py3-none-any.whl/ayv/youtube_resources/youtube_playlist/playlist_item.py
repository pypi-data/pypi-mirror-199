from ...search.video import FindVideo

class PlaylistItem:
    def __init__(self, id, publishedAt, channelId, title, description, thumbnails, 
                channelTitle, position, videoId, videoOwnerChannelTitle, 
                videoOwnerChannelId):
        self.__id = id
        self.__publishedAt = publishedAt
        self.__channelId = channelId
        self.__title = title
        self.__description = description
        self.__thumbnails = thumbnails
        self.__channelTitle = channelTitle
        self.__position = int(position)
        self.__videoId = videoId
        self.__videoOwnerChannelTitle = videoOwnerChannelTitle
        self.__videoOwnerChannelId = videoOwnerChannelId
        self.__video = None
        
    def get_video(self, youtube_client):
        if not self.__video:
            self.__video = FindVideo(self.__videoId).find_video(youtube_client)
        return self.__video