import os
import dotenv
import streamlit as st
from main import get_video_id_from_url, get_youtube_captions, generate_transcript

dotenv.load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

def main():
    # Center the title using HTML/Markdown
    st.markdown(
        """
        <style>
        .title {
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<h1 class='title'>YT-GPT</h1>", unsafe_allow_html=True)

    # Improved input with placeholder and help text
    video_url = st.text_input(
        "Enter YouTube Video URL:",
        placeholder="https://www.youtube.com/watch?v=...",
        help="Paste the full YouTube URL here.",
    )

    if video_url:
        video_id = get_video_id_from_url(video_url)

        if video_id:
            col1, col2 = st.columns([1, 2])  # Adjust column widths for better layout

            with col1:
                st.video(video_url)

            with col2:
                captions = get_youtube_captions(video_id)

                if captions:
                    formatted_transcript = generate_transcript(captions, api_key)

                    if formatted_transcript:
                        # Improved transcript display with expander for better readability
                        with st.expander("Show Transcript", expanded=True):
                            st.text_area("Transcript", formatted_transcript, height=400)
                    else:
                        st.error("Could not generate transcript.") #changed warning to error
                else:
                    st.error("Could not retrieve captions. Please check the video's caption availability.") #changed warning to error and added additional context.
        else:
            st.error("Invalid YouTube URL. Please enter a valid YouTube URL.") #changed warning to error.
    else:
        st.info("Please enter a YouTube URL to begin.") # added info to guide user.

if __name__ == "__main__":
    main()