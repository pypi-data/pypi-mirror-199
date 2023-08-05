class YouTubeVideoDetails:
    def __init__(self, id: str, channelId: str, title: str, channelTitle: str, 
                 description: str, thumbnails: str, tags: list[str], duration: str, licensedContent: bool):
        self.__id = id
        self.__channel_id = channelId
        self.__title = title
        self.__channel_title = channelTitle
        self.__description = description
        self.__thumbnails = thumbnails
        self.__tags = tags
        self.__duration = duration
        self.__licensed_content = licensedContent
        
    def get_video_details(self):
        video_details = {
            'id': self.__id,
            'channel_id': self.__channel_id,
            'title': self.__title,
            'channel_title': self.__channel_title,
            'description': self.__description,
            'thumbnail': self.__thumbnails['standard'],
            'tags': self.__tags,
            'duration': self.__duration,
            'licensed_content': self.__licensed_content
        }
        return video_details
    
    def get_video_id(self):
        return self.__id