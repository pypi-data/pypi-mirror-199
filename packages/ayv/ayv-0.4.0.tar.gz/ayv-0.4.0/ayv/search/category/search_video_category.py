from ...youtube_resources.youtube_video_category import YouTubeVideoCategory


class SearchYouTubeVideoCategories:
    def __init__(self, youtube_client, region_code='us'):
        self.__youtube_client = youtube_client
        self.__region_code = region_code
        self.__youtube_video_categories = self.__search_video_categories()
    
    def __generate_basic_info_params(self):
        basic_info_params = dict(
            part='snippet',
            regionCode=self.__region_code
        )
        return basic_info_params
    
    def __search_video_categories(self):
        basic_info_params = self.__generate_basic_info_params()
        search_request = self.__youtube_client.videoCategories().list(
                **basic_info_params
            )
        search_response = search_request.execute()
        video_categories = self.__parse_categories(search_response)
        return video_categories
    
    def __parse_categories(self, search_response):
        category_data = []
        items = search_response['items']
        for item in items:
            category = dict()
            category['id'] = item['id']
            category['title'] = item['snippet']['title']
            category_data.append(YouTubeVideoCategory(**category))
        return category_data
    
    def get_youtube_video_categories(self):
        return self.__youtube_video_categories