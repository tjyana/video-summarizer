import streamlit as st
from transcripter import summarize_transcript, extract_video_id
from youtube_transcript_api import YouTubeTranscriptApi

def main():
    '''
    Main function for the Streamlit app.
    '''

    # Title
    st.title("Video Summaries (YouTube)")


    # Input fields
    url = st.text_input("What are you too lazy to watch? (Paste URL here)", help="Enter video URL")

    # Submit button
    if st.button("Submit"):

        # Process the inputs
        video_id = extract_video_id(url)
        st.session_state.video_id = video_id
        st.write(st.session_state.video_id)

        # Get the summary
        st.write("Processing your request...")
        with st.spinner("Summarizing..."):
            

            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(st.session_state.video_id)
            except Exception as e:
                print("❌ Failed to fetch transcript:", e)
                return

            full_text = " ".join(seg["text"] for seg in transcript_list)
            st.write("\n— Transcript Preview —\n")
            st.write(full_text[:500] + "…\n")  # preview first 500 chars

            output = summarize_transcript(full_text)


        # Display 
        st.write(output)



if __name__ == "__main__":
    main()