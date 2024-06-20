from text_splitter import TextSplitter
from selenium_scraper import RedditScraper
from video_generator import VerticalVideoMaker
from text_to_voice import TTSGenerator
import time

# This file will serve as a controller, attempting each of the tasks below


# Generate content via ChatGPT or web scraping with Selenium

# Generate voice over using text to speech

# Create video output using text

# Stitch together video using stock footage, generated video, and generated speech


# May need to use these commands to run locally
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
# content_farm_venv\Scripts\activate

curr_time = time.time()
duration = time.time() - curr_time


def main():
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
    VerticalVideoMaker.main(list_of_text_tuples)
    times_to_complete.append(("Video Generation with MoviePY", time.time() - curr_time))
    for tuple in times_to_complete:
        print(f"{tuple[0]} took {tuple[1]} seconds.")


main()
