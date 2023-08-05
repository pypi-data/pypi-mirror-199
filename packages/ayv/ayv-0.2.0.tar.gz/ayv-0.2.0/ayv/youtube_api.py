from .oauth import YouTubeAPIAuth
from .search.video import VideoSearch, FindVideo
from .search.category import SearchYouTubeVideoCategories


class YouTube:
    def __init__(self):
        self.__youtube_api_auth = YouTubeAPIAuth()
        self.__youtube_client = None
        self.__video_categories = []
        
    def get_credentials_path(self):
        return self.__youtube_api_auth.get_credentials_path()
        
    def authenticate_from_client_secrets_file(self, client_secrets_file: str, 
                credentials_path: str = ''):
        self.__youtube_client = self.__youtube_api_auth.authenticate_from_client_secrets_file(client_secrets_file, credentials_path)
        return self.__youtube_client
    
    def authenticate_from_credentials(self, credentials_path: str):
        self.__youtube_client = self.__youtube_api_auth.authenticate_from_credentials(credentials_path)
        return self.__youtube_client
    
    def generate_credentials(self, client_secrets_file: str, credentials_path: str = ''):
        self.__youtube_api_auth.generate_credentials(client_secrets_file, credentials_path)
        
    def get_youtube(self):
        return self.__youtube_client
    
    def search_videos(self, query_string: str) -> list[str]:
        videos = VideoSearch().search_video(query_string, self.__youtube_client)
        return videos
    
    def find_related_videos(self, youtube_video):
        related_videos = VideoSearch().search_related_videos(youtube_video, self.__youtube_client)
        return related_videos
    
    def find_most_popular_videos_by_region(self, region_code):
        most_popular_videos_by_region = VideoSearch().search_most_popular_videos_by_region(
            region_code, self.__youtube_client)
        return most_popular_videos_by_region
    
    def get_video_categories(self):
        if not self.__video_categories:
            self.__video_categories = SearchYouTubeVideoCategories(self.__youtube_client).get_youtube_video_categories()
        return self.__video_categories
    
    def find_most_popular_videos_by_category(self, category_id):
        most_popular_videos_by_category = VideoSearch().search_most_popular_videos_by_category(
            category_id, self.__youtube_client)
        return most_popular_videos_by_category
    
    def find_video_by_url(self, video_url: str):
        """Get a specific video given the video url."""
        video_id = self.__get_video_id(video_url)
        return self.find_video_by_id(video_id)
        
    def find_video_by_id(self, video_id: str):
        """Find a video by id."""
        youtube_video = FindVideo(video_id).find_video(self.__youtube_client)
        return youtube_video
    
    @staticmethod
    def __get_video_id(video_url: str) -> str:
        """Get vdeo ID from video url"""
        if not video_url:
            raise ValueError('The video_ur has to be provided.')
        if not isinstance(video_url, str):
            raise TypeError('Te video_url has to be a string.')
        if '=' not in video_url:
            url_format = 'https://www.youtube.com/watch?v=Dqdu-FsBk0s'
            raise ValueError(f'The video_url should be of the format "{url_format}"')
        video_url = video_url.split('=')[1]
        return video_url