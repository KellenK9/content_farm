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

        return paragraphs_text


class LyricScraper:
    # Set Global Variables
    timeout = 10

    def buildPath():
        path_start = "https://www.genius.com/"
        artist = "Drake"  # Artist name should have the first letter capital and the rest lowercase with dashes instead of spaces
        song = "push-ups"  # Song name should be lowercase with dashes instead of spaces
        path = f"{path_start}{artist}-{song}-lyrics"
        return path

    def launchBrowser(path):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(path)
        return driver

    def main():
        print("driver")
        path = LyricScraper.buildPath()
        print("built path")
        driver = LyricScraper.launchBrowser(path)
        print("got driver")

        # Get Body Text
        body = EC.presence_of_element_located((By.ID, "lyrics-root-pin-spacer"))
        print("waiting")
        WebDriverWait(driver, LyricScraper.timeout).until(body)
        print("done waiting")
        paragraphs = driver.find_elements(
            By.CLASS_NAME, "ReferentFragmentdesktop__Highlight-sc-110r0d9-1 jAzSMw"
        )
        print(len(paragraphs))
        paragraphs_text = []
        for p in paragraphs:
            paragraphs_text.append(p.text)
            print(p)

        return paragraphs_text


# LyricScraper.main() # It's getting stuck and taking forever
