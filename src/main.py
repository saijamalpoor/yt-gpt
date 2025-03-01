import json
import re
import os

from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

def get_video_id_from_url(video_url):
    video_id_match = re.search(r"(?<=v=)[^&\s]+", video_url)
    if video_id_match:
        return video_id_match.group(0)

    video_id_match = re.search(r"(?<=be/)[^&\s]+", video_url)
    if video_id_match:
        return video_id_match.group(0)

    return None

def get_youtube_captions(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        print(f"Error: {e}")
        return None

def create_json_from_captions(captions):
    """
    Creates a JSON object from a list of caption dictionaries.

    Args:
        captions: A list of dictionaries, where each dictionary represents a caption.

    Returns:
        A JSON string representing the captions, or None if captions are empty.
    """
    if not captions:
        return None

    json_data = json.dumps(captions, indent=4)  # indent=4 for pretty printing
    return json_data



def generate_transcript(captions, api_key):
    """
    Generates a neat, formatted transcript from a list of caption dictionaries using Gemini.

    Args:
        captions: A list of dictionaries, where each dictionary represents a caption.
        api_key: Your Google Generative AI API key.

    Returns:
        A string containing the formatted transcript, or None if an error occurs.
    """
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-1219') # or gemini-2.0-flash-thinking-exp-1219, gemini-1.5-flash

    full_transcript = "\n".join([f"[{caption['start']:.2f} - {caption['start'] + caption['duration']:.2f}] {caption['text']}" for caption in captions])

    prompt = f"""
    You are an expert transcript formatter. Given the following raw transcript with timestamps, create a clean and neatly formatted transcript.
    and summarize the main ideas of the video as summary.

    Raw Transcript:
    {full_transcript}

    Formatted Transcript:
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating formatted transcript: {e}")
        return None

# Example usage (replace with your actual captions and API key):

# Simulated captions (replace with your actual caption data)
# example_captions = [
#     {"text": "Today, we'll discuss the fundamentals of machine learning.", "start": 0, "duration": 5},
#     {"text": "Machine learning algorithms learn patterns from data.", "start": 5, "duration": 4},
#     {"text": "Supervised learning involves labeled data for training.", "start": 9, "duration": 6},
#     {"text": "Unsupervised learning finds hidden structures in unlabeled data.", "start": 15, "duration": 7},
#     {"text": "Reinforcement learning trains agents through rewards and penalties.", "start":22, "duration": 8}
# ]



# Example usage:

if __name__ == '__main__':
    
    video_url = input('Please enter the YouTube URL: ') # Replace with your YouTube URL
    video_id = get_video_id_from_url(video_url)

    if video_id:
        captions = get_youtube_captions(video_id)
        print(captions)

        # if captions:
        #     json_output = create_json_from_captions(captions)
    #         if json_output:
    #             print(json_output)  # Print the JSON string
    #             # Optionally, you can write the JSON to a file:
    #             # with open("captions.json", "w") as f:
    #             #     f.write(json_output)
    #         else:
    #             print("Captions were empty.")

    #     else:
    #         print("Captions not available for this video.")
    # else:
    #     print("Invalid YouTube URL.")
        
    # api_key = api_key # GEMINI API key

    captions = captions #replace example_captions with your captions variable.

    formatted_transcript = generate_transcript(captions, api_key)

    if formatted_transcript:
        print(formatted_transcript)
        
        
