import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import re
import csv
import time
import random

options = Options()
# options.add_argument("-headless")
profile = FirefoxProfile()
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
profile.set_preference("general.useragent.override", userAgent)
profile.set_preference("network.http.referer.XOriginPolicy", 1)
profile.set_preference("network.http.referer.XOriginPolicy", 2)
driver = webdriver.Firefox(options=options, firefox_profile=profile)

class scrapeinator():

    def __init__(self, searchQuery, noOfResults):
        self.rootURL = searchQuery
        self.noOfResults = noOfResults
        self.File = "data.csv"
        self.offset = 5269
        self.results = [
                    {
                        "result type" : "init",
                        "channel link" : "init",
                        "channel name" : "init",
                        "search result link" : "init",
                        "title" : "init"
                    },
        ]
        self.videoPattern = r"^https://www.youtube.com/watch\?v=.+"
        self.shortsPattern = r"^https://www.youtube.com/shorts/.+"
        self.postPattern = r"^https://www.youtube.com/post/.+"
        self.channelPattern = r"^(https://www.youtube.com/channel/.+|https://www.youtube.com/c/.+)"
    
    def saveData(self):
        csvFile = self.File
        with open(csvFile, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["result type", "channel link", "channel name", "search result link", "title"])
            if file.tell() == 0:
                writer.writeheader()
            writer.writerows(self.results[2:])
        print(f"Data is saved to {csvFile}")

    def scrapeVideo(self, link):
    
        driver.get(link)
        time.sleep(random.uniform(2, 3))

        try:
            popUp = driver.find_element(By.ID, "dismiss-button")
            popUp.click()
        except Exception:
            print("No pop-up.")

        try:
            randomClick = driver.find_element(By.CLASS_NAME, "style-scope ytd-watch-metadata")
            randomClick.click()
        except Exception:
            print("Couldn't click.")

        HTML = driver.page_source
        soup = BeautifulSoup(HTML, "html.parser")

        infoContainer = soup.find(id="owner")
        if infoContainer:
            channelLink = infoContainer.find("a")["href"]
            channelName = channelLink.split("@")[-1]
            channelLink = "https://www.youtube.com" + channelLink

        else:
            infoContainer = soup.find(id="text-container")
            if not infoContainer:
                print("Counldn't find links.")
                return "NA", "NA", "NA"
            channelLink = infoContainer.find("a")["href"]
            channelName = channelLink.split("@")[-1]
            channelLink = "https://www.youtube.com" + channelLink

        titleContainer = soup.find("h1", class_="style-scope ytd-watch-metadata")
        title = titleContainer.text.strip()
        # print(title)
        # print(channelName)
        # print(channelLink)
        return channelLink, channelName, title

    def scrapeShort(self, link):

        driver.get(link)
        time.sleep(random.uniform(2, 3))

        try:
            popUp = driver.find_element(By.ID, "dismiss-button")
            popUp.click()

        except Exception:
            print("No pop-up")

        HTML = driver.page_source
        soup = BeautifulSoup(HTML, "html.parser")

        infoContainer = soup.find(id="channel-info")
        channelLink = infoContainer.find("a")["href"]
        channelName = channelLink.split("@")[-1]
        channelLink = "https://www.youtube.com" + channelLink
        titleContainer = soup.find("h2", class_="title style-scope ytd-reel-player-header-renderer")
        title = titleContainer.text.strip()

        # print(title)
        # print(channelName)
        # print(channelLink)

        return channelLink, channelName, title

    def scrapePost(self, link):

        driver.get(link)
        time.sleep(random.uniform(2, 3))

        try:
            popUp = driver.find_element(By.ID, "dismiss-button")
            popUp.click()

        except Exception:
            print("No pop-up")

        HTML = driver.page_source
        soup = BeautifulSoup(HTML, "html.parser")

        infoContainer = soup.find(id="header-author")

        if not infoContainer:
            print("Result unavailable.")
            return "NA", "NA", "NA"

        channelLink = infoContainer.find("a")["href"]
        channelName = channelLink.split("@")[-1]
        channelLink = "https://www.youtube.com" + channelLink
        titleContainer = soup.find(id="content-text")
        title = titleContainer.text.strip()

        # print(title)
        # print(channelName)
        # print(channelLink)

        return channelLink, channelName, title

    def scrapeChannel(self, link, name):
        
        vLinks = link + "/videos"
        sLinks = link + "/shorts"

        driver.get(vLinks)
        time.sleep(random.uniform(2, 3))

        try:
            popUp = driver.find_element(By.ID, "dismiss-button")
            popUp.click()
        except Exception:
            print("No pop-up")
        
        HTML = driver.page_source
        soup = BeautifulSoup(HTML, "html.parser")

        videosContainer = soup.find_all(id="video-title-link")

        for video in videosContainer:
            videoLink = "https://www.youtube.com" + video["href"]
            videoTitle = video["title"].strip()

            self.results.append(
                    {
                        "result type" : "video",
                        "channel link" : link,
                        "channel name" : name,
                        "search result link" : videoLink,
                        "title" : videoTitle
                    }
                )
        
        driver.get(sLinks)
        time.sleep(random.uniform(2, 3))

        try:
            popUp = driver.find_element(By.ID, "dismiss-button")
            popUp.click()
        except Exception:
            print("No pop-up")
        
        HTML = driver.page_source
        soup = BeautifulSoup(HTML, "html.parser")

        shortsContainer = soup.find_all(id="details")

        for short in shortsContainer:
            try:
                short = short.find("a")
                shortLink = "https://www.youtube.com" + short["href"]
                shortTitle = short["title"].strip()

                self.results.append(
                        {
                            "result type" : "short",
                            "channel link" : link,
                            "channel name" : name,
                            "search result link" : shortLink,
                            "title" : shortTitle
                        }
                    )
            except Exception:
                print("No shorts.")
        
        return


    def scrape(self, startResult):
        
        print("Starting to scrape.")
        currentResult = startResult
        while (len(self.results)+ self.offset) < self.noOfResults:

            url = f"https://www.google.com/search?q=site%3Ayoutube.com+openinapp&start={currentResult}&filter=0"
            
            driver.get(url)
            time.sleep(random.uniform(2, 3))
            HTML = driver.page_source
            soup = BeautifulSoup(HTML, "html.parser")

            page = soup.find(id="center_col")

            if not page:
                print("An error has occured. Most probably a captcha.")
                print("The current result is : ", currentResult)
                break

            # Splitting the page container into containers containing separate search results
            containers = page.find_all(class_="MjjYud")

            # Number of search results on current page
            resultsOnPage = len(containers)

            if resultsOnPage == 0:
                print("No results on page.")
                print(url)
                print("Current result : ", currentResult)
                print(soup.find(class_="card-section").text)
                break

            for container in containers:

                print(f"({len(self.results)}/{self.noOfResults})")

                linkContainer = container.find("a")
                titleContainer = container.find("h3")

                # No link in the container
                if not linkContainer:
                    resultsOnPage -= 1
                    continue

                link = linkContainer["href"]

                print(link)

                if re.search(self.videoPattern, link):
                    # Is a video link
                    channelLink, channelName, title = self.scrapeVideo(link)
                    resultType = "Video"

                elif re.search(self.shortsPattern, link):
                    # Is a youtube short link
                    channelLink, channelName, title = self.scrapeShort(link)
                    resultType = "Short"

                elif re.search(self.postPattern, link):
                    # Is a youtube post
                    channelLink, channelName, title = self.scrapePost(link)
                    resultType = "Post"


                elif re.search(self.channelPattern, link):
                    # Is a channel link
                    channelLink = link
                    title = titleContainer.text
                    channelName = title
                    resultType = "Channel"
                
                for result in self.results:
                    if channelName in result.values():
                        self.results.append(
                            {
                                "result type" : resultType,
                                "channel link" : channelLink,
                                "channel name" : channelName,
                                "search result link" : link,
                                "title" : title
                            }
                        )
                        break
                else:
                    if channelName != "NA" and channelLink != "NA":
                        self.scrapeChannel(channelLink, channelName)

            currentResult += resultsOnPage

        return self.results, currentResult


if __name__ == "__main__":

    searchQuery = "https://www.google.com/search?q=site%3Ayoutube.com+openinapp"
    scraper = scrapeinator(searchQuery, 10000)
    startResult = 0
    results, startResult = scraper.scrape(startResult)
    # driver.quit()
    scraper.saveData()