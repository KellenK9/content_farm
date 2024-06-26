from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class RedditScraper:

    # Set Global Variables
    timeout = 10

    def buildPath():
        path_start = "https://www.reddit.com/"
        subreddit = "r/MaliciousCompliance/"
        sortby = "top/?t=week"
        path = f"{path_start}{subreddit}{sortby}"
        return path

    def launchBrowser(path):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(path)
        return driver

    def scrapeTopArticle():
        print()
        # Click Article
        # Get Title
        # Get body text

    def main():
        print("driver")
        path = RedditScraper.buildPath()
        print("built path")
        driver = RedditScraper.launchBrowser(path)
        print("got driver")

        # Click Article
        article_xpath = '//*[@id="main-content"]/div[2]/shreddit-feed/article[1]'  # //*[@id="main-content"]/div[2]/article[1]')
        article = EC.presence_of_element_located((By.XPATH, article_xpath))
        WebDriverWait(driver, RedditScraper.timeout).until(article)
        article_element = driver.find_element(By.XPATH, article_xpath)
        article_element.click()
        time.sleep(3)

        # Get Title
        header = EC.presence_of_element_located((By.TAG_NAME, "h1"))
        WebDriverWait(driver, RedditScraper.timeout).until(header)
        header_element = driver.find_element(By.TAG_NAME, "h1")
        title = header_element.text
        print(title)

        # Get Body Text
        body = EC.presence_of_element_located((By.CLASS_NAME, "text-neutral-content"))
        WebDriverWait(driver, RedditScraper.timeout).until(body)
        body_element = driver.find_element(By.TAG_NAME, "shreddit-post")
        paragraphs = body_element.find_elements(By.TAG_NAME, "p")
        paragraphs_text = []
        for p in paragraphs:
            paragraphs_text.append(p.text)

        return title, paragraphs_text


class LyricScraperGenius:  # Genius has anti-scraping measures implemented
    # Set Global Variables
    timeout = 10

    def buildPath(artist, song):
        path_start = "https://www.genius.com/"
        # Artist name should have the first letter capital and the rest lowercase with dashes instead of spaces
        # Song name should be lowercase with dashes instead of spaces
        path = f"{path_start}{artist}-{song}-lyrics"
        return path

    def launchBrowser(path):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(path)
        return driver

    def main(artist, song):
        print("driver")
        path = LyricScraperGenius.buildPath(artist, song)
        print("built path")
        driver = LyricScraperGenius.launchBrowser(path)
        print("got driver")

        # Get Body Text
        body = EC.presence_of_element_located(
            By.CLASS_NAME, "ReferentFragmentdesktop__Highlight-sc-110r0d9-1"
        )
        print("waiting")
        WebDriverWait(driver, LyricScraperGenius.timeout).until(body)
        print("done waiting")
        # song_title = driver.find_element(
        #    By.CLASS_NAME, "SongHeaderdesktop__HiddenMask-sc-1effuo1-11"
        # )
        # artist_name = driver.find_element(
        #    By.CLASS_NAME, "HeaderArtistAndTracklistdesktop__Artist-sc-4vdeb8-1"
        # )
        paragraphs = driver.find_elements(
            By.CLASS_NAME, "ReferentFragmentdesktop__Highlight-sc-110r0d9-1"
        )
        driver.quit()
        print(len(paragraphs))
        paragraphs_text = []
        for p in paragraphs:
            paragraphs_text.append(p.text)
            print(p.text)

        # return [song_title.text, artist_name.text, paragraphs_text]


class LyricScraperAZ:
    # Set Global Variables
    timeout = 10

    def buildPath():
        path_start = "https://www.azlyrics.com/lyrics/"
        artist = "childishgambino"  # Artist name should be lowercase with no spaces
        song = "sweatpants"  # Song name should be lowercase with no spaces. Some songs may include strange titles
        path = f"{path_start}{artist}/{song}.html"
        return path

    def launchBrowser(path):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(path)
        return driver

    def main():
        print("driver")
        path = LyricScraperAZ.buildPath()
        print("built path")
        driver = LyricScraperAZ.launchBrowser(path)
        print("got driver")

        # Get Body Text
        body = EC.presence_of_element_located()
        print("waiting")
        WebDriverWait(driver, LyricScraperAZ.timeout).until(body)
        print("done waiting")
        paragraphs = driver.find_elements()
        print(len(paragraphs))
        paragraphs_text = []
        for p in paragraphs:
            paragraphs_text.append(p.text)
            print(p.text)

        return paragraphs_text


class LyricScraperSing:
    # Set Global Variables
    timeout = 10

    def launchBrowser(path):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(path)
        return driver

    def main(path):
        driver = LyricScraperSing.launchBrowser(path)

        # Get Body Text
        body = EC.presence_of_element_located((By.CLASS_NAME, "contentbox"))
        WebDriverWait(driver, LyricScraperSing.timeout).until(body)
        paragraphs = driver.find_elements(By.CLASS_NAME, "lyrics_part_text")
        paragraphs_text = []
        for p in paragraphs:
            paragraphs_text.append(p.text)

        driver.quit()

        return paragraphs_text
