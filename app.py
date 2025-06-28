import streamlit as st
from transcripter import summarize_transcript, extract_video_id

def main():
    '''
    Main function for the Streamlit app.
    '''

    # Title
    st.title("YouTube Video Summarizer")


    # Input fields
    url = st.text_input("What are you too lazy to watch?", help="Enter video URL")

    # Submit button
    if st.button("Submit"):

        # Process the inputs
        video_id = extract_video_id(url)
        st.session_state.video_id = video_id

        # Get the summary
        st.write("Processing your request...")
        with st.spinner("Summarizing..."):
            output = summarize_transcript(st.session_state.video_id)

        # Display 
        st.write(output)



if __name__ == "__main__":
    main()