from text_splitter import TextSplitter
from selenium_scraper import RedditScraper, LyricScraperSing
from video_generator import VerticalVideoMaker, HorizontalVideoMaker, LyricVideoMaker
from text_to_voice import TTSGenerator
from youtube_downloader import YouTubeDownloader
import time

# This file will serve as a controller, attempting each of the tasks below


# Generate content via ChatGPT or web scraping with Selenium

# Generate voice over using text to speech

# Create video output using text

# Stitch together video using stock footage, generated video, and generated speech


# May need to use these commands to run locally
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
# content_farm_venv\Scripts\activate


def create_reddit_story_video():
    list_of_text_tuples = []
    times_to_complete = []

    curr_time = time.time()
    paragraphs = RedditScraper.main()
    times_to_complete.append(("Reddit Scraper with Selenium", time.time() - curr_time))

    curr_time = time.time()
    text_pages = TextSplitter.text_splitter(paragraphs)
    times_to_complete.append(("Text Splitter with Python", time.time() - curr_time))

    curr_time = time.time()
    for i in range(len(text_pages)):
        duration = TTSGenerator.single_speaker_model(
            "tts_models/en/ljspeech/overflow",
            i,
            text_pages[i],
        )
        list_of_text_tuples.append((text_pages[i], duration))
    times_to_complete.append(("Text To Speech with CoquiTTS", time.time() - curr_time))

    curr_time = time.time()
    VerticalVideoMaker.main_story_format(list_of_text_tuples)
    times_to_complete.append(("Video Generation with MoviePY", time.time() - curr_time))

    for tuple in times_to_complete:
        print(f"{tuple[0]} took {tuple[1]} seconds.")


def create_lyric_video(song_title, artist_name, lyric_link, youtube_audio_link):
    list_of_text_tuples = []
    times_to_complete = []
    temp_audio_path = "./temp_audio/drake-push-ups-audio"

    curr_time = time.time()
    paragraphs = LyricScraperSing.main(lyric_link)
    times_to_complete.append(("Lyric Scraper with Selenium", time.time() - curr_time))

    curr_time = time.time()
    text_pages = TextSplitter.text_splitter(paragraphs)
    times_to_complete.append(("Text Splitter with Python", time.time() - curr_time))

    curr_time = time.time()
    YouTubeDownloader.downloadYouTubeAudio(
        youtube_audio_link,
        temp_audio_path,
    )
    times_to_complete.append(("Audio Downloading with PyTube", time.time() - curr_time))

    # Generate durations for each page of lyrics that corresponds to audio. Must be done manually.
    manual_page_duration_array = [
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
    ]
    for i in range(len(text_pages)):
        list_of_text_tuples.append((text_pages[i], manual_page_duration_array[i]))
    title_page_duration = 8

    curr_time = time.time()
    LyricVideoMaker.create_both_video_formats(
        list_of_text_tuples,
        f"{temp_audio_path}/{song_title}.mp4",
        title_page_duration,
        song_title,
        artist_name,
    )
    times_to_complete.append(("Video Generation with MoviePY", time.time() - curr_time))

    for tuple in times_to_complete:
        print(f"{tuple[0]} took {tuple[1]} seconds.")


create_lyric_video(
    "Push Ups",
    "Drake",
    "https://www.letssingit.com/drake-lyrics-push-ups-srp8n8w",
    "https://www.youtube.com/watch?v=HKH9p19PRLA&ab_channel=Drake-Topic",
)
