class YouTubeVideoStats:
    def __init__(self, viewCount: int, likeCount: int, commentCount: int):
        self.__view_count = int(viewCount)
        self.__like_count = int(likeCount)
        self.__comment_count = int(commentCount)
        
    def get_video_stats(self):
        video_stats = {
            'view_count': self.__view_count,
            'like_count': self.__like_count,
            'comment_count': self.__comment_count
        }
        return video_stats