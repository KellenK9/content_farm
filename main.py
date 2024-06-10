from text_splitter import TextSplitter
from selenium_scraper import RedditScraper
from video_generator import VerticalVideoMaker

# This file will serve as a controller, attempting each of the tasks below


# Generate content via ChatGPT or web scraping with Selenium

# Generate voice over using test to speech

# Create video output using text

# Stitch together video using stock footage, generated video, and generated speech


# May need to use these commands to run locally
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
# openai-env\Scripts\activate


def main():
    duration = 2  # This should be determined based off length of audio clips
    paragraphs = RedditScraper.main()
    text_pages = TextSplitter.text_splitter(paragraphs)
    list_of_text_tuples = []
    for text in text_pages:
        list_of_text_tuples.append((text, duration))
    VerticalVideoMaker.main(list_of_text_tuples)


main()
