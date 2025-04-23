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
        
        comments = []
        for item in response.get("items", []):
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            author = snippet["authorDisplayName"]
            text = snippet["textDisplay"]
        
            # Filter out uploader's comments and promo-like blocks
            if author.lower() == "networkchuck":
                continue
            if text.count("http") > 1 or "\n" in text:
                continue
        
            comments.append(text)
        return comments
        # comments = [item["snippet"]["topLevelComment"]["snippet"]["textDisplay"] for item in response.get("items", [])]
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
