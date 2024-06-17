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
        path = RedditScraper.buildPath()
        driver = RedditScraper.launchBrowser(path)
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
