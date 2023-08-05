from ..youtube_search import YouTubeSearch
from ..search_type import YouTubeSearchType
from ..search_query import YouTubeSearchQuery
from .find_playlist import FindPlaylist

class PlaylistSearch(YouTubeSearch):
    __MAX_RESULTS = 10
    __REGION_CODE = 'US'
    
    def __init__(self, query_string: str):
        self.__type = YouTubeSearchType.PLAYLIST
        self.__query = YouTubeSearchQuery(query_string)
        
    def __get_query(self):
        return self.__query.query_string
        
    def basic_info(self):
        basic_info_params = self.__generate_basic_info_params()
        return basic_info_params
    
    def advanced_info(self):
        pass
    
    def all_info(self):
        pass
    
    def __generate_basic_info_params(self):
        basic_info_params = dict(
            part='id',
            type=self.__type,
            q=self.__get_query(),
            maxResults=self.__MAX_RESULTS,
        ) 
        return basic_info_params
    
    def search_playlist(self, youtube_client, search_type='basic'):
        search_response = None
        if search_type == 'basic':
            basic_info_params = self.__generate_basic_info_params()
            search_request = youtube_client.search().list(
                **basic_info_params
            )
            search_response = search_request.execute()
            playlist_ids = self.__parse_playlists(search_response)
            play_lists = [FindPlaylist(playlist_id).find_playlist(youtube_client)
                         for playlist_id in playlist_ids]
        return play_lists
    
    def __parse_playlists(self, search_response):
        playlists_ids = []
        items = search_response['items']
        for item in items:
            playlists_ids.append(item['id']['playlistId'])
        return playlists_ids
        