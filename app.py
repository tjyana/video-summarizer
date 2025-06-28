import streamlit as st
from transcripter import summarize_transcript, extract_video_id
from youtube_transcript_api import YouTubeTranscriptApi

def main():
    '''
    Main function for the Streamlit app.
    '''

    # Title
    st.title("Video Summarizer")
    st.subheader("Let me summarize that YouTube video for you!")
    st.write("Paste a YouTube video URL below. (Only works for YouTube URLs, up to maybe 30min long.)")

    # Input fields
    url = st.text_input("What are you too lazy to watch?", help="Videos that probably won't work: live streams, videos longer than 30 minutes.")

    # Submit button
    if st.button("Submit"):

        # Process the inputs
        video_id = extract_video_id(url)
        st.session_state.video_id = video_id

        # st.write(st.session_state.video_id)

        # Get the summary
        st.write("Processing your request...")
        with st.spinner("Summarizing..."):
            

            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(st.session_state.video_id, languages=['en', 'ja'])
            except Exception as e:
                st.write("❌ Failed to fetch transcript:", e)
                return

            full_text = " ".join(seg["text"] for seg in transcript_list)
            # st.write("\n— Transcript Preview —\n")
            # st.write(full_text[:500] + "…\n")  # preview first 500 chars

            st.write("\n— Summary —\n")
            output = summarize_transcript(full_text)


        # Display 
        st.write(output)



if __name__ == "__main__":
    main()