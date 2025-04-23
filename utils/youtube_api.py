import os

from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('YOUTUBE_API_KEY')

def get_youtube_client(api_key):
    return build('youtube', 'v3', developerKey=api_key)

def fetch_comments(video_id):
    youtube = get_youtube_client(api_key)
    try:
        response = youtube.commentThreads().list(
            videoId=video_id,
            part="snippet",
            maxResults=100,
            textFormat="plainText",
            order="relevance"
        ).execute()
        comments = [item["snippet"]["topLevelComment"]["snippet"]["textDisplay"] for item in response.get("items", [])]
        return comments
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
