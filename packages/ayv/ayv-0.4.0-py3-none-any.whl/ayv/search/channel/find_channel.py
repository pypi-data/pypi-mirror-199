from ...youtube_resources.youtube_channel import Channel

class FindChannel:       
    def __generate_basic_info_params(self, channel_id):
        basic_info_params = dict(
            id=channel_id,
            part='id,snippet,contentDetails,contentOwnerDetails,statistics,topicDetails',
        ) 
        return basic_info_params
    
    def find_channel_by_name(self, youtube_client):
        pass
    
    def find_channel_by_id(self, channel_id, youtube_client):
        """Find the video."""
        basic_info_params = self.__generate_basic_info_params(channel_id)
        search_request = youtube_client.channels().list(
                **basic_info_params
            )
        search_response = search_request.execute()
        parsed_response = self.__parse_channel(search_response)
        youtube_channel = Channel(**parsed_response)
        return youtube_channel
    
    def __parse_channel(self, search_response):
        channel_details = {}
        items = search_response['items'][0]
        channel_details['id'] = items['id']
        channel_details['title'] = items['snippet']['title']
        channel_details['description'] = items['snippet']['description']
        channel_details['customUrl'] = items['snippet']['customUrl']
        channel_details['publishedAt'] = items['snippet']['publishedAt']
        channel_details['thumbnails'] = items['snippet']['thumbnails']
        channel_details['statistics'] = dict()
        channel_details['statistics']['viewCount'] = items['statistics']['viewCount']
        channel_details['statistics']['subscriberCount'] = items['statistics']['subscriberCount']
        channel_details['statistics']['videoCount'] = items['statistics']['videoCount']
        return channel_details