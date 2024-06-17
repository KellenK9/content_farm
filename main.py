from text_splitter import TextSplitter
from selenium_scraper import RedditScraper
from video_generator import VerticalVideoMaker
from text_to_voice import TTSGenerator

# This file will serve as a controller, attempting each of the tasks below


# Generate content via ChatGPT or web scraping with Selenium

# Generate voice over using text to speech

# Create video output using text

# Stitch together video using stock footage, generated video, and generated speech


# May need to use these commands to run locally
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
# content_farm_venv\Scripts\activate


def main():
    paragraphs = RedditScraper.main()
    text_pages = TextSplitter.text_splitter(paragraphs)
    list_of_text_tuples = []
    for i in range(len(text_pages)):
        duration = TTSGenerator.single_speaker_model(
            "tts_models/en/ljspeech/vits--neon",
            i,
            text_pages[i],
        )
        list_of_text_tuples.append((text_pages[i], duration))
    VerticalVideoMaker.main(list_of_text_tuples)


main()
