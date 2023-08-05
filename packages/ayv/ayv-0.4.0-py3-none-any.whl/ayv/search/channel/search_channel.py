from ..youtube_search import YouTubeSearch
from ..search_type import YouTubeSearchType
from ..search_query import YouTubeSearchQuery
from .find_channel import FindChannel

class ChannelSearch(YouTubeSearch):
    __MAX_RESULTS = 10
    __REGION_CODE = 'US'
    
    def __init__(self, query_string: str):
        self.__type = YouTubeSearchType.CHANNEL
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
    
    def search_channels(self, youtube_client, search_type='basic'):
        search_response = None
        if search_type == 'basic':
            basic_info_params = self.__generate_basic_info_params()
            search_request = youtube_client.search().list(
                **basic_info_params
            )
            search_response = search_request.execute()
            channel_ids = self.__parse_channels(search_response)
            channels = [FindChannel().find_channel_by_id(channel_id, youtube_client)
                         for channel_id in channel_ids]
        return channels
    
    def __parse_channels(self, search_response):
        channels_ids = []
        items = search_response['items']
        for item in items:
            channels_ids.append(item['id']['channelId'])
        return channels_ids
        