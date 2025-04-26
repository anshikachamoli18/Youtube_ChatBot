from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled, VideoUnavailable, CouldNotRetrieveTranscript

def fetch_transcript(video_id: str) -> str:
    """
    Fetches transcript text from a YouTube video ID.
    Returns the combined transcript text or None if not available.
    """
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        transcript = " ".join(chunk["text"] for chunk in transcript_list)
        return transcript

    except (NoTranscriptFound, TranscriptsDisabled, VideoUnavailable, CouldNotRetrieveTranscript):
        return None

    except Exception as e:
        raise Exception(f"Error fetching transcript: {str(e)}")
