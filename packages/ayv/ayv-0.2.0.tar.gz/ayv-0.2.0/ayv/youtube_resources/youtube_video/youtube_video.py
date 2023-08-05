from .youtube_video_stats import YouTubeVideoStats
from .youtube_video_details import YouTubeVideoDetails
from .youtube_video_comment_thread import YouTubeCommentThread


class YouTubeVideo:
    """A YouTube Video."""
    def __init__(self, video_details):
        self.__video_stats = self.__create_video_stats(video_details)
        self.__video_details = self.__create_video_details(video_details)
        self.__video_top_level_comments = None
        
    def get_video_stats_details(self):
        video_stats_details = dict()
        video_stats_details['details'] = self.get_video_details()
        video_stats_details['statistics'] = self.get_video_stats()
        return video_stats_details
    
    def get_video_comments(self, youtube_client):
        if not self.__video_top_level_comments:
            youtube_commenthread = YouTubeCommentThread(self.get_video_id())
            self.__video_top_level_comments = youtube_commenthread.get_video_comments(youtube_client)
        return self.__video_top_level_comments
        
    def __create_video_stats(self, video_details: dict):
        video_stats = YouTubeVideoStats(**video_details['statistics'])
        return video_stats
    
    def __create_video_details(self, video_details: dict):
        video_details = YouTubeVideoDetails(**video_details['details'])
        return video_details
        
    def get_video_stats(self):
        return self.__video_stats.get_video_stats()
    
    def get_video_details(self):
        return self.__video_details.get_video_details()
    
    def get_video_top_level_comments(self):
        pass
    
    def get_video_id(self):
        return self.__video_details.get_video_id()
    
    def get_video_title(self):
        return self.get_video_details()['title']
    
    def get_video_banner(self):
        return self.get_video_details()['thumbnail']['url']