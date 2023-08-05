from ...youtube_resources.youtube_video import YouTubeVideo

class FindVideo:
    def __init__(self, video_id: str):
        """Find the video with the given id."""
        self.__video_id = video_id
        
    def __generate_basic_info_params(self):
        basic_info_params = dict(
            id=self.__video_id,
            part='snippet,contentDetails,statistics'
        ) 
        return basic_info_params
    
    def find_video(self, youtube_client):
        """Find the video."""
        basic_info_params = self.__generate_basic_info_params()
        search_request = youtube_client.videos().list(
                **basic_info_params
            )
        search_response = search_request.execute()
        parsed_response = self.__parse_video_details(search_response)
        youtube_video = YouTubeVideo(parsed_response)
        return youtube_video
    
    def __parse_video_details(self, video_details: dict):
        """Parse the video details.

        Returns
        -------
        parsed_video_details: dict
            A dictionary of the YouTube video details.
        """
        parsed_video_details = dict()
        items = video_details['items'][0]
        parsed_video_details['details'] = dict()
        parsed_video_details['statistics'] = dict()
        parsed_video_details['details']['id'] = items['id']
        parsed_video_details['details']['channelId'] = items['snippet']['channelId']
        parsed_video_details['details']['title'] = items['snippet']['title']
        parsed_video_details['details']['channelTitle'] = items['snippet']['channelTitle']
        parsed_video_details['details']['description'] = items['snippet']['description']
        parsed_video_details['details']['thumbnails'] = items['snippet']['thumbnails']
        if items['snippet'].get('tags'):
            parsed_video_details['details']['tags'] = items['snippet']['tags']
        else:
            parsed_video_details['details']['tags'] = []
        parsed_video_details['details']['duration'] = items['contentDetails']['duration']
        parsed_video_details['details']['licensedContent'] = items['contentDetails']['licensedContent']
        parsed_video_details['statistics']['viewCount'] = items['statistics']['viewCount']
        parsed_video_details['statistics']['likeCount'] = items['statistics']['likeCount']
        parsed_video_details['statistics']['commentCount'] = items['statistics']['commentCount']
        return parsed_video_details