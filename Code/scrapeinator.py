import requests
from bs4 import BeautifulSoup
import re
import csv
import time
import random

from googleapiclient.discovery import build
DEVELOPER_KEY = "AIzaSyDpGylmTSTzrQUPhM0C7BpVCbOecanQXqk"
youtube = build("youtube", "v3", developerKey=DEVELOPER_KEY)

class scrapeinator():

    def __init__(self, searchQuery, noOfResults):
        self.rootURL = searchQuery
        self.noOfResults = noOfResults

        self.File = "data.csv"

        # Adding headers for organic search
        self.headers = {
                "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
            }

        # Regex for various types of links
        self.videoPattern = r"^https://www.youtube.com/watch\?v=.+"
        self.shortsPattern = r"^https://www.youtube.com/shorts/.+"
        self.postPattern = r"^https://www.youtube.com/post/.+"
        self.channelPattern = r"^(https://www.youtube.com/channel/.+|https://www.youtube.com/c/.+)"

    def scrapeVideo(self, link):

        videoId = link.split("=")[-1]
        response = youtube.videos().list(
            part = 'snippet',
            id = videoId
        ).execute()

        videoDetails = response["items"][0]["snippet"]

        channelLink = f"https://www.youtube.com/channel/{videoDetails['channelId']}"
        channelName = videoDetails["channelTitle"]
        videoTitle = videoDetails["title"]


        # response = requests.get(link, headers = self.headers)
        # soup = BeautifulSoup(response.text, "html.parser")
        # soup = soup.find_all("div")
        # for s in soup:
        # print(soup)
        # channelLinkContainer = soup.find(id="below")
        # print(channelLinkContainer)
        # channelLink = channelLinkContainer.find("a")["href"]
        # titleContainer = soup.find(id="title")
        # title = titleContainer.find("h1").text
        # return channelLink, title

        return channelLink, channelName, videoTitle

    def scrapeShort(self, link):

        shortId = link.split("/shorts/")[-1]
        response = youtube.videos().list(
            part = 'snippet',
            id = shortId
        ).execute()

        shortDetails = response["items"][0]["snippet"]

        channelLink = f"https://www.youtube.com/channel/{shortDetails['channelId']}"
        channelName = shortDetails["channelTitle"]
        shortTitle = shortDetails["title"]

        return channelLink, channelName, shortTitle

    # def scrapePost(self, link):

    #     response = requests.get(link, headers=self.headers)
    #     soup = BeautifulSoup(response.text, "html parser")

    #     text = soup.find(id="author-text").text
    #     print(text)

    #     return "To Be Continued ..."

    def scrape(self, startResult):

        results = []
        currentResult = startResult

        session = requests.Session()

        while currentResult < self.noOfResults:

            time.sleep(random.uniform(0.5, 3))

            # Adding the start parameter to start at the next result
            # url = f"https://www.google.com/search?q=site%3Ayoutube.com+openinapp&start={currentResult}"

            # response = requests.get(url, headers = self.headers)
            # soup = BeautifulSoup(response.text, "html.parser")
            # print(soup)

            url = f"https://www.google.com/search?q=site%3Ayoutube.com+openinapp&start={currentResult}"
            response = session.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")

            # Choosing the container containing all search results
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

            print(f"({currentResult}/{self.noOfResults})")

            for container in containers:


                # Container for the search result video link
                linkContainer = container.find("a")

                titleContainer = container.find("h3")

                # No link in the container
                if not linkContainer:
                    resultsOnPage -= 1
                    continue

                link = linkContainer["href"]

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
                    # channelLink = self.scrapePost(link)
                    # resultType = "Post"

                    continue

                elif re.search(self.channelPattern, link):
                    # Is a channel link
                    channelLink = link
                    title = titleContainer.text
                    channelName = title
                    resultType = "Channel"

                results.append(
                    {
                        "result type" : resultType,
                        "channel link" : channelLink,
                        "channel name" : channelName,
                        "search result link" : link,
                        "title" : title
                    }
                )

            currentResult += resultsOnPage

        session.close()

        return results, currentResult
    
    def saveData(self):
        
        csvFile = self.File

        with open(csvFile, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["result type", "channel link", "channel name", "search result link", "title"])
            writer.writeheader()
            writer.writerows(results)

        print(f"Data is saved to {csvFile}")


if __name__ == "__main__":

    searchQuery = "https://www.google.com/search?q=site%3Ayoutube.com+openinapp"
    scraper = scrapeinator(searchQuery, 10000)

    startResult = 0

    results, startResult = scraper.scrape(startResult)

    scraper.saveData()

    # for idx, result in enumerate(results, start=1):
    #     print(f"Result #{idx} \t: {result}")
