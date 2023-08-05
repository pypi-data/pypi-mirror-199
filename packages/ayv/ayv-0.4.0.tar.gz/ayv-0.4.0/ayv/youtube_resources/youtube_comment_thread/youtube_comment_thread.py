from ..youtube_comment import YouTubeComment

class YouTubeCommentThread:
    def __init__(self, video_id: str):
        self.__video_id = video_id
        
    def get_video_comments(self, youtube_client):
        """Get the top level comments for a video."""
        youtube_comments = self.__find_comments(youtube_client)
        youtube_comments = [self.__create_comment(comment) for comment in youtube_comments]
        return youtube_comments
        
    def __generate_basic_info_params(self):
        basic_info_params = dict(
            videoId=self.__video_id,
            part='snippet,replies'
        ) 
        return basic_info_params
    
    def __find_comments(self, youtube_client):
        """Find the video comments."""
        basic_info_params = self.__generate_basic_info_params()
        search_request = youtube_client.commentThreads().list(
                **basic_info_params
            )
        search_response = search_request.execute()
        comments = self.__parse_comments(search_response)
        return comments
    
    def __create_comment(self, comment_details):
        youtube_comment = YouTubeComment(**comment_details)
        return youtube_comment

    def __parse_comments(self, search_response):
        items = search_response['items']
        comments = []
        for item in items:
            comments.append({
                'id': item['id'],
                'videoId': item['snippet']['videoId'],
                'totalReplyCount': item['snippet']['totalReplyCount'],
                'textDisplay': item['snippet']['topLevelComment']['snippet']['textDisplay'],
                'authorDisplayName': item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                'authorProfileImageUrl': item['snippet']['topLevelComment']['snippet']['authorProfileImageUrl'],
                'authorChannelId': item['snippet']['topLevelComment']['snippet']['authorChannelId']['value'],
                'likeCount': item['snippet']['topLevelComment']['snippet']['likeCount'],
                'publishedAt': item['snippet']['topLevelComment']['snippet']['publishedAt'],
                'updatedAt': item['snippet']['topLevelComment']['snippet']['updatedAt']
        })
        return comments