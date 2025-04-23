import subprocess
subprocess.check_call(["pip", "install", "-r", "requirements.txt"])

import nltk
import spacy
import transformers
import re
import gradio as gr

from utils.youtube_api import fetch_comments
from utils.nlp_utils import analyze_sentiment, categorize_comments_by_sentiment, summarize_comments

def analyze_youtube_comments(youtube_url):
    # youtube_url = 'https://www.youtube.com/watch?v=MZbFDrFUMxk' # Example URL for testing
    if youtube_url:
        parsed_url = urlparse(youtube_url)
        query_params = parse_qs(parsed_url.query)
        video_id = query_params.get('v', [None])[0]
        if video_id:
            comments = fetch_comments(video_id)
            if comments:
                output = ""
                # Analyze sentiment and categorize comments
                categorized_comments = categorize_comments_by_sentiment(comments)
                for category, comment_list in categorized_comments.items():
                    output += f"\n**{category} Comments ({len(comment_list)}):**\n"
                    if comment_list:
                        summary = summarize_comments(comment_list[:20]) # Summarize a sample for brevity
                        output += f"Summary: {summary}\n"
                        for c in comment_list[:3]:
                            output += f"- {c}\n"
                            # st.write(f"Summary: {summary}")
                            # Option to display some example comments if needed
                            # for i, comment in enumerate(comment_list[:3]):
                            #     st.markdown(f"- {comment}")
                            # if st.checkbox(f"Show example {category} comments"):
                            #     for comment in comment_list[:5]:
                            #         st.markdown(f"- {comment}")
                    else:
                        output += "No comments in this category."
            else:
                return "No comments found for this video."
        else:
            return "Invalid YouTube URL. Please try again."

interface = gr.Interface(
    fn=analyze_youtube_comments,
    inputs=gr.Textbox(label="Enter YouTube URL:"),
    outputs=gr.Markdown() # Use Markdown to display formatted text output
)

if __name__ == "__main__":
    interface.launch()
