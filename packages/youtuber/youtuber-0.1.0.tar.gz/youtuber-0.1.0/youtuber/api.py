
from googleapiclient.discovery import build
import json


class YoutubeAPI:
    def __init__(self, DEVELOPER_KEY: str):
        self._DEV_KEY = DEVELOPER_KEY
        self.YOUTUBE_API_SERVICE_NAME = "youtube"
        self.YOUTUBE_API_VERSION = "v3"

    def get_links(self, search_keyword: str, max_link_len: int) -> list:
        youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION, developerKey=self._DEV_KEY)
        search_response = youtube.search().list(
            q=search_keyword,
            type='video',
            part='id,snippet',
            maxResults=max_link_len
        ).execute()

        links = []
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                links.append("https://www.youtube.com/watch?v={}".format(search_result["id"]["videoId"]))
        
        return links