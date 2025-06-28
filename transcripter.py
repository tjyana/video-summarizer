import os
import streamlit as st
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI

# ——— Load API key ——————————————————————————————————————————————
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    api_key = st.secrets['OPENAI_API_KEY']
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set. Check your secrets.")

# Instantiate the v1 client
client = OpenAI(api_key=api_key)


def extract_video_id(url: str) -> str | None:
    """
    Extract the YouTube video ID from a URL.
    """
    parsed = urlparse(url)
    if parsed.hostname in ("youtu.be", "www.youtu.be"):
        return parsed.path.lstrip("/")
    if parsed.hostname in ("www.youtube.com", "youtube.com"):
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]
        parts = parsed.path.split("/")
        if len(parts) > 2 and parts[1] in ("embed", "v"):
            return parts[2]
    return None


def summarize_transcript(
    transcript_text: str,
    model="gpt-3.5-turbo",
    max_tokens: int = 150
) -> str:
    """
    Sends the full transcript to OpenAI and returns a summary.
    """
    prompt = (
        "You are a helpful assistant that summarizes YouTube videos. "
        "Please provide a concise summary in 1 sentence, and also provide an outline of the main points in bulletpoints.\n\n"
        f"{transcript_text}"
    )
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You summarize transcripts."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=max_tokens,
        )
    except Exception as e:
        return f"❌ OpenAI error: {e}"

    return resp.choices[0].message.content.strip()


# def main():
#     url = input("Enter a YouTube URL: ").strip()
#     video_id = extract_video_id(url)
#     if not video_id:
#         print("❌ Could not extract a video ID from that URL.")
#         return

#     try:
#         transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
#     except Exception as e:
#         print("❌ Failed to fetch transcript:", e)
#         return

#     full_text = " ".join(seg["text"] for seg in transcript_list)
#     print("\n— Transcript Preview —\n")
#     print(full_text[:500] + "…\n")  # preview first 500 chars

#     summary = summarize_transcript(full_text)
#     print("\n— Video Summary —\n")
#     print(summary)


# if __name__ == "__main__":
#     main()
