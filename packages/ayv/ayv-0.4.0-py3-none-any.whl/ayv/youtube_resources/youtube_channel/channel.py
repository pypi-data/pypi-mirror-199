class Channel:
    def __init__(self, id, title, description, customUrl, publishedAt, thumbnails, statistics):
        self.__id = id
        self.__title = title
        self.__description = description
        self.__customUrl = customUrl
        self.__publishedAt = publishedAt
        self.__thumbnails = thumbnails
        self.__statistics = statistics