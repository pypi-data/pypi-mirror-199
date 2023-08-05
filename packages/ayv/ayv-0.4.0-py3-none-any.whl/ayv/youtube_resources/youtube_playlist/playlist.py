from .playlist_item import PlaylistItem

class Playlist:
    def __init__(self, id, channelId, title, description, thumbnails, channelTitle, 
                itemCount, player):
        self.__id = id
        self.__channelId = channelId
        self.__title = title
        self.__description = description
        self.__thumbnails = thumbnails
        self.__channelTitle = channelTitle
        self.__itemCount = itemCount
        self.__player = player
        self.__playlist_items = []
        self.__videos = []
        
    def get_playlist_items(self, youtube_client):
        if not self.__playlist_items:
            basic_info_params = self.__generate_basic_info_params()
            search_request = youtube_client.playlistItems().list(
                **basic_info_params
            )
            search_response = search_request.execute()
            parsed_response = self.__parse_playlist_items(search_response)
            self.__playlist_items = [PlaylistItem(**item) for item in parsed_response]
        return self.__playlist_items
    
    def get_videos(self, youtube_client):
        if not self.__videos:
            play_list_items = self.get_playlist_items(youtube_client)
            for playlist_item in play_list_items:
                self.__videos.append(playlist_item.get_video(youtube_client))
        return self.__videos
    
    def __generate_basic_info_params(self):
        basic_info_params = dict(
            part='id,snippet,contentDetails',
            playlistId=self.__id
        ) 
        return basic_info_params
    
    def __parse_playlist_items(self, search_response):
        playlist_items = []
        items = search_response['items']
        for item in items:
            playlist_item = dict()
            playlist_item['id'] = item['id']
            playlist_item['publishedAt'] = item['snippet']['publishedAt']
            playlist_item['channelId'] = item['snippet']['channelId']
            playlist_item['title'] = item['snippet']['title']
            playlist_item['description'] = item['snippet']['description']
            playlist_item['thumbnails'] = item['snippet']['thumbnails']
            playlist_item['channelTitle'] = item['snippet']['channelTitle']
            playlist_item['position'] = item['snippet']['position']
            playlist_item['videoId'] = item['snippet']['resourceId']['videoId']
            playlist_item['videoOwnerChannelTitle'] = item['snippet']['videoOwnerChannelTitle']
            playlist_item['videoOwnerChannelId'] = item['snippet']['videoOwnerChannelId']
            playlist_items.append(playlist_item)
        return playlist_items
    
    def get_playlist_thumbnail(self):
        pass
    
    def get_playlist_title(self):
        pass
    
    def get_playlist_channel_title(self):
        pass
    
    def get_playlist_channel_thumbnail(self):
        pass